from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QPushButton
)
from PySide6.QtCore import Qt


class SystemPanel(QWidget):
    """
    System Panel
    Think of this like a simplified control center.
    Buttons here will later connect to utils/system_utils.py.
    """

    def __init__(self, config=None):
        super().__init__()

        self.config = config
        self.accent = "#66ffcc"

        self.build_ui()

    # ---------- UI ----------

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # Title
        title = QLabel("System Controls")
        title.setObjectName("systemTitle")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        root.addWidget(title)

        # Grid of system cards
        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(self.make_card(
            "Display",
            "Resolution, scaling, brightness",
            ["Open Settings", "Detect Displays"]
        ), 0, 0)

        grid.addWidget(self.make_card(
            "Sound",
            "Output devices & volume",
            ["Audio Settings", "Mute Toggle"]
        ), 0, 1)

        grid.addWidget(self.make_card(
            "Power",
            "Sleep, shutdown, restart",
            ["Sleep", "Restart"]
        ), 1, 0)

        grid.addWidget(self.make_card(
            "Storage",
            "Disk info and cleanup",
            ["View Disks", "Cleanup"]
        ), 1, 1)

        root.addLayout(grid)
        root.addStretch()

        self.apply_styles()

    def make_card(self, title_text, desc_text, buttons):
        card = QFrame()
        card.setObjectName("systemCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")

        desc = QLabel(desc_text)
        desc.setObjectName("cardDesc")
        desc.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(desc)

        for b in buttons:
            btn = QPushButton(b)
            layout.addWidget(btn)

        return card

    # ---------- Styles ----------

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

            QLabel#cardDesc {{
                font-size: 11px;
                color: #8fcfb5;
            }}

            QPushButton {{
                background-color: #1a1f27;
                border-radius: 6px;
                padding: 6px 10px;
                text-align: left;
            }}

            QPushButton:hover {{
                background-color: #222833;
            }}
        """)
