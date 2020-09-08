from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from pyminer2.pmutil import get_main_window


class TopLevelWidget(QDialog):
    def __init__(self, parent=None):
        super(TopLevelWidget, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.title_layout = QHBoxLayout()
        self.layout().addLayout(self.title_layout)
        b=QPushButton('x')
        self.title_layout.addWidget(QLabel())
        self.title_layout.addWidget(b)
        b.setMaximumWidth(20)
        b.clicked.connect(self.hide)
        self.central_widget = None
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        get_main_window().resize_signal.connect(self.refresh_position)
        self.position: QPoint = None
        self.width: int = 500
        self.height = 500

    def set_central_widget(self, widget: 'QWidget'):
        self.layout().addWidget(widget)
        self.central_widget = widget

    def set_position(self, position: 'QPoint'):
        self.position = position
        self.refresh_position()

    def set_width(self, width: int):
        self.width = width

    def refresh_position(self) -> None:
        if self.position is None:
            return
        mw = get_main_window()
        self.setGeometry(mw.geometry().x() + self.position.x(), mw.geometry().y() + self.position.y() + 16,
                         self.width, self.height)
