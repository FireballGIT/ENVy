from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QInputDialog,
    QMessageBox
)
from PySide6.QtCore import Qt
from utils import env_manager


class EnvPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_env()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Environment Variables")
        title.setObjectName("envTitle")
        root.addWidget(title)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search variable...")
        self.search.textChanged.connect(self.filter_env)
        root.addWidget(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_env)
        self.edit_btn.clicked.connect(self.edit_env)
        self.remove_btn.clicked.connect(self.remove_env)
        self.refresh_btn.clicked.connect(self.load_env)

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.refresh_btn)

        root.addLayout(btn_row)
        self.apply_styles()

    def load_env(self):
        env = env_manager.get_env_vars()
        self.table.setRowCount(len(env))
        for row, (key, value) in enumerate(env.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(key)))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

    def filter_env(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text().lower()
            val = self.table.item(row, 1).text().lower()
            match = text in key or text in val
            self.table.setRowHidden(row, not match)

    def get_selected_key(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 0).text()

    def add_env(self):
        key, ok = QInputDialog.getText(self, "Add Variable", "Variable name:")
        if not ok or not key:
            return
        value, ok = QInputDialog.getText(self, "Add Variable", "Value:")
        if not ok:
            return
        env_manager.set_env_var(key, value)
        self.load_env()

    def edit_env(self):
        key = self.get_selected_key()
        if not key:
            return
        value, ok = QInputDialog.getText(self, "Edit Variable", "New value:")
        if not ok:
            return
        env_manager.set_env_var(key, value)
        self.load_env()

    def remove_env(self):
        key = self.get_selected_key()
        if not key:
            return
        confirm = QMessageBox.question(self, "Remove Variable", f"Delete {key}?")
        if confirm == QMessageBox.Yes:
            env_manager.delete_env_var(key)
            self.load_env()

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#envTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {self.accent};
            }}
            QLineEdit {{
                background-color: #161a21;
                border-radius: 6px;
                padding: 6px;
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
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #222833;
            }}
        """)
