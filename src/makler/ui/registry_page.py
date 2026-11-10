from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RegistryPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("Картотека заявок")
        title.setObjectName("pageTitle")
        description = QLabel("Все действующие заявки на обмен квартир.")
        description.setObjectName("pageDescription")

        self.table = QTableWidget(0, 4)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(
            ["№", "Требуемая квартира", "Имеющаяся квартира", "Дата подачи"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setColumnWidth(0, 55)
        self.table.setColumnWidth(3, 115)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.table, 1)

    def set_requests(self, requests: list[dict]) -> None:
        self.table.clearContents()
        self.table.setRowCount(len(requests))
        for row, request in enumerate(requests):
            values = [
                request["id"],
                request["desired"],
                request["offered"],
                request["created_at"],
            ]
            self.table.setRowHeight(row, 54)
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, column, item)
        self.table.scrollToTop()
