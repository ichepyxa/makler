MAIN_STYLE = """
* {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #172033;
}
QMainWindow, QWidget#page, QStackedWidget {
    background: #f7f9fc;
    color: #172033;
}
QLabel {
    color: #172033;
}
#sidebar {
    background: #edf5ff;
    border-right: 1px solid #d7e3f1;
}
#navButton, #exitButton {
    min-height: 48px;
    padding: 8px 12px;
    text-align: left;
    color: #10345d;
    background: transparent;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
}
#navButton:hover, #exitButton:hover {
    background: #e3effd;
}
#navButton:checked {
    background: #d9eaff;
}
#pageTitle {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
}
#pageDescription {
    color: #607d9f;
    font-size: 14px;
}
#contentCard {
    background: white;
    border: 1px solid #cbd7e6;
    border-radius: 10px;
}
QGroupBox#apartmentForm {
    background: white;
    border: 1px solid #cbd7e6;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 8px;
    font-size: 16px;
    font-weight: 600;
}
QGroupBox#apartmentForm[accent="blue"] {
    border-color: #b9d5f5;
}
QGroupBox#apartmentForm[accent="green"] {
    border-color: #b9ddc7;
}
QGroupBox#apartmentForm::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 2px 6px;
    color: #075aa6;
}
QGroupBox#apartmentForm[accent="green"]::title {
    color: #075a32;
}
QSpinBox, QDoubleSpinBox, QComboBox, QAbstractSpinBox {
    min-height: 32px;
    padding: 2px 7px;
    border: 1px solid #bec9d7;
    border-radius: 5px;
    background: white;
    color: #172033;
    selection-background-color: #dcecff;
    selection-color: #172033;
}
QComboBox QAbstractItemView {
    background: white;
    color: #172033;
    selection-background-color: #dcecff;
    selection-color: #172033;
}
QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #2788dc;
}
#primaryButton, #secondaryButton {
    min-height: 38px;
    padding: 0 16px;
    border-radius: 6px;
    font-weight: 600;
}
#primaryButton {
    background: #2187d9;
    color: white;
    border: none;
}
#primaryButton:hover {
    background: #1478c8;
}
#secondaryButton {
    background: white;
    color: #172033;
    border: 1px solid #aeb9c8;
}
#resultLabel {
    padding: 14px;
    border-radius: 8px;
    background: #edf5ff;
    border: 1px solid #b8d4f2;
    color: #075aa6;
}
#resultLabel[state="success"] {
    background: #f0faf3;
    border-color: #a9dabb;
    color: #075a32;
}
#dataTable {
    background: white;
    alternate-background-color: #f5f8fc;
    border: 1px solid #ccd6e2;
    gridline-color: #d9e0e8;
    selection-background-color: #dcecff;
    selection-color: #111827;
}
#dataTable QHeaderView::section {
    background: #eef2f7;
    color: #172033;
    border: 1px solid #d7dee7;
    padding: 8px;
    font-weight: 600;
}
QTableWidget {
    color: #172033;
}
QTableWidget::item {
    color: #172033;
}
"""
