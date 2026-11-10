from PySide6.QtCore import QLocale
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

        layout = QFormLayout(self)
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

    def reset(self) -> None:
        self.rooms_spin.setValue(2)
        self.area_spin.setValue(55.0)
        self.floor_spin.setValue(5)
        self.district_combo.setCurrentIndex(0)
