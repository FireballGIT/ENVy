import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt


class EnvPanel(QWidget):
    """
    ENV Panel
    - View environment variables
    - Add / Edit / Remove
    Real system modification logic should live in utils/,
    NOT directly in this panel.
    """

    def __init__(self, config=None):
        super().__init__()

        self.config = config
        self.accent = "#66ffcc"

        self.build_ui()
        self.load_env()

    # ---------- UI ----------

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        # Title
        title = QLabel("Environment Variables")
        title.setObjectName("envTitle")
        root.addWidget(title)

        # --- Search Bar ---
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search variable...")
        self.search.textChanged.connect(self.filter_env)
        root.addWidget(self.search)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        root.addWidget(self.table)

        # --- Buttons ---
        btn_row = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")
        self.refresh_btn = QPushButton("Refresh")

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.refresh_btn)

        root.addLayout(btn_row)

        self.apply_styles()

    # ---------- Data ----------

    def load_env(self):
        """Load environment variables into table."""
        env = dict(os.environ)

        self.table.setRowCount(len(env))

        for row, (key, value) in enumerate(env.items()):
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(value))

    def filter_env(self, text):
        """Simple client-side filter."""
        text = text.lower()

        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            value_item = self.table.item(row, 1)

            key = key_item.text().lower()
            value = value_item.text().lower()

            match = text in key or text in value
            self.table.setRowHidden(row, not match)

    # ---------- Styles ----------

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
                background-color: #161a21;
                border-radius: 6px;
                padding: 6px 12px;
            }}

            QPushButton:hover {{
                background-color: #1c212b;
            }}
        """)
