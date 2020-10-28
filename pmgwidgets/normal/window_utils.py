from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget


def center_window(window: QWidget):
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move(int((screen.width() - size.width()) / 2),
                int((screen.height() - size.height()) / 2))


def set_always_on_top(window: QWidget):
    flags = window.windowFlags()
    window.setWindowFlags(flags | Qt.WindowStaysOnTopHint)  # 窗体总在最前端


def set_minimizable(window: QWidget):
    flags = window.windowFlags()
    window.setWindowFlags(flags | Qt.WindowMinMaxButtonsHint)


def set_closable(window: QWidget):
    flags = window.windowFlags()
    window.setWindowFlags(flags | Qt.WindowCloseButtonHint)
