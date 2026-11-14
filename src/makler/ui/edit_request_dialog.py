from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
  QDialog,
  QDialogButtonBox,
  QHBoxLayout,
  QVBoxLayout,
)

from makler.domain import CITY_DISTRICTS, Apartment, ExchangeRequest
from makler.ui.widgets.apartment_form import ApartmentForm


class EditRequestDialog(QDialog):
  def __init__(
    self,
    request: ExchangeRequest,
    parent=None,
  ) -> None:
    super().__init__(parent)
    self.setObjectName("editRequestDialog")
    self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.setWindowTitle("Изменение заявки")
    self.setMinimumWidth(760)
    self.resize(980, 480)

    self.desired_form = ApartmentForm(
      "Требуемая квартира",
      "blue",
      list(CITY_DISTRICTS),
    )
    self.offered_form = ApartmentForm(
      "Имеющаяся квартира",
      "green",
      list(CITY_DISTRICTS),
    )
    self.desired_form.set_values(request.desired)
    self.offered_form.set_values(request.offered)

    forms = QHBoxLayout()
    forms.setSpacing(14)
    forms.addWidget(self.desired_form, 1)
    forms.addWidget(self.offered_form, 1)

    buttons = QDialogButtonBox(
      QDialogButtonBox.StandardButton.Save
      | QDialogButtonBox.StandardButton.Cancel
    )
    save_button = buttons.button(QDialogButtonBox.StandardButton.Save)
    cancel_button = buttons.button(QDialogButtonBox.StandardButton.Cancel)
    save_button.setText("Сохранить")
    save_button.setObjectName("primaryButton")
    cancel_button.setText("Отмена")
    cancel_button.setObjectName("secondaryButton")
    buttons.accepted.connect(self.accept)
    buttons.rejected.connect(self.reject)

    layout = QVBoxLayout(self)
    layout.setContentsMargins(22, 22, 22, 20)
    layout.setSpacing(18)
    layout.addLayout(forms)
    layout.addWidget(buttons)

  def get_request(self) -> ExchangeRequest:
    return ExchangeRequest(
      desired=Apartment(**self.desired_form.get_values()),
      offered=Apartment(**self.offered_form.get_values()),
    )
