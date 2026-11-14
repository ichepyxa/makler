from PySide6.QtCore import QLocale, Qt
from PySide6.QtWidgets import (
  QComboBox,
  QDoubleSpinBox,
  QFormLayout,
  QGroupBox,
  QSpinBox,
  QSizePolicy,
)

from makler.domain import Apartment


class ApartmentForm(QGroupBox):
  def __init__(
    self,
    title: str,
    accent: str,
    districts: list[str],
    parent=None,
  ) -> None:
    super().__init__(title, parent)
    self.setObjectName("apartmentForm")
    self.setProperty("accent", accent)

    self.rooms_spin = QSpinBox()
    self.rooms_spin.setRange(1, 20)
    self.rooms_spin.setValue(2)

    self.area_spin = QDoubleSpinBox()
    self.area_spin.setRange(1.0, 1000.0)
    self.area_spin.setDecimals(1)
    self.area_spin.setLocale(QLocale("ru_RU"))
    self.area_spin.setValue(55.0)
    self.area_spin.setSuffix(" м²")

    self.floor_spin = QSpinBox()
    self.floor_spin.setRange(1, 100)
    self.floor_spin.setValue(5)

    self.district_combo = QComboBox()
    self.district_combo.addItems(districts)

    for field in (
      self.rooms_spin,
      self.area_spin,
      self.floor_spin,
      self.district_combo,
    ):
      field.setMinimumWidth(190)
      field.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed,
      )

    layout = QFormLayout(self)
    layout.setFieldGrowthPolicy(
      QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
    )
    layout.setLabelAlignment(
      Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
    layout.setContentsMargins(16, 20, 16, 16)
    layout.setHorizontalSpacing(12)
    layout.setVerticalSpacing(10)
    layout.addRow("Комнат:", self.rooms_spin)
    layout.addRow("Площадь:", self.area_spin)
    layout.addRow("Этаж:", self.floor_spin)
    layout.addRow("Район:", self.district_combo)

  def get_values(self) -> dict:
    return {
      "rooms": self.rooms_spin.value(),
      "area": self.area_spin.value(),
      "floor": self.floor_spin.value(),
      "district": self.district_combo.currentText(),
    }

  def set_values(self, apartment: Apartment) -> None:
    self.rooms_spin.setValue(apartment.rooms)
    self.area_spin.setValue(apartment.area)
    self.floor_spin.setValue(apartment.floor)
    index = self.district_combo.findText(apartment.district)
    if index < 0:
      self.district_combo.addItem(apartment.district)
      index = self.district_combo.count() - 1
    self.district_combo.setCurrentIndex(index)

  def reset(self) -> None:
    self.rooms_spin.setValue(2)
    self.area_spin.setValue(55.0)
    self.floor_spin.setValue(5)
    self.district_combo.setCurrentIndex(0)
