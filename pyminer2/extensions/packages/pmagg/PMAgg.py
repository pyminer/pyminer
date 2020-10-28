# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 10:29
# @Author  : 别着急慢慢来
# @FileName: PMAgg.py


import os
import io
import pickle
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QCursor, QImage
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from ui.pmagg_ui import Ui_MainWindow
from ui.axes_control_manager import Ui_Form_Manager
from ui import linestyle_manager, legend_setting, rectangle_setting, ellipse_setting, colorbar_setting, text_setting, \
    axis_setting
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Arrow
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy, QMenu, QApplication, QHBoxLayout, QFormLayout
from matplotlib.lines import Line2D
from matplotlib.text import Annotation, Text
from matplotlib.legend import Legend
from matplotlib.font_manager import FontProperties
from ui.value_inputs import SettingsPanel
import mpl_toolkits.mplot3d as mpl3d
from ui.linestyles import *
from matplotlib.colors import to_hex, to_rgb, to_rgba
import matplotlib.font_manager
from matplotlib import rcParams
from pathlib import Path
import configparser
import re
from functools import partial
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.axis import Axis
from matplotlib.axes import Axes
import copy
from matplotlib import rcParams

"""
前提，将该文件所在文件夹注册到path环境变量
1. 永久添加
2. 临时添加
import os
import sys
current_path=os.getcwd()
sys.path.append(current_path)
最好永久添加，这样脚本和控制台都能用


使用时，先申明
import matplotlib
matplotlib.use('module://pmagg')

然后就可以
plt.plot([1,2,3],[4,5,6])
plt.show()


Window类功能需求
1. 拖拽窗口，绘图区始终处于窗口中心，且窗口大小改变时，绘图区能跟着扩展
2. 实现对绘图区坐标轴，图例，标题，文字等各类信息的修改和添加
3. 实现绘图区参数的保存，方便下次调用
4. 实现图片保存
5. 模仿matlab实现更多的功能

Extension 使用时被加载
"""


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    重写修改该类即可实现自定义后端界面，相加什么按钮可以随便加，目前还只是个demo

    self.canvas.draw() 每执行该函数，图形重绘
    """

    def __init__(self, config_path: str):
        super(Window, self).__init__()
        self.setupUi(self)  # 先执行父类方法，以产生成员变量
        self.retranslateUi(self)

        self.current_path = os.path.dirname(__file__)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.current_path, 'icons/Icon.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # 翻译家
        self.trans = QtCore.QTranslator()
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        assert os.path.exists(self.config_path)
        self.config.read(self.config_path, encoding='utf-8-sig')
        # 工具栏设置

        self.saveAction = QAction(QIcon(os.path.join(self.current_path, 'icons/save.png')), 'save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.save_slot)
        self.toolBar.addAction(self.saveAction)

        self.settingAction = QAction(QIcon(os.path.join(self.current_path, 'icons/setting.png')), 'setting', self)
        self.settingAction.triggered.connect(self.axes_control_slot)
        self.toolBar.addAction(self.settingAction)

        self.spaceAction = QAction(QIcon(os.path.join(self.current_path, 'icons/space.png')), 'space', self)
        self.spaceAction.setShortcut('Ctrl+H')
        self.spaceAction.triggered.connect(self.space_slot)
        self.toolBar.addAction(self.spaceAction)

        self.homeAction = QAction(QIcon(os.path.join(self.current_path, 'icons/home.png')), 'home', self)
        self.homeAction.setShortcut('Ctrl+H')
        self.homeAction.triggered.connect(self.home_slot)
        self.toolBar.addAction(self.homeAction)

        self.backAction = QAction(QIcon(os.path.join(self.current_path, 'icons/back.png')), 'back', self)
        self.backAction.triggered.connect(self.back_slot)
        self.toolBar.addAction(self.backAction)

        self.frontAction = QAction(QIcon(os.path.join(self.current_path, 'icons/front.png')), 'front', self)
        self.frontAction.triggered.connect(self.front_slot)
        self.toolBar.addAction(self.frontAction)

        self.zoomAction = QAction(QIcon(os.path.join(self.current_path, 'icons/zoom.png')), 'zoom', self)
        self.zoomAction.triggered.connect(self.zoom_slot)
        self.toolBar.addAction(self.zoomAction)

        self.panAction = QAction(QIcon(os.path.join(self.current_path, 'icons/pan.png')), '平移', self)
        self.panAction.triggered.connect(self.pan_slot)
        self.toolBar.addAction(self.panAction)

        self.rotateAction = QAction(QIcon(os.path.join(self.current_path, 'icons/rotate.png')), 'rotate', self)
        self.rotateAction.triggered.connect(self.rotate_slot)
        self.toolBar.addAction(self.rotateAction)

        self.gridAction = QAction(QIcon(os.path.join(self.current_path, 'icons/grid.png')), '显示/隐藏网格', self)
        self.gridAction.triggered.connect(self.show_grid_slot)
        self.toolBar.addAction(self.gridAction)

        self.legendAction = QAction(QIcon(os.path.join(self.current_path, 'icons/legend.png')), '显示/隐藏图例', self)
        self.legendAction.triggered.connect(self.legend_slot)
        self.toolBar.addAction(self.legendAction)

        self.colorbarAction = QAction(QIcon(os.path.join(self.current_path, 'icons/colorbar.png')), '显示/隐藏colorbar',
                                      self)
        self.colorbarAction.triggered.connect(self.show_colorbar_slot)
        self.toolBar.addAction(self.colorbarAction)

        # 文件菜单栏设置
        self.action_save_image.triggered.connect(self.save_slot)
        self.action_save_figure.triggered.connect(self.save_figure_slot)
        self.action_load_figure.triggered.connect(self.load_figure_slot)
        self.action_close.triggered.connect(self.close)

        # 编辑菜单栏设置
        self.action_copy_figure_to_clipboard.triggered.connect(self.copy_figure_to_clipboard_slot)

        # 注释菜单栏设置
        self.action_rectangle.triggered.connect(self.rect_slot)
        self.action_text.triggered.connect(self.text_slot)
        self.action_oval.triggered.connect(self.oval_slot)
        self.action_annotation.triggered.connect(self.annotation_slot)

        # 视图菜单栏设置
        self.action_main_view.triggered.connect(partial(self.change_view_slot, azim=0, elev=0))
        self.action_left_view.triggered.connect(partial(self.change_view_slot, azim=90, elev=0))
        self.action_right_view.triggered.connect(partial(self.change_view_slot, azim=-90, elev=0))
        self.action_bottom_view.triggered.connect(partial(self.change_view_slot, azim=0, elev=90))
        self.action_top_view.triggered.connect(partial(self.change_view_slot, azim=0, elev=-90))
        self.action_back_view.triggered.connect(partial(self.change_view_slot, azim=180, elev=0))
        self.action45_45_view.triggered.connect(partial(self.change_view_slot, azim=45, elev=45))
        self.action45_m45_view.triggered.connect(partial(self.change_view_slot, azim=45, elev=-45))
        self.action_m45_45_view.triggered.connect(partial(self.change_view_slot, azim=-45, elev=45))
        self.action_m45_m45_view.triggered.connect(partial(self.change_view_slot, azim=-45, elev=-45))

        # set page widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_slot)
        self.tabWidget.currentChanged.connect(self.switch_tab_slot)

        # 多语言切换
        self.action_zh_cn.triggered.connect(self._trigger_zh_cn)
        self.action_english.triggered.connect(self._trigger_english)

        # 提示label 放在statusbar中，显示矩形或点的坐标等
        self.label = QtWidgets.QLabel()
        self.statusbar.addWidget(self.label)

        # 所有的标志
        self.add_rect_flag = False
        self.add_oval_flag = False
        self.add_text_flag = False
        self.rotate_flag = False
        self.home_flag = False
        self.pan_flag = False
        self.zoom_flag = False
        self.add_style_flag = False
        self.show_grid_flag = False
        self.show_legend_flag = False
        self.add_annotation_flag = False
        # 当前的artist对象
        self.current_artist = None
        # 这里面装着可以被home去除的组件
        self.can_remove_elements = []
        self.current_subplot = None
        self.pick = False
        # 这个button的出现是因为在添加文字时，明明鼠标移动时，没有按下按钮，但是mpl识别出按下了按钮，所以另外做一个标志
        self.button = 0
        self.canvases = []
        self.canvas = None
        # page 页
        self.tab_page_title_index = 1
        self.toolBar.setStyleSheet("padding-left:2px;")

    def init_figure(self):
        self.set_subplots()
        # 所有的按钮标志
        self.make_flag_invalid()
        self.read_all_settings()
        self.set_pickers()
        self.set_all_fonts()
        self.set_mpl_events()
        self.set_gui_language()

    def set_gui_language(self):
        if self.current_language == 'en':
            self._trigger_english()
        if self.current_language == 'zh_CN':
            self._trigger_zh_cn()

    def _trigger_english(self):
        """切换英语，并且写入配置文件"""
        self.current_language = 'en'
        en_qm = os.path.join(self.current_path, 'langs/en_pmagg_ui.qm')
        self.trans.load(en_qm)
        _app = QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)  # 重新翻译主界面
        self.retranslateUi(self)
        self.set_config('language', 'current_language', 'en')
        with open(self.config_path, "w+", encoding='utf-8') as f:
            self.config.write(f)

    def _trigger_zh_cn(self):
        self.current_language = 'zh_CN'
        zh_qm = os.path.join(self.current_path, 'langs/zh_CN_pmagg_ui.qm')
        self.trans.load(zh_qm)
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.set_config('language', 'current_language', 'zh_CN')
        with open(self.config_path, "w+", encoding='utf-8') as f:
            self.config.write(f)

    def set_subplots(self):
        """给子图combobox和菜单栏中的子图menu设置项"""
        # 获取子图对象
        self.axes = self.canvas.figure.get_axes()
        if not self.axes:
            QtWidgets.QMessageBox.warning(
                self.canvas.parent(), "Error", "There are no axes to edit.")
            return
        elif len(self.axes) == 1:
            self.current_subplot, = self.axes
            titles = ['子图1']
        else:
            titles = ['子图' + str(i + 1) for i in range(len(self.axes))]
            self.current_subplot = self.axes[0]
        # 将三维图的初始视角保存下来，便于旋转之后可以复原
        self.init_views = [(index, item.azim, item.elev) for index, item in enumerate(self.axes) if
                           hasattr(item, 'azim')]
        self.menu.clear()
        actions = []
        for index, title in enumerate(titles):
            action = QtWidgets.QAction(self)
            action.setObjectName('action_subplot_' + str(index))
            action.setText(title)
            action.setCheckable(True)
            action.triggered.connect(partial(self.menu_subplots_slot, index))
            actions.append(action)
        self.menu.addActions(actions)
        self.menu.actions()[0].setChecked(True)

    def set_mpl_events(self):
        # 鼠标拖拽，实现三维图形旋转功能
        self.canvas.mpl_connect('motion_notify_event', self.on_rotate)

        # 为图例绑定监听事件
        self.canvas.mpl_connect('axes_enter_event', self.drag_legend)
        self.canvas.mpl_connect('axes_leave_event', self.drag_legend)
        # 为右键功能集成
        self.canvas.mpl_connect('pick_event', self.right_button_menu)

    def get_canvas(self, figure):
        if self.canvas:
            old_canvas = self.canvas
        self.canvas = FigureCanvas(figure)  # 这里的canvas就是曲线图
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()  # 隐藏QT原来的工具栏
        self.toolbar.mode = None  # 禁用移动和缩放
        self.init_figure()  # 先初始化图形，设置项等
        if self.canvas.figure._suptitle:
            tab_page_title = self.canvas.figure._suptitle.get_text()
        else:
            tab_page_title = 'figure ' + str(self.tab_page_title_index)
        if self.draw_tab == 'new':
            tab_widget_page = QtWidgets.QWidget()
            grid_layout = QtWidgets.QGridLayout(tab_widget_page)
            self.canvases.append(self.canvas)
            self.tabWidget.addTab(tab_widget_page, tab_page_title)
            grid_layout.addWidget(self.canvas)
            grid_layout.removeWidget(self.canvas)
            grid_layout.addWidget(self.canvas)
            self.tab_page_title_index += 1
            self.tabWidget.setCurrentWidget(tab_widget_page)
        if self.draw_tab == 'cover':
            if self.tabWidget.count() == 0:  # 还未产生tab页
                tab_widget_page = QtWidgets.QWidget()
                grid_layout = QtWidgets.QGridLayout(tab_widget_page)
                self.canvases.append(self.canvas)
                self.tabWidget.addTab(tab_widget_page, tab_page_title)
                grid_layout.addWidget(self.canvas)
                self.tab_page_title_index += 1
            else:
                self.canvases[self.tabWidget.currentIndex()] = self.canvas  # 更改当前页的canvas
                self.tabWidget.currentWidget().layout().removeWidget(old_canvas)
                self.tabWidget.currentWidget().layout().addWidget(self.canvas)

    def close_tab_slot(self, index):
        self.tabWidget.removeTab(index)
        self.canvases.pop(index)

    def switch_tab_slot(self, index):
        """切换tab页之后，无需重新读取setting，因为所有的setting都是通用的"""
        if self.tabWidget.count() != 0:
            self.canvas = self.canvases[index]
            self.set_subplots()

    def select_font(self, text: Text):
        content = text.get_text()
        zh_model = re.compile(u'[\u4e00-\u9fa5]')
        en_model = re.compile(u'[a-z]')
        zh = zh_model.search(content)
        en = en_model.search(content)
        if zh and en and self.mix_font != 'None' and os.path.exists(self.mix_font_path):
            text.set_fontproperties(Path(self.mix_font_path))
            return text
        if zh and not en and self.local_font != 'None' and os.path.exists(self.local_font_path):
            text.set_fontproperties(Path(self.local_font_path))
            return text
        if not zh and self.english_font != 'None' and os.path.exists(self.english_font_path):
            text.set_fontproperties(Path(self.english_font_path))
            return text
        return text

    def get_config(self, section, option, value=None):
        if not self.config.has_section(section):
            self.config.add_section(section)
        if not self.config.has_option(section, option):
            self.config.set(section, option, value=str(value))
        return self.config.get(section, option)

    def set_config(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        return self.config.set(section, option, value=str(value))

    def read_all_settings(self):
        self.local_font = self.get_config('font', 'local_font')
        self.english_font = self.get_config('font', 'english_font')
        self.mix_font = self.get_config('font', 'mix_font')
        self.english_font_path = self.get_config('font', 'english_font_path')
        self.local_font_path = self.get_config('font', 'local_font_path')
        self.mix_font_path = self.get_config('font', 'mix_font_path')
        # annotation
        self.an_axis_style = self.get_config('annotation', 'axis_style', '({:.2f},{:.2f})')
        self.an_bg_color = self.get_config('annotation', 'bg_color', 'white')
        self.an_border_color = self.get_config('annotation', 'border_color', 'blue')
        self.an_border = self.get_config('annotation', 'border', '1')
        self.an_bg_color = self.get_config('annotation', 'bg_color', 'white')
        self.an_offset = self.get_config('annotation', 'offset', '(-5,5)')
        self.an_arrow_width = self.get_config('annotation', 'arrow_width', '1')
        self.an_arrow_color = self.get_config('annotation', 'arrow_color', 'black')
        self.an_arrow_shape = self.get_config('annotation', 'arrow_shape', '->')
        self.an_text_size = self.get_config('annotation', 'text_size', '')
        self.an_text_color = self.get_config('annotation', 'text_color', 'black')
        self.an_show_point = self.get_config('annotation', 'show_point', 'True')
        self.an_show_text = self.get_config('annotation', 'show_text', 'True')
        self.an_show_arrow = self.get_config('annotation', 'show_arrow', 'False')
        # grid
        self.grid_axis = self.get_config('grid', 'axis', 'both')
        self.grid_color = self.get_config('grid', 'color', 'gray')
        self.grid_which = self.get_config('grid', 'which', 'major')
        self.grid_linestyle = self.get_config('grid', 'linestyle', '-')
        self.grid_linewidth = self.get_config('grid', 'linewidth', '1')
        # 选择绘图方式
        self.draw_tab = self.get_config('draw', 'tab', 'new')
        self.draw_width = self.get_config('draw', 'width', self.canvas.figure.get_figwidth())
        self.draw_height = self.get_config('draw', 'height', self.canvas.figure.get_figheight())
        self.draw_dpi = self.get_config('draw', 'dpi', self.canvas.figure.get_dpi())
        self.draw_style = self.get_config('draw', 'style', 'None')
        # 选择语言
        self.current_language = self.get_config('language', 'current_language', 'en')
        # 上次打开的路径
        self.last_path = self.get_config('path', 'last_path', os.path.expanduser('~'))
        if not os.path.exists(self.last_path):
            self.last_path = os.path.expanduser('~')
            self.set_config('path', 'last_path', self.last_path)

    def set_pickers(self, flag=True):
        """将所有的对象都设置成可pick的对象，使能被事件响应，这里有一个特别大的陷阱，如果存在可picker的对象，那么figure将无法pickle！！"""
        for ax in self.axes:
            for line in ax.lines:
                line.set_picker(flag)
            for patch in ax.patches:
                patch.set_picker(flag)
            for text in ax.texts:
                text.set_picker(flag)
            legend = ax.get_legend()
            ax.set_picker(flag)
            if legend:
                legend.set_picker(flag)

    def set_all_fonts(self):
        if self.canvas.figure._suptitle:
            self.select_font(self.canvas.figure._suptitle)
        for ax in self.axes:
            for text in ax.texts:
                self.select_font(text)
            for label in ax.get_xticklabels():  # make the xtick labels pickable
                self.select_font(label)
            for label in ax.get_yticklabels():  # make the ytick labels pickable
                self.select_font(label)
            self.select_font(ax.title)
            self.select_font(ax.xaxis.label)
            self.select_font(ax.yaxis.label)
            if hasattr(ax, 'zaxis'):
                self.select_font(ax.zaxis.label)
            legend = ax.get_legend()
            if legend:
                for text in legend.texts:
                    self.select_font(text)
            if hasattr(ax, 'get_zticklabels()'):
                for label in ax.get_zticklabels():
                    self.select_font(label)

    def set_figure(self):
        self.canvas.figure.set_figwidth(float(self.draw_width))
        self.canvas.figure.set_figheight(float(self.draw_height))
        self.canvas.figure.set_dpi(float(self.draw_dpi))

    def make_flag_invalid(self):
        self.add_rect_flag = False
        self.add_oval_flag = False
        self.add_text_flag = False
        self.rotate_flag = False
        self.home_flag = False
        self.pan_flag = False
        self.zoom_flag = False
        self.add_style_flag = False
        self.show_grid_flag = False
        self.show_legend_flag = False
        self.add_annotation_flag = False
        # 禁用移动和缩放
        self.toolbar.mode = None
        self.space_flag = False
        self.legend_draggable_flag = False

    def menu_annotation_selected(self, menu_action: QAction):
        """将当前的menu选中，其余关闭"""
        for menu in self.menu_annotation.actions():
            if menu != menu_action:
                menu.setChecked(False)

    def copy_figure_to_clipboard_slot(self):
        with io.BytesIO() as buffer:
            self.canvas.figure.savefig(buffer)
            QApplication.clipboard().setImage(QImage.fromData(buffer.getvalue()))

    def home_slot(self):
        """matplotlib lines里面放曲线，patches可以放图形，artists也可以放东西，设为空则可以删除对应的对象"""
        if not self.home_flag:
            return
        # 运行QT5Agg原来的home，实现平移的复位
        self.toolbar.home()
        # 将三维图视角还原
        for item in self.init_views:
            self.axes[item[0]].view_init(azim=item[1], elev=item[2])
        # 将can_remove_elements中的对应的元素全部删除
        for item in self.axes:
            # print(self.can_remove_elements)
            for i in self.can_remove_elements:
                if i in item.texts:
                    item.texts.remove(i)
                if i in item.artists:
                    item.artists.remove(i)
                if i in item.patches:
                    item.patches.remove(i)
                if i in item.lines:
                    item.lines.remove(i)
        self.canvas.draw()

    def space_slot(self):
        self.toolbar.configure_subplots()

    def zoom_slot(self):
        self.make_flag_invalid()
        self.zoom_flag = not self.zoom_flag
        self.zoom()

    def zoom(self):
        if not self.zoom_flag:
            return
        self.toolbar.zoom()

    def pan_slot(self):
        self.make_flag_invalid()
        self.pan_flag = not self.pan_flag
        self.pan()

    def pan(self):
        if not self.pan_flag:
            return
        self.toolbar.pan()

    def save_slot(self):
        """
        在按默认参数保存图片后，将图片大小重新调整到窗口实际大小。
        """
        width = self.canvas.figure.get_figwidth()
        height = self.canvas.figure.get_figheight()
        dpi = self.canvas.figure.get_dpi()
        self.set_figure()
        self.toolbar.save_figure()
        self.canvas.figure.set_figwidth(width)
        self.canvas.figure.set_figheight(height)
        self.canvas.figure.set_dpi(dpi)
        self.canvas.draw_idle()

    def save_figure_slot(self):
        """保存figure的pickle对象到文件，一定要先关闭picker"""
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save figure object', self.last_path,
                                                              filter="Pickle object (*.pickle)")
        if file_name != '':
            if file_name.split('.')[-1] != 'pickle':  # 添加后缀
                file_name = file_name + '.pickle'
            with open(file_name, 'wb') as f:
                self.set_pickers(flag=False)
                pickle.dump(self.canvas.figure, f)
            self.set_pickers(True)
        dir_name = os.path.dirname(file_name)
        self.last_path = dir_name
        self.set_config('path', 'last_path', self.last_path)

    def load_figure_slot(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open figure object', self.last_path,
                                                     filter='Pickle object (*.pickle)')
        if os.path.exists(name[0]):
            with open(name[0], 'rb') as f:
                self.get_canvas(pickle.load(f))
        dir_name = os.path.dirname(name[0])
        self.last_path = dir_name
        self.set_config('path', 'last_path', self.last_path)

    def front_slot(self):
        self.toolbar._nav_stack.forward()
        self.toolbar._update_view()

    def back_slot(self):
        self.toolbar._nav_stack.back()
        self.toolbar._update_view()

    def rotate_slot(self):
        self.make_flag_invalid()
        self.rotate_flag = not self.rotate_flag

    def on_rotate(self, event):
        """
        通过观察发现，旋转时产生的xdata,ydata是以图像中心为原点，正负0.1范围内的数值
        """
        if not self.rotate_flag:
            return
        # 如果鼠标移动过程有按下，视为拖拽，判断当前子图是否有azim属性来判断当前是否3D
        if event.button and hasattr(event.inaxes, 'azim'):
            for item in self.init_views:
                if self.axes[item[0]] == event.inaxes:
                    delta_azim = -180 * event.xdata / 0.1
                    delta_elev = -180 * event.ydata / 0.1
                    azim = delta_azim + item[1]
                    elev = delta_elev + item[2]
                    event.inaxes.view_init(azim=azim, elev=elev)
                    self.canvas.draw()

    def rect_slot(self):
        self.current_artist = None
        self.make_flag_invalid()
        self.menu_annotation_selected(self.action_rectangle)
        self.canvas.mpl_connect('button_press_event', self.rect_event)
        self.canvas.mpl_connect('motion_notify_event', self.rect_event)
        self.canvas.mpl_connect('button_release_event', self.rect_event)
        self.canvas.mpl_connect('pick_event', self.rect_event)

    def rect_event(self, event):
        if not self.action_rectangle.isChecked():
            self.canvas.mpl_disconnect(self.rect_event)
            self.canvas.mpl_disconnect(self.rect_event)
            self.canvas.mpl_disconnect(self.rect_event)
            self.canvas.mpl_disconnect(self.rect_event)
            return
        if event.name == 'pick_event' and event.mouseevent.button == 1 and isinstance(event.artist, Rectangle):
            """点击到对象，先将该对象移除，并保存背景"""
            if self.current_artist is None or (self.current_artist and self.current_artist == event.artist):
                """确保始终只会点击到一个对象"""
                self.pick = True
                if event.artist in self.can_remove_elements:
                    self.current_artist = self.can_remove_elements[self.can_remove_elements.index(event.artist)]
                else:
                    self.current_artist = event.artist
                    self.can_remove_elements.append(self.current_artist)
                event.mouseevent.inaxes.artists.remove(event.artist)
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(event.mouseevent.inaxes.bbox)
        if isinstance(event, matplotlib.backend_bases.MouseEvent):
            if event.inaxes and event.button == 1 and not hasattr(event.inaxes, 'azim'):
                if event.name == 'button_press_event' and not self.pick and not self.current_artist:
                    """判断为按下鼠标事件，并且是在子图区域内，并且鼠标为左键，并且当前pick标志为True，因为pick和press会同时触发，所以
                    先用pick标志让其pick事件先做判断。
                    """
                    self.event_init = event
                    self.current_artist = Rectangle((self.event_init.xdata, self.event_init.ydata), 0, 0, fill=False,
                                                    edgecolor='red', linewidth=3, picker=True)
                    event.inaxes.add_artist(self.current_artist)  # 这里不能使用event.inaxes.patches.append方法
                    self.current_artist.set_animated(True)
                    self.can_remove_elements.append(self.current_artist)
                    self.background = self.canvas.copy_from_bbox(event.inaxes.bbox)
                    event.inaxes.draw_artist(self.current_artist)
                    self.canvas.blit(event.inaxes.bbox)
                if event.name == 'motion_notify_event' and isinstance(self.current_artist, Rectangle):
                    """pick为False表示改变形状，为True改变位置"""
                    if not self.pick:
                        width = event.xdata - self.event_init.xdata
                        height = event.ydata - self.event_init.ydata
                        center = (self.event_init.xdata + width / 2, self.event_init.ydata + height / 2)
                        self.current_artist.set_width(width)
                        self.current_artist.set_height(height)
                    else:
                        width = self.current_artist.get_width()
                        height = self.current_artist.get_height()
                        center = (event.xdata + width / 2, event.ydata + height / 2)
                        self.current_artist.set_xy((event.xdata, event.ydata))
                    self.label.setText('Rect Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % (
                        center[0], center[1], np.abs(width), np.abs(height), np.abs(width * height)))
                    self.canvas.restore_region(self.background)
                    event.inaxes.draw_artist(self.current_artist)
                    self.canvas.blit(event.inaxes.bbox)
            if event.name == 'button_release_event' and isinstance(self.current_artist, Rectangle):
                """鼠标放开，将current_artist重新添加到canvas，并且令动画效果为False"""
                self.current_artist.set_animated(False)
                event.inaxes.artists.append(self.current_artist)
                self.canvas.draw_idle()
                self.label.setText('')
                self.current_artist = None
                self.pick = False

    def oval_slot(self):
        self.current_artist = None
        self.make_flag_invalid()
        self.menu_annotation_selected(self.action_oval)
        self.canvas.mpl_connect('button_press_event', self.oval_event)
        self.canvas.mpl_connect('motion_notify_event', self.oval_event)
        self.canvas.mpl_connect('button_release_event', self.oval_event)
        self.canvas.mpl_connect('pick_event', self.oval_event)

    def oval_event(self, event):
        if not self.action_oval.isChecked():
            self.canvas.mpl_disconnect(self.oval_event)
            self.canvas.mpl_disconnect(self.oval_event)
            self.canvas.mpl_disconnect(self.oval_event)
            self.canvas.mpl_disconnect(self.oval_event)
            return
        if event.name == 'pick_event' and event.mouseevent.button == 1 and isinstance(event.artist, Ellipse):
            """点击到对象，先将该对象移除，并保存背景"""
            if self.current_artist is None or (self.current_artist and self.current_artist == event.artist):
                """确保始终只会点击到一个对象"""
                self.pick = True
                if event.artist in self.can_remove_elements:
                    self.current_artist = self.can_remove_elements[self.can_remove_elements.index(event.artist)]
                else:
                    self.current_artist = event.artist
                    self.can_remove_elements.append(self.current_artist)
                event.mouseevent.inaxes.artists.remove(event.artist)
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(event.mouseevent.inaxes.bbox)
        if isinstance(event, matplotlib.backend_bases.MouseEvent):
            if event.inaxes and event.button == 1 and not hasattr(event.inaxes, 'azim'):
                if event.name == 'button_press_event' and not self.pick and not self.current_artist:
                    """判断为按下鼠标事件，并且是在子图区域内，并且鼠标为左键，并且当前pick标志为True，因为pick和press会同时触发，所以
                    先用pick标志让其pick事件先做判断。
                    """
                    self.event_init = event
                    self.current_artist = Ellipse(xy=(self.event_init.xdata, self.event_init.ydata),
                                                  width=abs(event.xdata - self.event_init.xdata) * 2,
                                                  height=abs(event.ydata - self.event_init.ydata) * 2, angle=0,
                                                  fill=False,
                                                  edgecolor='red', linewidth=3, picker=True)
                    event.inaxes.add_artist(self.current_artist)  # 这里不能使用event.inaxes.patches.append方法
                    self.current_artist.set_animated(True)
                    self.can_remove_elements.append(self.current_artist)
                    self.background = self.canvas.copy_from_bbox(event.inaxes.bbox)
                    event.inaxes.draw_artist(self.current_artist)
                    self.canvas.blit(event.inaxes.bbox)
                if event.name == 'motion_notify_event' and isinstance(self.current_artist, Ellipse):
                    """pick为False表示改变形状，为True改变位置"""
                    if not self.pick:
                        width = 2 * (event.xdata - self.event_init.xdata)
                        height = 2 * (event.ydata - self.event_init.ydata)
                        center = self.current_artist.get_center()
                        self.current_artist.set_width(width)
                        self.current_artist.set_height(height)
                    else:
                        width = self.current_artist.get_width()
                        height = self.current_artist.get_height()
                        center = (event.xdata, event.ydata)
                        self.current_artist.set_center(center)
                    self.label.setText('Oval:Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % (
                        center[0], center[1], np.abs(width), np.abs(height), np.abs(np.pi * width * height / 4)))
                    self.canvas.restore_region(self.background)
                    event.inaxes.draw_artist(self.current_artist)
                    self.canvas.blit(event.inaxes.bbox)
            if event.name == 'button_release_event' and isinstance(self.current_artist, Ellipse):
                """鼠标放开，将current_artist重新添加到canvas，并且令动画效果为False"""
                self.current_artist.set_animated(False)
                event.inaxes.artists.append(self.current_artist)
                self.canvas.draw_idle()
                self.label.setText('')
                self.current_artist = None
                self.pick = False

    def text_slot(self):
        self.current_artist = None
        self.make_flag_invalid()
        self.menu_annotation_selected(self.action_text)
        self.canvas.mpl_connect('button_press_event', self.text_event)
        self.canvas.mpl_connect('motion_notify_event', self.text_event)
        self.canvas.mpl_connect('button_release_event', self.text_event)
        self.canvas.mpl_connect('pick_event', self.text_event)

    def text_event(self, event):
        if not self.action_text.isChecked():
            self.canvas.mpl_disconnect(self.text_event)
            self.canvas.mpl_disconnect(self.text_event)
            self.canvas.mpl_disconnect(self.text_event)
            self.canvas.mpl_disconnect(self.text_event)
            return
        if event.name == 'pick_event' and event.mouseevent.button == 1 and isinstance(event.artist, Text):
            """点击到对象，先将该对象移除，并保存背景"""
            if self.current_artist is None or (self.current_artist and self.current_artist == event.artist):
                """确保始终只会点击到一个对象"""
                self.pick = True
                if event.artist in self.can_remove_elements:
                    self.current_artist = self.can_remove_elements[self.can_remove_elements.index(event.artist)]
                else:
                    self.current_artist = event.artist
                    self.can_remove_elements.append(self.current_artist)
                event.mouseevent.inaxes.texts.remove(event.artist)
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(event.mouseevent.inaxes.bbox)
        if isinstance(event, matplotlib.backend_bases.MouseEvent):
            if event.inaxes and event.button == 1 and not hasattr(event.inaxes, 'azim'):
                if event.name == 'button_press_event' and not self.pick and not self.current_artist:
                    """判断为按下鼠标事件，并且是在子图区域内，并且鼠标为左键，并且当前pick标志为True，因为pick和press会同时触发，所以
                    先用pick标志让其pick事件先做判断。
                    """
                    text, ok = QtWidgets.QInputDialog.getText(self.canvas.parent(), '输入文字', '添加注释')
                    if ok and text:
                        self.event_init = event
                        self.current_artist = event.inaxes.text(event.xdata, event.ydata, text)
                        self.current_artist.set_picker(True)
                        self.can_remove_elements.append(self.current_artist)
                        self.select_font(self.current_artist)
                        event.inaxes.texts.append(self.current_artist)
                        self.button = 0
                        self.current_artist.set_animated(True)
                        self.can_remove_elements.append(self.current_artist)
                        self.background = self.canvas.copy_from_bbox(event.inaxes.bbox)
                        event.inaxes.draw_artist(self.current_artist)
                        self.canvas.blit(event.inaxes.bbox)
                if event.name == 'motion_notify_event' and isinstance(self.current_artist, Text):
                    """pick为False表示改变形状，为True改变位置"""
                    if self.pick:
                        self.current_artist.set_position((event.xdata, event.ydata))
                        self.label.setText('Text Position:(%0.2f,%0.2f)' % (event.xdata, event.ydata))
                    self.canvas.restore_region(self.background)
                    event.inaxes.draw_artist(self.current_artist)
                    self.canvas.blit(event.inaxes.bbox)
            if event.name == 'button_release_event' and isinstance(self.current_artist, Text):
                """鼠标放开，将current_artist重新添加到canvas，并且令动画效果为False"""
                self.current_artist.set_animated(False)
                event.inaxes.texts.append(self.current_artist)
                self.canvas.draw_idle()
                self.label.setText('')
                self.current_artist = None
                self.pick = False

    def annotation_slot(self):
        self.current_artist = None
        self.make_flag_invalid()
        self.menu_annotation_selected(self.action_annotation)
        self.canvas.mpl_connect('pick_event', self.annotation_event)
        self.canvas.mpl_connect('pick_event', self.annotation_event)

    def annotation_event(self, event):
        """
        由于annotation是可拖拽的，所以只需要实现，pick后将annotation的位置调整过去，并且可见，但是这里限制了只能在当前子图内操作
        """
        if not self.action_annotation.isChecked():
            self.canvas.mpl_disconnect(self.annotation_event)
            return
        if event.name == 'pick_event' and event.mouseevent.button == 1 and not isinstance(event.artist, Annotation):
            x, y = event.mouseevent.xdata, event.mouseevent.ydata
            if self.current_artist is None:
                self.annotation = event.mouseevent.inaxes.annotate(
                    self.an_axis_style.format(x, y),
                    xy=(x, y),
                    xytext=eval(self.an_offset),
                    textcoords='offset points',
                    ha='right', va='bottom',
                    bbox=dict(
                        boxstyle='round,pad=0.5',
                        fc=self.an_bg_color,
                        alpha=0.5,
                        linewidth=self.an_border,
                        edgecolor=self.an_border_color),
                    arrowprops=dict(
                        arrowstyle=self.an_arrow_shape,
                        connectionstyle='arc3,rad=0',
                        alpha=float(eval(self.an_show_arrow))),
                    picker=True)
                self.point = Line2D([x],
                                    [y],
                                    ls="",
                                    marker='o',
                                    markerfacecolor='r',
                                    animated=False,
                                    pickradius=5,
                                    picker=True)
                event.mouseevent.inaxes.add_artist(self.point)
                self.can_remove_elements.append(self.annotation)
                self.can_remove_elements.append(self.point)
                self.set_all_fonts()
                self.annotation.draggable(True, use_blit=True)
                self.current_artist = event.artist
            else:
                self.point.set_data(([x], [y]))
                self.annotation.xy = x, y
                self.annotation.set_text(self.an_axis_style.format(x, y))
                self.annotation.set_visible(True)
            self.canvas.draw_idle()

    def legend_slot(self):
        if self.show_legend_flag:
            if self.current_subplot.lines:  # 如果存在曲线才允许画图例
                legend = self.current_subplot.get_legend()
                if legend:
                    legend.remove()
                self.show_legend_flag = False
                self.canvas.draw()
        else:
            legend_titles = []
            for index in range(len(self.current_subplot.lines)):
                label = self.current_subplot.lines[index]._label
                if label.startswith('_line'):
                    legend_titles.append('curve ' + str(index + 1))
                else:
                    legend_titles.append(label)
            if self.current_subplot.lines:  # 如果存在曲线才允许画图例
                leg = self.current_subplot.legend(self.current_subplot.lines, legend_titles)
                leg.set_draggable(True)  # 设置legend可拖拽
                for legline in leg.get_lines():
                    legline.set_pickradius(10)
                    legline.set_picker(True)  # 给每个legend设置可点击
                self.canvas.draw()
                self.show_legend_flag = True

    def show_colorbar_slot(self):
        colorbar_setting.Window(self.current_subplot, self.canvas)

    def change_view_slot(self, azim, elev):
        if not hasattr(self.current_subplot, 'azim'):
            return
        self.current_subplot.view_init(azim=azim, elev=elev)
        self.canvas.draw()

    def show_grid_slot(self):
        self.show_grid_flag = not self.show_grid_flag
        self.current_subplot.grid(
            axis=self.grid_axis,
            color=self.grid_color,
            linestyle=self.grid_linestyle,
            linewidth=self.grid_linewidth,
            which=self.grid_which,
            visible=self.show_grid_flag)
        if not self.show_grid_flag:
            self.make_flag_invalid()
        self.canvas.draw_idle()

    def menu_subplots_slot(self, index):
        """将menu子图和当前子图对象关联起来"""
        for action in self.menu.actions():
            action.setChecked(False)
        self.menu.actions()[index].setChecked(True)
        self.current_subplot = self.axes[index]  # 将当前选择付给子图对象

    def axes_control_slot(self):
        if not self.current_subplot:
            QtWidgets.QMessageBox.warning(
                self.canvas.parent(), "错误", "没有可选的子图！")
            return
        if self.current_language == 'en':
            lang = 'en_axes_control'
        if self.current_language == 'zh_CN':
            lang = 'zh_CN_axes_control'
        Ui_Form_Manager(self.current_subplot, self.canvas, self.config, self.config_path, lang)
        self.set_pickers()  # 设置之后，改变配置文件中的变量，更新字体等
        self.read_all_settings()
        self.set_all_fonts()
        self.canvas.draw()

    def delete_artist(self, event: matplotlib.backend_bases.PickEvent):
        """删除对象，既要调用Artist.remove，又要从axes.xxs中删除该对象才能删除"""
        event.artist.remove()
        if event.artist in self.can_remove_elements:
            self.can_remove_elements.remove(event.artist)
        if event.artist in event.mouseevent.inaxes.artists:
            event.mouseevent.inaxes.artists.remove(event.artist)
        if event.artist in event.mouseevent.inaxes.lines:
            event.mouseevent.inaxes.lines.remove(event.artist)
        if event.artist in event.mouseevent.inaxes.patches:
            event.mouseevent.inaxes.patches.remove(event.artist)
        if event.artist in event.mouseevent.inaxes.collections:
            event.mouseevent.inaxes.collections.remove(event.artist)
        self.canvas.draw()

    def generate_trend_line(self, event):
        assert isinstance(event.artist, Line2D)
        deg, ok = QtWidgets.QInputDialog.getInt(self, '趋势线对话框', '拟合次数')
        xs, ys = event.artist.get_data()
        xs = xs.reshape(-1)
        ys = ys.reshape(-1)
        parameter = np.polyfit(xs, ys, deg)
        # 对参数进行拼接
        label = '$'
        for i in range(deg + 1):
            bb = round(parameter[i], 6)  # bb是i次项系数
            if bb >= 0:
                if i == 0:
                    bb = str(bb)
                else:
                    bb = ' +' + str(bb)
            else:
                bb = ' ' + str(bb)
            if deg == i:
                label = label + bb
            else:
                if deg - i != 1:
                    label = label + bb + 'x^' + str(deg - i)
                else:
                    label = label + bb + 'x'
        label += '$'
        f = np.poly1d(parameter)
        event.mouseevent.inaxes.plot(xs, f(xs), 'r--', label=label)
        self.canvas.draw_idle()

    def drag_legend(self, event):
        """鼠标进入axes，默认legend可以拖拽，离开axes，使之不可拖拽，因为legend可拖拽会导致figure无法pickle"""
        ax = event.inaxes
        legend = ax.get_legend()
        self.legend_draggable_flag = not self.legend_draggable_flag
        if legend:
            legend.set_draggable(self.legend_draggable_flag, use_blit=True)

    def right_button_menu(self, event):
        """"""
        if event.mouseevent.button == 3:
            if isinstance(event.artist, Axes):
                self.contextMenu = QMenu()
                axes = event.artist
                action_axis = self.contextMenu.addAction('修改坐标轴样式')
                action_axis.triggered.connect(lambda: axis_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Legend):
                self.contextMenu = QMenu()
                action_visible = self.contextMenu.addAction('显示/隐藏')
                action_style = self.contextMenu.addAction('修改图例样式')
                action_visible.triggered.connect(self.legend_slot)
                action_style.triggered.connect(lambda: legend_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Rectangle):
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除矩形')
                action_style = self.contextMenu.addAction('修改矩形样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: rectangle_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Ellipse):
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除椭圆')
                action_style = self.contextMenu.addAction('修改椭圆样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: ellipse_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Line2D):
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除')
                action_style = self.contextMenu.addAction('修改曲线样式')
                action_trend_line = self.contextMenu.addAction('添加趋势线')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: linestyle_manager.Ui_Dialog_Manager(self.canvas, event.artist))
                action_trend_line.triggered.connect(lambda: self.generate_trend_line(event))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Annotation):
                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle('Annotation setting')
                views = []
                views.append((str, 'text', 'text', event.artist.get_text()))
                views.append((bool, 'show_coord', 'show coord', True))
                views.append((str, 'xy', 'xy position', '(%.2f,%.2f)' % event.artist.xy))
                views.append((str, 'xyann', 'text position', '(%.2f,%.2f)' % event.artist.xyann))
                views.append(
                    ('choose_box', 'arrowstyle', 'arrow style', event.artist.arrowprops['arrowstyle'], arrowstyles))
                sp = SettingsPanel(views=views, parent=dialog)
                dialog.setLayout(QHBoxLayout())
                dialog.layout().addWidget(sp)
                dialog.exec_()
                event.mouseevent.button = 0
                view_dict = sp.get_value()
                if not view_dict['show_coord']:
                    event.artist.set_text(view_dict['text'])
                event.artist.xy = tuple(eval(view_dict['xy']))
                event.artist.xyann = tuple(eval(view_dict['xyann']))
                event.artist.arrowprops = {'arrowstyle': view_dict['arrowstyle']}
                self.canvas.draw_idle()
            if isinstance(event.artist, Text):
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除文字')
                action_style = self.contextMenu.addAction('修改文字样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: text_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()

    def close(self):
        with open(self.config_path, 'w') as f:
            self.config.write(f)
        super().close()


if QtWidgets.QApplication.instance() is None:
    config_path = os.path.join(os.path.dirname(__file__), 'settings.cfg')
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            pass
    _pmagg_app = QtWidgets.QApplication(sys.argv)  # 没有app，则创建
    agg = Window(config_path=config_path)
    agg.setWindowTitle('Powered by PyMiner')


class FigureManagerPyMiner(FigureManagerBase):
    def show(self):
        agg.get_canvas(self.canvas.figure)
        agg.show()
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython is not None:
            ipython.magic("gui qt5")
        else:
            _pmagg_app.exec()


"""下面这堆可以不用管"""


def show(*, block=None):
    """
    For image backends - is not required.
    For GUI backends - show() is usually the last line of a pyplot script and
    tells the backend that it is time to draw.  In interactive mode, this
    should do nothing.
    """
    for manager in Gcf.get_all_fig_managers():
        # do something to display the GUI
        # t = threading.Thread(target=manager.show())
        # t.daemon = True
        # t.start()
        manager.show()
        Gcf.destroy(manager.num)


def draw_if_interactive(flag=0):
    # 如果setting.cfg存在，且默认字体存在则设置默认字体
    import matplotlib.font_manager as font_manager
    config = configparser.ConfigParser()
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.cfg')
    man = font_manager.FontManager()
    plt.style.use('default')
    if os.path.exists(settings_path):
        config.read(settings_path, encoding='utf-8-sig')
        # 设置绘图风格
        if config.has_option('draw', 'style'):
            style = config.get('draw', 'style')
            if style != 'None':
                plt.style.use(config.get('draw', 'style'))
        # 设置字体
        if config.has_option('font', 'local_font_path') and config.has_option('font', 'local_font'):
            font = config.get('font', 'local_font')
            path = config.get('font', 'local_font_path')
            if font != 'None' and os.path.exists(path):
                man.addfont(path=path)
                matplotlib.rcParams['font.sans-serif'] = [font]
                matplotlib.rcParams['axes.unicode_minus'] = False  # 解决‘-’bug
                return
        if config.has_option('font', 'mix_font_path') and config.has_option('font', 'mix_font'):
            font = config.get('font', 'mix_font')
            path = config.get('font', 'mix_font_path')
            if font != 'None' and os.path.exists(path):
                man.addfont(path=path)
                matplotlib.rcParams['font.sans-serif'] = [font]
                matplotlib.rcParams['axes.unicode_minus'] = False  # 解决‘-’bug
                return
        if config.has_option('font', 'english_font_path') and config.has_option('font', 'english_font'):
            font = config.get('font', 'english_font')
            path = config.get('font', 'english_font_path')
            if font != 'None' and os.path.exists(path):
                man.addfont(path=path)
                matplotlib.rcParams['font.sans-serif'] = [font]
                matplotlib.rcParams['axes.unicode_minus'] = False  # 解决‘-’bug
                return


def new_figure_manager(num, *args, FigureClass=Figure, **kwargs):
    """Create a new figure manager instance."""
    # If a main-level app must be created, this (and
    # new_figure_manager_given_figure) is the usual place to do it -- see
    # backend_wx, backend_wxagg and backend_tkagg for examples.  Not all GUIs
    # require explicit instantiation of a main-level app (e.g., backend_gtk3)
    # for pylab.
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    """Create a new figure manager instance for the given figure."""
    # canvas = FigureCanvasTemplate(figure)
    # manager = FigureManagerTemplate(canvas, num)
    # return manager
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas = FigureCanvasAgg(figure)
    manager = FigureManagerPyMiner(canvas, num)
    return manager
