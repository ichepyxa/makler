from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout


class Sidebar(QFrame):
    page_changed = Signal(int)
    exit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(230)

        self.buttons: list[QPushButton] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 18, 12, 16)
        layout.setSpacing(8)

        for index, title in enumerate(("＋  Новая заявка", "▤  Картотека")):
            button = QPushButton(title)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, page=index: self.select_page(page)
            )
            self.buttons.append(button)
            layout.addWidget(button)

        layout.addStretch()

        exit_button = QPushButton("Выход")
        exit_button.setObjectName("exitButton")
        exit_button.clicked.connect(self.exit_requested)
        layout.addWidget(exit_button)

        self.select_page(0)

    def select_page(self, index: int) -> None:
        for page, button in enumerate(self.buttons):
            button.setChecked(page == index)
        self.page_changed.emit(index)
