import sys

from PySide6.QtWidgets import QApplication

from makler.database.database import Database
from makler.ui.main_window import MainWindow
from makler.ui.styles import MAIN_STYLE


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    database = Database()
    database.create_tables()

    window = MainWindow(database)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
