from PySide6.QtWidgets import (
  QComboBox,
  QDoubleSpinBox,
  QFormLayout,
  QGroupBox,
  QSpinBox,
)


class ApartmentForm(QGroupBox):
  def __init__(
    self,
    title: str,
    title_color: str,
    districts: list[str] | None = None,
    parent=None,
  ) -> None:
    super().__init__(title, parent)

    self.setObjectName("apartmentForm")
    self.setProperty("formColor", title_color)

    self.rooms_spin = QSpinBox()
    self.rooms_spin.setRange(1, 20)

    self.area_spin = QDoubleSpinBox()
    self.area_spin.setRange(1.0, 1000.0)
    self.area_spin.setDecimals(1)
    self.area_spin.setSuffix(" м²")

    self.floor_spin = QSpinBox()
    self.floor_spin.setRange(1, 100)

    self.district_combo = QComboBox()

    if districts:
      self.district_combo.addItems(districts)

    layout = QFormLayout()
    layout.setContentsMargins(20, 18, 20, 20)
    layout.setHorizontalSpacing(18)
    layout.setVerticalSpacing(12)

    layout.addRow("Количество комнат:", self.rooms_spin)
    layout.addRow("Площадь (м²):", self.area_spin)
    layout.addRow("Этаж:", self.floor_spin)
    layout.addRow("Район:", self.district_combo)

    self.setLayout(layout)

  def get_values(self) -> dict:
    return {
      "rooms": self.rooms_spin.value(),
      "area": self.area_spin.value(),
      "floor": self.floor_spin.value(),
      "district": self.district_combo.currentText(),
    }