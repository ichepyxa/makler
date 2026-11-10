from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RegistryTable(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        desired_header = QLabel("Требуемая квартира")
        desired_header.setObjectName("desiredTableHeader")
        desired_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        offered_header = QLabel("Имеющаяся квартира")
        offered_header.setObjectName("offeredTableHeader")
        offered_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        group_layout = QHBoxLayout()
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(0)
        group_layout.addSpacing(48)
        group_layout.addWidget(desired_header, 4)
        group_layout.addWidget(offered_header, 4)
        group_layout.addSpacing(140)

        self.table = QTableWidget(0, 10)
        self.table.setObjectName("registryTable")

        self.table.setHorizontalHeaderLabels(
            [
                "№",
                "Комнаты",
                "Площадь",
                "Этаж",
                "Район",
                "Комнаты",
                "Площадь",
                "Этаж",
                "Район",
                "Дата подачи",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Fixed,
        )
        header.setSectionResizeMode(
            9,
            QHeaderView.ResizeMode.Fixed,
        )

        self.table.setColumnWidth(0, 48)
        self.table.setColumnWidth(9, 140)
        self.table.horizontalHeader().setMinimumHeight(42)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(group_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def set_requests(self, requests: list[dict]) -> None:
        self.table.setRowCount(len(requests))

        for row_index, request in enumerate(requests):
            self.table.setRowHeight(row_index, 36)

            values = [
                request["id"],
                request["desired_rooms"],
                request["desired_area"],
                request["desired_floor"],
                request["desired_district"],
                request["offered_rooms"],
                request["offered_area"],
                request["offered_floor"],
                request["offered_district"],
                request["created_at"],
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )