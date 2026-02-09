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
from utils import network


class NetworkPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.accent = "#66ffcc"
        self.build_ui()
        self.load_connections()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        title = QLabel("Network")
        title.setObjectName("networkTitle")
        root.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["SSID / IP", "Type", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.disconnect_btn = QPushButton("Disconnect")
        self.ping_btn = QPushButton("Ping")

        self.refresh_btn.clicked.connect(self.load_connections)
        self.disconnect_btn.clicked.connect(self.disconnect_network)
        self.ping_btn.clicked.connect(self.ping_target)

        btn_row.addWidget(self.refresh_btn)
        btn_row.addWidget(self.disconnect_btn)
        btn_row.addWidget(self.ping_btn)
        root.addLayout(btn_row)

        self.apply_styles()

    def load_connections(self):
        data = network.get_connections()
        self.table.setRowCount(len(data))
        for row, conn in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(conn["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(conn["type"]))
            self.table.setItem(row, 2, QTableWidgetItem(conn["status"]))

    def get_selected_connection(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 0).text()

    def disconnect_network(self):
        target = self.get_selected_connection()
        if not target:
            return
        confirm = QMessageBox.question(self, "Disconnect Network", f"Disconnect {target}?")
        if confirm == QMessageBox.Yes:
            network.disconnect(target)
            self.load_connections()

    def ping_target(self):
        target = self.get_selected_connection()
        if not target:
            return
        result = network.ping(target)
        QMessageBox.information(self, "Ping Result", f"{target}:\n{result}")

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f1115;
                color: {self.accent};
                font-family: Segoe UI, Arial;
            }}
            QLabel#networkTitle {{
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
