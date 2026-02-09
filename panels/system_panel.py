from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QPushButton
)
from PySide6.QtCore import Qt
from utils import system_tools


class SystemPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        title = QLabel("System Controls")
        title.setObjectName("systemTitle")
        root.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(self.make_card("Display", ["Open Settings", "Detect Displays"]), 0, 0)
        grid.addWidget(self.make_card("Sound", ["Audio Settings", "Mute Toggle"]), 0, 1)
        grid.addWidget(self.make_card("Power", ["Sleep", "Restart"]), 1, 0)
        grid.addWidget(self.make_card("Storage", ["View Disks", "Cleanup"]), 1, 1)

        root.addLayout(grid)
        root.addStretch()
        self.apply_styles()

    def make_card(self, title_text, buttons):
        card = QFrame()
        card.setObjectName("systemCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        for b in buttons:
            btn = QPushButton(b)
            btn.clicked.connect(lambda _, name=b: self.handle_action(title_text, name))
            layout.addWidget(btn)

        return card

    def handle_action(self, card, action):
        if card == "Display":
            if action == "Open Settings":
                system_tools.open_display_settings()
            elif action == "Detect Displays":
                system_tools.detect_displays()
        elif card == "Sound":
            if action == "Audio Settings":
                system_tools.open_audio_settings()
            elif action == "Mute Toggle":
                system_tools.toggle_mute()
        elif card == "Power":
            if action == "Sleep":
                system_tools.sleep_system()
            elif action == "Restart":
                system_tools.restart_system()
        elif card == "Storage":
            if action == "View Disks":
                system_tools.view_disks()
            elif action == "Cleanup":
                system_tools.cleanup_storage()

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#systemTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {self.accent};
            }}
            QFrame#systemCard {{
                background-color: #161a21;
                border-radius: 8px;
            }}
            QLabel#cardTitle {{
                font-size: 14px;
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
