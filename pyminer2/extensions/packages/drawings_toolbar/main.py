import os
from typing import TYPE_CHECKING, Callable, Dict
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QSizePolicy, QListWidget, QListWidgetItem, QToolButton, QSpacerItem

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from typing import Dict, Callable

from pyminer2.extensions.extensionlib import pmwidgets
from pmgwidgets import PMGToolBar, create_icon
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

_ = lambda s: s
if TYPE_CHECKING:
    pass
    from pyminer2.extensions.extensionlib import extension_lib


class PMMenuToolPanel(QFrame):
    """
    面板控件，用于放置绘图按钮或其他插件按钮
    """
    def __init__(self):
        super(PMMenuToolPanel, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(QtCore.QSize(500, 85))
        self.setMaximumSize(QtCore.QSize(16777215, 85))
        self.setObjectName("frame")
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        self.widget_panel = QWidget()
        self.widget_panel_hbox = QHBoxLayout()
        self.widget_panel_hbox.setContentsMargins(0, 0, 0, 0)
        self.widget_panel_hbox.setSpacing(0)
        self.widget_panel.setLayout(self.widget_panel_hbox)

        self.hspace = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_down = QToolButton()
        self.btn_down.setObjectName("btn_tool_select")
        self.btn_down.setToolTip("查看更多")
        self.btn_down.setMinimumSize(QtCore.QSize(25, 85))
        self.btn_down.setMaximumSize(QtCore.QSize(25, 85))
        self.btn_down.setStyleSheet("#btn_tool_select{border:1px solid rgb(189,189,189);border-top-left-radius:0px;border-top-right-radius:5px;border-bottom-left-radius:0px;border-bottom-right-radius:5px;background-color: rgb(230,230,230);padding:0px 0px 0px 0px;}#btn_tool_select:hover{background:lightgray;}")

        self.current_path = os.path.dirname(__file__)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(self.current_path, 'source/down.svg')), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.btn_down.setIcon(icon1)

        self.btn_down.setAutoRaise(True)

        # 添加按钮和弹簧到水平布局
        self.hbox.addWidget(self.widget_panel)
        self.hbox.addItem(self.hspace)
        self.hbox.addWidget(self.btn_down)
        self.setLayout(self.hbox)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(1)
        self.setStyleSheet(
            "#frame{border:1px solid rgb(189,189,189);padding: -5px -10px 0px 20px;margin: 0px 0px 0px 0px;border-radius:5px;}")

        self.btn_down.clicked.connect(self.close)

        #测试添加按钮
        self.add_button("柱形图",os.path.join(self.current_path, 'source/柱形图.png'),self.close)
        self.add_button("折线图", os.path.join(self.current_path, 'source/折线图.png'), self.close)
        self.add_button("饼图", os.path.join(self.current_path, 'source/饼图.png'), self.close)
        self.add_button("条形图", os.path.join(self.current_path, 'source/条形图.png'), self.close)
        self.add_button("面积图", os.path.join(self.current_path, 'source/面积图.png'), self.close)
        self.add_button("气泡图", os.path.join(self.current_path, 'source/气泡图.png'), self.close)
        self.add_button("箱线图", os.path.join(self.current_path, 'source/箱线图.png'), self.close)
        self.add_button("直方图", os.path.join(self.current_path, 'source/直方图.png'), self.close)
        self.add_button("雷达图", os.path.join(self.current_path, 'source/雷达图.png'), self.close)
        self.add_button("热力图", os.path.join(self.current_path, 'source/热力图.png'), self.close)
        self.add_button("地图", os.path.join(self.current_path, 'source/地图.png'), self.close)
        self.add_button("组合图", os.path.join(self.current_path, 'source/组合图.png'), self.close)



    def add_button(self,btn_text:str,icon_path:str,btn_action:Callable)->None:
        sub_widget = QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        sub_widget.setIcon(icon)
        sub_widget.setIconSize(QtCore.QSize(50, 50))
        sub_widget.setMinimumSize(QtCore.QSize(85, 75))
        sub_widget.setMaximumSize(QtCore.QSize(85, 75))
        sub_widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        sub_widget.setAutoRaise(True)
        sub_widget.setText(btn_text)
        self.widget_panel_hbox.addWidget(sub_widget)
        sub_widget.clicked.connect(btn_action)


class ToolbarBlock(QWidget):
    def __init__(self, parent=None):
        global _
        super(ToolbarBlock, self).__init__(parent=parent)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        self.annotation_label = QLabel(_('Variable Selected'))
        variable_show_label = QLabel(_('No Variable'))
        h_layout.addWidget(variable_show_label)
        variable_show_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        variable_show_label.setMaximumWidth(100)

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
        self.item: QListWidgetItem = item
        self.parent: 'PMDrawingsToolBar' = parent
        self.clicked.connect(self.on_mouse_clicked)

    def on_mouse_clicked(self):
        self.parent.on_item_double_clicked(self.item)


class PMDrawingsToolBar(PMGToolBar):
    drawing_item_double_clicked_signal: 'pyqtSignal' = pyqtSignal(str)
    extension_lib: 'extension_lib' = None
    variable = None

    def __init__(self):
        super().__init__()
        self.selected_var_show_label = QLabel()


        self.selected_var_show_label.setText('var:')

        tb_block = ToolbarBlock()
        self.toolbar_block = tb_block
        self.add_widget('variable_show_block', tb_block)
        self._control_widget_dic['variable_show_label'] = tb_block.variable_show_label

        self._control_widget_dic[
            'drawing_selection_panel'] = pmwidgets.TopLevelWidget(self)

        drawing_selection_panel: 'pmgwidgets.TopLevelWidget' \
            = self._control_widget_dic['drawing_selection_panel']
        drawing_selection_panel.set_central_widget(QListWidget())

        self.addSeparator()

        self.drawing_button_bar = PMMenuToolPanel()
        self._control_widget_dic['button_list'] = self.drawing_button_bar
        self.addWidget(self.drawing_button_bar)

        self.drawing_button_bar.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        # drawing_selection_panel.setSizePolicy(
        #     QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.drawing_selection_panel = drawing_selection_panel
        # btn = self.add_tool_button('button_show_more_plots', text='▼')
        # btn.setMaximumWidth(15)
        # btn.clicked.connect(self.set_panel_visibility)

    def on_data_selected(self, data_name: str):
        """
        当文件树中的数据被单击选中时，调用这个方法。
        """
        print('on_data_selected')
        self.toolbar_block.variable_show_label.setText('%s' % data_name)
        self.variable = self.extension_lib.get_var(data_name)
        print('variable name is \''+data_name+'\' , value is',self.variable)

    def on_data_modified(self, var_name: str, variable: object, data_source: str):
        """
        在数据被修改时，调用这个方法。
        """
        pass

    def on_close(self):
        self.hide()
        self.deleteLater()

    def set_panel_visibility(self):
        self.refresh_pos()
        w: 'pmgwidgets.TopLevelWidget' = self._control_widget_dic['drawing_selection_panel']
        w.setVisible(not w.isVisible())

    def refresh_pos(self):
        """
        刷新顶上的ToplevelWidget的位置。
        """
        return
        btn = self.get_control_widget('button_show_more_plots')
        panel: 'pmgwidgets.TopLevelWidget' = self.get_control_widget(
            'drawing_selection_panel')
        width = self.get_control_widget('button_list').width()
        panel.set_width(width)
        panel.set_position(QPoint(btn.x() - width, btn.y()))

    def bind_events(self):
        """
        绑定事件。这个将在界面加载完成之后被调用。
        """

        drawing_list_widget: 'pmgwidgets.TopLevelWidget' = self.get_control_widget(
            'drawing_selection_panel')
        cw: QListWidget = drawing_list_widget.central_widget
        cw.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.extension_lib.Signal.get_window_geometry_changed_signal().connect(self.refresh_pos)
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)

    def refresh_outer_buttons(self):
        """
        刷新显示在按纽条上面的按钮们。
        首先全部移除，然后添加进来。
        这些按钮不是由用户控制添加的，而是自动的呈现listwidget的前最多10项。
        """
        for w in self.drawing_button_bar.buttons:
            self.drawing_button_bar.button_layout.removeWidget(w)
        selection_list: 'QListWidget' = self.get_control_widget(
            'drawing_selection_panel').central_widget
        for i in range(10):
            item = selection_list.item(i)

            if item is None:
                break
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
        """
        将控件添加到工具箱，成为QListWidgetItem，通过这些Item生成对应的按钮。
        """
        item = QListWidgetItem('%s\n%s' % (text, hint))
        item.name = name
        cw: QListWidget = self.drawing_selection_panel.central_widget
        cw.addItem(item)
        item.setIcon(create_icon((icon_path)))
        cw.setIconSize(QSize(40, 40))
        item.setSizeHint(QSize(self.drawing_selection_panel.width - 20, 40))
        if refresh:
            self.refresh_outer_buttons()

    def on_item_double_clicked(self, widget_item: QListWidgetItem):

        listwidget: QListWidget = self.drawing_selection_panel.central_widget
        self.drawing_item_double_clicked_signal.emit(widget_item.name)


class Extension(BaseExtension):
    if TYPE_CHECKING:
        interface: 'DrawingsInterface' = None
        widget: 'PMDrawingsToolBar' = None
        extension_lib: 'extension_lib' = None

    def on_loading(self):
        global _
        _ = self.extension_lib.Program._
        self.extension_lib.Program.add_translation('zh_CN', {'Drawings': '绘图', 'Variable Selected': '选择的变量',
                                                             'No Variable': '尚未选择变量'})

    def on_load(self):
        drawings_toolbar: 'PMDrawingsToolBar' = self.widgets['PMDrawingsToolBar']
        drawings_toolbar.extension_lib = self.extension_lib
        self.drawings_toolbar = drawings_toolbar
        self.interface.drawing_item_double_clicked_signal = drawings_toolbar.drawing_item_double_clicked_signal

        self.interface.drawing_item_double_clicked_signal.connect(self.interface.on_clicked)
        self.interface.drawings_toolbar = drawings_toolbar

        self.extension_lib.on_modification(drawings_toolbar.on_data_modified)
        self.extension_lib.Signal.get_widgets_ready_signal().connect(self.bind_events)

    def bind_events(self):
        workspace_interface = self.extension_lib.get_interface('workspace_inspector')
        workspace_interface.add_select_data_callback(self.drawings_toolbar.on_data_selected)


class DrawingsInterface(BaseInterface):
    drawing_item_double_clicked_signal: 'pyqtSignal' = None
    drawings_toolbar: 'PMDrawingsToolBar' = None

    def on_clicked(self, name: str):
        pass
        # print('interface', name)

    def add_graph_button(self, name: str, text: str, icon_path: str, callback: Callable, hint: str = ''):
        """
        添加一个绘图按钮。name表示按钮的名称,text表示按钮的文字，icon_path表示按钮的图标路径，callback表示按钮的回调函数
        hint表示的就是按钮鼠标悬浮时候的提示文字。
        例如：
        extension_lib.get_interface('drawings_toolbar').add_graph_button('aaaaaa','hahahaahahah',
                                                                         ':/pyqt/source/images/lc_searchdialog.png',lambda :print('123123123'))
        """
        self.drawings_toolbar.add_toolbox_widget(name, text, icon_path, hint, refresh=True)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win1 = PmMenuToolPanel()
    win1.show()

    sys.exit(app.exec())