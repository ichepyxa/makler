from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from makler.domain import CITY_DISTRICTS
from makler.ui.widgets.apartment_form import ApartmentForm

DISTRICTS = list(CITY_DISTRICTS)


class RequestPage(QWidget):
    requestsubmit_requestted = Signal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("page")

        title = QLabel("Новая заявка на обмен")
        title.setObjectName("pageTitle")
        description = QLabel(
            "Укажите квартиру, которую хотите получить, "
            "и квартиру, предлагаемую для обмена."
        )
        description.setObjectName("pageDescription")
        description.setWordWrap(True)

        self.desired_form = ApartmentForm(
            "Требуемая квартира", "blue", DISTRICTS
        )
        self.offered_form = ApartmentForm(
            "Имеющаяся квартира", "green", DISTRICTS
        )
        self.offered_form.area_spin.setValue(60.0)
        self.offered_form.district_combo.setCurrentText(DISTRICTS[1])

        forms = QHBoxLayout()
        forms.setSpacing(14)
        forms.addWidget(self.desired_form, 1)
        forms.addWidget(self.offered_form, 1)

        self.result_label = QLabel()
        self.result_label.setObjectName("resultLabel")
        self.result_label.setWordWrap(True)
        self.result_label.hide()

        submit_button = QPushButton("Проверить обмен и обработать заявку")
        submit_button.setObjectName("primaryButton")
        submit_button.clicked.connect(self.submit_request)

        clear_button = QPushButton("Очистить")
        clear_button.setObjectName("secondaryButton")
        clear_button.clicked.connect(self.clear_form)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(clear_button)
        buttons.addWidget(submit_button)

        card = QFrame()
        card.setObjectName("contentCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(16)
        card_layout.addLayout(forms)
        card_layout.addLayout(buttons)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(card)
        layout.addWidget(self.result_label)
        layout.addStretch()

    def submit_request(self) -> None:
        self.result_label.hide()
        self.requestsubmit_requestted.emit(
            {
                "desired": self.desired_form.get_values(),
                "offered": self.offered_form.get_values(),
            }
        )

    def clear_form(self) -> None:
        self.desired_form.reset()
        self.offered_form.reset()
        self.offered_form.area_spin.setValue(60.0)
        self.offered_form.district_combo.setCurrentText("Московский")
        self.result_label.clear()
        self.result_label.hide()

    def show_saved(self) -> None:
        self.result_label.setProperty("state", "info")
        self.result_label.setText(
            "Заявка добавлена в картотеку: подходящего взаимного обмена не найдено."
        )
        self.update_result_style()

    def show_exchange(self, request_id: int, first: str, second: str) -> None:
        self.result_label.setProperty("state", "success")
        self.result_label.setText(
            f"Найдено соответствие с заявкой № {request_id}.\n"
            "Найденная заявка удалена из картотеки.\n\n"
            f"Заявка из картотеки — ищет: {first}\n"
            f"Заявка из картотеки — предлагает: {second}"
        )
        self.update_result_style()

    def update_result_style(self) -> None:
        self.result_label.style().unpolish(self.result_label)
        self.result_label.style().polish(self.result_label)
        self.result_label.show()
