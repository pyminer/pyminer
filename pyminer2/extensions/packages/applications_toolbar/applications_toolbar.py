import os
from typing import TYPE_CHECKING, Callable
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize
from PyQt5.QtGui import QPalette, QColor, QPaintEvent, QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QSizePolicy, QListWidgetItem, QToolButton, QSpacerItem

from pmgwidgets.containers import PMGToolBox
from pyminer2.extensions.extensionlib import pmwidgets
from pmgwidgets import PMGToolBar, create_icon

if TYPE_CHECKING:
    pass
    from pyminer2.extensions.extensionlib import extension_lib


class ToolbarBlock(QWidget):
    def __init__(self, parent=None):
        global _
        super(ToolbarBlock, self).__init__(parent=parent)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        self.annotation_label = QLabel(self.tr('Variable Selected'))
        variable_show_label = QLabel(self.tr('No Variable'))
        h_layout.addWidget(variable_show_label)
        variable_show_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        variable_show_label.setMaximumWidth(100)
        variable_show_label.setMaximumHeight(200)

        variable_show_label.setAlignment(Qt.AlignCenter)
        self.variable_show_label = variable_show_label

        layout.addWidget(self.annotation_label)
        layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.annotation_label.setMaximumHeight(20)
        self.annotation_label.setMinimumHeight(20)
        self.annotation_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)


class ButtonBar(QWidget):
    buttons = []

    def __init__(self, parent=None):
        super(ButtonBar, self).__init__(parent)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColor(218,218,218))
        self.setPalette(palette)
        self.setLayout(QHBoxLayout())
        self.button_layout = QHBoxLayout()
        self.layout().addLayout(self.button_layout)
        self.layout().addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Expanding,
                QSizePolicy.Minimum))

    def add_button(self, button: QPushButton):
        """
        添加按钮。
        """
        if len(self.buttons) >= 10:
            import warnings
            warnings.warn('按钮数量已经达到上限！')
            return
        self.buttons.append(button)
        self.button_layout.addWidget(button)



class ButtonMappedToItem(QToolButton):
    """
    这个按钮类的意思是，将按钮与QListWidget的条目一一对应起来
    当使用循环生成按钮的时候，按钮没有办法通过匿名函数或者函数传参的方式进行类的传递，所以只能给每个按钮的对象都分别绑定一个QListWidgetitem

    """

    def __init__(self, parent: 'PMDrawingsToolBar', item: 'QListWidgetItem'):
        super().__init__(parent)
        self.item: QPushButton = item
        self.parent: 'PMDrawingsToolBar' = parent
        self.clicked.connect(self.item.click)


class PMDrawingsToolBar(PMGToolBar):
    drawing_item_double_clicked_signal: 'pyqtSignal' = pyqtSignal(str)
    extension_lib: 'extension_lib' = None
    variable = None
    widgets = {}

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        src_path = os.path.join(os.path.dirname(__file__), 'src')
        self.open_qtdesigner_button = \
            self.add_tool_button('open_qtdesigner_button', self.tr('应用设计'),
                                 icon=create_icon(os.path.join(src_path, 'qt-logo.png')))
        self.packup_app_button = \
            self.add_tool_button('packup_app_button', self.tr('应用打包'),
                                 icon=create_icon(os.path.join(src_path, 'package.svg')))
        self.install_app_button = \
            self.add_tool_button('install_app_button', self.tr('应用安装'),
                                 icon=create_icon(os.path.join(src_path, 'install.svg')))
        self.install_app_button = \
            self.add_tool_button('install_app_button', self.tr('获取应用'),
                                 icon=create_icon(os.path.join(src_path, 'appstore.svg')))
        self.addSeparator()
        self.apps_panel = pmwidgets.TopLevelWidget(self)

        self.buttons_toolbox = PMGToolBox()
        self.apps_panel.set_central_widget(self.buttons_toolbox)
        self.show_apps_button_bar = ButtonBar(self)
        self._control_widget_dic['button_list'] = self.show_apps_button_bar
        self.addWidget(self.show_apps_button_bar)

        self.show_apps_button_bar.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.apps_panel.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn = self.add_tool_button('button_show_more_plots', text='▼')
        btn.setStyleSheet('QPushButton{height:200px;}')
        btn.setMaximumWidth(15)
        btn.clicked.connect(self.set_panel_visibility)

    def on_close(self):
        self.hide()
        self.deleteLater()

    def set_panel_visibility(self):
        self.refresh_pos()

        self.apps_panel.setVisible(not self.apps_panel.isVisible())

    def refresh_pos(self):
        """
        刷新顶上的ToplevelWidget的位置。
        """
        btn = self.get_control_widget('button_show_more_plots')

        width = self.get_control_widget('button_list').width()
        self.apps_panel.set_width(width)
        self.apps_panel.set_position(QPoint(btn.x() - width, btn.y()))

    def main_appstore_dispaly(self):
        """
        显示"应用商店"窗口
        """
        self.appstore = base.AppstoreForm()
        # self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.appstore.show()

    def bind_events(self):
        """
        绑定事件。这个将在界面加载完成之后被调用。
        """
        self.extension_lib.Signal.get_window_geometry_changed_signal().connect(self.refresh_pos)
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)
        self.open_qtdesigner_button.clicked.connect(self.open_designer)
    def open_designer(self):
        """
        打开QtDesigner。
        """
        import subprocess
        import platform
        if platform.system()=="Windows":
            subprocess.Popen(['pyqt5designer'])
        else:
            subprocess.Popen(['designer'])

    def refresh_outer_buttons(self):
        """
        刷新显示在按纽条上面的按钮们。
        首先全部移除，然后添加进来。
        这些按钮不是由用户控制添加的，而是自动的呈现listwidget的前最多10项。
        """
        for w in self.show_apps_button_bar.buttons:
            self.show_apps_button_bar.button_layout.removeWidget(w)
            w.deleteLater()
        self.show_apps_button_bar.buttons = []
        num = 0
        for i in range(self.buttons_toolbox.count()):
            for widget in self.buttons_toolbox.widget(i).widgets_list:
                if widget is None:
                    break

                if num > 10:
                    break
                num += 1
                b = ButtonMappedToItem(self, widget)
                b.setIcon(widget.icon())
                b.setText(widget.text())
                b.setToolTip(widget.text())
                b.setMaximumWidth(80)
                b.setMaximumHeight(60)
                b.setIconSize(QSize(40, 40))
                b.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                # b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                self.show_apps_button_bar.add_button(b)

    def add_toolbox_widget(self, group: str, text: str,
                           icon_path: str, action: Callable, hint: str = '', refresh=True):
        """
        将控件添加到工具箱，成为QListWidgetItem，通过这些Item生成对应的按钮。
        """
        tb = self.buttons_toolbox.add_button(group, text, icon_path, action)
        if refresh:
            self.refresh_outer_buttons()

    def on_item_double_clicked(self, widget_item: QListWidgetItem):
        self.drawing_item_double_clicked_signal.emit(widget_item.name)
