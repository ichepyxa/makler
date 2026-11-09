from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
  QFrame,
  QHBoxLayout,
  QLabel,
  QPushButton,
  QScrollArea,
  QVBoxLayout,
  QWidget,
)

from makler.ui.icons import DOCUMENT_ADD, create_icon
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
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(20, 18, 20, 30)
    content_layout.setSpacing(14)

    # Заголовок страницы
    header_layout = QHBoxLayout()
    header_layout.setSpacing(14)

    icon = QLabel()
    icon.setPixmap(
      create_icon(DOCUMENT_ADD).pixmap(50, 50),
    )

    title = QLabel("Ввод заявки на обмен квартир")
    title.setObjectName("pageTitle")

    header_layout.addWidget(icon)
    header_layout.addWidget(title)
    header_layout.addStretch()

    content_layout.addLayout(header_layout)

    # Карточка заявки
    request_card = QFrame()
    request_card.setObjectName("requestCard")

    card_layout = QVBoxLayout(request_card)
    card_layout.setContentsMargins(20, 0, 20, 14)
    card_layout.setSpacing(10)

    card_header = QFrame()
    card_header.setObjectName("requestCardHeader")

    card_header_layout = QHBoxLayout(card_header)
    card_header_layout.setContentsMargins(20, 10, 12, 10)

    card_title = QLabel("Новая заявка на обмен")
    card_title.setObjectName("requestCardTitle")

    close_button = QPushButton("×")
    close_button.setObjectName("closeButton")
    close_button.setFixedSize(32, 32)

    card_header_layout.addWidget(card_title)
    card_header_layout.addStretch()
    card_header_layout.addWidget(close_button)

    card_layout.addWidget(card_header)

    forms_layout = QHBoxLayout()
    forms_layout.setSpacing(16)

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

    forms_layout.addWidget(self.desired_form)
    forms_layout.addWidget(self.offered_form)

    card_layout.addLayout(forms_layout)

    buttons_layout = QHBoxLayout()
    buttons_layout.setSpacing(12)
    buttons_layout.addStretch()

    find_button = QPushButton("Найти подходящий вариант")
    find_button.setObjectName("findButton")
    find_button.setMinimumWidth(290)
    find_button.clicked.connect(self._submit_request)

    cancel_button = QPushButton("Отмена")
    cancel_button.setObjectName("cancelButton")
    cancel_button.setMinimumWidth(110)
    cancel_button.clicked.connect(self._clear_forms)

    buttons_layout.addWidget(find_button)
    buttons_layout.addWidget(cancel_button)

    card_layout.addLayout(buttons_layout)

    content_layout.addWidget(request_card)

    # Результат
    self.match_result = MatchResult()
    content_layout.addWidget(self.match_result)

    # Картотека
    registry_header = QHBoxLayout()

    registry_icon = QLabel()
    registry_icon.setText("☷")
    registry_icon.setObjectName("registryIcon")

    registry_title = QLabel("Картотека заявок")
    registry_title.setObjectName("sectionTitle")

    registry_header.addWidget(registry_icon)
    registry_header.addWidget(registry_title)
    registry_header.addStretch()

    content_layout.addLayout(registry_header)

    self.registry_table = RegistryTable()
    content_layout.addWidget(self.registry_table)

    scroll.setWidget(content)

    layout = QVBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(scroll)

    self.setLayout(layout)

  def _submit_request(self) -> None:
    data = {
      "desired": self.desired_form.get_values(),
      "offered": self.offered_form.get_values(),
    }

    self.request_submitted.emit(data)

  def _clear_forms(self) -> None:
    self.desired_form.rooms_spin.setValue(1)
    self.desired_form.area_spin.setValue(1.0)
    self.desired_form.floor_spin.setValue(1)

    self.offered_form.rooms_spin.setValue(1)
    self.offered_form.area_spin.setValue(1.0)
    self.offered_form.floor_spin.setValue(1)