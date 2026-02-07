from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QHBoxLayout
)
from PySide6.QtCore import Qt


class HomePanel(QWidget):
    """
    ENVy Home Panel
    This is the landing dashboard shown when the app opens.
    Keep it lightweight — real data can be injected later.
    """

    def __init__(self, config=None):
        super().__init__()

        self.config = config
        self.accent = "#66ffcc"

        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # ---- Title ----
        title = QLabel("ENVy Dashboard")
        title.setObjectName("envyTitle")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # ---- Subtitle ----
        subtitle = QLabel("System overview and quick access.")
        subtitle.setObjectName("envySubtitle")

        root.addWidget(title)
        root.addWidget(subtitle)

        # ---- Cards Row ----
        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)

        cards_row.addWidget(self.make_card("Environment", "Manage variables easily"))
        cards_row.addWidget(self.make_card("System", "Quick control panel access"))
        cards_row.addWidget(self.make_card("Hotkeys", "Automation made simple"))

        root.addLayout(cards_row)

        # Spacer
        root.addStretch()

        self.apply_styles()

    def make_card(self, title, desc):
        card = QFrame()
        card.setObjectName("envyCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)

        t = QLabel(title)
        t.setObjectName("cardTitle")

        d = QLabel(desc)
        d.setObjectName("cardDesc")
        d.setWordWrap(True)

        layout.addWidget(t)
        layout.addWidget(d)

        return card

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}

            QLabel#envyTitle {{
                font-size: 22px;
                font-weight: bold;
                color: {self.accent};
            }}

            QLabel#envySubtitle {{
                font-size: 12px;
                color: #9be3c6;
            }}

            QFrame#envyCard {{
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
        """)
