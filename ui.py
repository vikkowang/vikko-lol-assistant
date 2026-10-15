"""置顶悬浮窗：显示单条答案，可拖动、置顶开关、收起成点、关闭、手动缩放。"""

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)


class OverlayWindow(QWidget):
    status = Signal(str)      # 更新状态行（正在听 / 你说：xxx）
    question = Signal(str)    # 识别出的问题（语音转文字结果）
    answer = Signal(str)      # 大模型的回答
    open_settings = Signal()  # 打开设置对话框

    BTN_STYLE = (
        "QPushButton { background: transparent; color: #9aa0b0; border: none;"
        " padding: 2px 6px; font-size: 12px; }"
        "QPushButton:hover { color: #e5e7eb; }"
    )
    DOT_STYLE = (
        "QPushButton { background: #3b82f6; border-radius: 9px; border: none; }"
    )
    PIN_STYLE = (
        "QPushButton { background: transparent; color: #e5e7eb; border: none;"
        " padding: 2px 6px; font-size: 14px; }"
    )

    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self._collapsed = False
        self._pinned = True
        self._user_size = None
        self._press_global = None
        self._moved = False
        self._build()
        self.status.connect(self._on_status)
        self.question.connect(self._on_question)
        self.answer.connect(self._on_answer)

    def _build(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("LOL 助手")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(320)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(
            "#card { background: rgba(20, 22, 30, 0.92); border-radius: 10px; }"
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(card)

        self.card_layout = QVBoxLayout(card)
        self.card_layout.setContentsMargins(14, 8, 14, 12)
        self.card_layout.setSpacing(6)

        bar = QHBoxLayout()
        self.title_label = QLabel("LOL 助手")
        self.title_label.setStyleSheet("color: #9aa0b0; font-size: 12px;")
        bar.addWidget(self.title_label)
        bar.addStretch()

        self.pin_btn = QPushButton("📌")
        self.pin_btn.setStyleSheet(self.PIN_STYLE)
        self.settings_btn = QPushButton("设置")
        self.settings_btn.setStyleSheet(self.BTN_STYLE)
        self.collapse_btn = QPushButton("—")
        self.collapse_btn.setStyleSheet(self.BTN_STYLE)
        self.close_btn = QPushButton("✕")
        self.close_btn.setStyleSheet(self.BTN_STYLE)
        bar.addWidget(self.pin_btn)
        bar.addWidget(self.settings_btn)
        bar.addWidget(self.collapse_btn)
        bar.addWidget(self.close_btn)
        self.card_layout.addLayout(bar)

        self.sub = QLabel("按住 = 键说话")
        self.sub.setStyleSheet("color: #6b7280; font-size: 11px;")
        self.sub.setWordWrap(True)
        self.card_layout.addWidget(self.sub)

        self.question_label = QLabel("")
        self.question_label.setStyleSheet("color: #93c5fd; font-size: 13px;")
        self.question_label.setWordWrap(True)
        self.card_layout.addWidget(self.question_label)

        self.body = QLabel("")
        self.body.setStyleSheet("color: #e5e7eb; font-size: 14px;")
        self.body.setWordWrap(True)
        self.card_layout.addWidget(self.body)

        self.collapse_btn.clicked.connect(self._toggle_collapse)
        self.pin_btn.clicked.connect(self._toggle_pin)
        self.settings_btn.clicked.connect(lambda: self.open_settings.emit())
        self.close_btn.clicked.connect(self.close)

        # 右下角手动缩放把手（PySide6 6.12 的 QSizeGrip 不会自动贴角，需手动钉住）
        self.size_grip = QSizeGrip(self)
        self.size_grip.installEventFilter(self)
        self._place_size_grip()

        self._apply_pin_style()

    def _place_size_grip(self):
        g = self.size_grip.sizeHint()
        self.size_grip.setGeometry(
            self.width() - g.width() - 2,
            self.height() - g.height() - 2,
            g.width(),
            g.height(),
        )
        self.size_grip.raise_()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place_size_grip()

    def _on_status(self, text):
        self.sub.setText(text)

    def _on_question(self, text):
        self.question_label.setText(f"你：{text}")
        self.body.setText("")

    def _on_answer(self, text):
        self.body.setText(text)

    def _apply_pin_style(self):
        if self._pinned:
            self.pin_btn.setGraphicsEffect(None)
            self.pin_btn.setToolTip("取消置顶")
        else:
            eff = QGraphicsOpacityEffect(self.pin_btn)
            eff.setOpacity(0.35)
            self.pin_btn.setGraphicsEffect(eff)
            self.pin_btn.setToolTip("置顶")

    def _toggle_pin(self):
        self._pinned = not self._pinned
        flags = self.windowFlags()
        flags ^= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self._apply_pin_style()
        self.show()

    def eventFilter(self, obj, event):
        # 拖动右下角缩放把手，记录用户自定义的窗口大小
        if obj is self.size_grip and event.type() == QEvent.MouseButtonRelease:
            self._user_size = self.size()
        return super().eventFilter(obj, event)

    def expand(self):
        if self._collapsed:
            self._toggle_collapse()

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self.title_label.hide()
            self.pin_btn.hide()
            self.settings_btn.hide()
            self.close_btn.hide()
            self.sub.hide()
            self.question_label.hide()
            self.body.hide()
            self.setMinimumWidth(0)
            self.card_layout.setContentsMargins(2, 2, 2, 2)
            self.collapse_btn.setFixedSize(18, 18)
            self.collapse_btn.setText("")
            self.collapse_btn.setStyleSheet(self.DOT_STYLE)
            # 圆点不拦截鼠标，把事件交给窗口，实现拖动 + 点击展开
            self.collapse_btn.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.size_grip.hide()
            self.setFixedSize(22, 22)
        else:
            self.title_label.show()
            self.pin_btn.show()
            self.settings_btn.show()
            self.close_btn.show()
            self.sub.show()
            self.question_label.show()
            self.body.show()
            self.setMinimumWidth(320)
            self.card_layout.setContentsMargins(14, 8, 14, 12)
            self.collapse_btn.setFixedSize(28, 22)
            self.collapse_btn.setText("—")
            self.collapse_btn.setStyleSheet(self.BTN_STYLE)
            self.collapse_btn.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.size_grip.show()
            self.setMinimumHeight(0)
            self.setMaximumSize(16777215, 16777215)
            self.layout().activate()
            self.resize(self._user_size if self._user_size else self.sizeHint())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self._press_global = e.globalPosition().toPoint()
            self._moved = False

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton and self._drag_pos is not None:
            if not self._moved and (e.globalPosition().toPoint() - self._press_global).manhattanLength() > 3:
                self._moved = True
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        if self._collapsed and not self._moved:
            self._toggle_collapse()
        self._drag_pos = None
        self._press_global = None
        self._moved = False
