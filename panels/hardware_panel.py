import platform
import psutil

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout
)
from PySide6.QtCore import Qt, QTimer


class HardwarePanel(QWidget):
    """
    Hardware Panel
    Displays basic system information:
    CPU usage, RAM usage, OS info.
    """

    def __init__(self, config=None):
        super().__init__()

        self.config = config
        self.accent = "#66ffcc"

        self.build_ui()
        self.update_stats()

        # auto refresh every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    # ---------- UI ----------

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        title = QLabel("Hardware")
        title.setObjectName("hwTitle")
        root.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        # cards
        self.cpu_label = self.make_card("CPU Usage")
        self.ram_label = self.make_card("Memory Usage")
        self.sys_label = self.make_card("System Info")
        self.platform_label = self.make_card("Platform")

        grid.addWidget(self.cpu_label.parentWidget(), 0, 0)
        grid.addWidget(self.ram_label.parentWidget(), 0, 1)
        grid.addWidget(self.sys_label.parentWidget(), 1, 0)
        grid.addWidget(self.platform_label.parentWidget(), 1, 1)

        root.addLayout(grid)
        root.addStretch()

        self.apply_styles()

    def make_card(self, title_text):
        card = QFrame()
        card.setObjectName("hwCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")

        value = QLabel("Loading...")
        value.setObjectName("cardValue")
        value.setAlignment(Qt.AlignLeft)

        layout.addWidget(title)
        layout.addWidget(value)

        # return the value label but keep card container
        value._card = card
        return value

    # ---------- Data ----------

    def update_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()

        self.cpu_label.setText(f"{cpu}%")
        self.ram_label.setText(f"{mem.percent}% ({self.bytes_to_gb(mem.used)} / {self.bytes_to_gb(mem.total)})")

        self.sys_label.setText(platform.system() + " " + platform.release())
        self.platform_label.setText(platform.machine())

    def bytes_to_gb(self, b):
        return f"{b / (1024**3):.1f} GB"

    # ---------- Styles ----------

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}

            QLabel#hwTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {self.accent};
            }}

            QFrame#hwCard {{
                background-color: #161a21;
                border-radius: 8px;
            }}

            QLabel#cardTitle {{
                font-size: 13px;
                color: #8fcfb5;
            }}

            QLabel#cardValue {{
                font-size: 18px;
                font-weight: bold;
                color: {self.accent};
            }}
        """)
