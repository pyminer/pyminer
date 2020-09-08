'''
这里定义了MainWindow的基类。
基类主要包含带选项卡工具栏的管理功能，以及浮动窗口的管理功能
添加浮动窗口时，默认‘关闭’事件就是隐藏。如果是彻底的关闭，需要进行重写。
每次界面关闭时，布局会被存入文件pyminer/config/customized/layout.ini之中。再次启动时，若这个文件存在，就会加载，反之不会加载。
'''
import os
from typing import Dict, TYPE_CHECKING

import chardet
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QMessageBox, QWidget, QMenu, QDialog

if TYPE_CHECKING:
    from pyminer2.pmappmodern import PMToolBarHome
    from pyminer2.ui.generalwidgets import PMDockWidget, ActionWithMessage, PMToolBar


class BaseMainWindow(QMainWindow):
    dialog_classes: Dict[str, 'QDialog'] = {}
    toolbars: Dict[str, QToolBar] = {}
    _current_toolbar_name: str = ''  # 当前的窗口标题栏选项卡
    dock_widgets: Dict[str, 'PMDockWidget'] = {}
    dock_places = {'left': Qt.LeftDockWidgetArea, 'right': Qt.RightDockWidgetArea, 'top': Qt.TopDockWidgetArea,
                   'bottom': Qt.BottomDockWidgetArea}
    settings = {}

    def load_settings(self):
        import json
        from pyminer2.pmutil import get_root_dir
        default_settings = {
            'work_dir': get_root_dir(),
            'main_theme': '#F7F7F7',
            'margin_theme': '#dadada'}
        # default_settings = {'work_dir': get_root_dir(), 'main_theme':
        # '#232323','margin_theme':'#565656'}
        try:
            with open(os.path.join(get_root_dir(), 'config', 'customized', 'ui_settings.json'), 'r') as f:
                settings = json.load(f)
        except BaseException:
            settings = {}
        print(settings, default_settings)
        self.settings.update(default_settings)
        self.settings.update(settings)
        print(self.settings)

        with open(os.path.join(get_root_dir(), 'config', 'ui', 'standard.qss'), 'rb') as f:
            b = f.read()
            enc = chardet.detect(b)
            if enc.get('encoding') is not None:
                s = b.decode(enc['encoding'])
                self.setStyleSheet(s.replace('MAIN_THEME', self.settings['main_theme']).replace('MARGIN_THEME',
                                                                                                self.settings[
                                                                                                    'margin_theme']))

    def save_settings(self):
        import json
        from pyminer2.pmutil import get_root_dir
        try:
            config_file = os.path.join(
                get_root_dir(),
                'config',
                'customized',
                'ui_settings.json')
            if not os.path.exists(os.path.join(
                    get_root_dir(), 'config', 'customized')):
                os.mkdir(os.path.join(get_root_dir(), 'config', 'customized'))
            with open(config_file, 'w') as f:
                json.dump(self.settings, f)
        except FileNotFoundError as e:
            print(e)

    def init_toolbar_tab(self):
        from pyminer2.ui.generalwidgets import TopToolBar
        tt = TopToolBar()
        tt.setFloatable(False)
        tt.setLayoutDirection(Qt.LeftToRight)
        tt.setMovable(False)
        tt.setObjectName('tab_bar_for_tool_bar')

        self.addToolBar(tt)
        self.top_toolbar_tab = tt

    def refresh_toolbar_appearance(self):
        for k in self.toolbars.keys():
            tab_button: 'QPushButton' = self.toolbars[k].tab_button
            width = len(tab_button.text()) * 20
            if k != self._current_toolbar_name:
                self.toolbars[k].hide()
                self.toolbars[k].tab_button.setStyleSheet(
                    'QPushButton{background-color:%s;width:%dpx;} '
                    'QPushButton:hover{background-color:%s;}' % (self.settings['main_theme'],
                                                                 width, self.settings['margin_theme']))
            else:
                self.toolbars[k].show()
                self.toolbars[k].tab_button.setStyleSheet(
                    'QPushButton{background-color:%s;width:%dpx;}' % (self.settings['margin_theme'], width))

    def show_toolbar(self, name):
        if self.toolbars.get(name) is not None:
            if name == self._current_toolbar_name:
                return
            else:
                self._current_toolbar_name = name
                self.refresh_toolbar_appearance()
        else:
            raise Exception('toolbar tab \'%s\' is not defined!' % name)

    def switch_toolbar(self, name: str):
        if self.toolbars.get(name) is not None:
            if name == self._current_toolbar_name:
                current_tb = self.toolbars[self._current_toolbar_name]
                current_tb.setVisible(not current_tb.isVisible())
            else:
                self._current_toolbar_name = name
                self.refresh_toolbar_appearance()
        else:
            raise Exception('toolbar tab \'%s\' is not defined!' % name)

    def add_toolbar(self, name: str, toolbar: QToolBar,
                    text: str = 'untitled toolbar'):

        b = self.top_toolbar_tab.add_button(text)
        toolbar.tab_button = b
        b.clicked.connect(lambda: self.switch_toolbar(name))

        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(toolbar)
        toolbar.setObjectName(name)
        self.toolbars[name] = toolbar
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        if self._current_toolbar_name != '':
            self.refresh_toolbar_appearance()

    def save_layout(self):
        from pyminer2.pmutil import get_root_dir
        try:
            root = os.path.join(get_root_dir(), 'config', 'customized')
            if not os.path.isdir(root):
                os.mkdir(root)
            p = os.path.join(root, 'layout.ini')
            with open(p, 'wb') as f:
                s = self.saveState()
                f.write(s)
        except FileNotFoundError:
            print("file not found:", p)

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
        from pyminer2.ui.generalwidgets import PMDockWidget, ActionWithMessage
        dw = PMDockWidget(name=dock_name, text=text, parent=self)
        dw.text = text
        dw.setObjectName(dock_name)
        dw.setWidget(widget)
        if hasattr(widget, 'signal_raise_into_view'):
            widget.signal_raise_into_view.connect(dw.raise_into_view)

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

        home_toolbar: 'PMToolBarHome' = self.toolbars.get('toolbar_home')

        self.refresh_view_configs()
        return dw

    def get_dock_widget(self, widget_name: str) -> 'PMDockWidget':
        dw = self.dock_widgets.get(widget_name)
        if dw is None:
            raise Exception(
                'dockwidget named \'%s\' is not defined!' %
                widget_name)
        return dw

    def delete_dock_widget(self, widget_name: str):
        '''
        删除dock_widget。
        :param widget_name:
        :return:
        '''
        if self.dock_widgets.get(widget_name) is not None:
            dock_widget = self.dock_widgets.pop(widget_name)
            if hasattr(dock_widget.widget(), 'on_dock_widget_deleted'):
                dock_widget.widget().on_dock_widget_deleted()
            dock_widget.deleteLater()

    def refresh_view_configs(self):
        from pyminer2.ui.generalwidgets import ActionWithMessage

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

    def on_boot_finished(self):
        self.refresh_view_configs()

    def raise_dock_into_view(self, dock_name: str):
        dock = self.dock_widgets.get(dock_name)
        if dock is not None:
            dock.raise_into_view()
            dock.setVisible(True)

    def bind_events(self):
        '''
        在启动的最后调用这个绑定事件的方法，让全部的控件都绑定事件。这样可以避免绑定的时候，由于对应控件未加载，发生找不到对应控件的错误
        :return:
        '''
        for k in self.dock_widgets.keys():
            w = self.dock_widgets[k]
            if hasattr(w, 'bind_events'):
                w.bind_events()
        for k in self.toolbars.keys():
            w = self.toolbars[k]
            if hasattr(w, 'bind_events'):
                w.bind_events()
