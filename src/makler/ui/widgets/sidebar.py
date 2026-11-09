from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class SidebarItem(QPushButton):
    def __init__(
        self,
        symbol: str,
        title: str,
        description: str,
        is_add: bool = False,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("sidebarItem")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(88)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        icon = QLabel(symbol)
        icon.setObjectName(
            "sidebarIconAdd" if is_add else "sidebarIcon"
        )
        icon.setFixedSize(58, 58)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("sidebarTitle")

        description_label = QLabel(description)
        description_label.setObjectName("sidebarDescription")
        description_label.setWordWrap(True)

        for widget in (icon, title_label, description_label):
            widget.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(3)
        text_layout.addWidget(title_label)
        text_layout.addWidget(description_label)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 10, 10)
        layout.setSpacing(14)
        layout.addWidget(icon)
        layout.addLayout(text_layout, 1)

        self.setLayout(layout)


class Sidebar(QFrame):
    page_changed = Signal(int)
    exit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(340)

        self.items = [
            SidebarItem(
                "＋",
                "Ввести заявку",
                "Добавление новой заявки\nна обмен квартир",
                is_add=True,
            ),
            SidebarItem(
                "⌕",
                "Поиск варианта",
                "Поиск подходящего\nварианта обмена",
            ),
            SidebarItem(
                "▤",
                "Картотека",
                "Просмотр всех заявок",
            ),
            SidebarItem(
                "⚙",
                "Настройки",
                "Параметры программы",
            ),
        ]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 24, 12, 18)
        layout.setSpacing(10)

        for index, item in enumerate(self.items):
            item.clicked.connect(
                lambda checked=False, i=index: self._select(i)
            )
            layout.addWidget(item)

        layout.addStretch()

        self.exit_item = SidebarItem(
            "⇥",
            "Выход",
            "Завершение работы",
        )
        self.exit_item.clicked.connect(self.exit_requested)
        layout.addWidget(self.exit_item)

        self._select(0)

    def _select(self, index: int) -> None:
        for i, item in enumerate(self.items):
            item.setChecked(i == index)

        self.page_changed.emit(index)