from PySide6.QtWidgets import (
  QDialog,
  QHBoxLayout,
  QMainWindow,
  QMessageBox,
  QStackedWidget,
  QWidget,
)
from sqlalchemy.exc import SQLAlchemyError

from makler.database.database import Database
from makler.database.repositories import RequestRepository
from makler.domain import Apartment, ExchangeRequest
from makler.services.request_service import RequestService
from makler.ui.edit_request_dialog import EditRequestDialog
from makler.ui.registry_page import RegistryPage
from makler.ui.request_page import RequestPage
from makler.ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
  def __init__(self, database: Database) -> None:
    super().__init__()
    self.database = database
    self.setWindowTitle("Маклер — учёт заявок на обмен квартир")
    self.setMinimumSize(950, 650)
    self.move(100, 100)

    self.sidebar = Sidebar()
    self.pages = QStackedWidget()
    self.request_page = RequestPage()
    self.registry_page = RegistryPage()

    self.pages.addWidget(self.request_page)
    self.pages.addWidget(self.registry_page)

    self.sidebar.page_changed.connect(self.change_page)
    self.sidebar.exit_requested.connect(self.close)
    self.request_page.request_submitted.connect(self.process_request)
    self.registry_page.edit_requested.connect(self.edit_request)
    self.registry_page.delete_requested.connect(self.delete_request)

    central = QWidget()
    layout = QHBoxLayout(central)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(self.sidebar)
    layout.addWidget(self.pages, 1)
    self.setCentralWidget(central)
    self.refresh_views()

  def process_request(self, data: dict) -> None:
    try:
      request = ExchangeRequest(
        desired=Apartment(**data["desired"]),
        offered=Apartment(**data["offered"]),
      )
      with self.database.session() as session:
        result = RequestService(session).add_request(request)

      self.refresh_views()
      if result.matched_request_id is None:
        self.request_page.show_saved()
      else:
        matched = result.matched_request
        if matched is None:
          raise RuntimeError("Не удалось получить найденную заявку.")
        self.request_page.show_exchange(
          result.matched_request_id,
          self.format_apartment(matched.desired),
          self.format_apartment(matched.offered),
        )
    except (SQLAlchemyError, ValueError, TypeError, RuntimeError) as error:
      QMessageBox.critical(
        self,
        "Ошибка",
        f"Не удалось обработать заявку:\n{error}",
      )

  def edit_request(self, request_id: int) -> None:
    try:
      with self.database.session() as session:
        request = RequestRepository(session).get_by_id(request_id)

      if request is None:
        QMessageBox.warning(
          self,
          "Заявка не найдена",
          "Выбранная заявка уже отсутствует в картотеке.",
        )
        self.refresh_views()
        return

      dialog = EditRequestDialog(request, self)
      if dialog.exec() != QDialog.DialogCode.Accepted:
        return

      updated_request = dialog.get_request()
      with self.database.session() as session:
        updated = RequestService(session).update_request(
          request_id,
          updated_request,
        )

      if not updated:
        QMessageBox.warning(
          self,
          "Заявка не найдена",
          "Не удалось изменить заявку: запись отсутствует.",
        )
      else:
        QMessageBox.information(
          self,
          "Готово",
          "Сведения о заявке обновлены.",
        )
      self.refresh_views()
    except (SQLAlchemyError, ValueError, TypeError) as error:
      QMessageBox.critical(
        self,
        "Ошибка",
        f"Не удалось изменить заявку:\n{error}",
      )

  def delete_request(self, request_id: int) -> None:
    confirmation = QMessageBox(self)
    confirmation.setWindowTitle("Удаление заявки")
    confirmation.setText(
      f"Удалить заявку № {request_id} из картотеки?"
    )
    confirmation.setIcon(QMessageBox.Icon.Question)
    confirmation.setStandardButtons(
      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    confirmation.setDefaultButton(QMessageBox.StandardButton.No)
    confirmation.setStyleSheet("""
      QMessageBox {
        background-color: #f7f9fc;
        color: #172033;
      }
      QMessageBox QLabel {
        color: #172033;
        font-size: 15px;
      }
      QMessageBox QPushButton {
        min-width: 88px;
        min-height: 34px;
        padding: 4px 14px;
        border-radius: 6px;
        color: #172033;
        background-color: white;
        border: 1px solid #aeb9c8;
        font-weight: 600;
      }
    """)
    yes_button = confirmation.button(QMessageBox.StandardButton.Yes)
    no_button = confirmation.button(QMessageBox.StandardButton.No)
    yes_button.setText("Да, удалить")
    yes_button.setStyleSheet(
      "background-color: #fff0f0; color: #a52828; "
      "border: 1px solid #e3b6b6;"
    )
    no_button.setText("Отмена")

    if confirmation.exec() != QMessageBox.StandardButton.Yes:
      return

    try:
      with self.database.session() as session:
        deleted = RequestService(session).delete_request(request_id)

      if deleted:
        QMessageBox.information(
          self,
          "Готово",
          "Заявка удалена из картотеки.",
        )
      else:
        QMessageBox.warning(
          self,
          "Заявка не найдена",
          "Выбранная заявка уже отсутствует в картотеке.",
        )
      self.refresh_views()
    except SQLAlchemyError as error:
      QMessageBox.critical(
        self,
        "Ошибка",
        f"Не удалось удалить заявку:\n{error}",
      )

  def change_page(self, index: int) -> None:
    self.pages.setCurrentIndex(index)
    self.refresh_views()

  def refresh_views(self) -> None:
    with self.database.session() as session:
      self.card_index = RequestService(session).get_card_index()
      requests = RequestRepository(session).get_all_with_ids()

    self.registry_page.set_requests(
      [self.create_request_row(item) for item in requests]
    )

  @staticmethod
  def format_apartment(apartment: Apartment) -> str:
    area = f"{apartment.area:.1f}".replace(".", ",")
    return (
      f"{apartment.rooms} комн., {area} м², "
      f"{apartment.floor} этаж, {apartment.district} район"
    )

  @classmethod
  def create_request_row(cls, item) -> dict:
    return {
      "id": item.id,
      "desired": cls.format_apartment(item.request.desired),
      "offered": cls.format_apartment(item.request.offered),
      "created_at": item.created_at.strftime("%d.%m.%Y"),
    }
