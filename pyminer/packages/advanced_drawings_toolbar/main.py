import logging
import os
from typing import TYPE_CHECKING, Callable, Dict, ClassVar

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QLocale, QCoreApplication, Qt, Signal
from PySide2.QtWidgets import *
from numpy import ndarray
from pandas import Series, DataFrame

file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_%s.qm' % QLocale.system().name())
app = QtWidgets.QApplication.instance()
trans_editor = QtCore.QTranslator()
app.trans_editor = trans_editor
trans_editor.load(file_name)
app.installTranslator(trans_editor)
import numpy as np
import pandas as pd
from lib.extensions.extensionlib import BaseExtension, BaseInterface
from widgets import PMGToolBar, create_icon
from packages.drawings_toolbar.group_chart import DialogGroup
from packages.drawings_toolbar.radar_chart import radar_factory
from matplotlib import pyplot as plt
from matplotlib import cm, colors, colorbar
import json

from lib.comm import get_var

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from lib.extensions.extensionlib import extension_lib


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
        self.widget_panel.setStyleSheet("margin:1px;")
        self.widget_panel_hbox = QHBoxLayout()
        self.widget_panel_hbox.setContentsMargins(0, 0, 0, 0)
        self.widget_panel_hbox.setSpacing(10)
        self.widget_panel.setLayout(self.widget_panel_hbox)

        self.hspace = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_down = QToolButton()
        self.btn_down.setObjectName("btn_tool_select")
        self.btn_down.setToolTip("查看更多")
        self.btn_down.setMinimumSize(QtCore.QSize(25, 85))
        self.btn_down.setMaximumSize(QtCore.QSize(25, 85))
        self.btn_down.setStyleSheet(
            "#btn_tool_select{border:1px solid rgb(189,189,189);border-top-left-radius:0px;border-top-right-radius:5px;border-bottom-left-radius:0px;border-bottom-right-radius:5px;background-color: rgb(230,230,230);padding:0px 0px 0px 0px;}#btn_tool_select:hover{background:lightgray;}")

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
        self.dialog_grp = DialogGroup()
        self.setStyleSheet(
            "#frame{border:1px solid rgb(189,189,189);padding: -5px -10px 0px 20px;margin: 0px 0px 0px 0px;border-radius:5px;}")

        self.btn_down.clicked.connect(self.close)
        self.draw_funcs = {'line_chart': lambda: print('draw line chart!'),
                           'bar_chart': lambda: print('draw bar chart!'),
                           'pie_chart': lambda: print('draw pie chart!'),
                           'barh_chart': lambda: print('draw barh chart!'),
                           'stack_chart': lambda: print('draw stack chart!'),
                           'scatter_chart': lambda: print('draw scatter chart!'),
                           'box_chart': lambda: print('draw box chart!'),
                           'hist_chart': lambda: print('draw hist chart!'),
                           'radar_chart': lambda: print('draw radar chart!'),
                           'heap_chart': lambda: print('draw heap chart!'),
                           'map_chart': lambda: print('draw map!'),
                           'group_chart': lambda: print('draw group chart!')}
        # 测试添加按钮 lambda部分不能改
        self.add_button(self.tr("Bar"), os.path.join(self.current_path, 'source/柱形图.png'),
                        lambda: self.draw('bar_chart'))
        self.add_button(self.tr("Line"), os.path.join(self.current_path, 'source/折线图.png'),
                        lambda: self.draw('line_chart'))
        self.add_button(self.tr("Pie"), os.path.join(self.current_path, 'source/饼图.png'),
                        lambda: self.draw('pie_chart'))
        self.add_button(self.tr('HBar'), os.path.join(self.current_path, 'source/条形图.png'),
                        lambda: self.draw('barh_chart'))
        self.add_button(self.tr("Area"), os.path.join(self.current_path, 'source/面积图.png'),
                        lambda: self.draw('stack_chart'))
        self.add_button(self.tr("Bubble"), os.path.join(self.current_path, 'source/气泡图.png'),
                        lambda: self.draw('scatter_chart'))
        self.add_button(self.tr("Box"), os.path.join(self.current_path, 'source/箱线图.png'),
                        lambda: self.draw('box_chart'))
        self.add_button(self.tr("Histogram"), os.path.join(self.current_path, 'source/直方图.png'),
                        lambda: self.draw('hist_chart'))
        self.add_button(self.tr("Radar"), os.path.join(self.current_path, 'source/雷达图.png'),
                        lambda: self.draw('radar_chart'))
        self.add_button(self.tr("Heap"), os.path.join(self.current_path, 'source/热力图.png'),
                        lambda: self.draw('heap_chart'))
        # self.add_button("地图", os.path.join(self.current_path, 'source/地图.png'), lambda: self.draw('step_chart'))
        self.add_button(self.tr("Group"), os.path.join(self.current_path, 'source/组合图.png'),
                        lambda: self.draw('group_chart'))
        self.add_button(self.tr("Map"), os.path.join(self.current_path, 'source/地图.png'),
                        lambda: self.draw('map_chart'))

    def add_button(self, btn_text: str, icon_path: str, btn_action: Callable) -> None:
        sub_widget = QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        sub_widget.setIcon(icon)
        sub_widget.setIconSize(QtCore.QSize(50, 40))
        sub_widget.setMinimumSize(QtCore.QSize(85, 75))
        sub_widget.setMaximumSize(QtCore.QSize(85, 75))
        sub_widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        sub_widget.setAutoRaise(True)
        sub_widget.setText(btn_text)
        self.widget_panel_hbox.addWidget(sub_widget)
        sub_widget.clicked.connect(btn_action)

    def draw(self, chart_type: str):
        draw_chart_func = self.draw_funcs.get(chart_type)
        if draw_chart_func is not None:
            draw_chart_func()


class ToolbarBlock(QWidget):
    def __init__(self, parent=None):
        super(ToolbarBlock, self).__init__(parent=parent)

        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        self.annotation_label = QLabel(QCoreApplication.translate('ToolbarBlock', 'Variable Selected'))
        variable_show_label = QLabel(QCoreApplication.translate('ToolbarBlock', 'No Variable'))
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


class ButtonMappedToItem(QToolButton):
    """
    这个按钮类的意思是，将按钮与QListWidget的条目一一对应起来
    当使用循环生成按钮的时候，按钮没有办法通过匿名函数或者函数传
    参的方式进行类的传递，所以只能给每个按钮的对象都分别绑定一个
    QListWidgetitem.
    """

    def __init__(self, parent: 'PMDrawingsToolBar', item: 'QListWidgetItem'):
        super().__init__(parent)
        self.item: QListWidgetItem = item
        self.parent: 'PMDrawingsToolBar' = parent
        self.clicked.connect(self.on_mouse_clicked)

    def on_mouse_clicked(self):
        self.parent.on_item_double_clicked(self.item)


class PMDrawingsToolBar(PMGToolBar):
    drawing_item_double_clicked_signal: 'Signal' = Signal(str)
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

        self.addSeparator()
        self.drawing_button_bar = PMMenuToolPanel()

        self.dialog_group = DialogGroup()
        self.dialog_group.btn_combin.clicked.connect(self.draw_group_chart)
        self.dialog_group.cb_select1.currentIndexChanged.connect(self.cb1_change)
        self.dialog_group.cb_select2.currentIndexChanged.connect(self.cb2_change)
        self.draw_fig = None
        self._control_widget_dic['button_list'] = self.drawing_button_bar

        self.add_tool_button("button_draw_hist", "直方图", "选择变量并绘制直方图",
                             create_icon(os.path.join(os.path.dirname(__file__), 'source/直方图.png')))

        self.addWidget(self.drawing_button_bar)
        self.drawing_button_bar.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drawing_button_bar.draw_funcs['line_chart'] = self.draw_line_chart
        self.drawing_button_bar.draw_funcs['bar_chart'] = self.draw_bar_chart
        self.drawing_button_bar.draw_funcs['pie_chart'] = self.draw_pie_chart
        self.drawing_button_bar.draw_funcs['barh_chart'] = self.draw_barh_chart
        self.drawing_button_bar.draw_funcs['stack_chart'] = self.draw_stack_chart
        self.drawing_button_bar.draw_funcs['scatter_chart'] = self.draw_scatter_chart
        self.drawing_button_bar.draw_funcs['box_chart'] = self.draw_box_chart
        self.drawing_button_bar.draw_funcs['hist_chart'] = self.draw_hist_chart
        self.drawing_button_bar.draw_funcs['radar_chart'] = self.draw_radar_chart
        self.drawing_button_bar.draw_funcs['heap_chart'] = self.draw_heap_chart
        self.drawing_button_bar.draw_funcs['map_chart'] = self.draw_map_chart
        self.drawing_button_bar.draw_funcs['group_chart'] = self.draw_group_before


    def bind_events(self):
        """
        绑定事件。这个将在界面加载完成之后被调用。
        """
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)

    def get_toolbar_text(self) -> str:
        return self.tr('Drawings')

    def on_data_selected(self, data_name: str):
        """
        当变量树中的数据被单击选中时，调用这个方法。
        """
        self.toolbar_block.variable_show_label.setText('%s' % data_name)
        logger.info('Variable clicked. Name is ' + data_name)

    def get_variable(self):
        var_name: str = self.toolbar_block.variable_show_label.text()
        if var_name.isidentifier():
            return get_var(var_name)
        return None

    def prepare_draw_data(self, draw_data):
        """对画图的数据进行检测，如果是2维的int,float数据类型可以进行绘图,
        现在只支持对list,dict,tuple,ndarray,Series,DataFrame数据类型进行绘图"""

        if draw_data is None:
            self.console_message("ERROR: Please select a variable", flag=True)
            return False
        if isinstance(draw_data, (list, tuple)):
            draw_value = np.array(draw_data)
        elif isinstance(draw_data, dict):
            dv = pd.Series(draw_data)
            draw_value = np.array(dv.values)
        elif isinstance(draw_data, (Series, DataFrame)):
            if isinstance(draw_data, DataFrame):
                from widgets import PMGPanelDialog
                dlg = PMGPanelDialog(parent=self, views=[[
                    'combo_ctrl', 'series', '选择系列', '全部', draw_data.select_dtypes(['number']).columns.tolist() + ['全部']]
                ])
                dlg.exec_()
                if dlg.changes_accepted:  # 仅当绘图的变更被接受的时候，才进行绘图。
                    series_name = dlg.get_value()['series']
                    if series_name == '全部':
                        draw_value = np.array(draw_data.values)  # TODO:缺失值是否要删除？如何删除？
                    else:
                        draw_value = draw_data[series_name].dropna()
                else:
                    return False
            else:
                draw_value = np.array(draw_data.values)
        elif isinstance(draw_data, ndarray):
            draw_value = draw_data
        else:  # 如果不是这些类型提示数据类型错误
            self.console_message('ERROR: Data type is wrong!', flag=True)
            return False

        int_float_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        if draw_value.dtype in int_float_types:
            ndim = draw_value.ndim
            if ndim < 3:
                if 0 not in draw_value.shape:
                    return draw_value
            else:
                self.console_message('ERROR: Please select 1D or 2D data', flag=True)
                return False
        else:
            self.console_message('ERROR: Data type is wrong', flag=True)
            return False

    def setup_draw_window(self):
        """初始化绘图窗口"""
        if self.draw_fig is None:
            from packages.pmagg import PMAgg
            self.draw_fig = PMAgg.Window()
        plt.clf()

    def cb1_change(self):
        """绘制提示窗口图形"""
        plt.clf()  # Clear figure
        line_var_name = self.dialog_group.cb_select1.currentText()
        line_var = self.extension_lib.get_var(line_var_name)
        self.line_real_value = self.prepare_draw_data(line_var).flatten()
        if self.line_real_value is not False:
            self.dialog_group.draw_line_widget.get_figure().gca().cla()
            ax_line = self.dialog_group.draw_line_widget.axes
            ax_line.plot(self.line_real_value, color='orange')
            self.dialog_group.draw_line_widget.draw()
        else:
            self.dialog_group.close()

    def cb2_change(self):
        bar_var_name = self.dialog_group.cb_select2.currentText()
        bar_var = self.extension_lib.get_var(bar_var_name)
        self.bar_real_value = self.prepare_draw_data(bar_var).flatten()
        if self.bar_real_value is not False:
            self.dialog_group.draw_bar_widget.get_figure().gca().cla()
            ax_bar = self.dialog_group.draw_bar_widget.axes
            x_axis = [i for i in range(self.bar_real_value.shape[0])]
            ax_bar.bar(x_axis, self.bar_real_value)
            self.dialog_group.draw_bar_widget.draw()
        else:
            self.dialog_group.close()

    def draw_group_before(self):
        """绘制组合图1-显示提示窗口"""
        vars_name_list = self.extension_lib.Data.get_all_variable_names()
        self.dialog_group.cb_select1.clear()
        self.dialog_group.cb_select2.clear()
        if len(vars_name_list) > 9:
            new_vars = vars_name_list[8:]
            self.dialog_group.cb_select1.addItems(new_vars)
            self.dialog_group.cb_select1.setCurrentIndex(0)
            self.dialog_group.cb_select2.addItems(new_vars)
            self.dialog_group.cb_select2.setCurrentIndex(1)
            self.dialog_group.show()
        else:
            self.console_message("ERROR：Can't draw chart with one variable!", flag=True)

    def draw_group_chart(self):
        """绘制组合图2-组合画图"""
        self.setup_draw_window()
        line_var_name = self.dialog_group.cb_select1.currentText()
        bar_var_name = self.dialog_group.cb_select2.currentText()
        if self.bar_real_value.ndim == 2:
            draw_value1 = self.bar_real_value.flatten()
        else:
            draw_value1 = self.bar_real_value
        if self.line_real_value.ndim == 2:
            draw_value2 = self.line_real_value.flatten()
        else:
            draw_value2 = self.line_real_value
        ncols1 = draw_value1.shape[0]
        ncols2 = draw_value2.shape[0]
        if ncols1 > ncols2:
            x_axis = [x for x in range(ncols2)]
            draw_value1 = draw_value1[:ncols2]
        else:
            x_axis = [x for x in range(ncols1)]
            draw_value2 = draw_value2[:ncols1]
        plt.bar(x_axis, draw_value1, zorder=1)
        plt.plot(x_axis, draw_value2, color='orange', zorder=2)
        fig = plt.gcf()
        self.draw_fig.get_canvas(fig)
        self.draw_fig.show()
        self.extension_lib.get_interface('ipython_console').run_command(command="",
                                                                        hint_text='plotting {} and {}'.format(
                                                                            line_var_name, bar_var_name), hidden=False)
        self.dialog_group.close()

    def get_lvl_i(self, data, ncnt=10):
        """数据在分级后在哪一级内'"""
        nid = []
        d_min, d_max = min(data), max(data)
        levels = np.linspace(d_min, d_max, ncnt + 1)
        levels[0] -= 0.1
        levels[-1] += 0.1
        for dt in data:
            nl = np.append(levels, dt)
            nl = pd.Series(nl).sort_values().tolist()
            nid.append((nl.index(dt) - 1) / ncnt)
        return nid

    def draw_china_map(self, map_path, small_map_path, fig, data=None):
        """draw china map"""
        map_json_file = os.path.join(self.drawing_button_bar.current_path, 'map_var.json')
        with open(map_json_file, 'r') as jf:
            mv = json.load(jf)
        map_blocks = mv['map_blocks']
        lvl_n = 10
        new_colors = cm.get_cmap('spring_r', lvl_n)
        if data is not None:
            if data.shape[0] > 35:
                data = data[:34]
                data_num = 34
            else:
                data_num = data.shape[0]
            city_file_name = list(map_blocks.keys())[:data_num]
            city_data = {}
            cid = self.get_lvl_i(data)
            for i, cfn in enumerate(city_file_name):
                city_data[cfn] = new_colors(cid[i])
        else:
            pass
            # print('Data is None')

        ax = fig.add_axes([0.1, 0.1, 0.77, 0.8])
        map_files = os.listdir(map_path)
        for mf in map_files:
            map_polys = np.load(os.path.join(map_path, mf))
            main_file_name = mf.split('.')[0]
            map_block = map_blocks[main_file_name]
            map_block = np.array(map_block).cumsum(axis=0)
            ns = 0
            for mb in map_block:
                nov = mb
                draw_data = map_polys[ns:nov, :].T
                ax.plot(draw_data[0], draw_data[1], color='k', lw=0.5)
                if data is not None:
                    if main_file_name in city_data.keys():
                        ax.fill(draw_data[0], draw_data[1], color=city_data[main_file_name], alpha=0.5)

                ns = nov
        ax.set_xlim(72, 139)
        ax.set_ylim(18, 57)
        ax.set_xticks([80, 100, 120])
        ax.set_yticks([25, 35, 45, 55])
        ax.set_xticklabels(labels=['80$°$E', '100$°$E', '120$°$E'])
        ax.set_yticklabels(labels=['25$°$N', '35$°$N', '45$°$N', '55$°$N'])

        ax_add = fig.add_axes([0.72, 0.1, 0.15, 0.24])
        small_map_files = os.listdir(small_map_path)

        for mf in small_map_files:
            map_polys = np.load(os.path.join(map_path, mf))
            main_file_name = mf.split('.')[0]
            map_block = map_blocks[main_file_name]
            map_block = np.array(map_block).cumsum(axis=0)
            ns = 0
            for mb in map_block:
                nov = mb
                draw_data = map_polys[ns:nov, :].T
                ax_add.plot(draw_data[0], draw_data[1], color='k', lw=0.6)
                ns = nov
        ax_add.set_xlim(107.5, 120.5)
        ax_add.set_ylim(2, 22)
        ax_add.set_xticks([])
        ax_add.set_yticks([])
        d_min, d_max = min(data), max(data)
        levels = np.linspace(d_min, d_max, 11)
        norm_map = colors.BoundaryNorm(levels, 10)
        cax = plt.axes([0.87, 0.1, 0.03, 0.8])
        fcb = colorbar.ColorbarBase(norm=norm_map, cmap=new_colors, ax=cax)
        return plt.gcf()

    def draw_map_chart(self):
        """绘制地图"""
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            if draw_value.ndim == 2:
                draw_value = draw_value.flatten()
            if draw_value.shape[0] > 5:
                var_name = self.toolbar_block.variable_show_label.text()
                map_path = os.path.join(self.drawing_button_bar.current_path, r'pmmap\china\all')
                small_map_path = os.path.join(self.drawing_button_bar.current_path, r'pmmap\china\small')
                fig = plt.figure()
                fig_res = self.draw_china_map(map_path, small_map_path, fig, draw_value)
                self.draw_fig.get_canvas(fig_res)
                self.draw_fig.show()
                self.console_message(var_name)
            else:
                self.console_message("Data length less than 5", flag=True)

    def draw_heap_chart(self):
        """绘制热力图"""
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            if draw_value.ndim == 2:
                var_name = self.toolbar_block.variable_show_label.text()
                plt.imshow(draw_value)
                fig = plt.gcf()
                self.draw_fig.get_canvas(fig)
                self.draw_fig.show()
                self.console_message(var_name)
            else:
                self.console_message('ERROR: Heap chart need 2D data', flag=True)

    def draw_radar_chart(self):
        """绘制雷达图"""
        draw_value = self.prepare_draw_data(self.get_variable())
        plt.clf()  # Clear figure
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            if (draw_value.ndim == 2 and draw_value.shape[0] == 1) or draw_value.ndim == 1:
                draw_value = draw_value.flatten()
            ncols = draw_value.shape[draw_value.ndim - 1]
            if ncols <= 2:
                self.console_message("ERROR: Can't draw with little data", flag=True)
                return False
            else:
                x_axis = [x + 1 for x in range(ncols)]
                angles = radar_factory(ncols, frame='polygon')
                angles = np.concatenate((angles, [angles[0]]))
                x_axis = np.concatenate((x_axis, [x_axis[0]]))
                fig, ax = plt.subplots(1, 1, subplot_kw=dict(projection='radar'))
                if draw_value.ndim == 1:
                    draw_value = np.concatenate((draw_value, [draw_value[0]]))
                    ax.plot(angles, draw_value, marker="o")
                    ax.fill(angles, draw_value, alpha=0.2)
                else:
                    for dv in draw_value:
                        draw_val = np.concatenate((dv, [dv[0]]))
                        ax.plot(angles, draw_val, marker="o")
                        ax.fill(angles, draw_val, alpha=0.2)
                ax.set_xticks(angles)
                ax.set_xticklabels(x_axis)
                yticks = ax.get_yticks()
                grids = [[i] * (ncols + 1) for i in yticks[:-1]]
                for gd in grids:
                    ax.plot(angles, gd, linestyle='--', color='grey', linewidth=0.5)
                ax.grid(axis='y')
                fig = plt.gcf()
                self.draw_fig.get_canvas(fig)
                self.draw_fig.show()
                self.console_message(var_name)

    def draw_hist_chart(self):
        """绘制直方图"""
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            if draw_value.ndim == 2:
                draw_value = draw_value.flatten()
            var_name = self.toolbar_block.variable_show_label.text()
            plt.hist(draw_value)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_box_chart(self):
        """ 绘制箱线图"""
        plt.clf()  # Clear figure
        draw_value = self.prepare_draw_data(self.get_variable())
        print('draw_value', draw_value, type(draw_value))
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            plt.boxplot(draw_value, widths=0.25)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_scatter_chart(self):
        """绘制散点图"""
        plt.clf()  # Clear figure
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            if (draw_value.ndim == 2 and draw_value.shape[0] == 1) or draw_value.ndim == 1:
                draw_value = draw_value.flatten()
                ncols = draw_value.shape[0]
                x_axis = [x for x in range(ncols)]
                plt.scatter(x_axis, draw_value)
            elif draw_value.ndim == 2:
                if draw_value.shape[0] == 2:
                    draw_x = draw_value[0]
                    draw_y = draw_value[1]
                    plt.scatter(draw_x, draw_y)
                elif draw_value.shape[0] == 3:
                    draw_x = draw_value[0]
                    draw_y = draw_value[1]
                    draw_s = draw_value[2] * (25 / draw_value[2].min())
                    plt.scatter(draw_x, draw_y, s=draw_s)
                elif draw_value.shape[0] >= 4:
                    draw_x = draw_value[0]
                    draw_y = draw_value[1]
                    draw_s = draw_value[2] * (25 / draw_value[2].min())
                    draw_c = draw_value[3]
                    plt.scatter(draw_x, draw_y, s=draw_s, c=draw_c)
                    if draw_value.shape[0] > 4:
                        var_name = var_name + '[:4]'
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_stack_chart(self):
        """绘制面积图"""
        plt.clf()  # Clear figure
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            ncols = draw_value.shape[draw_value.ndim - 1]
            x_axis = [x for x in range(ncols)]
            var_name = self.toolbar_block.variable_show_label.text()
            plt.stackplot(x_axis, draw_value)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_pie_chart(self):
        """绘制饼图"""
        plt.clf()  # Clear figure
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            lbl = []
            var_name = self.toolbar_block.variable_show_label.text()
            if draw_value.ndim == 2:
                draw_value = draw_value.flatten()
            if draw_value.shape[0] > 9:
                dv_sort = np.argsort(draw_value)
                dv_shp = draw_value.shape[0]
                others_num = dv_shp - 8
                others_data = draw_value[dv_sort[:others_num]]
                others_sum = others_data.sum()
                dv_new = np.delete(draw_value, dv_sort[:others_num], axis=0)
                dv_new = np.append(dv_new, others_sum)
                for i in range(8):
                    lbl.append(str(i + 1))
                lbl.append('others')
                plt.pie(dv_new, autopct="%3.1f%%", labels=lbl)
            else:
                for i in range(draw_value.shape[0]):
                    lbl.append(str(i + 1))
                plt.pie(draw_value, autopct="%3.1f%%", labels=lbl)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_bar_chart(self):
        """绘制柱状图"""
        plt.clf()  # Clear figure
        bar_width = 0.6
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            if (draw_value.ndim == 2 and draw_value.shape[0] == 1) or draw_value.ndim == 1:
                draw_value = draw_value.flatten()
                ncols = draw_value.shape[0]
                x_axis = [x for x in range(ncols)]
                plt.bar(x_axis, draw_value, width=bar_width)
                plt.xticks(x_axis)
            if draw_value.ndim == 2 and 1 < draw_value.shape[0] < 6:
                bar_start = bar_width / 2
                ncols = draw_value.shape[1]
                bar_step = bar_width / draw_value.shape[0]
                x_lbl = [x for x in range(ncols)]
                x_axis = np.array([x for x in range(ncols)]) - bar_start
                for bar_n in range(draw_value.shape[0]):
                    plt.bar(x_axis, draw_value[bar_n], width=bar_step, align='edge')
                    x_axis = x_axis + bar_step
                plt.xticks(x_lbl)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_barh_chart(self):
        """绘制条形图"""
        bar_width = 0.6
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            if (draw_value.ndim == 2 and draw_value.shape[0] == 1) or draw_value.ndim == 1:
                draw_value = draw_value.flatten()
                ncols = draw_value.shape[0]
                x_axis = [x for x in range(ncols)]
                plt.barh(x_axis, draw_value, height=bar_width)
                plt.yticks(x_axis)
            if draw_value.ndim == 2 and 1 < draw_value.shape[0] < 6:
                bar_start = bar_width / 2
                ncols = draw_value.shape[1]
                bar_step = bar_width / draw_value.shape[0]
                x_lbl = [x for x in range(ncols)]
                x_axis = np.array([x for x in range(ncols)]) - bar_start
                for bar_n in range(draw_value.shape[0]):
                    plt.barh(x_axis, draw_value[bar_n], height=bar_step, align='edge')
                    x_axis = x_axis + bar_step
                plt.yticks(x_lbl)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def draw_line_chart(self):
        """
        绘制折线图
        """
        plt.clf()  # Clear figure
        draw_value = self.prepare_draw_data(self.get_variable())
        if draw_value is not False:
            self.setup_draw_window()
            var_name = self.toolbar_block.variable_show_label.text()
            plt.plot(draw_value)
            fig = plt.gcf()
            self.draw_fig.get_canvas(fig)
            self.draw_fig.show()
            self.console_message(var_name)

    def console_message(self, var_name: str, flag=False):
        mess = ''
        if flag:
            mess = var_name
        else:
            mess = f'plotting {var_name}'
        self.extension_lib.get_interface('ipython_console').run_command(command='',
                                                                        hint_text=mess, hidden=False)

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
        w: 'widgets.TopLevelWidget' = self._control_widget_dic['drawing_selection_panel']
        w.setVisible(not w.isVisible())

    def refresh_pos(self):
        """
        刷新顶上的ToplevelWidget的位置。
        """
        return
        btn = self.get_control_widget('button_show_more_plots')
        panel: 'widgets.TopLevelWidget' = self.get_control_widget(
            'drawing_selection_panel')
        width = self.get_control_widget('button_list').width()
        panel.set_width(width)
        panel.set_position(QPoint(btn.x() - width, btn.y()))

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

    def insert_after(self) -> str:
        return 'code_editor_toolbar'


class Extension(BaseExtension):
    if TYPE_CHECKING:
        interface: 'DrawingsInterface' = None
        widget: 'PMDrawingsToolBar' = None
        extension_lib: 'extension_lib' = None

    def on_loading(self):
        pass

    def on_load(self):
        drawings_toolbar: 'PMDrawingsToolBar' = self.widgets['PMDrawingsToolBar']
        drawings_toolbar.extension_lib = self.extension_lib
        self.drawings_toolbar = drawings_toolbar
        self.interface.drawing_item_double_clicked_signal = drawings_toolbar.drawing_item_double_clicked_signal

        self.interface.drawing_item_double_clicked_signal.connect(self.interface.on_clicked)
        self.interface.drawings_toolbar = drawings_toolbar

        self.extension_lib.Data.add_data_changed_callback(drawings_toolbar.on_data_modified)
        self.extension_lib.Signal.get_widgets_ready_signal().connect(self.bind_events)

    def bind_events(self):
        workspace_interface = self.extension_lib.get_interface('workspace_inspector')
        workspace_interface.add_select_data_callback(self.drawings_toolbar.on_data_selected)


class DrawingsInterface(BaseInterface):
    drawing_item_double_clicked_signal: 'Signal' = None
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
    # win1 = PMMenuToolPanel()
    win1 = PMDrawingsToolBar()
    win1.show()
    a = [1, 2, 3, 4]

    sys.exit(app.exec_())
