from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QInputDialog,
    QMessageBox
)
from PySide6.QtCore import Qt
from utils import hotkeys


class HotkeysPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_hotkeys()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Hotkeys")
        title.setObjectName("hotkeysTitle")
        root.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Action", "Shortcut"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_hotkey)
        self.edit_btn.clicked.connect(self.edit_hotkey)
        self.remove_btn.clicked.connect(self.remove_hotkey)
        self.refresh_btn.clicked.connect(self.load_hotkeys)

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.refresh_btn)
        root.addLayout(btn_row)

        self.apply_styles()

    def load_hotkeys(self):
        data = hotkeys.get_hotkeys()
        self.table.setRowCount(len(data))
        for row, hk in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(hk["action"]))
            self.table.setItem(row, 1, QTableWidgetItem(hk["shortcut"]))

    def get_selected_action(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 0).text()

    def add_hotkey(self):
        action, ok = QInputDialog.getText(self, "Add Hotkey", "Action name:")
        if not ok or not action:
            return
        shortcut, ok = QInputDialog.getText(self, "Add Hotkey", "Shortcut:")
        if not ok or not shortcut:
            return
        hotkeys.add_hotkey(action, shortcut)
        self.load_hotkeys()

    def edit_hotkey(self):
        action = self.get_selected_action()
        if not action:
            return
        shortcut, ok = QInputDialog.getText(self, "Edit Hotkey", "New shortcut:")
        if not ok:
            return
        hotkeys.update_hotkey(action, shortcut)
        self.load_hotkeys()

    def remove_hotkey(self):
        action = self.get_selected_action()
        if not action:
            return
        confirm = QMessageBox.question(self, "Remove Hotkey", f"Delete hotkey for {action}?")
        if confirm == QMessageBox.Yes:
            hotkeys.delete_hotkey(action)
            self.load_hotkeys()

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#hotkeysTitle {{
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
