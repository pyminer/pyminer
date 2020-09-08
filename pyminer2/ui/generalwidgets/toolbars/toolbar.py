from typing import List,Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QPushButton, QMenu, QToolButton, QAction, QWidget, QLabel


class ActionWithMessage(QAction):
    def __init__(self, text: str = '', icon: QIcon = None, parent: QWidget = None, message: str = ''):
        super().__init__(parent)
        self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self.message = message


class TopToolBar(QToolBar):
    def __init__(self):
        super().__init__()

    def add_button(self, text: str):
        b = QPushButton(text)
        b.setObjectName('pmtopToolbarButton')
        self.addWidget(b)
        self.addWidget(QLabel('  '))# 增加一段空间。
        return b

    def get_button(self, name: str):
        return self.findChild(QPushButton, name)


class PMToolBar(QToolBar):
    tab_button: QPushButton = None
    _control_widget_dic = {}

    def __init__(self):
        super().__init__()
        self.setFixedHeight(90)
        self._control_widget_dic = {}

    def get_control_widget(self, widget_name: str) -> QPushButton:
        w = self._control_widget_dic.get(widget_name)
        if w is None:
            raise Exception('Toolbar \'%s\' has no widget named \'%s\'' % widget_name)
        return w

    def add_tool_button(self, name: str, text: str = '', icon: QIcon = None, menu: QMenu = None):
        tb = QToolButton()
        tb.setPopupMode(QToolButton.InstantPopup)
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setText(text)
        tb.setStyleSheet('QToolButton{height:60px;width:50px;border:0px;}')
        if icon is not None:
            tb.setIcon(icon)
        if menu is not None:
            tb.setMenu(menu)
        self.addWidget(tb)
        self._control_widget_dic[name] = tb
        return tb

    def add_buttons(self, button_num: int, names: List[str], texts: List[str], icons_path: List[str]=None)->List[
        'QPushButton']:
        from pyminer2.ui.generalwidgets import PMPushButtonPane
        pp = PMPushButtonPane()
        button_list = pp.add_buttons(button_num, texts, icons_path)
        for i, name in enumerate(names):
            self._control_widget_dic[name] = button_list[i]
        self.addWidget(pp)
        return button_list

    def add_widget(self, name: str, widget: 'QWidget'):
        self._control_widget_dic[name] = widget
        self.addWidget(widget)
        return widget

    def add_menu_to(self, button_name: str, action_texts: List[str], action_commands: List['Callable']) -> List['QAction']:
        button = self.get_control_widget(button_name)
        menu = QMenu(self)
        for text,cmd in zip(action_texts,action_commands):
            a=QAction(text=text, parent=menu)
            menu.addAction(a)
            a.triggered.connect(cmd)
        button.setMenu(menu)
