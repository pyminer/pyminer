"""

这里定义了MainWindow的基类。

基类主要包含带选项卡工具栏的管理功能，以及浮动窗口的管理功能。

添加浮动窗口时，默认‘关闭’事件就是隐藏。如果是彻底的关闭，需要进行重写。

每次界面关闭时，布局会被存入文件pyminer/config/customized/layout.ini之中。

再次启动时，若这个文件存在，就会加载，反之不会加载。

"""

import logging
import os
from typing import Dict, TYPE_CHECKING

import chardet
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QToolBar, QPushButton, QWidget, QMenu, QDialog

import utils
from lib.ui.common.pmlocale import pmlocale
from widgets import TopToolBarRight

if TYPE_CHECKING:
    from app2 import PMToolBarHome
    from lib.ui.pmwidgets.dockwidget import PMDockWidget
    from widgets import ActionWithMessage
logger = logging.getLogger(__name__)


class BaseMainWindow(QMainWindow):
    """
    PyMiner MainWindow主界面类的基类.

    """
    dialog_classes: Dict[str, 'QDialog'] = {}
    toolbars: Dict[str, QToolBar] = {}
    _current_toolbar_name: str = ''  # 当前的窗口标题栏选项卡
    __dock_widgets: Dict[str, 'PMDockWidget']
    dock_places = {'left': Qt.LeftDockWidgetArea, 'right': Qt.RightDockWidgetArea, 'top': Qt.TopDockWidgetArea,
                   'bottom': Qt.BottomDockWidgetArea}

    @property
    def dock_widgets(self):
        return self.__dock_widgets

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__dock_widgets = {}
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 隐藏主界面的菜单栏。

        self.resize(1366, 768)  # 设置主窗体默认大小

    def set_dock_titlebar_visible(self, show: bool):
        """
        切换停靠窗口的标题栏是否可见。只有可见的时候才能拖动。
        Args:
            show:

        Returns:

        """
        if show:
            for k, w in self.dock_widgets.items():
                w.setTitleBarWidget(None)

        else:
            for k, w in self.dock_widgets.items():
                w.setTitleBarWidget(QWidget())
        utils.write_settings_item_to_file("config.ini", "MAIN/PATH_WORKDIR", show)

    @staticmethod
    def get_stylesheet(style_sheet_name: str = 'standard'):
        """
        获取样式表
        TODO:这个方法应该拿到外面去，不应该和主界面深度绑定！
        Args:
            style_sheet_name:

        Returns:

        """
        style_sheet = ""
        with open(os.path.join(utils.get_root_dir(), 'resources', 'qss', '%s.qss' % style_sheet_name), 'rb') as f:
            b = f.read()
            enc = chardet.detect(b)
            if enc.get('encoding') is not None:
                s = b.decode(enc['encoding'])
                style_sheet = s
            else:
                logger.fatal("加载样式表%s失败！" % style_sheet_name)
        return style_sheet

    def init_toolbar_tab(self):
        """
        初始化工具栏的选项卡
        Returns:

        """
        from widgets import TopToolBar
        ttb = TopToolBar()
        ttb.setObjectName('tab_bar_for_tool_bar')
        self.addToolBar(ttb)
        ttbr = TopToolBarRight()
        ttbr.setObjectName('top_toolbar_right')
        self.addToolBar(ttbr)
        self.toolbar_hide_button = ttbr.hide_button
        self.toolbar_hide_button.clicked.connect(self.on_toolbar_hide_button_pressed)
        self.top_toolbar_tab = ttb

    def on_toolbar_hide_button_pressed(self):
        """
        当点击隐藏工具栏的按钮时
        Returns:

        """
        current_toolbar = self.toolbars[self._current_toolbar_name]
        if current_toolbar.isVisible():
            current_toolbar.hide()

        else:
            current_toolbar.show()
        self.refresh_toolbar_hide_button_status()

    def refresh_toolbar_appearance(self, force_to_show: bool = True):
        """
        刷新工具栏的外观
        Args:
            force_to_show:

        Returns:

        """
        for k in self.toolbars.keys():
            tab_button: 'QPushButton' = self.toolbars[k].tab_button
            width = len(tab_button.text()) * 10 + 20
            button: 'QPushButton' = self.toolbars[k].tab_button
            if k != self._current_toolbar_name:
                self.toolbars[k].hide()
                button.setProperty('stat', 'unselected')
            else:
                if force_to_show:
                    self.toolbars[k].show()
                button.setProperty('stat', 'selected')
            button.setStyle(button.style())

    def refresh_toolbar_hide_button_status(self):
        """
        刷新工具栏隐藏按钮的状态（按钮的箭头向上还是向下）
        Returns:

        """
        current_toolbar = self.toolbars[self._current_toolbar_name]
        if not current_toolbar.isVisible():
            self.toolbar_hide_button.setArrowType(Qt.DownArrow)
        else:
            self.toolbar_hide_button.setArrowType(Qt.UpArrow)

    def on_toolbar_switch_button_clicked(self, name):
        self.switch_toolbar(name, switch_only=False)

    def switch_toolbar(self, name: str, switch_only: bool = True):
        """
        name：工具栏的名称
        switch_only:如果为True，那么在调用时只会切换工具栏，当当前的工具栏名称与name相等时，
        调用多次不会改变当前工具栏的显示状态。为False的时候，若当前工具栏名称为name，那么就会改变显示状态，
        亦即原先显示的隐藏，原先隐藏的显示。
        """
        if self.toolbars.get(name) is not None:
            if name == self._current_toolbar_name:
                if not switch_only:
                    current_tb = self.toolbars[self._current_toolbar_name]
                    current_tb.setVisible(not current_tb.isVisible())
            else:
                self._current_toolbar_name = name
                self.refresh_toolbar_appearance(force_to_show=True)
        else:
            raise Exception('toolbar tab \'%s\' is not defined!' % name)
        self.refresh_toolbar_hide_button_status()

    def save_layout(self):
        """
        当关闭程序时保存布局
        Returns:

        """
        cfg_dir = utils.get_user_config_dir()
        layout_path = os.path.join(cfg_dir, 'layout.ini')
        try:
            with open(layout_path, 'wb') as f:
                s = b''  # self.saveState()
                f.write(s)
        except FileNotFoundError:
            logging.warning("file not found:" + layout_path)

    def load_layout(self):
        # p = os.path.join(Settings.get_instance().settings_path, 'layout.ini')

        # if os.path.exists(p):
        #     with open(p, 'rb') as f:
        #         s = f.read()
        #         self.restoreState(s)

        p = os.path.join(utils.get_root_dir(), 'resources', 'qss', 'standard.ini')
        with open(p, 'rb') as f:
            s = f.read()
            self.restoreState(s)
        self.refresh_view_configs()

    def load_predefined_layout(self, layout_type: str = 'standard'):
        layouts = {'standard': 'standard.ini'}
        p = os.path.join(utils.get_root_dir(), 'resources', 'qss', layouts[layout_type])
        if os.path.exists(p):
            with open(p, 'rb') as f:
                s = f.read()
                self.restoreState(s)
        for name in self.toolbars.keys():
            self.toolbars[name].setVisible(False)
        self.toolbars[self._current_toolbar_name].setVisible(True)
        self.refresh_view_configs()

    def add_widget_on_dock(self, dock_name: str,
                           widget: QWidget, text: str = '', side='left'):
        """
        向界面添加控件
        Args:
            dock_name:
            widget:
            text:
            side:

        Returns:

        """
        from lib.ui.pmwidgets import PMDockWidget
        text = pmlocale.translate(text)
        dw = PMDockWidget(name=dock_name, text=text, parent=self)
        dw.text = text
        dw.setObjectName(dock_name)
        dw.setWidget(widget)

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
            raise Exception(
                'docked widget name: \'%s\' is already used!' %
                dock_name)

        self.refresh_view_configs()
        return dw

    def get_dock_widget(self, widget_name: str) -> 'PMDockWidget':
        """
        获取停靠的控件
        Args:
            widget_name:

        Returns:

        """
        dw = self.dock_widgets.get(widget_name)
        if dw is None:
            logging.debug('dockwidget named \'%s\' is not defined!' % widget_name)
        return dw

    def delete_dock_widget(self, widget_name: str):
        """
        删除dock_widget。
        Args:
            widget_name:

        Returns:

        """
        if self.dock_widgets.get(widget_name) is not None:
            dock_widget = self.dock_widgets.pop(widget_name)
            if hasattr(dock_widget.widget(), 'on_dock_widget_deleted'):
                dock_widget.widget().on_dock_widget_deleted()
            dock_widget.deleteLater()

    def refresh_view_configs(self):
        """
        刷新工具栏的可见状态,更新视图菜单
        Returns:

        """
        from widgets import ActionWithMessage

        home_toolbar: 'PMToolBarHome' = self.toolbars.get('toolbar_home')
        # menu = home_toolbar.get_control_widget('view_config').menu()
        # if menu is None:
        menu = QMenu()
        menu.triggered.connect(home_toolbar.process_visibility_actions)
        for k in self.dock_widgets.keys():
            a = ActionWithMessage(
                text=self.dock_widgets[k].text,
                parent=home_toolbar,
                message=k)
            a.setCheckable(True)
            a.setChecked(self.dock_widgets[k].widget().isVisible())
            menu.addAction(a)
        menu.addSeparator()
        a = ActionWithMessage(
            text=self.tr('Normal View'),
            parent=home_toolbar,
            message='load_standard_layout')
        menu.addAction(a)
        a = ActionWithMessage(
            text=self.tr('Lock UI Layout'),
            parent=home_toolbar,
            message='lock_layout')
        a.setCheckable(True)
        dock_title_visible = utils.get_settings_item_from_file("config.ini", "MAIN/DOCK_TITLEBAR_VISIBLE")
        a.setChecked(not dock_title_visible)
        menu.addAction(a)
        home_toolbar.get_control_widget('view_config').setMenu(menu)
        self._view_config_menu = menu

    def on_main_window_shown(self):
        """
        主界面显示时调用的方法
        Returns:

        """
        self.refresh_view_configs()

    def raise_dock_into_view(self, dock_name: str):
        """
        将dockwidget提升到可见。
        """
        dock = self.get_dock_widget(dock_name)
        if dock is not None:
            dock.raise_into_view()
            dock.setVisible(True)

    def delete_temporary_dock_windows(self):
        """
        删除临时性的窗口
        """
        keys = list(self.dock_widgets.keys())
        for dock_name in keys:
            dock = self.dock_widgets.get(dock_name)
            if dock.widget().is_temporary():
                self.dock_widgets.pop(dock_name)
                logging.info('Closing and deleting temporary dock widget object:%s,named:%s, with widget :%s'
                             % (dock, dock_name, dock.widget()))
                dock.close()
                dock.deleteLater()

    def bind_events(self):
        """
        让全部的控件都绑定事件。

        在启动的最后调用这个绑定事件的方法，
        这样可以避免绑定的时候，由于对应控件未加载，发生找不到对应控件的错误
        """
        for k, w in self.dock_widgets.items():
            if hasattr(w, 'bind_events'):
                w.bind_events()
        for k, w in self.toolbars.items():
            if hasattr(w, 'bind_events'):
                w.bind_events()
