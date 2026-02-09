from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QMessageBox,
    QInputDialog
)
from PySide6.QtCore import Qt
from utils import startup


class StartupPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_startup_items()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Startup Programs")
        title.setObjectName("startupTitle")
        root.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_startup)
        self.remove_btn.clicked.connect(self.remove_startup)
        self.refresh_btn.clicked.connect(self.load_startup_items)

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.refresh_btn)
        root.addLayout(btn_row)

        self.apply_styles()

    def load_startup_items(self):
        items = startup.get_startup_items()
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["path"]))

    def get_selected_item(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return {
            "name": self.table.item(row, 0).text(),
            "path": self.table.item(row, 1).text()
        }

    def add_startup(self):
        name, ok = QInputDialog.getText(self, "Add Startup Program", "Program name:")
        if not ok or not name:
            return
        path, ok = QInputDialog.getText(self, "Add Startup Program", "Program path:")
        if not ok or not path:
            return
        startup.add_startup_item(name, path)
        self.load_startup_items()

    def remove_startup(self):
        item = self.get_selected_item()
        if not item:
            return
        confirm = QMessageBox.question(self, "Remove Startup Program", f"Delete {item['name']}?")
        if confirm == QMessageBox.Yes:
            startup.remove_startup_item(item["name"])
            self.load_startup_items()

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#startupTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {self.accent};
            }}
            QTableWidget {{
                background-color: #161a21;
                border: none;
                gridline-color: #1e232c;
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
