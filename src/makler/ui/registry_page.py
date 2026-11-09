from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from makler.ui.widgets.registry_table import RegistryTable


class RegistryPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        title = QLabel("Картотека заявок")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Просмотр всех активных заявок на обмен квартир."
        )
        description.setObjectName("pageDescription")

        self.table = RegistryTable()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(16)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.table, 1)

        self.setLayout(layout)