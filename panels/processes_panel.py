import psutil

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


class ProcessesPanel(QWidget):
    """
    Processes Panel
    Shows running processes similar to a lightweight task manager.
    Later you can connect buttons to utils/process_utils.py.
    """

    def __init__(self, config=None):
        super().__init__()

        self.config = config
        self.accent = "#66ffcc"

        self.build_ui()
        self.load_processes()

    # ---------- UI ----------

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Processes")
        title.setObjectName("procTitle")
        root.addWidget(title)

        # Search
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search process...")
        self.search.textChanged.connect(self.filter_processes)
        root.addWidget(self.search)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "PID", "CPU %", "Memory %"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        root.addWidget(self.table)

        # Buttons
        btn_row = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh")
        self.end_btn = QPushButton("End Process")

        self.refresh_btn.clicked.connect(self.load_processes)

        btn_row.addWidget(self.refresh_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.end_btn)

        root.addLayout(btn_row)

        self.apply_styles()

    # ---------- Data ----------

    def load_processes(self):
        processes = []

        for proc in psutil.process_iter(["name", "pid", "cpu_percent", "memory_percent"]):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.table.setRowCount(len(processes))

        for row, p in enumerate(processes):
            self.table.setItem(row, 0, QTableWidgetItem(str(p["name"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(p["pid"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["cpu_percent"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{p['memory_percent']:.2f}"))

    def filter_processes(self, text):
        text = text.lower()

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            match = text in name_item.text().lower()
            self.table.setRowHidden(row, not match)

    # ---------- Styles ----------

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}

            QLabel#procTitle {{
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
                padding: 6px 10px;
            }}

            QPushButton:hover {{
                background-color: #222833;
            }}
        """)
