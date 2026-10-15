"""置顶悬浮窗：显示单条答案，可拖动、置顶开关、收起成点、关闭。"""

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)


class OverlayWindow(QWidget):
    status = Signal(str)      # 更新状态行（正在听 / 你说：xxx）
    answer = Signal(str, str)  # (识别文本, 回答)

    BTN_STYLE = (
        "QPushButton { background: transparent; color: #9aa0b0; border: none;"
        " padding: 2px 6px; font-size: 12px; }"
        "QPushButton:hover { color: #e5e7eb; }"
    )
    DOT_STYLE = (
        "QPushButton { background: #3b82f6; border-radius: 9px; border: none; }"
    )

    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self._collapsed = False
        self._user_size = None
        self._build()
        self.status.connect(self._on_status)
        self.answer.connect(self._on_answer)

    def _build(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
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

        self.collapse_btn = QPushButton("—")
        self.pin_btn = QPushButton("置顶")
        self.close_btn = QPushButton("✕")
        for b in (self.collapse_btn, self.pin_btn, self.close_btn):
            b.setStyleSheet(self.BTN_STYLE)
            bar.addWidget(b)
        self.card_layout.addLayout(bar)

        self.sub = QLabel("按住 = 键说话")
        self.sub.setStyleSheet("color: #6b7280; font-size: 11px;")
        self.sub.setWordWrap(True)
        self.card_layout.addWidget(self.sub)

        self.body = QLabel("")
        self.body.setStyleSheet("color: #e5e7eb; font-size: 14px;")
        self.body.setWordWrap(True)
        self.card_layout.addWidget(self.body)

        self.collapse_btn.clicked.connect(self._toggle_collapse)
        self.pin_btn.clicked.connect(self._toggle_pin)
        self.close_btn.clicked.connect(self.close)

        self.size_grip = QSizeGrip(self)
        self.size_grip.installEventFilter(self)

    def _on_status(self, text):
        self.sub.setText(text)

    def _on_answer(self, question, text):
        self.sub.setText(f"你说：{question}")
        self.body.setText(text)

    def _toggle_pin(self):
        flags = self.windowFlags()
        flags ^= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def eventFilter(self, obj, event):
        # 用户拖动右下角缩放把手时，记录他自定义的窗口大小
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
            self.close_btn.hide()
            self.sub.hide()
            self.body.hide()
            self.setMinimumWidth(0)
            self.card_layout.setContentsMargins(2, 2, 2, 2)
            self.collapse_btn.setFixedSize(18, 18)
            self.collapse_btn.setText("")
            self.collapse_btn.setStyleSheet(self.DOT_STYLE)
            self.size_grip.hide()
            self.setFixedSize(22, 22)
        else:
            self.title_label.show()
            self.pin_btn.show()
            self.close_btn.show()
            self.sub.show()
            self.body.show()
            self.setMinimumWidth(320)
            self.card_layout.setContentsMargins(14, 8, 14, 12)
            self.collapse_btn.setFixedSize(28, 22)
            self.collapse_btn.setText("—")
            self.collapse_btn.setStyleSheet(self.BTN_STYLE)
            self.size_grip.show()
            self.setMinimumHeight(0)
            self.setMaximumSize(16777215, 16777215)
            self.layout().activate()
            self.resize(self._user_size if self._user_size else self.sizeHint())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton and self._drag_pos is not None:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
