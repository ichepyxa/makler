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


class HistoryPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("История обменов")
        title.setObjectName("pageTitle")
        description = QLabel("Завершённые обмены квартир.")
        description.setObjectName("pageDescription")

        self.table = QTableWidget(0, 6)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(
            [
                "№",
                "Дата обмена",
                "Заявка 1 — ищет",
                "Заявка 1 — предлагает",
                "Заявка 2 — ищет",
                "Заявка 2 — предлагает",
            ]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.table, 1)

    def set_exchanges(self, exchanges: list[dict]) -> None:
        self.table.clearContents()
        self.table.setRowCount(len(exchanges))
        for row, exchange in enumerate(exchanges):
            values = [
                exchange["id"],
                exchange["created_at"],
                exchange["first_desired"],
                exchange["first_offered"],
                exchange["second_desired"],
                exchange["second_offered"],
            ]
            self.table.setRowHeight(row, 64)
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, column, item)
        self.table.scrollToTop()
