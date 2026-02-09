from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QColorDialog,
    QHBoxLayout
)
from PySide6.QtCore import Qt
import config


class SettingsPanel(QWidget):
    def __init__(self, config_data=None):
        super().__init__()
        self.config_data = config_data or config.load_config()
        self.accent = self.config_data.get("accent_color", "#66ffcc")
        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Settings")
        title.setObjectName("settingsTitle")
        root.addWidget(title)

        color_row = QHBoxLayout()
        self.color_label = QLabel(f"Accent Color: {self.accent}")
        self.color_btn = QPushButton("Change")
        self.color_btn.clicked.connect(self.change_accent)

        color_row.addWidget(self.color_label)
        color_row.addStretch()
        color_row.addWidget(self.color_btn)
        root.addLayout(color_row)

        self.apply_styles()

    def change_accent(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.accent = color.name()
            self.color_label.setText(f"Accent Color: {self.accent}")
            self.config_data["accent_color"] = self.accent
            config.save_config(self.config_data)
            self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#settingsTitle {{
                font-size: 20px;
                font-weight: bold;
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
