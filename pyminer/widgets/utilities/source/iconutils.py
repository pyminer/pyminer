from typing import Tuple

from PySide2.QtGui import QIcon, QPixmap


def create_icon(icon_path: str = ":/pyqt/source/images/New.png"):
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
    return icon


def color_rgb_to_str(value: Tuple[int, ...]) -> str:
    result = '#'
    for i in value:
        result += hex(int(i))[-2:].replace('x', '0')
    return result
