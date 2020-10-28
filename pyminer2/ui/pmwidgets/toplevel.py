from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFocusEvent, QMouseEvent
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from pyminer2.pmutil import get_main_window


class TopLevelWidget(QDialog):
    def __init__(self, parent=None):
        super(TopLevelWidget, self).__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)  # 点击其他位置之后，可以隐藏。
        self.setLayout(QVBoxLayout())
        self.title_layout = QHBoxLayout()
        self.layout().addLayout(self.title_layout)
        b = QPushButton('x')
        self.title_layout.addWidget(QLabel())
        self.title_layout.addWidget(b)
        b.setMaximumWidth(20)
        b.clicked.connect(self.hide)
        self.central_widget = None

        get_main_window().window_geometry_changed_signal.connect(self.refresh_position)
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
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """
        在鼠标事件中，当鼠标点击弹出的窗口外部时，弹出窗口应当会隐藏。但如果不改写这一事件，在点击其他位置的时候，
        假如点击的位置时按钮，那么就会在隐藏窗口的同时触发按钮事件。如果这个按钮恰好可以控制该窗口的弹出和隐藏，
        那么就会发现窗口消失之后又立刻蹦了出来，这是因为窗口消失之后，它的出现事件又被触发了。
        设置为Qt.WA_NoMouseReplay，就是为了避免这种糟糕的状况。
        """
        self.setAttribute(Qt.WA_NoMouseReplay)
        super().mousePressEvent(a0)