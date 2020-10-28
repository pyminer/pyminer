from PyQt5.QtGui import QIcon, QPixmap


def create_icon(icon_path: str = ":/pyqt/source/images/New.png"):
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
    return icon


def colorTup2Str(self, value: tuple) -> str:
    if value is None:
        return None
    strcolor = '#'
    for i in value:
        strcolor += hex(int(i))[-2:].replace('x', '0')
    return strcolor
