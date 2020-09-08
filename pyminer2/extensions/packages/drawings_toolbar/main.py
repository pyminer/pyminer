from typing import TYPE_CHECKING
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QSizePolicy, QListWidget, QListWidgetItem, QToolButton, QSpacerItem

from pyminer2.extensions.extensionlib import generalwidgets,pmwidgets

if TYPE_CHECKING:
    pass
    from pyminer2.extensions.extensionlib import extension_lib

properties = [
    {
        'name': 'button_new_script',
        'text': '新建\脚本',
        'icon_path': ':/pyqt/source/images/lc_newdoc.png'
    },
    {
        'name': 'button_open_script',
        'text': '打开\脚本',
        'icon_path': ':/pyqt/source/images/lc_open.png'
    },
    {'names': ['']}
]


class ToolbarBlock(QWidget):
    def __init__(self, parent=None):
        super(ToolbarBlock, self).__init__(parent=parent)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        self.annotation_label = QLabel('选择的变量')
        b1 = QLabel('尚未选择变量')
        h_layout.addWidget(b1)
        b1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        b1.setMaximumWidth(100)

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
        self.setLayout(QHBoxLayout())
        self.button_layout = QHBoxLayout()
        self.layout().addLayout(self.button_layout)
        self.layout().addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    def add_button(self, button: QPushButton):
        if len(self.buttons) >= 10:
            import warnings
            warnings.warn('按钮数量已经达到上限！')
            return
        self.buttons.append(button)
        self.button_layout.addWidget(button)


class ButtonMappedToItem(QToolButton):
    def __init__(self, parent, item: 'QListWidgetItem'):
        super().__init__(parent)
        self.item: QListWidgetItem = item
        self.parent: 'PMDrawingsToolBar' = parent
        self.clicked.connect(self.on_mouse_clicked)

    def on_mouse_clicked(self):
        self.parent.on_item_double_clicked(self.item)


class PMDrawingsToolBar(generalwidgets.PMToolBar):
    drawing_item_double_clicked_signal: 'pyqtSignal' = pyqtSignal(str)
    extension_lib: 'extension_lib' = None

    def __init__(self):
        super().__init__()
        self.selected_var_show_label = QLabel()

        self.addSeparator()
        self.selected_var_show_label.setText('var:')
        tb_block = ToolbarBlock()
        self.add_widget('variable_show_block', tb_block)
        self._control_widget_dic['variable_show_label'] = tb_block.annotation_label

        self._control_widget_dic[
            'drawing_selection_panel'] = pmwidgets.TopLevelWidget(self)

        drawing_selection_panel: 'pmgwidgets.TopLevelWidget' \
            = self._control_widget_dic['drawing_selection_panel']
        drawing_selection_panel.set_central_widget(QListWidget())

        self.drawing_button_bar = ButtonBar(self)
        self._control_widget_dic['button_list'] = self.drawing_button_bar
        self.addWidget(self.drawing_button_bar)

        self.drawing_button_bar.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        drawing_selection_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drawing_selection_panel = drawing_selection_panel
        btn = self.add_tool_button('button_show_more_plots', text='▼')
        btn.setMaximumWidth(15)
        btn.clicked.connect(self.set_panel_visibility)

    def on_close(self):
        self.hide()
        self.deleteLater()

    def set_panel_visibility(self):
        self.refresh_pos()
        w: 'pmgwidgets.TopLevelWidget' = self._control_widget_dic['drawing_selection_panel']
        w.setVisible(not w.isVisible())

    def refresh_pos(self):
        btn = self.get_control_widget('button_show_more_plots')
        panel: 'pmgwidgets.TopLevelWidget' = self.get_control_widget('drawing_selection_panel')
        width = self.get_control_widget('button_list').width()
        panel.set_width(width)
        panel.set_position(QPoint(btn.x() - width, btn.y()))

    def bind_events(self):
        self.drawing_button_bar.setStyleSheet(
            'QWidget{background-color:#%s}' % self.extension_lib.Program.get_settings()['margin_theme'])
        drawing_list_widget: 'pmgwidgets.TopLevelWidget' = self.get_control_widget('drawing_selection_panel')
        cw: QListWidget = drawing_list_widget.central_widget
        cw.itemDoubleClicked.connect(self.on_item_double_clicked)
        for i, s in enumerate(['折线', '饼状', '条形', '散点', '热力'] * 10):
            self.add_toolbox_widget('aaaaa%d' % i, s,
                                    ':/pyqt/source/images/hist_simple.png', hint='',refresh=False)

        self.refresh_outer_buttons()
        self.extension_lib.Signal.get_resize_signal().connect(self.refresh_pos)
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)

    def refresh_outer_buttons(self):
        for w in self.drawing_button_bar.buttons:
            self.drawing_button_bar.button_layout.removeWidget(w)
        selection_list: 'QListWidget' = self.get_control_widget('drawing_selection_panel').central_widget
        for i in range(10):
            item = selection_list.item(i)
            b = ButtonMappedToItem(self, item)
            b.setIcon(item.icon())
            b.setText(item.text())
            b.setToolTip(item.text())
            b.setMaximumWidth(60)
            b.setMaximumHeight(40)
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.drawing_button_bar.button_layout.addWidget(b)

    def add_toolbox_widget(self, name: str, text: str,
                           icon_path: str, hint: str = '', refresh=True):
        pb = QPushButton()
        pb.setIcon(generalwidgets.create_icon(icon_path))
        self._control_widget_dic[name] = pb
        item = QListWidgetItem('%s图\n%s' % (text, hint))
        item.name = name
        cw: QListWidget = self.drawing_selection_panel.central_widget
        cw.addItem(item)
        item.setIcon(generalwidgets.create_icon((icon_path)))
        cw.setIconSize(QSize(40, 40))
        item.setSizeHint(QSize(self.drawing_selection_panel.width - 20, 40))
        if refresh:
            self.refresh_outer_buttons()

    def on_item_double_clicked(self, widget_item: QListWidgetItem):

        listwidget: QListWidget = self.drawing_selection_panel.central_widget
        self.drawing_item_double_clicked_signal.emit(widget_item.name)


class Extension():
    if TYPE_CHECKING:
        interface: 'DrawingsInterface' = None
        widget: 'PMDrawingsToolBar' = None
        extension_lib: 'extension_lib' = None

    def on_load(self):
        drawings_toolbar: 'PMDrawingsToolBar' = self.widgets['PMDrawingsToolBar']
        drawings_toolbar.extension_lib = self.extension_lib
        self.interface.drawing_item_double_clicked_signal = drawings_toolbar.drawing_item_double_clicked_signal
        self.interface.drawing_item_double_clicked_signal.connect(self.interface.on_clicked)

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class DrawingsInterface():
    drawing_item_double_clicked_signal: 'pyqtSignal' = None

    def on_clicked(self, name: str):
        print('interface', name)
