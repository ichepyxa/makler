from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QWidget,
)
from sqlalchemy.exc import SQLAlchemyError

from makler.database.database import Database
from makler.database.repositories import HistoryRepository, RequestRepository
from makler.domain import Apartment, ExchangeRequest
from makler.services.request_service import RequestService
from makler.ui.history_page import HistoryPage
from makler.ui.registry_page import RegistryPage
from makler.ui.request_page import RequestPage
from makler.ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self, database: Database) -> None:
        super().__init__()
        self.database = database
        self.setWindowTitle("Маклер — учёт заявок на обмен квартир")
        self.resize(1280, 820)
        self.setMinimumSize(950, 650)

        self.sidebar = Sidebar()
        self.pages = QStackedWidget()
        self.request_page = RequestPage()
        self.registry_page = RegistryPage()
        self.history_page = HistoryPage()

        self.pages.addWidget(self.request_page)
        self.pages.addWidget(self.registry_page)
        self.pages.addWidget(self.history_page)

        self.sidebar.page_changed.connect(self._change_page)
        self.sidebar.exit_requested.connect(self.close)
        self.request_page.request_submitted.connect(self._process_request)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(central)
        self._refresh_views()

    def _process_request(self, data: dict) -> None:
        try:
            request = ExchangeRequest(
                desired=Apartment(**data["desired"]),
                offered=Apartment(**data["offered"]),
            )
            with self.database.session() as session:
                result = RequestService(session).add_request(request)

            self._refresh_views()
            if result.exchange is None:
                self.request_page.show_saved()
            else:
                matched = result.matched_request
                matched_id = result.matched_request_id
                if matched is None or matched_id is None:
                    raise RuntimeError("Не удалось получить данные найденной заявки.")
                self.request_page.show_exchange(
                    matched_id,
                    self._format_apartment(matched.desired),
                    self._format_apartment(matched.offered),
                )
        except (SQLAlchemyError, ValueError, TypeError, RuntimeError) as error:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось обработать заявку:\n{error}",
            )

    def _change_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self._refresh_views()

    def _refresh_views(self) -> None:
        with self.database.session() as session:
            requests = RequestRepository(session).get_all_with_ids()
            exchanges = HistoryRepository(session).get_all()

        self.registry_page.set_requests(
            [self._request_row(item) for item in requests]
        )
        self.history_page.set_exchanges(
            [self._exchange_row(item) for item in exchanges]
        )

    @staticmethod
    def _format_apartment(apartment: Apartment) -> str:
        area = f"{apartment.area:.1f}".replace(".", ",")
        return (
            f"{apartment.rooms} комн., {area} м², "
            f"{apartment.floor} этаж, {apartment.district} район"
        )

    @classmethod
    def _request_row(cls, item) -> dict:
        return {
            "id": item.id,
            "desired": cls._format_apartment(item.request.desired),
            "offered": cls._format_apartment(item.request.offered),
            "created_at": item.created_at.strftime("%d.%m.%Y"),
        }

    @classmethod
    def _exchange_row(cls, item) -> dict:
        first = item.exchange.first_request
        second = item.exchange.second_request
        return {
            "id": item.id,
            "created_at": item.created_at.strftime("%d.%m.%Y %H:%M"),
            "first_desired": cls._format_apartment(first.desired),
            "first_offered": cls._format_apartment(first.offered),
            "second_desired": cls._format_apartment(second.desired),
            "second_offered": cls._format_apartment(second.offered),
        }
