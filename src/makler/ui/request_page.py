from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from makler.ui.widgets.apartment_form import ApartmentForm
from makler.ui.widgets.match_result import MatchResult
from makler.ui.widgets.registry_table import RegistryTable


DISTRICTS = [
    "Центральный",
    "Московский",
    "Советский",
    "Первомайский",
    "Партизанский",
    "Фрунзенский",
]


class RequestPage(QWidget):
    request_submitted = Signal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("requestPage")
        self._create_ui()

    def _create_ui(self) -> None:
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 28)
        content_layout.setSpacing(16)

        icon = QLabel("▤")
        icon.setObjectName("pageHeadingIcon")

        title = QLabel("Ввод заявки на обмен квартир")
        title.setObjectName("pageTitle")

        heading = QHBoxLayout()
        heading.setSpacing(14)
        heading.addWidget(icon)
        heading.addWidget(title)
        heading.addStretch()
        content_layout.addLayout(heading)

        description = QLabel(
            "Укажите квартиру, которую необходимо получить, "
            "и квартиру, предлагаемую для обмена."
        )
        description.setObjectName("pageDescription")
        content_layout.addWidget(description)

        card = QFrame()
        card.setObjectName("requestCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 0, 18, 16)
        card_layout.setSpacing(14)

        card_header = QFrame()
        card_header.setObjectName("requestCardHeader")

        header_layout = QHBoxLayout(card_header)
        header_layout.setContentsMargins(18, 8, 12, 8)

        card_title = QLabel("Новая заявка на обмен")
        card_title.setObjectName("requestCardTitle")

        close_button = QPushButton("×")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(34, 34)
        close_button.clicked.connect(self._clear_forms)

        header_layout.addWidget(card_title)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        card_layout.addWidget(card_header)

        forms_layout = QHBoxLayout()
        forms_layout.setSpacing(18)

        self.desired_form = ApartmentForm(
            "Требуемая (искомая) квартира",
            "blue",
            DISTRICTS,
        )

        self.offered_form = ApartmentForm(
            "Имеющаяся квартира",
            "green",
            DISTRICTS,
        )

        self.desired_form.area_spin.setValue(55.0)
        self.offered_form.area_spin.setValue(60.0)
        self.offered_form.district_combo.setCurrentText(
            "Московский"
        )

        forms_layout.addWidget(self.desired_form, 1)
        forms_layout.addWidget(self.offered_form, 1)
        card_layout.addLayout(forms_layout)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        buttons.addStretch()

        find_button = QPushButton("Найти подходящий вариант")
        find_button.setObjectName("findButton")
        find_button.setMinimumWidth(290)
        find_button.setMinimumHeight(44)
        find_button.clicked.connect(self._submit_request)

        cancel_button = QPushButton("Отмена")
        cancel_button.setObjectName("cancelButton")
        cancel_button.setMinimumWidth(110)
        cancel_button.setMinimumHeight(44)
        cancel_button.clicked.connect(self._clear_forms)

        buttons.addWidget(find_button)
        buttons.addWidget(cancel_button)
        card_layout.addLayout(buttons)

        content_layout.addWidget(card)

        self.match_result = MatchResult()
        self.match_result.hide()
        content_layout.addWidget(self.match_result)

        registry_icon = QLabel("☷")
        registry_icon.setObjectName("registryIcon")

        registry_title = QLabel("Картотека заявок")
        registry_title.setObjectName("sectionTitle")

        registry_heading = QHBoxLayout()
        registry_heading.setSpacing(12)
        registry_heading.addWidget(registry_icon)
        registry_heading.addWidget(registry_title)
        registry_heading.addStretch()
        content_layout.addLayout(registry_heading)

        self.registry_table = RegistryTable()
        content_layout.addWidget(self.registry_table)
        content_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setObjectName("pageScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll.setWidget(content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

    def _submit_request(self) -> None:
        self.match_result.hide()

        self.request_submitted.emit(
            {
                "desired": self.desired_form.get_values(),
                "offered": self.offered_form.get_values(),
            }
        )

    def _clear_forms(self) -> None:
        self.desired_form.reset()
        self.offered_form.reset()
        self.offered_form.area_spin.setValue(60.0)
        self.offered_form.district_combo.setCurrentText(
            "Московский"
        )
        self.match_result.hide()

    def show_match_result(
        self,
        request_id: int,
        desired: str,
        offered: str,
    ) -> None:
        self.match_result.set_match(
            request_id,
            desired,
            offered,
        )

    def show_no_match_result(self) -> None:
        self.match_result.set_no_match()

    def set_requests(self, requests: list[dict]) -> None:
        self.registry_table.set_requests(requests)