from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RegistryPage(QWidget):
    edit_requested = Signal(int)
    delete_requested = Signal(int)

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
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setColumnWidth(0, 55)
        self.table.setColumnWidth(3, 115)
        self.table.itemSelectionChanged.connect(self.update_action_buttons)

        self.edit_button = QPushButton("Изменить выбранную")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.emitedit_requested)

        self.delete_button = QPushButton("Удалить выбранную")
        self.delete_button.setObjectName("dangerButton")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.emitdelete_requested)

        actions = QHBoxLayout()
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        actions.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(actions)
        layout.addWidget(self.table, 1)

    def selected_request_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        request_id = item.data(Qt.ItemDataRole.UserRole)
        return int(request_id) if request_id is not None else None

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
                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, request["id"])
                self.table.setItem(row, column, item)
        self.table.clearSelection()
        self.update_action_buttons()
        self.table.scrollToTop()

    def update_action_buttons(self) -> None:
        hasselect_pageion = self.selected_request_id() is not None
        self.edit_button.setEnabled(hasselect_pageion)
        self.delete_button.setEnabled(hasselect_pageion)

    def emitedit_requested(self) -> None:
        request_id = self.selected_request_id()
        if request_id is not None:
            self.edit_requested.emit(request_id)

    def emitdelete_requested(self) -> None:
        request_id = self.selected_request_id()
        if request_id is not None:
            self.delete_requested.emit(request_id)
