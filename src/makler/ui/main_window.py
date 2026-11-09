from sqlalchemy.exc import SQLAlchemyError

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from makler.database.database import Database
from makler.database.repositories import RequestRepository
from makler.domain import Apartment, ExchangeRequest
from makler.services.request_service import RequestService
from makler.ui.registry_page import RegistryPage
from makler.ui.request_page import RequestPage
from makler.ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self, database: Database) -> None:
        super().__init__()

        self.database = database

        self.setWindowTitle(
            "Маклер - учет заявок на обмен квартир"
        )
        self.resize(1500, 950)
        self.setMinimumSize(1100, 700)

        self.sidebar = Sidebar()
        self.pages = QStackedWidget()

        self.request_page = RequestPage()

        self.search_page = self._create_placeholder(
            "Поиск варианта",
            "Поиск подходящего варианта обмена квартир.",
        )

        self.registry_page = RegistryPage()

        self.settings_page = self._create_placeholder(
            "Настройки",
            "Параметры программы.",
        )

        self.pages.addWidget(self.request_page)
        self.pages.addWidget(self.search_page)
        self.pages.addWidget(self.registry_page)
        self.pages.addWidget(self.settings_page)

        self.sidebar.page_changed.connect(
            self._on_page_changed
        )
        self.sidebar.exit_requested.connect(self.close)

        self.request_page.request_submitted.connect(
            self._handle_request
        )

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        self.setCentralWidget(central)

        self._refresh_registry()

    def _handle_request(self, data: dict) -> None:
        try:
            desired = Apartment(**data["desired"])
            offered = Apartment(**data["offered"])

            request = ExchangeRequest(
                desired=desired,
                offered=offered,
            )

            with self.database.session() as session:
                service = RequestService(session)
                result = service.add_request(request)

            self._refresh_registry()

            if (
                result.exchange is not None
                and result.matched_request is not None
                and result.matched_request_id is not None
            ):
                self.request_page.show_match_result(
                    request_id=result.matched_request_id,
                    desired=self._format_apartment(
                        result.matched_request.desired
                    ),
                    offered=self._format_apartment(
                        result.matched_request.offered
                    ),
                )
            else:
                self.request_page.show_no_match_result()

        except (SQLAlchemyError, ValueError, TypeError) as error:
          QMessageBox.critical(
              self,
              "Ошибка",
              f"Не удалось обработать заявку:\n{error}",
          )

    def _refresh_registry(self) -> None:
        with self.database.session() as session:
            repository = RequestRepository(session)
            stored_requests = repository.get_all_with_ids()

        rows = [
            self._request_to_row(item)
            for item in stored_requests
        ]

        self.request_page.set_requests(rows)
        self.registry_page.table.set_requests(rows)

    def _on_page_changed(self, index: int) -> None:
        self.pages.setCurrentIndex(index)

        if index == 2:
            self._refresh_registry()

    @staticmethod
    def _format_apartment(apartment: Apartment) -> str:
        area = f"{apartment.area:.1f}".replace(".", ",")

        return (
            f"{apartment.rooms} комн., "
            f"{area} м², "
            f"{apartment.floor} этаж, "
            f"{apartment.district} район"
        )

    @staticmethod
    def _request_to_row(item) -> dict:
        request = item.request

        return {
            "id": item.id,
            "desired_rooms": request.desired.rooms,
            "desired_area": (
                f"{request.desired.area:.1f}".replace(".", ",")
            ),
            "desired_floor": request.desired.floor,
            "desired_district": request.desired.district,
            "offered_rooms": request.offered.rooms,
            "offered_area": (
                f"{request.offered.area:.1f}".replace(".", ",")
            ),
            "offered_floor": request.offered.floor,
            "offered_district": request.offered.district,
            "created_at": item.created_at.strftime("%d.%m.%Y"),
        }

    @staticmethod
    def _create_placeholder(
        title: str,
        description: str,
    ) -> QWidget:
        page = QWidget()

        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")

        description_label = QLabel(description)
        description_label.setObjectName("pageDescription")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(12)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()

        return page