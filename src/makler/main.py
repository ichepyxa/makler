import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
  def __init__(self) -> None:
    super().__init__()

    self.setWindowTitle("Маклер")
    self.resize(1000, 700)

    label = QLabel("Программа Маклер")
    label.setStyleSheet("font-size: 24px;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    self.setCentralWidget(label)

def main() -> int:
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())