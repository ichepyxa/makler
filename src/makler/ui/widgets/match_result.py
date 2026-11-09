from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class MatchResult(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("matchResult")

        self.icon = QLabel("✓")
        self.icon.setObjectName("matchCheck")
        self.icon.setFixedSize(44, 44)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel()
        self.title.setObjectName("matchResultTitle")

        self.description = QLabel()
        self.description.setObjectName("matchResultDescription")

        header = QHBoxLayout()
        header.setContentsMargins(20, 12, 20, 4)
        header.setSpacing(14)

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.title)
        text_layout.addWidget(self.description)

        header.addWidget(self.icon)
        header.addLayout(text_layout, 1)

        self.desired_label = QLabel()
        self.offered_label = QLabel()

        self.desired_label.setObjectName("matchDetail")
        self.offered_label.setObjectName("matchDetail")

        self.details = QFrame()
        self.details.setObjectName("matchDetails")

        details_layout = QHBoxLayout(self.details)
        details_layout.setContentsMargins(14, 8, 14, 8)
        details_layout.addWidget(self.desired_label, 1)
        details_layout.addWidget(self.offered_label, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(6)
        layout.addLayout(header)
        layout.addWidget(self.details)

        self.setLayout(layout)

    def set_match(
        self,
        request_id: int,
        desired: str,
        offered: str,
    ) -> None:
        self.setProperty("state", "success")
        self.icon.setText("✓")
        self.title.setText("Подходящий вариант найден!")
        self.description.setText(
            f"Найдена заявка № {request_id}. "
            "Обе заявки удалены из картотеки."
        )
        self.desired_label.setText(
            f"Требуемая квартира:\n{desired}"
        )
        self.offered_label.setText(
            f"Имеющаяся квартира:\n{offered}"
        )
        self.details.show()
        self._refresh_style()
        self.show()

    def set_no_match(self) -> None:
        self.setProperty("state", "info")
        self.icon.setText("i")
        self.title.setText("Подходящий вариант не найден")
        self.description.setText(
            "Новая заявка добавлена в картотеку."
        )
        self.details.hide()
        self._refresh_style()
        self.show()

    def _refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()