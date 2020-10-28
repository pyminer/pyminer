"""
这里定义了MainWindow的基类。
基类主要包含带选项卡工具栏的管理功能，以及浮动窗口的管理功能
添加浮动窗口时，默认‘关闭’事件就是隐藏。如果是彻底的关闭，需要进行重写。
每次界面关闭时，布局会被存入文件pyminer/config/customized/layout.ini之中。再次启动时，若这个文件存在，就会加载，反之不会加载。
"""
import os
from typing import Dict, TYPE_CHECKING

import chardet
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QWidget, QMenu, QDialog

from pmgwidgets.toolbars.toolbar import TopToolBarRight

from pyminer2.ui.common.locale import pmlocale
import logging
from pyminer2.features.io.settings import Settings

if TYPE_CHECKING:
    from pyminer2.pmappmodern import PMToolBarHome
    from pyminer2.ui.pmwidgets.dockwidget import PMDockWidget
    from pmgwidgets import ActionWithMessage


class BaseMainWindow(QMainWindow):
    dialog_classes: Dict[str, 'QDialog'] = {}
    toolbars: Dict[str, QToolBar] = {}
    _current_toolbar_name: str = ''  # 当前的窗口标题栏选项卡
    dock_widgets: Dict[str, 'PMDockWidget'] = {}
    dock_places = {'left': Qt.LeftDockWidgetArea, 'right': Qt.RightDockWidgetArea, 'top': Qt.TopDockWidgetArea,
                   'bottom': Qt.BottomDockWidgetArea}

    def load_stylesheet(self, style_sheet_name: str = 'standard'):
        self.setStyleSheet(self.get_stylesheet(style_sheet_name))

    @staticmethod
    def get_stylesheet(style_sheet_name: str = 'standard'):
        style_sheet = ""
        from pyminer2.pmutil import get_root_dir
        with open(os.path.join(get_root_dir(), 'config', 'ui', '%s.qss' % style_sheet_name), 'rb') as f:
            b = f.read()
            enc = chardet.detect(b)
            if enc.get('encoding') is not None:
                s = b.decode(enc['encoding'])
                style_sheet = s.replace(
                    'MAIN_THEME', Settings.get_instance()['main_theme']).replace(
                    'MARGIN_THEME', Settings.get_instance()['margin_theme'])
        return style_sheet

    def init_toolbar_tab(self):
        from pmgwidgets import TopToolBar
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
        current_toolbar = self.toolbars[self._current_toolbar_name]
        if current_toolbar.isVisible():
            current_toolbar.hide()

        else:
            current_toolbar.show()
        self.refresh_toolbar_hide_button_status()

    def refresh_toolbar_appearance(self, force_to_show: bool = True):
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
        from pyminer2.pmutil import get_root_dir
        p = ''
        try:
            root = os.path.join(get_root_dir(), 'config', 'customized')
            if not os.path.isdir(root):
                os.mkdir(root)
            p = os.path.join(root, 'layout.ini')
            with open(p, 'wb') as f:
                s = self.saveState()
                f.write(s)
        except FileNotFoundError:
            logging.warning("file not found:" + p)

    def load_layout(self):
        from pyminer2.pmutil import get_root_dir
        p = os.path.join(get_root_dir(), 'config', 'customized', 'layout.ini')
        if os.path.exists(p):
            with open(p, 'rb') as f:
                s = f.read()
                self.restoreState(s)
        else:
            p = os.path.join(get_root_dir(), 'config', 'ui', 'standard.ini')
            with open(p, 'rb') as f:
                s = f.read()
                self.restoreState(s)

    def load_predefined_layout(self, layout_type: str = 'standard'):
        from pyminer2.pmutil import get_root_dir
        layouts = {'standard': 'standard.ini'}
        p = os.path.join(get_root_dir(), 'config', 'ui', layouts[layout_type])
        if os.path.exists(p):
            with open(p, 'rb') as f:
                s = f.read()
                self.restoreState(s)
        self.refresh_view_configs()

    def add_widget_on_dock(self, dock_name: str,
                           widget: QWidget, text: str = '', side='left'):
        from pyminer2.ui.pmwidgets import PMDockWidget
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
        dw = self.dock_widgets.get(widget_name)
        if dw is None:
            logging.debug('dockwidget named \'%s\' is not defined!' % widget_name)
        return dw

    def delete_dock_widget(self, widget_name: str):
        """
        删除dock_widget。
        :param widget_name:
        :return:
        """
        if self.dock_widgets.get(widget_name) is not None:
            dock_widget = self.dock_widgets.pop(widget_name)
            if hasattr(dock_widget.widget(), 'on_dock_widget_deleted'):
                dock_widget.widget().on_dock_widget_deleted()
            dock_widget.deleteLater()

    def refresh_view_configs(self):
        from pmgwidgets import ActionWithMessage

        home_toolbar: 'PMToolBarHome' = self.toolbars.get('toolbar_home')
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
            text='标准视图',
            parent=home_toolbar,
            message='load_standard_layout')
        menu.addAction(a)
        home_toolbar.view_config_button.setMenu(menu)

    def on_main_window_shown(self):
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
        :return:
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
        在启动的最后调用这个绑定事件的方法，让全部的控件都绑定事件。这样可以避免绑定的时候，由于对应控件未加载，发生找不到对应控件的错误
        :return:
        """
        for k in self.dock_widgets.keys():
            w = self.dock_widgets[k]
            if hasattr(w, 'bind_events'):
                w.bind_events()
        for k in self.toolbars.keys():
            w = self.toolbars[k]
            if hasattr(w, 'bind_events'):
                w.bind_events()
