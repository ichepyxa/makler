from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


def create_icon(svg: str) -> QIcon:
    renderer = QSvgRenderer(
        QByteArray(svg.encode("utf-8")),
    )

    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


PLUS = """
<svg width="36" height="36" viewBox="0 0 36 36"
    xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="34" height="34" rx="7" fill="#2788DC"/>
  <path d="M18 9V27M9 18H27"
        stroke="white" stroke-width="3"
        stroke-linecap="round"/>
</svg>
"""

SEARCH = """
<svg width="44" height="44" viewBox="0 0 44 44"
    xmlns="http://www.w3.org/2000/svg">
  <circle cx="18" cy="18" r="12"
          fill="none" stroke="#155A91" stroke-width="3"/>
  <path d="M27 27L39 39"
        stroke="#155A91" stroke-width="3"
        stroke-linecap="round"/>
</svg>
"""

LIST = """
<svg width="44" height="44" viewBox="0 0 44 44"
    xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="28" height="32"
        rx="3" fill="none"
        stroke="#155A91" stroke-width="3"/>
  <path d="M15 14H30M15 21H30M15 28H30"
        stroke="#2788DC" stroke-width="3"
        stroke-linecap="round"/>
</svg>
"""

SETTINGS = """
<svg width="44" height="44" viewBox="0 0 44 44"
    xmlns="http://www.w3.org/2000/svg">
  <circle cx="22" cy="22" r="7"
          fill="none" stroke="#155A91" stroke-width="3"/>
  <path d="M22 4V9M22 35V40M4 22H9M35 22H40
            M9.3 9.3L12.8 12.8M31.2 31.2L34.7 34.7
            M34.7 9.3L31.2 12.8M12.8 31.2L9.3 34.7"
        stroke="#155A91" stroke-width="3"
        stroke-linecap="round"/>
</svg>
"""

EXIT = """
<svg width="44" height="44" viewBox="0 0 44 44"
    xmlns="http://www.w3.org/2000/svg">
  <path d="M11 6H28V38H11"
        fill="none" stroke="#155A91"
        stroke-width="3"/>
  <path d="M22 22H39M33 16L39 22L33 28"
        fill="none" stroke="#2788DC"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"/>
</svg>
"""

DOCUMENT_ADD = """
<svg width="50" height="50" viewBox="0 0 50 50"
    xmlns="http://www.w3.org/2000/svg">
  <path d="M10 5H30L40 15V44H10Z"
        fill="none" stroke="#2788DC" stroke-width="3"/>
  <path d="M30 5V16H40"
        fill="none" stroke="#2788DC" stroke-width="3"/>
  <path d="M33 30V44M26 37H40"
        stroke="#2788DC" stroke-width="3"
        stroke-linecap="round"/>
</svg>
"""

CHECK = """
<svg width="42" height="42" viewBox="0 0 42 42"
    xmlns="http://www.w3.org/2000/svg">
  <circle cx="21" cy="21" r="19" fill="#168B45"/>
  <path d="M12 21L18 27L31 14"
        fill="none"
        stroke="white"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"/>
</svg>
"""