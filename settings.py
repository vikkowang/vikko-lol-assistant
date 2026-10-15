"""设置对话框：编辑 api_key、systemPrompt 与联网搜索开关，保存回 config.json。"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from config import load_config, save_config

STYLE = """
QDialog { background: #1a1c22; color: #e5e7eb; }
QLabel { color: #9aa0b0; }
QLineEdit, QPlainTextEdit {
    background: #22252e; color: #e5e7eb;
    border: 1px solid #33363f; border-radius: 6px; padding: 6px;
}
QPushButton {
    background: #2a2d37; color: #e5e7eb;
    border: none; border-radius: 6px; padding: 6px 16px;
}
QPushButton:hover { background: #3a3e4a; }
QCheckBox { color: #e5e7eb; }
"""


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setStyleSheet(STYLE)
        self.setMinimumWidth(440)
        self._build()
        self._load()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        form = QFormLayout()
        form.setSpacing(10)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("阿里云百炼（千问）API Key，sk- 开头")
        form.addRow("千问 API Key", self.api_key_edit)

        key_hint = QLabel(
            '<a href="https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key">'
            "https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key</a>"
        )
        key_hint.setOpenExternalLinks(True)
        key_hint.setWordWrap(True)
        key_hint.setStyleSheet("font-size: 11px;")
        form.addRow("", key_hint)

        self.prompt_edit = QPlainTextEdit()
        self.prompt_edit.setPlaceholderText("systemPrompt，例如：你是英雄联盟（LOL）游戏助手……")
        self.prompt_edit.setFixedHeight(110)
        form.addRow("systemPrompt", self.prompt_edit)

        self.web_search_check = QCheckBox("联网搜索（回答前先搜索最新信息，会稍慢）")
        form.addRow("", self.web_search_check)

        root.addLayout(form)

        hint = QLabel("保存后立即生效，无需重启。")
        root.addWidget(hint)

        btns = QHBoxLayout()
        btns.addStretch()
        self.cancel_btn = QPushButton("取消")
        self.save_btn = QPushButton("保存")
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.save_btn)
        root.addLayout(btns)

        self.save_btn.clicked.connect(self._save)
        self.cancel_btn.clicked.connect(self.reject)

    def _load(self):
        try:
            cfg = load_config()
        except FileNotFoundError:
            return
        self.api_key_edit.setText(cfg.get("api_key", ""))
        self.prompt_edit.setPlainText(cfg.get("prompt", ""))
        self.web_search_check.setChecked(cfg.get("web_search", True))

    def _save(self):
        try:
            cfg = load_config()
        except FileNotFoundError:
            cfg = {}
        cfg["api_key"] = self.api_key_edit.text().strip()
        cfg["prompt"] = self.prompt_edit.toPlainText().strip()
        cfg["web_search"] = self.web_search_check.isChecked()
        save_config(cfg)
        self.accept()
