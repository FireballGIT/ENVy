from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox
)
from PySide6.QtCore import Qt
from utils import logs


class LogsPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_logs()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Logs")
        title.setObjectName("logsTitle")
        root.addWidget(title)

        self.list_widget = QListWidget()
        root.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.clear_btn = QPushButton("Clear")
        self.download_btn = QPushButton("Download")

        self.refresh_btn.clicked.connect(self.load_logs)
        self.clear_btn.clicked.connect(self.clear_logs)
        self.download_btn.clicked.connect(self.download_logs)

        btn_row.addWidget(self.refresh_btn)
        btn_row.addWidget(self.clear_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.download_btn)
        root.addLayout(btn_row)

        self.apply_styles()

    def load_logs(self):
        self.list_widget.clear()
        for entry in logs.get_logs():
            self.list_widget.addItem(entry)

    def clear_logs(self):
        confirm = QMessageBox.question(self, "Clear Logs", "Are you sure you want to clear all logs?")
        if confirm == QMessageBox.Yes:
            logs.clear_logs()
            self.load_logs()

    def download_logs(self):
        logs.download_logs()
        QMessageBox.information(self, "Download", "Logs have been downloaded.")

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#logsTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {self.accent};
            }}
            QListWidget {{
                background-color: #161a21;
                border: none;
                color: {self.accent};
            }}
            QPushButton {{
                background-color: #1a1f27;
                border-radius: 6px;
                padding: 6px 10px;
            }}
            QPushButton:hover {{
                background-color: #222833;
            }}
        """)
