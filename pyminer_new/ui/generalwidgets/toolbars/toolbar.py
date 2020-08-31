from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QPushButton, QMenu, QToolButton, QAction,QWidget


class ActionWithMessage(QAction):
    def __init__(self,text:str='',icon:QIcon=None,parent:QWidget=None,message:str = ''):
        super().__init__(parent)
        self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self.message=message

class TopToolBar(QToolBar):
    def __init__(self):
        super().__init__()

    def add_button(self, name: str, text: str):
        b = QPushButton(text)
        b.setObjectName(name)

        self.addWidget(b)

    def get_button(self, name: str):
        return self.findChild(QPushButton, name)

class PMToolBar(QToolBar):
    tab_button: QPushButton = None
    widget_dic = {}

    def __init__(self):
        super().__init__()
        self.setFixedHeight(90)

    def add_tool_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None):
        tb = QToolButton()
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setText(text)
        tb.setStyleSheet('QToolButton{height:60px;width:50px;border:0px;}QToolButton::hover{background-color:#ededed;}')
        if icon is not None:
            tb.setIcon(icon)
        if menu is not None:
            tb.setMenu(menu)
        self.addWidget(tb)
        return tb