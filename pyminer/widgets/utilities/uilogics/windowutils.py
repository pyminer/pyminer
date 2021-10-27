from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QDesktopWidget


def in_unit_test():
    """
    判断是否在单元测试中。
    方便控件单独测试。返回True的时候说明在单元测试；返回False的时候说明不在单元测试。
    当PyMiner主程序启动后，它会将这个函数用lambda:False这个匿名函数覆盖掉。

    :return:
    """
    return True


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
