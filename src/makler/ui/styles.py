MAIN_STYLE = """
* {
    font-family: "SF Pro Display", "Segoe UI", Arial, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background: #f7f9fc;
}

QWidget {
    color: #111827;
}

QScrollArea,
QScrollArea QWidget {
    background: #f7f9fc;
    border: none;
}

/* SIDEBAR */

#sidebar {
    background: #edf5ff;
    border-right: 1px solid #d7e3f1;
}

#sidebarItem {
    background: transparent;
    border: none;
    border-radius: 9px;
    text-align: left;
}

#sidebarItem:hover {
    background: #e3effd;
}

#sidebarItem:checked {
    background: #d9eaff;
}

#sidebarIcon {
    color: #155a91;
    font-size: 42px;
}

#sidebarIconAdd {
    background: #0789df;
    color: white;
    border-radius: 9px;
    font-size: 40px;
}

#sidebarTitle {
    color: #10345d;
    font-size: 18px;
    font-weight: 700;
}

#sidebarDescription {
    color: #5d789c;
    font-size: 15px;
}

/* PAGE */

#requestPage {
    background: #f7f9fc;
}

#pageHeadingIcon {
    color: #2788dc;
    font-size: 46px;
    font-weight: 500;
}

#pageTitle {
    color: #101828;
    font-size: 30px;
    font-weight: 800;
}

#pageDescription {
    color: #66809f;
    font-size: 16px;
}

/* REQUEST CARD */

#requestCard {
    background: #ffffff;
    border: 1px solid #bfccde;
    border-radius: 11px;
}

#requestCardHeader {
    background: #f0f3f8;
    border-bottom: 1px solid #d5deea;
}

#requestCardTitle {
    font-size: 22px;
    font-weight: 700;
    color: #15213b;
}

#closeButton {
    background: transparent;
    border: none;
    color: #17233d;
    font-size: 30px;
}

#closeButton:hover {
    color: #2788dc;
}

/* APARTMENT FORMS */

#apartmentForm {
    background: white;
    border: 1px solid #c9d8ea;
    border-radius: 7px;
}

#apartmentForm[accent="blue"] {
    border-color: #bdd6f5;
}

#apartmentForm[accent="green"] {
    border-color: #b9ddc7;
}

QLabel#apartmentFormTitle {
    background: #eaf3ff;
    color: #075aa6;
    padding: 12px 20px;
    font-size: 19px;
    font-weight: 700;
}

#apartmentForm[accent="green"] QLabel#apartmentFormTitle {
    background: #eaf7ef;
    color: #075a32;
}

#apartmentFormBody {
    background: #ffffff;
    border-radius: 7px;
}

#fieldLabel {
    color: #182033;
    font-size: 16px;
}

QSpinBox,
QDoubleSpinBox,
QComboBox {
    min-height: 36px;
    background: #ffffff;
    border: 1px solid #bec9d7;
    border-radius: 5px;
    padding: 0 9px;
    color: #111827;
    font-size: 16px;
}

QSpinBox:focus,
QDoubleSpinBox:focus,
QComboBox:focus {
    border: 1px solid #348bd3;
}

/* BUTTONS */

#findButton {
    background: #2187d9;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 0 22px;
    font-size: 16px;
    font-weight: 600;
}

#findButton:hover {
    background: #1478c8;
}

#findButton:pressed {
    background: #0f68b0;
}

#cancelButton {
    background: white;
    color: #172033;
    border: 1px solid #aeb9c8;
    border-radius: 7px;
    padding: 0 20px;
    font-size: 16px;
}

#cancelButton:hover {
    background: #f2f5f9;
}

/* MATCH RESULT */

#matchResult {
    background: #f1fbf5;
    border: 1px solid #a9dabb;
    border-radius: 9px;
}

#matchCheck {
    background: #168b45;
    color: white;
    border-radius: 22px;
    font-size: 30px;
    font-weight: 700;
}

#matchResultTitle {
    color: #05662f;
    font-size: 19px;
    font-weight: 800;
}

#matchResultDescription {
    color: #173f2b;
    font-size: 15px;
}

#matchDetails {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid #acd9bc;
    border-radius: 5px;
}

#matchDetail {
    color: #173f2b;
    padding: 8px;
    font-size: 14px;
}

/* REGISTRY */

#registryIcon {
    color: #2586d5;
    font-size: 36px;
}

#sectionTitle {
    font-size: 25px;
    font-weight: 800;
    color: #111827;
}

#desiredTableHeader {
    background: #dceaff;
    color: #0755a5;
    font-size: 16px;
    font-weight: 700;
    padding: 8px;
    border: 1px solid #c4d9f2;
}

#offeredTableHeader {
    background: #e0f2e5;
    color: #075a32;
    font-size: 16px;
    font-weight: 700;
    padding: 8px;
    border: 1px solid #c3dfcb;
}

#registryTable {
    background: white;
    alternate-background-color: #f7f9fc;
    border: 1px solid #ccd6e2;
    gridline-color: #d9e0e8;
    selection-background-color: #dcecff;
    selection-color: #111827;
    font-size: 14px;
}

#registryTable QHeaderView::section {
    background: #f1f3f7;
    color: #111827;
    border: 1px solid #d7dee7;
    padding: 9px 5px;
    font-weight: 600;
}

#registryTable QTableCornerButton::section {
    background: #f1f3f7;
    border: 1px solid #d7dee7;
}

#matchResult[state="info"] {
    background: #edf5ff;
    border: 1px solid #b8d4f2;
}

#matchResult[state="info"] #matchCheck {
    background: #2788dc;
}

#matchResult[state="info"] #matchResultTitle {
    color: #075aa6;
}
"""