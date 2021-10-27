from typing import List, Callable, Optional

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QToolBar, QPushButton, QMenu, QToolButton, QAction, QWidget, QHBoxLayout


class ActionWithMessage(QAction):
    def __init__(self, text: str = '', icon: QIcon = None,
                 parent: QWidget = None, message: str = ''):
        super().__init__(parent)
        self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self.message = message


class TopToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setFloatable(False)
        self.setMovable(False)
        self.buttonbar_widget = QWidget()
        self.addWidget(self.buttonbar_widget)
        self.buttonbar_widget.setLayout(QHBoxLayout())
        self.buttonbar_widget.setContentsMargins(0, 0, 0, 0)
        self.buttonbar_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.button_names = []

    def add_button(self, name: str, text: str):
        pbtn = QPushButton(text)
        pbtn.setObjectName('pmtopToolbarButton')
        pbtn.setProperty('stat', 'unselected')
        self.buttonbar_widget.layout().addWidget(pbtn)
        self.button_names.append(name)
        return pbtn

    def insert_button(self, name: str, text: str, insert_after: str):
        pbtn = QPushButton(text)
        pbtn.setObjectName('pmtopToolbarButton')
        pbtn.setProperty('stat', 'unselected')

        assert insert_after in self.button_names, f'{insert_after} do not in buttons: {self.button_names}'
        index = self.button_names.index(insert_after)
        self.button_names.insert(index + 1, name)
        self.buttonbar_widget.layout().insertWidget(index + 1, pbtn)
        return pbtn

    def get_button(self, name: str):
        return self.findChild(QPushButton, name)


class TopToolBarRight(QToolBar):
    def __init__(self):
        super().__init__()
        self.setFloatable(False)
        self.setMovable(False)
        self.setLayoutDirection(Qt.RightToLeft)
        self.hide_button = QToolButton()
        self.hide_button.setObjectName("hidebutton")
        self.hide_button.setArrowType(Qt.UpArrow)
        self.addWidget(self.hide_button)


class PMGToolBar(QToolBar):
    tab_button: QPushButton = None
    _control_widget_dic = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self._control_widget_dic = {}

    def get_toolbar_text(self) -> str:
        return 'Toolbar'

    def get_control_widget(self, widget_name: str) -> QPushButton:
        w = self._control_widget_dic.get(widget_name)
        if w is None:
            raise Exception(
                'Toolbar has no widget named \'%s\'' %
                widget_name)
        return w

    def bind_events(self):
        pass

    def add_tool_button(self, name: str, text: str = '', tooltip: str = '',
                        icon: QIcon = None, menu: QMenu = None):
        tb = QToolButton()
        tb.setPopupMode(QToolButton.InstantPopup)
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setText(text)
        tb.setToolTip(tooltip)
        tb.setProperty('qssp', 'tooliconbtn')
        if icon is not None:
            pixmap = icon.pixmap(QSize(40, 40))
            icon = QIcon(pixmap)
            tb.setIcon(icon)

            tb.setIconSize(QSize(40, 40))
        if menu is not None:
            tb.setMenu(menu)
        self.addWidget(tb)
        self._control_widget_dic[name] = tb
        return tb

    def add_height_occupation(self):
        from widgets import PMPushButtonPane

        pp = PMPushButtonPane()
        button_list = pp.add_height_occu_buttons()
        self.addWidget(pp)
        return button_list

    def add_buttons(self, button_num: int, names: List[str], texts: List[str], icons_path: List[str] = None) \
            -> List['QPushButton']:
        from widgets import PMPushButtonPane

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

    def add_menu_to(self, button_name: str,
                    action_texts: List[str],
                    action_commands: List['Callable'],
                    action_icon: QIcon = None) -> Optional[QMenu]:
        button = self.get_control_widget(button_name)
        if button is not None:
            menu = QMenu(self)
            for text, cmd in zip(action_texts, action_commands):
                a = QAction(text=text, parent=menu)
                if action_icon is not None:
                    a.setIcon(action_icon)
                menu.addAction(a)
                a.triggered.connect(cmd)
            button.setMenu(menu)
            return menu
        return None

    def append_menu(self, button_name: str, action_text: str, action_command: 'Callable',
                    action_icon: QIcon = None) -> 'QAction':
        button: 'QToolButton' = self.get_control_widget(button_name)
        action = None
        if button is not None:
            menu = button.menu()
            if menu is None:
                menu = self.add_menu_to(button_name, [action_text], [action_command], action_icon=action_icon)
                return menu.actions()[0]
            else:
                action = QAction(text=action_text, parent=menu)
                if action_icon is not None:
                    action.setIcon(action_icon)
                menu.addAction(action)
                action.triggered.connect(action_command)

        return action

    def append_qmenu(self, button_name: str, menu_text: str, menu_icon: QIcon = None) -> QMenu:
        button: 'QToolButton' = self.get_control_widget(button_name)
        action = None
        if button is not None:
            menu = button.menu()
            new_menu = QMenu(menu)
            new_menu.setTitle(menu_text)
            # menu.addMenu()
            menu.addMenu(new_menu)
            # if menu is None:
            #     self.add_menu_to(button_name, [action_text], [action_command], action_icon=action_icon)
            # else:
            #     action = QAction(text=action_text, parent=menu)
            #     if action_icon is not None:
            #         action.setIcon(action_icon)
            #     menu.addAction(action)
            #     action.triggered.connect(action_command)

        return new_menu

    def add_menu_separator(self, button_name):
        button: 'QToolButton' = self.get_control_widget(button_name)
        action = None
        if button is not None:
            menu: QMenu = button.menu()
            if menu is not None:
                menu.addSeparator()

    def insert_after(self) -> str:
        """
        返回插入在某某后面
        Returns:

        """
        return ''
