from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from utils import hardware


class HardwarePanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.update_stats()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        title = QLabel("Hardware")
        title.setObjectName("hwTitle")
        root.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.cpu_label = self.make_card("CPU Usage")
        self.ram_label = self.make_card("Memory Usage")
        self.sys_label = self.make_card("System Info")
        self.platform_label = self.make_card("Platform")

        grid.addWidget(self.cpu_label._card, 0, 0)
        grid.addWidget(self.ram_label._card, 0, 1)
        grid.addWidget(self.sys_label._card, 1, 0)
        grid.addWidget(self.platform_label._card, 1, 1)

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
        value._card = card
        return value

    def update_stats(self):
        self.cpu_label.setText(f"{hardware.get_cpu_usage()}%")
        mem_used, mem_total, mem_percent = hardware.get_memory_usage()
        self.ram_label.setText(f"{mem_percent:.2f}% ({mem_used} / {mem_total})")
        self.sys_label.setText(hardware.get_system_info())
        self.platform_label.setText(hardware.get_platform())

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
