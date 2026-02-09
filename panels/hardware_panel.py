from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt
from utils import processes


class ProcessesPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_processes()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Processes")
        title.setObjectName("procTitle")
        root.addWidget(title)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search process...")
        self.search.textChanged.connect(self.filter_processes)
        root.addWidget(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "PID", "CPU %", "Memory %"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.end_btn = QPushButton("End Process")

        self.refresh_btn.clicked.connect(self.load_processes)
        self.end_btn.clicked.connect(self.kill_process)

        btn_row.addWidget(self.refresh_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.end_btn)
        root.addLayout(btn_row)

        self.apply_styles()

    def load_processes(self):
        data = processes.get_process_list()
        self.table.setRowCount(len(data))
        for row, proc in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(proc["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(proc["pid"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(proc["cpu"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{proc['memory']:.2f}"))

    def filter_processes(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            match = text in name_item.text().lower()
            self.table.setRowHidden(row, not match)

    def get_selected_pid(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 1).text())

    def kill_process(self):
        pid = self.get_selected_pid()
        if not pid:
            return
        confirm = QMessageBox.question(self, "Kill Process", f"End PID {pid}?")
        if confirm == QMessageBox.Yes:
            processes.terminate_process(pid)
            self.load_processes()

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
