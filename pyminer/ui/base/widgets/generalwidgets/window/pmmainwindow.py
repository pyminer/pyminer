'''
这里定义了MainWindow的基类。
基类主要包含带选项卡工具栏的管理功能，以及浮动窗口的管理功能
添加浮动窗口时，默认‘关闭’事件就是隐藏。如果是彻底的关闭，需要进行重写。
每次界面关闭时，布局会被存入文件pyminer/config/qtlayout.ini之中。再次启动时，若这个文件存在，就会加载，反之不会加载。
'''
import os
from typing import Dict,TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QMessageBox, QWidget, QMenu

# from pyminer.pmappmodern import TopToolBar, PMToolBarHome
from pyminer.ui.base.widgets.generalwidgets.toolbars import TopToolBar, ActionWithMessage
from pyminer.ui.base.widgets.codeeditwidget import PMToolBar
from pyminer.ui.base.widgets.generalwidgets.buttons import PushButtonPane
from pyminer.ui.base.widgets.generalwidgets.window import PMDockWidget
from pyminer.pmutil import get_root_dir

if TYPE_CHECKING:
    from pyminer.pmappmodern import PMToolBarHome

class BaseMainWindow(QMainWindow):
    toolbars: Dict[str, QToolBar] = {}
    _current_toolbar_name: str = ''# 当前的窗口标题栏选项卡
    dock_widgets: Dict[str, PMDockWidget] = {}
    dock_places = {'left': Qt.LeftDockWidgetArea, 'right': Qt.RightDockWidgetArea, 'top': Qt.TopDockWidgetArea,
                   'bottom': Qt.BottomDockWidgetArea}

    def init_toolbar_tab(self):
        tt = TopToolBar()
        tt.setFloatable(False)
        tt.setLayoutDirection(Qt.LeftToRight)
        tt.setMovable(False)
        tt.setObjectName('tab_bar_for_tool_bar')

        self.addToolBar(tt)
        self.top_toolbar_tab = tt

    def switch_toolbar(self, name: str):
        if self.toolbars.get(name) is not None:

            if name == self._current_toolbar_name:
                return
            else:
                for k in self.toolbars.keys():
                    if k == name:
                        self.toolbars[k].show()
                        self.toolbars[k].tab_button.setStyleSheet(
                            'QPushButton{color:#444444;background-color:#ffffff;border:0px;width:100px;}')
                        self._current_toolbar_name = k
                    else:
                        self.toolbars[k].hide()
                        self.toolbars[k].tab_button.setStyleSheet(
                            'QPushButton{color:#efefef;background-color:#1234ee;border:0px;width:100px;}')
        else:
            raise Exception('toolbar tab \'%s\' is not defined!' % name)

    def add_toolbar(self, name: str, toolbar: QToolBar, text: str = 'untitled toolbar'):

        b = QPushButton(text)
        self.top_toolbar_tab.addWidget(b)
        toolbar.tab_button = b
        b.setStyleSheet('QPushButton{color:#efefef;background-color:#1234ee;border:0px;width:100px;}')
        b.clicked.connect(lambda: self.switch_toolbar(name))

        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(toolbar)
        toolbar.setObjectName(name)
        self.toolbars[name] = toolbar
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.addWidget(PushButtonPane())

    def save_layout(self):

        p = os.path.join(get_root_dir(), 'config', 'qtlayout.ini')
        with open(p, 'wb') as f:
            s = self.saveState()
            f.write(s)

    def load_layout(self):
        p = os.path.join(get_root_dir(), 'config', 'qtlayout.ini')
        if os.path.exists(p):
            with open(p, 'rb') as f:
                s = f.read()
                self.restoreState(s)

    def closeEvent(self, event: QCloseEvent) -> None:

        reply = QMessageBox.question(self, '注意', '确认退出吗？', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()

    def add_widget_on_dock(self, dock_name: str, widget: QWidget, text: str = '', side='left'):
        dw = PMDockWidget(text=text, parent=self)
        dw.text = text
        dw.setObjectName(dock_name)
        dw.setWidget(widget)
        if hasattr(widget, 'load_actions'):
            widget.load_actions()
        if hasattr(widget, 'setup_ui'):
            if hasattr(widget, 'show_directly'):
                if widget.show_directly:
                    widget.setup_ui()
                else:
                    self.setupui_tasks.append(widget.setup_ui)
            else:
                self.setupui_tasks.append(widget.setup_ui)

        self.addDockWidget(self.dock_places[side], dw)
        if dock_name not in self.dock_widgets.keys():
            self.dock_widgets[dock_name] = dw
        else:
            raise Exception('docked widget name: \'%s\' is already used!' % dock_name)

        home_toolbar:'PMToolBarHome' = self.toolbars.get('toolbar_home')

        menu = QMenu()
        menu.triggered.connect(home_toolbar.process_visibility_actions)
        for k in self.dock_widgets.keys():
            a = ActionWithMessage(text=self.dock_widgets[k].text, parent=home_toolbar, message=k)

            a.setCheckable(True)

            menu.addAction(a)

        home_toolbar.view_config_button.setMenu(menu)

    def refresh_view_configs(self):
        home_toolbar:'PMToolBarHome' = self.toolbars.get('toolbar_home')
        menu = QMenu()
        menu.triggered.connect(home_toolbar.process_visibility_actions)
        for k in self.dock_widgets.keys():
            a = ActionWithMessage(text=self.dock_widgets[k].text, parent=home_toolbar, message=k)
            a.setCheckable(True)
            a.setChecked(self.dock_widgets[k].widget().isVisible())
            menu.addAction(a)
        home_toolbar.view_config_button.setMenu(menu)

    def on_boot_finished(self):
        self.refresh_view_configs()
