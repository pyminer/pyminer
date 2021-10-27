# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 10:29
# @Author  : 别着急慢慢来
# @FileName: PMAgg.py

from pathlib import Path
import os
import io
import pickle
import numpy as np
from PySide2 import QtWidgets, QtGui
from PySide2 import QtCore
from PySide2.QtGui import QIcon, QCursor, QImage
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, FancyBboxPatch
from matplotlib.backend_bases import MouseEvent
from matplotlib.transforms import Transform, IdentityTransform

import sys
from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from .ui import pmagg_ui, axis_edit_manager, default_setting_manager, legend_setting, \
        rectangle_setting, ellipse_setting, colorbar_setting, text_setting, \
        title_setting, arrow_setting, line2d_setting, color_table, image_setting, save_image_setting
else:
    from packages.pmagg.ui import pmagg_ui, axis_edit_manager, default_setting_manager, \
        legend_setting, \
        rectangle_setting, ellipse_setting, colorbar_setting, text_setting, \
        title_setting, arrow_setting, line2d_setting, color_table, image_setting, save_image_setting
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from PySide2.QtWidgets import QAction, QMenu, QApplication
from matplotlib.lines import Line2D
from matplotlib.text import Annotation, Text
from matplotlib.legend import Legend
import matplotlib.font_manager as font_manager
import matplotlib.font_manager
import re
from functools import partial
from matplotlib.axes import Axes
import webbrowser
from IPython import get_ipython

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


def draw_if_interactive(*args, **kwargs):
    # 设置绘图风格，None和default都用default
    config_path = Path.home().joinpath('.pyminer/packages/pmagg/settings.cfg')
    config = QtCore.QSettings(str(config_path), QtCore.QSettings.IniFormat)
    style = config.value('draw/style')
    plt.style.use('default')  # 防止样式叠加
    try:
        plt.style.use(style)
    except Exception as e:
        config.setValue('draw/style', 'default')
        plt.style.use('default')
    # 预先设置字体
    # 虽然在Window中有set font函数可以设置figure中所有的文字，但文字中含有中文时，控制台会出现很多警告
    # 所以给出默认字体,对消除警告是必须的。
    font_list = ['local', 'mix', 'english']
    man = font_manager.FontManager()
    for item in font_list:
        font = config.value('font/{}_font'.format(item))
        path = config.value('font/{}_font_path'.format(item))
        if font and os.path.exists(path):
            man.addfont(path=path)
            matplotlib.rcParams['font.sans-serif'] = [font]
            matplotlib.rcParams['axes.unicode_minus'] = False  # 解决‘-’bug
            break


class Window(QtWidgets.QMainWindow, pmagg_ui.Ui_MainWindow):
    """
    PMAgg主窗口，PMAgg对matplotlib绘图窗口进行了增强，集成了一些手动添加注释和预览样式的功能
    继承该类实现自定义后端界面，可以自行往menubar和toolbar中添加action，或者添加右键功能菜单
    self.canvas.draw() 每执行该函数，图形重绘
    """

    def __init__(self, *args, **kwargs):
        self.switch_backend()
        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)  # 需要有这样一句话存在，否则无法super
        else:
            self.app = QtWidgets.QApplication.instance()
        super(Window, self).__init__()
        self.setupUi(self)  # 先执行父类方法，以产生成员变量
        self.retranslateUi(self)
        self.current_path = os.path.dirname(__file__)  # 当前文件路径
        self.config_path = str(Path.home().joinpath('.pyminer/packages/pmagg/settings.cfg'))
        self.icon_path = os.path.join(self.current_path, 'icons/Icon.ico')
        self.config = QtCore.QSettings(self.config_path, QtCore.QSettings.IniFormat)
        # 设置gui字体
        if self.config.value('font/gui_font'):
            font = QtGui.QFont()
            font.setFamily(self.config.value('font/gui_font'))
            self.app.setFont(font)
        # 设置图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # 翻译家
        self.trans = QtCore.QTranslator()
        # 所有的标志
        self.flags = {
            'rect': False,
            'oval': False,
            'rotate': False,
            'pan': False,
            'zoom': False,
            'text': False,
            'legend': False,
            'annotation': False,
            'legend_draggable': False,
            'image': False,
            'move': False,
            'add': False,
            'space': True,
            'front': True,
            'back': True,
            'home': True,
        }
        # 工具栏设置
        self.toolBar.addAction(self.action_save_image)
        self.toolBar.addAction(self.action_default_setting)
        self.toolBar.addAction(self.action_space)
        self.toolBar.addAction(self.action_home)
        self.toolBar.addAction(self.action_back)
        self.toolBar.addAction(self.action_front)
        self.toolBar.addAction(self.action_zoom)
        self.toolBar.addAction(self.action_pan)
        self.toolBar.addAction(self.action_rotate)
        self.toolBar.addAction(self.action_axis_edit)
        self.toolBar.addAction(self.action_legend)
        self.toolBar.addAction(self.action_colorbar)

        # 文件菜单栏设置
        self.action_save_image.setIcon(QIcon(os.path.join(self.current_path, 'icons/save.png')))
        self.action_save_image.triggered.connect(self.save_slot)
        self.action_save_figure.triggered.connect(self.save_figure_slot)
        self.action_load_figure.triggered.connect(self.load_figure_slot)
        self.action_close.triggered.connect(self.close)
        self.action_save_image.setShortcut('Ctrl+S')
        self.action_save_figure.setShortcut('Ctrl+Shift+S')
        self.action_load_figure.setShortcut('Ctrl+L')
        self.action_close.setShortcut('Ctrl+C')

        # 编辑菜单栏设置
        self.action_space.setIcon(QIcon(os.path.join(self.current_path, 'icons/space.png')))
        self.action_default_setting.setIcon(QIcon(os.path.join(self.current_path, 'icons/setting.png')))
        self.action_copy_figure_to_clipboard.triggered.connect(self.copy_figure_to_clipboard_slot)
        self.action_space.triggered.connect(lambda: self.event_slot('space', True))
        self.action_title_edit.triggered.connect(self.title_edit_slot)
        self.action_default_setting.triggered.connect(self.axes_control_slot)
        self.action_home.setIcon(QIcon(os.path.join(self.current_path, 'icons/home.png')))
        self.action_home.triggered.connect(lambda: self.event_slot('home', True))
        self.action_home.setShortcut('Ctrl+H')
        self.action_back.setIcon(QIcon(os.path.join(self.current_path, 'icons/back.png')))
        self.action_back.triggered.connect(lambda: self.event_slot('back', True))
        self.action_front.setIcon(QIcon(os.path.join(self.current_path, 'icons/front.png')))
        self.action_front.triggered.connect(lambda: self.event_slot('front', True))
        self.action_axis_edit.setIcon(QIcon(os.path.join(self.current_path, 'icons/axis.png')))
        self.action_axis_edit.triggered.connect(self.axis_edit_slot)
        self.action_legend.setIcon(QIcon(os.path.join(self.current_path, 'icons/legend.png')))
        self.action_legend.triggered.connect(lambda: self.event_slot('legend', not self.flags['legend']))
        self.action_colorbar.setIcon(QIcon(os.path.join(self.current_path, 'icons/colorbar.png')))
        self.action_colorbar.triggered.connect(self.show_colorbar_slot)

        # 注释菜单栏设置
        self.action_rectangle.triggered.connect(lambda: self.event_slot('rect', True))
        self.action_oval.triggered.connect(lambda: self.event_slot('oval', True))
        self.action_text.triggered.connect(lambda: self.event_slot('text', True))
        self.action_annotation.triggered.connect(lambda: self.event_slot('annotation', True))
        self.action_arrow.triggered.connect(lambda: self.event_slot('arrow', True))
        self.action_image.triggered.connect(lambda: self.event_slot('image', True))
        self.action_rectangle.setIcon(QIcon(os.path.join(self.current_path, 'icons/rect.png')))
        self.action_text.setIcon(QIcon(os.path.join(self.current_path, 'icons/text.png')))
        self.action_oval.setIcon(QIcon(os.path.join(self.current_path, 'icons/oval.png')))
        self.action_annotation.setIcon(QIcon(os.path.join(self.current_path, 'icons/annotation.png')))
        self.action_arrow.setIcon(QIcon(os.path.join(self.current_path, 'icons/arrow.png')))
        self.action_image.setIcon(QIcon(os.path.join(self.current_path, 'icons/image.png')))
        self.action_rectangle.setShortcut('Alt+R')
        self.action_text.setShortcut('Alt+T')
        self.action_oval.setShortcut('Alt+O')
        self.action_annotation.setShortcut('Alt+X')
        self.action_arrow.setShortcut('Alt+A')
        self.action_image.setShortcut('Alt+I')

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
        self.action_show_toolbar.triggered.connect(self.show_toolbar_slot)
        self.action_show_menubar.triggered.connect(self.show_menubar_slot)
        self.action_zoom.setIcon(QIcon(os.path.join(self.current_path, 'icons/zoom.png')))
        self.action_zoom.triggered.connect(lambda: self.event_slot('zoom', not self.flags['zoom']))
        self.action_pan.setIcon(QIcon(os.path.join(self.current_path, 'icons/pan.png')))
        self.action_pan.triggered.connect(lambda: self.event_slot('pan', not self.flags['pan']))
        self.action_rotate.setIcon(QIcon(os.path.join(self.current_path, 'icons/rotate.png')))
        self.action_rotate.triggered.connect(lambda: self.event_slot('rotate', not self.flags['rotate']))

        # 帮助菜单栏设置
        self.action_help.triggered.connect(self.help_slot)
        self.action_matplotlib.triggered.connect(self.open_mpl_website_slot)
        self.action_color_table.triggered.connect(self.show_color_table_slot)
        self.action_help.setShortcut('F1')
        self.action_matplotlib.setShortcut('F2')

        # 提示label 放在statusbar中，显示矩形或点的坐标等
        self.label = QtWidgets.QLabel()
        self.statusBar.addWidget(self.label)
        # 当前的artist对象
        self.current_artist = None
        # 这里面装着可以被home去除的组件
        self.can_remove_elements = []
        self.current_subplot = None
        self.legend_draggable_flag = False
        # 这个button的出现是因为在添加文字时，明明鼠标移动时，没有按下按钮，但是mpl识别出按下了按钮，所以另外做一个标志
        self.button = 0
        self.canvas = None
        self.toolbar = None
        self.toolBar.layout().setMargin(0)  # 使pyminer中图标不变得过小

        self.relative_pos: Tuple[int, int] = (0, 0)  # 记录相对位置，默认是0

    def switch_backend(self):
        # 先切换后端，调用draw_if_interactive
        sys.path.append(os.path.dirname(__file__))
        matplotlib.use('module://PMAgg')

    def init_figure(self):
        self.canvas.figure.tight_layout()
        self.set_subplots()
        self.read_all_settings()
        self.set_pickers()
        self.set_all_fonts()
        self.set_mpl_events()
        self.set_gui_language()

    def set_gui_language(self):
        if self.config.value('language/current_language') == 'en':
            self._trigger_english()
        if self.config.value('language/current_language') == 'zh_CN':
            self._trigger_zh_cn()

    def _trigger_english(self):
        """切换英语，并且写入配置文件"""
        self.current_language = 'en'
        en_qm = os.path.join(self.current_path, 'langs/en_pmagg_ui.qm')
        self.trans.load(en_qm)
        _app = QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)  # 重新翻译主界面
        self.retranslateUi(self)
        self.config.setValue('language/current_language', 'en')

    def _trigger_zh_cn(self):
        self.current_language = 'zh_CN'
        zh_qm = os.path.join(self.current_path, 'langs/zh_CN_pmagg_ui.qm')
        self.trans.load(zh_qm)
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.config.setValue('language/current_language', 'zh_CN')

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
        self.canvas.mpl_connect('button_press_event', self.on_rotate)
        self.canvas.mpl_connect('motion_notify_event', self.on_rotate)

        # 为图例绑定监听事件
        self.canvas.mpl_connect('axes_enter_event', self.drag_legend)
        self.canvas.mpl_connect('axes_leave_event', self.drag_legend)
        # 为右键功能集成
        self.canvas.mpl_connect('pick_event', self.right_button_menu)
        # 移动事件
        self.canvas.mpl_connect('motion_notify_event', self.move_event)
        self.canvas.mpl_connect('button_release_event', self.move_event)
        self.canvas.mpl_connect('pick_event', self.move_event)
        # 添加事件
        self.canvas.mpl_connect('button_press_event', self.add_event)
        self.canvas.mpl_connect('motion_notify_event', self.add_event)
        self.canvas.mpl_connect('button_release_event', self.add_event)

    def get_canvas(self, figure):
        if not self.canvas:
            self.canvas = FigureCanvas(figure)  # 这里的canvas就是曲线图
            self.init_figure()  # 先初始化图形，设置项等
            self.centralwidget.layout().addWidget(self.canvas)
        else:
            # 重置figure的大小
            size = self.canvas.figure.get_size_inches()
            self.canvas.figure = figure
            self.canvas.figure.set_size_inches(size)
            self.init_figure()
            self.canvas.draw()

    def select_font(self, text: Text):
        content = text.get_text()
        zh_model = re.compile(u'[\u4e00-\u9fa5]')
        en_model = re.compile(u'[a-z]')
        zh = zh_model.search(content)
        en = en_model.search(content)
        if zh and en and self.config.value('font/mix_font') and os.path.exists(self.config.value('font/mix_font_path')):
            text.set_fontproperties(Path(self.config.value('font/mix_font_path')))
            return text
        if zh and not en and self.config.value('font/local_font') and os.path.exists(
                self.config.value('font/local_font_path')):
            text.set_fontproperties(Path(self.config.value('font/local_font_path')))
            return text
        if not zh and self.config.value('font/english_font') and os.path.exists(
                self.config.value('font/english_font_path')):
            text.set_fontproperties(Path(self.config.value('font/english_font_path')))
            return text
        return text

    def read_all_settings(self):
        """对一些默认设置进行预处理"""
        # 选择语言
        if not self.config.value('language/current_language'):
            self.config.setValue('language/current_language', 'en')
        # 上次打开的路径
        if not os.path.exists(str(self.config.value('path/last_path'))):
            self.config.setValue('path/last_path', os.path.expanduser('~'))
        if not self.config.value('annotation/coord'):
            self.config.setValue('annotation/coord', 'data')

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
        # 运行QT5Agg原来的home，实现平移的复位
        self.toolbar.home()
        # 将三维图视角还原
        for item in self.init_views:
            self.axes[item[0]].view_init(azim=item[1], elev=item[2])
        # 将can_remove_elements中的对应的元素全部删除
        for i in self.can_remove_elements:
            i.remove()
            for item in self.axes:
                if i in item.texts:
                    item.texts.remove(i)
                if i in item.artists:
                    item.artists.remove(i)
                if i in item.patches:
                    item.patches.remove(i)
                if i in item.lines:
                    item.lines.remove(i)
        self.can_remove_elements.clear()
        self.canvas.draw()

    def event_slot(self, flag: str, status) -> None:
        """
        完成所有事件按钮的切换工作
        Args:
            flag: 标志
            status: 标志要切换过去的状态

        Returns:

        """
        self.label.setText('')
        if not self.canvas.toolbar:
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.toolbar.hide()  # 隐藏QT原来的工具栏
        else:
            self.toolbar = self.canvas.toolbar
        self.current_artist = None
        self.toolbar.mode = None
        self.canvas.widgetlock.release(self.toolbar)
        self.canvas.setCursor(QtCore.Qt.ArrowCursor)
        for item in self.flags.keys():
            if item == flag:
                self.flags[item] = status
            else:
                self.flags[item] = False
        self.flags['move'] = True  # 移动标志常开
        # 所有选中置否
        for menu in self.menu_annotation.actions():
            menu.setChecked(False)
        self.action_zoom.setChecked(False)
        self.action_rotate.setChecked(False)
        self.action_pan.setChecked(False)
        if status:
            if flag == 'rotate':
                self.canvas.setCursor(QtCore.Qt.SizeAllCursor)
                self.action_rotate.setChecked(True)
            if flag == 'space':
                self.toolbar.configure_subplots()
            if flag == 'front':
                self.toolbar._nav_stack.forward()
                self.toolbar._update_view()
            if flag == 'back':
                self.toolbar._nav_stack.back()
                self.toolbar._update_view()
            if flag == 'home':
                self.home_slot()
            if flag == 'rect':
                self.action_rectangle.setChecked(True)
                self.flags['move'] = False
            if flag == 'oval':
                self.action_oval.setChecked(True)
                self.flags['move'] = False
            if flag == 'text':
                self.action_text.setChecked(True)
            if flag == 'annotation':
                self.action_annotation.setChecked(True)
            if flag == 'arrow':
                self.action_arrow.setChecked(True)
                self.flags['move'] = False
            if flag == 'image':
                self.action_image.setChecked(True)
            if flag == 'zoom':
                self.toolbar.zoom()
                self.action_zoom.setChecked(True)
            if flag == 'pan':
                self.toolbar.pan()
                self.action_pan.setChecked(True)
        if flag == 'legend':  # 无论status，都要执行的
            self.legend_slot()

    def save_slot(self):
        """
        在按默认参数保存图片后，将图片大小重新调整到窗口实际大小。
        """
        save_image_setting.Window(self.canvas)

    def save_figure_slot(self):
        """保存figure的pickle对象到文件，一定要先关闭picker"""
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save figure object',
                                                              self.config.value('path/last_path'),
                                                              filter="Pickle object (*.pickle)")
        if file_name != '':
            if file_name.split('.')[-1] != 'pickle':  # 添加后缀
                file_name = file_name + '.pickle'
            with open(file_name, 'wb') as f:
                self.set_pickers(flag=False)
                pickle.dump(self.canvas.figure, f)
            self.set_pickers(True)
        dir_name = os.path.dirname(file_name)
        self.config.setValue('path/last_path', dir_name)

    def load_figure_slot(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open figure object', self.last_path,
                                                     filter='Pickle object (*.pickle)')
        if os.path.exists(name[0]):
            with open(name[0], 'rb') as f:
                self.get_canvas(pickle.load(f))
        dir_name = os.path.dirname(name[0])
        self.last_path = dir_name
        self.set_config('path', 'last_path', self.last_path)

    def on_rotate(self, event):
        if not self.flags['rotate']:
            return
        # 如果鼠标移动过程有按下，视为拖拽，判断当前子图是否有azim属性来判断当前是否3D
        if event.button == 1 and hasattr(event.inaxes, 'azim'):
            self.canvas.setCursor(QtCore.Qt.SizeAllCursor)
            if event.name == 'button_press_event':
                pseudo_bbox = event.inaxes.transLimits.inverted().transform([(0, 0), (1, 1)])
                self._pseudo_w, self._pseudo_h = pseudo_bbox[1] - pseudo_bbox[0]
                self.mouse_x, self.mouse_y = event.xdata, event.ydata
                self.axes3d_azim = event.inaxes.azim
                self.axes3d_elev = event.inaxes.elev
            if event.name == 'motion_notify_event' and self.axes3d_azim:
                delta_azim = -180 * (event.xdata - self.mouse_x) / self._pseudo_w
                delta_elev = -180 * (event.ydata - self.mouse_y) / self._pseudo_h
                azim = delta_azim + self.axes3d_azim
                elev = delta_elev + self.axes3d_elev
                event.inaxes.view_init(azim=azim, elev=elev)
                self.canvas.draw_idle()

    def switch_coord(self, ax):
        coord = self.config.value('annotation/coord')
        if coord == 'data':
            return ax.transData
        if coord == 'axes':
            return ax.transAxes
        if coord == 'pixel':
            return IdentityTransform()
        if coord == 'figure':
            return ax.transFigure

    def convert_axes_coord(self, point, ax=None, artist=None):
        """将figure像素坐标系中的点转为其它坐标系"""
        if ax is not None:
            return self.switch_coord(ax).inverted().transform(point)  # 适用于add_event，用于新建对象时选择坐标系
        if artist is not None:
            if isinstance(artist, Text) or isinstance(artist, AnnotationBbox):
                return artist.get_transform().inverted().transform(point)
            else:
                return artist.get_data_transform().inverted().transform(point)
        return point

    def get_axes(self, ax: Axes = None, artist=None):
        """获取子图或figure"""
        if artist and artist.axes:
            return artist.axes  # 如果artist在子图里
        if artist and artist.figure:
            return artist.figure  # 如果artist在figure里
        coord = self.config.value('annotation/coord')
        if coord == 'figure' or coord == 'pixel':
            return self.canvas.figure  # 放在figure内
        return ax  # ax可能为None或者子图对象，如果为None，则不绘图

    def set_annotation_axes(self, artist: Annotation, ax):
        coord = self.config.value('annotation/coord')
        if coord == 'figure' or coord == 'pixel':
            artist.figure = ax  # 放在figure内
            ax.texts.append(artist)
            artist._remove_method = ax.texts.remove  # 由于Annotation没有实现添加到figure中去的方法，需要手动做一些事情
            ax.stale = True
        else:
            artist.axes = ax
            artist.figure = ax.figure
            ax._add_text(artist)  # 请这样写，否则删除对象会失败

    def get_annotation_text_offset(self, ax):
        coord = self.config.value('annotation/coord')
        if coord == 'data':  # 数据坐标偏离0.05
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            x_offset = (xlim[1] - xlim[0]) * 0.05
            y_offset = (ylim[1] - ylim[0]) * 0.05
            return np.array((x_offset, y_offset))
        if coord == 'axes' or coord == 'figure':  # 轴坐标偏离0.05
            return np.array((0.05, 0.05))
        if coord == 'pixel':  # 像素坐标偏离20个像素
            return np.array((20, 20))

    def move_event(self, event):
        if not self.flags['move']:
            return
        if event.name == 'pick_event' and event.mouseevent.button == 1 and self.current_artist is None:
            """点击到对象，先将该对象更改为不可见，并保存背景"""
            if event.artist in self.can_remove_elements:
                self.current_artist = event.artist
                xdata, ydata = self.convert_axes_coord(point=(event.mouseevent.x, event.mouseevent.y),
                                                       artist=self.current_artist)
                ax = self.get_axes(artist=self.current_artist)
                self.current_artist.set_visible(False)
                relative_pos = (0, 0)
                self.current_artist.move_flag = 'xy'  # 动态添加的属性，用于标识移动的是哪端
                if type(event.artist) == Rectangle:
                    relative_pos = tuple(np.array((xdata, ydata)) - np.array(self.current_artist.xy))
                if type(event.artist) == Ellipse:
                    relative_pos = tuple(np.array((xdata, ydata)) - np.array(self.current_artist.get_center()))
                if type(event.artist) == AnnotationBbox:
                    relative_pos = tuple(np.array((xdata, ydata)) - np.array(self.current_artist.xybox))
                if type(event.artist) == Annotation:
                    xy = np.array(self.current_artist.xy)
                    xy_ann = np.array(self.current_artist.xyann)
                    xy_data = np.array((xdata, ydata))
                    distance_xy = np.std(xy_data - xy)
                    distance_xyann = np.std(xy_data - xy_ann)
                    if distance_xyann < distance_xy:
                        self.current_artist.move_flag = 'xyann'
                self.relative_pos = relative_pos
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(ax.bbox)

        if event.name == 'motion_notify_event' and event.button == 1:
            """恢复可见，移动位置"""
            ax = self.get_axes(artist=self.current_artist)
            if ax and self.current_artist in self.can_remove_elements:
                new_pos = self.convert_axes_coord(point=(event.x, event.y),
                                                  artist=self.current_artist) - self.relative_pos  # 在这里减去相对位置。
                self.current_artist.set_visible(True)
                if type(self.current_artist) == Rectangle:
                    width = self.current_artist.get_width()
                    height = self.current_artist.get_height()
                    center = (new_pos[0] + width / 2, new_pos[1] + height / 2)
                    self.current_artist.set_xy(new_pos)
                    self.label.setText('Rect Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % (
                        center[0], center[1], abs(width), abs(height), abs(width * height)))
                if type(self.current_artist) == Ellipse:
                    self.current_artist.set_center(new_pos)
                    width = self.current_artist.width
                    height = self.current_artist.height
                    self.label.setText('Oval:Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % (
                        new_pos[0], new_pos[1], np.abs(width), np.abs(height), np.abs(np.pi * width * height / 4)))
                if type(self.current_artist) == Text:
                    self.current_artist.set_position(new_pos)
                    self.label.setText('Text Position:(%0.2f,%0.2f)' % tuple(new_pos))
                if type(self.current_artist) == AnnotationBbox:
                    self.current_artist.xybox = new_pos
                if type(self.current_artist) == Annotation:
                    if hasattr(self.current_artist, 'move_flag'):
                        if self.current_artist.move_flag == 'xy':
                            self.current_artist.xy = new_pos
                        else:
                            self.current_artist.xyann = new_pos
                    if hasattr(self.current_artist, 'format_text'):
                        self.current_artist.set_text(self.current_artist.format_text % tuple(self.current_artist.xy))
                self.canvas.restore_region(self.background)
                ax.draw_artist(self.current_artist)
                self.canvas.blit(ax.bbox)
        if event.name == 'button_release_event' and self.current_artist in self.can_remove_elements:
            """鼠标放开，令动画效果为False，物体可见，重绘"""
            self.current_artist.set_animated(False)
            self.current_artist.set_visible(True)
            self.canvas.draw()
            self.label.setText('')
            self.current_artist = None

    def add_event(self, event: MouseEvent):
        if self.action_rectangle.isChecked():
            if event.button == 1:
                ax = self.get_axes(ax=event.inaxes)
                if event.name == 'button_press_event' and ax:
                    xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                    self.current_artist = Rectangle(xy, 0, 0,
                                                    fill=False,
                                                    edgecolor='red',
                                                    linewidth=1,
                                                    picker=True,
                                                    transform=self.switch_coord(ax),
                                                    zorder=3)
                    ax.add_artist(self.current_artist)  # 这里不能使用event.inaxes.patches.append方法
                    self.current_artist.set_animated(True)
                    self.can_remove_elements.append(self.current_artist)
                    self.background = self.canvas.copy_from_bbox(ax.bbox)
                if event.name == 'motion_notify_event' and isinstance(self.current_artist, Rectangle):
                    ax = self.get_axes(artist=self.current_artist)
                    x = self.current_artist.get_x()
                    y = self.current_artist.get_y()
                    pos = self.convert_axes_coord(point=(event.x, event.y), artist=self.current_artist)
                    size = pos - np.array((x, y))
                    center = pos + size / 2
                    self.current_artist.set_width(size[0])
                    self.current_artist.set_height(size[1])
                    label_text = (center[0], center[1], np.abs(size[0]), np.abs(size[1]), np.abs(size[0] * size[1]))
                    self.label.setText('Rect Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % label_text)
                    self.canvas.restore_region(self.background)
                    ax.draw_artist(self.current_artist)
                    self.canvas.blit(ax.bbox)
            if event.name == 'button_release_event' and isinstance(self.current_artist, Rectangle):
                """鼠标放开，令动画效果为False"""
                self.current_artist.set_animated(False)
                self.event_slot('rect', False)

        if self.action_oval.isChecked():
            if event.button == 1:
                ax = self.get_axes(ax=event.inaxes)
                if event.name == 'button_press_event' and ax:
                    xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                    self.current_artist = Ellipse(xy=xy,
                                                  width=0,
                                                  height=0, angle=0,
                                                  fill=False,
                                                  edgecolor='red',
                                                  linewidth=1,
                                                  picker=True,
                                                  transform=self.switch_coord(ax),
                                                  zorder=3)
                    ax.add_artist(self.current_artist)
                    self.current_artist.set_animated(True)
                    self.can_remove_elements.append(self.current_artist)
                    self.background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)
                if event.name == 'motion_notify_event' and isinstance(self.current_artist, Ellipse):
                    ax = self.get_axes(artist=self.current_artist)
                    center = np.array(self.current_artist.get_center())
                    pos = self.convert_axes_coord(point=(event.x, event.y), artist=self.current_artist)
                    width, height = 2 * (pos - center)
                    self.current_artist.set_width(width)
                    self.current_artist.set_height(height)
                    self.label.setText('Oval:Center:(%0.2f,%0.2f) Width=%0.2f Height=%0.2f Area=%0.2f' % (
                        center[0], center[1], np.abs(width), np.abs(height), np.abs(np.pi * width * height / 4)))
                    self.canvas.restore_region(self.background)
                    ax.draw_artist(self.current_artist)
                    self.canvas.blit(self.canvas.figure.bbox)
            if event.name == 'button_release_event' and isinstance(self.current_artist, Ellipse):
                """鼠标放开，令动画效果为False"""
                self.current_artist.set_animated(False)
                self.event_slot('oval', False)

        if self.action_text.isChecked():
            if event.button == 1:
                ax = self.get_axes(ax=event.inaxes)
                if event.name == 'button_press_event' and ax:
                    text, ok = QtWidgets.QInputDialog.getText(self.canvas.parent(), '输入文字', '添加注释')
                    if ok:
                        xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                        if hasattr(ax, 'azim'):
                            self.current_artist = ax.text2D(xy[0], xy[1], s=text,
                                                            transform=self.switch_coord(ax))
                        else:
                            self.current_artist = ax.text(xy[0], xy[1], s=text,
                                                          transform=self.switch_coord(ax))
                        self.current_artist.set_picker(True)
                        self.can_remove_elements.append(self.current_artist)
                        self.select_font(self.current_artist)
                        ax.texts.append(self.current_artist)
                        self.button = 0
                        self.canvas.draw()
                        self.event_slot('rect', False)

        if self.action_image.isChecked():
            if event.button == 1:
                ax = self.get_axes(ax=event.inaxes)
                if event.name == 'button_press_event' and ax:
                    image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,
                                                                          "openImage", "",
                                                                          "*.jpg;;*.png;;All Files(*)")
                    if image_path:
                        xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                        image = plt.imread(image_path)
                        bbox = self.current_subplot.get_window_extent().transformed(
                            self.canvas.figure.dpi_scale_trans.inverted())
                        ax_width, ax_height = bbox.width, bbox.height
                        ax_width *= self.canvas.figure.dpi
                        ax_height *= self.canvas.figure.dpi
                        image_width = image.shape[0]
                        zoom = 0.2 * ax_width / image_width
                        imagebox = OffsetImage(image, zoom=zoom)
                        self.current_artist = AnnotationBbox(imagebox, xy,
                                                             xycoords=self.switch_coord(ax),
                                                             boxcoords=self.switch_coord(ax)
                                                             )
                        self.current_artist.set_picker(True)
                        ax.add_artist(self.current_artist)
                        self.can_remove_elements.append(self.current_artist)
                        self.canvas.draw()
                        self.current_artist = None
                        self.action_image.setChecked(False)

        if self.action_arrow.isChecked():
            if event.button == 1:
                ax = self.get_axes(ax=event.inaxes)
                if event.name == 'button_press_event' and ax:
                    xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                    self.current_artist = Annotation(
                        "",
                        xy=xy,
                        xytext=xy,
                        arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.'),
                        picker=self.annotation_picker,
                        xycoords=self.switch_coord(ax),
                        textcoords=self.switch_coord(ax)
                    )
                    self.current_artist.connectionstyle='arc3,rad=0.'
                    self.set_annotation_axes(self.current_artist, ax)  # 这句必须要有，可能是因为annotation没有figure的添加方法，需手动添加
                    self.current_artist.set_animated(True)
                    self.can_remove_elements.append(self.current_artist)
                    self.background = self.canvas.copy_from_bbox(ax.bbox)
                if event.name == 'motion_notify_event' and type(self.current_artist) == Annotation:
                    ax = self.get_axes(artist=self.current_artist)
                    length = np.std(np.array(self.current_artist.xy) - np.array(self.current_artist.xyann))
                    xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                    self.current_artist.xy = xy
                    self.label.setText('Arrow:Position:(%0.2f,%0.2f) Length=%0.2f' % (
                        xy[0], xy[1], length))
                    self.canvas.restore_region(self.background)
                    ax.draw_artist(self.current_artist)
                    self.canvas.blit(ax.bbox)

            if event.name == 'button_release_event' and type(self.current_artist) == Annotation:
                """鼠标放开，令动画效果为False"""
                self.current_artist.set_animated(False)
                self.event_slot('arrow', False)

        if self.action_annotation.isChecked():
            if event.button == 1:
                if event.name == 'button_press_event':
                    ax = self.get_axes(ax=event.inaxes)
                    xy = self.convert_axes_coord(point=(event.x, event.y), ax=ax)
                    format_text = "x: %.2f\ny: %.2f"
                    self.current_artist = Annotation(
                        format_text % tuple(xy),
                        xy=xy,
                        xytext=xy + self.get_annotation_text_offset(ax),  # 加上偏移量
                        bbox=dict(
                            boxstyle='round,pad=0.5',
                            fc='white',
                            alpha=0.5,
                            linewidth=1,
                            edgecolor='blue'),
                        arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.'),
                        picker=self.annotation_picker,
                        xycoords=self.switch_coord(ax),
                        textcoords=self.switch_coord(ax)
                    )

                    self.current_artist.connectionstyle = 'arc3,rad=0.'
                    self.current_artist.format_text = format_text  # 用于保存文字格式，动态添加了属性
                    self.set_all_fonts()
                    self.set_annotation_axes(self.current_artist, ax)
                    self.can_remove_elements.append(self.current_artist)
                    self.canvas.draw()
                    self.event_slot('annotation', False)

    def annotation_picker(self, artist: Annotation, mouseevent: MouseEvent, radius=20):
        """自定义picker函数，参见
        https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.artist.Artist.set_picker.html#matplotlib.artist.Artist.set_picker
        判断依据，点到线段距离不超过半径值
        """
        # 转为像素坐标
        x1, y1 = artist.get_transform().transform(artist.xy)
        x2, y2 = artist.get_transform().transform(artist.xyann)
        x, y = mouseevent.x, mouseevent.y
        dis1 = np.std([x - x1, y - y1])
        dis2 = np.std([x - x2, y - y2])
        return dis1 < radius or dis2 < radius, dict()

    def legend_slot(self):
        if not self.flags['legend']:
            if self.current_subplot.lines:  # 如果存在曲线才允许画图例
                legend = self.current_subplot.get_legend()
                if legend:
                    legend.remove()
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

    def show_colorbar_slot(self):
        colorbar_setting.Window(self.canvas)

    def change_view_slot(self, azim, elev):
        if not hasattr(self.current_subplot, 'azim'):
            return
        self.current_subplot.view_init(azim=azim, elev=elev)
        self.canvas.draw()

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
        default_setting_manager.Ui_Form_Manager(self)

    def axis_edit_slot(self):
        axis_edit_manager.Ui_Dialog_Manager(ax=None, canvas=self.canvas, path=self.current_path, parent=self)

    def title_edit_slot(self):
        title_setting.Window(self.canvas)

    def delete_artist(self, event: matplotlib.backend_bases.PickEvent):
        """删除对象，既要调用Artist.remove，又要从axes.xxs中删除该对象才能删除"""
        ax = self.get_axes(artist=event.artist)
        event.artist.remove()
        if event.artist in ax.artists:
            ax.artists.remove(event.artist)
        if event.artist in ax.lines:
            event.mouseevent.inaxes.lines.remove(event.artist)
        if event.artist in ax.patches:
            ax.patches.remove(event.artist)
        if event.artist in ax.texts:
            ax.texts.remove(event.artist)
        if event.artist in self.can_remove_elements:
            self.can_remove_elements.remove(event.artist)

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
            # if isinstance(event.artist,matplotlib.patches.Wedge):
            #     print(event.artist.get_edgecolor())
            #     print(event.artist.get_facecolor())
            #     print(event.artist.theta1)
            #     print(event.artist.theta2)
            #     print(event.artist.r)
            #     print(event.artist.center)
            #     print(event.artist)
            if isinstance(event.artist, Axes):
                self.contextMenu = QMenu()
                self.contextMenu.addMenu(self.menuFile)
                self.contextMenu.addMenu(self.menu_edit)
                self.contextMenu.addMenu(self.menu_annotation)
                self.contextMenu.addMenu(self.menu_6)
                self.contextMenu.addMenu(self.menu)
                self.contextMenu.addMenu(self.menu_2)
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Legend):
                self.contextMenu = QMenu()
                action_visible = self.contextMenu.addAction('隐藏图例')
                action_style = self.contextMenu.addAction('修改图例样式')
                action_visible.triggered.connect(lambda: self.event_slot('legend', False))
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
                action_style.triggered.connect(lambda: line2d_setting.Window(event, self.canvas))
                action_trend_line.triggered.connect(lambda: self.generate_trend_line(event))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if isinstance(event.artist, Annotation):
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除箭头')
                action_style = self.contextMenu.addAction('修改箭头样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: arrow_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if type(event.artist) == Text:
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除文字')
                action_style = self.contextMenu.addAction('修改文字样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: text_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()
            if type(event.artist) == AnnotationBbox:
                self.contextMenu = QMenu()
                action_delete = self.contextMenu.addAction('删除图片')
                action_style = self.contextMenu.addAction('修改图片样式')
                action_delete.triggered.connect(lambda: self.delete_artist(event))
                action_style.triggered.connect(lambda: image_setting.Window(event, self.canvas))
                self.contextMenu.popup(QCursor.pos())
                self.contextMenu.show()

    def help_slot(self):
        webbrowser.open("https://gitee.com/py2cn/pyminer/tree/master/pyminer2/extensions/packages/pmagg")

    def open_mpl_website_slot(self):
        webbrowser.open("https://matplotlib.org/")

    def show_color_table_slot(self):
        color_table.Window()

    def show_toolbar_slot(self):
        self.toolBar.setVisible(not self.toolBar.isVisible())

    def show_menubar_slot(self):
        self.menuBar.setVisible(not self.menuBar.isVisible())

    def show(self):
        # 使pmagg每次绘图之后，窗口在最前
        self.activateWindow()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        super(Window, self).show()
        ipython = get_ipython()
        if ipython is not None:
            ipython.magic("gui qt5")
        else:
            QtWidgets.QApplication.instance().exec_()


class FigureManagerPyMiner(FigureManagerBase):

    def show(self):
        agg = Window()
        agg.get_canvas(self.canvas.figure)
        agg.show()


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
