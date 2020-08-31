from PyQt5.QtGui import QIcon, QPixmap


def create_icon(icon_path: str = ":/pyqt/source/images/New.png"):
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
    return icon