from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedLayout,
    QLabel
)
from PySide6.QtCore import Qt
from panels import (
    env_panel,
    system_panel,
    processes_panel,
    hardware_panel,
    startup_panel,
    network_panel,
    logs_panel,
    hotkeys_panel,
    settings_panel
)
from utils import config
import sys


class ENVyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.config_data = config.load_config()
        self.accent = self.config_data.get("accent_color", "#66ffcc")
        self.setWindowTitle("ENVy")
        self.resize(1000, 650)
        self.build_ui()

    def build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSpacing(0)

        self.stack = QStackedLayout()

        self.panels = {
            "Home": QLabel("Welcome to ENVy"),
            "ENV": env_panel.EnvPanel(self.config_data),
            "System": system_panel.SystemPanel(self.config_data),
            "Processes": processes_panel.ProcessesPanel(self.config_data),
            "Hardware": hardware_panel.HardwarePanel(self.config_data),
            "Startup": startup_panel.StartupPanel(self.config_data),
            "Network": network_panel.NetworkPanel(self.config_data),
            "Logs": logs_panel.LogsPanel(self.config_data),
            "Hotkeys": hotkeys_panel.HotkeysPanel(self.config_data),
            "Settings": settings_panel.SettingsPanel(self.config_data)
        }

        for name, panel in self.panels.items():
            if isinstance(panel, QLabel):
                panel.setAlignment(Qt.AlignCenter)
            self.stack.addWidget(panel)

        for name in self.panels.keys():
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, n=name: self.switch_panel(n))
            btn.setFixedHeight(40)
            self.sidebar.addWidget(btn)

        self.sidebar.addStretch()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(self.sidebar)
        sidebar_widget.setFixedWidth(140)
        sidebar_widget.setStyleSheet(f"background-color: #161a21; color: {self.accent};")

        main_widget = QWidget()
        main_widget.setLayout(self.stack)

        root.addWidget(sidebar_widget)
        root.addWidget(main_widget)
        self.apply_styles()

    def switch_panel(self, name):
        panel = list(self.panels.keys()).index(name)
        self.stack.setCurrentIndex(panel)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QPushButton {{
                background-color: #1a1f27;
                border: none;
                color: {self.accent};
            }}
            QPushButton:hover {{
                background-color: #222833;
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ENVyApp()
    window.show()
    sys.exit(app.exec())
