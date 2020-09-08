# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 10:29
# @Author  : 别着急慢慢来
# @FileName: PMAgg.py


import os
import sys
import time
import numpy as np
import threading
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QIcon, QCursor
import matplotlib
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from pmagg_ui import Ui_MainWindow
from axes_control_manager import Ui_Form_Manager
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QDialog, QAction, QWidget, QSizePolicy, QMenu, QFileDialog
from matplotlib.lines import Line2D

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

    def __init__(self, figure):
        super(Window, self).__init__()
        self.setupUi(self)  # 先执行父类方法，以产生成员变量
        self.figure = figure
        self.canvas = FigureCanvas(self.figure)  # 这里的canvas就是曲线图
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()  # 隐藏QT原来的工具栏
        # self.graphicsView.addWidget(self.canvas)  # 将canvas渲染到布局中
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
        self.actionX_X.triggered.connect(self.axes_control_slot)
        # 初始化当前界面
        self.init_gui()
        # 槽函数连接
        # 当前子图对象切换
        self.current_path = os.path.dirname(__file__)
        self.saveAction = QAction(QIcon(os.path.join(self.current_path, 'icons/save.png')), 'save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.save_slot)
        self.toolBar.addAction(self.saveAction)

        self.settingAction = QAction(QIcon(os.path.join(self.current_path, 'icons/setting.png')), 'setting', self)
        self.settingAction.triggered.connect(self.axes_control_slot)
        self.toolBar.addAction(self.settingAction)

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

        self.textAction = QAction(QIcon(os.path.join(self.current_path, 'icons/text.png')), 'text', self)
        self.textAction.triggered.connect(self.add_text_slot)
        self.toolBar.addAction(self.textAction)

        self.rectAction = QAction(QIcon(os.path.join(self.current_path, 'icons/rect.png')), 'rect', self)
        self.rectAction.triggered.connect(self.add_rect_slot)
        self.toolBar.addAction(self.rectAction)

        self.ovalAction = QAction(QIcon(os.path.join(self.current_path, 'icons/oval.png')), 'oval', self)
        self.ovalAction.triggered.connect(self.add_oval_slot)
        self.toolBar.addAction(self.ovalAction)

        self.arrowAction = QAction(QIcon(os.path.join(self.current_path, 'icons/arrow.png')), 'arrow', self)
        self.arrowAction.triggered.connect(self.add_arrow_slot)
        self.toolBar.addAction(self.arrowAction)

        self.pointAction = QAction(QIcon(os.path.join(self.current_path, 'icons/point.png')), 'point', self)
        self.pointAction.triggered.connect(self.add_point_slot)
        self.toolBar.addAction(self.pointAction)

        self.styleAction = QAction(QIcon(os.path.join(self.current_path, 'icons/style.png')), 'style', self)
        self.styleAction.triggered.connect(self.add_style_slot)
        self.toolBar.addAction(self.styleAction)

        # 将下拉菜单放在最右边
        self.toolBar.addSeparator()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.toolBar.addWidget(self.comboBox)

        # 以上为工具栏1

        self.gridAction = QAction(QIcon(os.path.join(self.current_path, 'icons/grid.png')), '显示/隐藏网格', self)
        self.gridAction.triggered.connect(self.show_grid_slot)
        self.toolBar_2.addAction(self.gridAction)

        self.legendAction = QAction(QIcon(os.path.join(self.current_path, 'icons/legend.png')), '显示/隐藏图例', self)
        self.legendAction.triggered.connect(self.show_legend_slot)
        self.toolBar_2.addAction(self.legendAction)

        self.colorbarAction = QAction(QIcon(os.path.join(self.current_path, 'icons/colorbar.png')), '显示/隐藏colorbar',
                                      self)
        self.colorbarAction.triggered.connect(self.show_colorbar_slot)
        self.toolBar_2.addAction(self.colorbarAction)

        self.layoutAction = QAction(QIcon(os.path.join(self.current_path, 'icons/layout.png')), '改变布局', self)
        # self.layoutAction.triggered.connect(self.show_layout_slot)
        self.toolBar_2.addAction(self.layoutAction)

        self.mainViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/mainView.png')), 'mainView', self)
        self.mainViewAction.triggered.connect(self.mainView_slot)
        self.toolBar_2.addAction(self.mainViewAction)

        self.leftViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/leftView.png')), 'leftView', self)
        self.leftViewAction.triggered.connect(self.leftView_slot)
        self.toolBar_2.addAction(self.leftViewAction)

        self.rightViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/rightView.png')), 'rightView', self)
        self.rightViewAction.triggered.connect(self.rightView_slot)
        self.toolBar_2.addAction(self.rightViewAction)

        self.topViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/topView.png')), 'topView', self)
        self.topViewAction.triggered.connect(self.topView_slot)
        self.toolBar_2.addAction(self.topViewAction)

        self.bottomViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/bottomView.png')), 'bottomView',
                                        self)
        self.bottomViewAction.triggered.connect(self.bottomView_slot)
        self.toolBar_2.addAction(self.bottomViewAction)

        self.backViewAction = QAction(QIcon(os.path.join(self.current_path, 'icons/backView.png')), 'backView', self)
        self.backViewAction.triggered.connect(self.backView_slot)
        self.toolBar_2.addAction(self.backViewAction)

        # 样式右键菜单功能集
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.rightMenuShow()  # 创建上下文菜单

        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        # 获取子图对象
        self.axes = self.canvas.figure.get_axes()
        if not self.axes:
            QtWidgets.QMessageBox.warning(
                self.canvas.parent(), "Error", "There are no axes to edit.")
            return
        elif len(self.axes) == 1:
            self.current_subplot, = self.axes
            titles = ['图1']
        else:
            titles = ['图' + str(i + 1) for i in range(len(self.axes))]
        # 将三维图的初始视角保存下来，便于旋转之后可以复原
        self.init_views = [(index, item.azim, item.elev) for index, item in enumerate(self.axes) if
                           hasattr(item, 'azim')]
        self.comboBox.addItems(titles)

        # 鼠标拖拽，实现三维图形旋转功能
        self.canvas.mpl_connect('motion_notify_event', self.on_rotate)
        # 鼠标拖拽，实现画矩形功能
        self.canvas.mpl_connect('motion_notify_event', self.add_rect)
        self.mouse_pressed = False
        # 鼠标拖拽，实现画椭圆和按住shift画圆的功能实现
        self.canvas.mpl_connect('motion_notify_event', self.add_oval)
        # 画箭头
        self.canvas.mpl_connect('motion_notify_event', self.add_arrow)
        # 画点，并且按住点能够移动
        self.canvas.mpl_connect('button_press_event', self.add_point)
        self.canvas.mpl_connect('motion_notify_event', self.add_point)
        self.canvas.mpl_connect('button_release_event', self.add_point)
        self.canvas.mpl_connect('pick_event', self.add_point)
        self.press_time = 0
        # 记录鼠标运动的位置
        self.rotate_mouse_point = None
        self.canvas.mpl_connect('button_press_event', self.add_text)
        # 为曲线添加样式的功能实现
        self.canvas.mpl_connect('button_press_event', self.add_style)
        self.canvas.mpl_connect('pick_event', self.add_style)
        # 为图例绑定监听事件
        self.canvas.mpl_connect('button_press_event', self.change_legend)
        self.canvas.mpl_connect('pick_event', self.change_legend)
        # 所有的按钮标志
        self.make_flag_invalid()
        self.artist = None
        for ax in self.axes:
            for line in ax.lines:
                line.set_picker(True)
                line.set_pickradius(5)

    def make_flag_invalid(self):
        self.add_rect_flag = False
        self.add_oval_flag = False
        self.add_text_flag = False
        self.rotate_flag = False
        self.home_flag = False
        self.pan_flag = False
        self.zoom_flag = False
        self.add_arrow_flag = False
        self.add_point_flag = False
        self.add_style_flag = False
        self.show_grid_flag = False
        self.show_legend_flag = False
        # 禁用移动和缩放
        self.toolbar.mode = None

    def home_slot(self):
        self.make_flag_invalid()
        self.home_flag = not self.home_flag
        self.home()

    def home(self):
        """
        matplotlib lines里面放曲线，patches可以放图形，artists也可以放东西，设为空则可以删除对应的对象
        """
        if not self.home_flag:
            return
        self.toolbar.home()
        # 将三维图视角还原
        for item in self.init_views:
            self.axes[item[0]].view_init(azim=item[1], elev=item[2])
        # 将所有添加的形状去除
        for item in self.axes:
            item.patches = []
            item.artists = []  # 去除画在图中的点，是否需要去掉有待考究
        self.canvas.draw()

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
        self.toolbar.save_figure()

    def front_slot(self):
        self.toolbar._nav_stack.forward()
        self.toolbar._update_view()

    def back_slot(self):
        self.toolbar._nav_stack.back()
        self.toolbar._update_view()

    def add_text_slot(self):
        self.make_flag_invalid()
        self.add_text_flag = not self.add_text_flag

    def add_text(self, event):
        if not self.add_text_flag:
            return
        if self.add_text_flag and event.xdata and event.ydata and not hasattr(event.inaxes, 'azim'):
            text, ok = QtWidgets.QInputDialog.getText(self.canvas.parent(), '输入文字', '添加注释')
            if ok and text:
                event.inaxes.text(event.xdata, event.ydata, text)
                # plt.text(event.xdata, event.ydata, text)
                self.canvas.draw()

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
                    delta_azim = 180 * event.xdata * -1 / 0.1
                    delta_elev = 180 * event.ydata / 0.1
                    azim = delta_azim + item[1]
                    elev = delta_elev + item[2]
                    event.inaxes.view_init(azim=azim, elev=elev)
                    self.canvas.draw()

    def add_rect_slot(self):
        # 除了本标记，其余全置False
        self.make_flag_invalid()
        self.add_rect_flag = not self.add_rect_flag

    def add_rect(self, event):
        if not self.add_rect_flag:
            return
        if not event.button and event.inaxes:
            self.ax_init = event
            if self.mouse_pressed and event.inaxes.patches:
                event.inaxes.add_patch(event.inaxes.patches[0])
            self.mouse_pressed = False

        # 仅能在二维图形中画矩形，鼠标按下，且当前子图和初始点的子图相同
        try:
            if event.button and event.inaxes and event.inaxes == self.ax_init.inaxes and not hasattr(event.inaxes,
                                                                                                     'azim'):
                self.mouse_pressed = True
                if event.inaxes.patches:
                    event.inaxes.patches.pop()
                rect = plt.Rectangle((self.ax_init.xdata, self.ax_init.ydata), event.xdata - self.ax_init.xdata,
                                     event.ydata - self.ax_init.ydata,
                                     fill=False, edgecolor='red', linewidth=1)
                event.inaxes.add_patch(rect)
                self.canvas.draw()
                self.canvas.flush_events()
        except Exception:
            pass

    def add_oval_slot(self):
        self.make_flag_invalid()
        self.add_oval_flag = not self.add_oval_flag

    def add_oval(self, event):
        if not self.add_oval_flag:
            return
        if not event.button and event.inaxes:
            self.ax_init = event
            if self.mouse_pressed and event.inaxes.patches:
                event.inaxes.add_patch(event.inaxes.patches[0])
            self.mouse_pressed = False
        try:
            if event.button and event.inaxes and event.inaxes == self.ax_init.inaxes and not hasattr(event.inaxes,
                                                                                                     'azim'):
                self.mouse_pressed = True
                if event.inaxes.patches:
                    event.inaxes.patches.pop()
                oval = Ellipse(xy=(self.ax_init.xdata, self.ax_init.ydata),
                               width=abs(event.xdata - self.ax_init.xdata) * 2,
                               height=abs(event.ydata - self.ax_init.ydata) * 2, angle=0, fill=False, edgecolor='red',
                               linewidth=1)
                event.inaxes.add_patch(oval)
                self.canvas.draw()
                self.canvas.flush_events()
        except Exception:
            pass

    def add_arrow_slot(self):
        self.make_flag_invalid()
        self.add_arrow_flag = not self.add_arrow_flag

    def add_arrow(self, event):
        if not self.add_arrow_flag:
            return
        if not event.button and event.inaxes:
            self.ax_init = event
            if self.mouse_pressed and event.inaxes.patches:
                event.inaxes.add_patch(event.inaxes.patches[0])
            self.mouse_pressed = False
        try:
            if event.button and event.inaxes and event.inaxes == self.ax_init.inaxes and not hasattr(event.inaxes,
                                                                                                     'azim'):
                self.mouse_pressed = True
                if event.inaxes.patches:
                    event.inaxes.patches.pop()
                arrow = event.inaxes.arrow(self.ax_init.xdata, self.ax_init.ydata, event.xdata - self.ax_init.xdata,
                                           event.ydata - self.ax_init.ydata, width=0.01, length_includes_head=True,
                                           head_width=0.05, head_length=0.1, fc='r', ec='r')
                event.inaxes.add_patch(arrow)
                # 请恕我无知，我也不懂这里为什么还要pop一次，我不想思考，但的确这样是正确的。
                if event.inaxes.patches:
                    event.inaxes.patches.pop()
                self.canvas.draw()
                self.canvas.flush_events()
        except Exception:
            pass

    def add_point_slot(self):
        self.make_flag_invalid()
        self.add_point_flag = not self.add_point_flag

    # def add_point(self, event):
    #     if not self.add_point_flag:
    #         return
    #     if event.inaxes and event.button and not hasattr(event.inaxes, 'azim'):
    #         x_range = np.array(event.inaxes.get_xlim())
    #         y_range = np.array(event.inaxes.get_ylim())
    #         self.offset = np.sqrt(np.sum((x_range - y_range) ** 2)) / 20 # 将坐标轴范围的1/50视为误差
    #         self.nearest_point = None
    #         d_min = 10 * self.offset
    #         for point in event.inaxes.artists:
    #             xt, yt = point.get_data()
    #             d = ((xt - event.xdata) ** 2 + (yt - event.ydata) ** 2) ** 0.5
    #             if d <= self.offset and d < d_min:  # 如果在误差范围内，移动该点
    #                 d_min = d
    #                 self.nearest_point = point
    #         if self.nearest_point:
    #             new_point = Line2D([event.xdata], [event.ydata], ls="",
    #                                marker='o', markerfacecolor='r',
    #                                animated=False)
    #             event.inaxes.add_artist(new_point)
    #             event.inaxes.artists.remove(self.nearest_point)
    #             self.canvas.restore_region(self.bg)
    #             event.inaxes.draw_artist(new_point)
    #             self.canvas.blit(event.inaxes.bbox)
    #             self.bg = self.canvas.copy_from_bbox(event.inaxes.bbox)
    def add_point(self, event):
        if not self.add_point_flag:
            return
        if event.name == 'pick_event':
            self.artist = event.artist
            return
        if event.name == 'button_press_event' and not self.artist and hasattr(event, 'inaxes') and not hasattr(
                event.inaxes, 'azim'):
            point = Line2D([event.xdata], [event.ydata], ls="",
                           marker='o', markerfacecolor='r',
                           animated=False, pickradius=5, picker=True)
            event.inaxes.add_artist(point)
            self.canvas.draw()
            return
        if event.name == 'motion_notify_event' and self.artist and hasattr(event,
                                                                           'inaxes') and event.button and not hasattr(
            event.inaxes, 'azim'):
            xy = self.artist.get_data()
            if len(xy[0]) == 1:  # 判断该对象是否是一个点。
                self.artist.set_data(([event.xdata], [event.ydata]))
                self.canvas.draw()
        if event.name == 'button_release_event':
            self.artist = None

    def add_style_slot(self):
        self.make_flag_invalid()
        self.add_style_flag = not self.add_style_flag

    def add_style(self, event):
        if not self.add_style_flag:
            return
        if event.name == 'pick_event':
            self.artist = event.artist
        if self.artist and event.name == 'button_press_event':
            for line in event.inaxes.lines:
                if self.artist != line:
                    line.set_alpha(0.5)
                else:
                    line.set_alpha(1)
            self.canvas.draw_idle()
            if event.button == 3:
                self.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
                self.contextMenu.show()
                return
            elif event.button == 1:
                self.artist = None
                return
        if not self.artist and event.name == 'button_press_event' and event.button == 1:
            for line in event.inaxes.lines:
                line.set_alpha(1)
            self.canvas.draw_idle()

    def show_legend_slot(self):
        legend_titles = []
        for index in range(len(self.current_subplot.lines)):
            legend_titles.append('curve ' + str(index + 1))  # 从1开始算
        if self.current_subplot.lines:  # 如果存在曲线才允许画图例
            leg = self.current_subplot.legend(self.current_subplot.lines, legend_titles)
            leg.set_draggable(True) # 设置legend可拖拽
            for legline in leg.get_lines():
                legline.set_pickradius(10)
                legline.set_picker(True)  # 给每个legend设置可点击
            self.canvas.draw()

    def change_legend(self, event):
        if event.name == 'pick_event':
            self.artist = event.artist
        if self.artist and event.name == 'button_press_event' and event.button == 3:
            self.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
            self.contextMenu.show()

    def show_colorbar_slot(self):
        # print(self.current_subplot.curves)
        pass
        # self.canvas.figure.colorbar(self.canvas,self.current_subplot)

    def rightMenuShow(self):
        self.contextMenu = QMenu()
        self.actionStyle = self.contextMenu.addAction('修改曲线样式')
        self.actionLegend = self.contextMenu.addAction('修改图例样式')
        self.actionCurve = self.contextMenu.addAction('修改曲线类型')
        self.actionStyle.triggered.connect(self.styleHandler)
        self.actionLegend.triggered.connect(self.legendHandler)
        self.actionLegend.triggered.connect(self.curveHandler)

    def styleHandler(self):
        print(self.artist)

    def legendHandler(self):
        print(self.artist)

    def curveHandler(self):
        print(self.artist)

    def mainView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=0, elev=0)
            self.canvas.draw()

    def leftView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=90, elev=0)
            self.canvas.draw()

    def rightView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=-90, elev=0)
            self.canvas.draw()

    def topView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=0, elev=90)
            self.canvas.draw()

    def bottomView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=0, elev=-90)
            self.canvas.draw()

    def backView_slot(self):
        if hasattr(self.current_subplot, 'azim'):
            self.current_subplot.view_init(azim=180, elev=0)
            self.canvas.draw()

    def show_grid_slot(self):
        self.show_grid_flag = not self.show_grid_flag
        self.current_subplot.grid(self.show_grid_flag)
        self.canvas.draw_idle()

    def init_gui(self):
        self.toolbar._update_view()

    def combobox_slot(self):
        self.current_subplot = self.axes[self.comboBox.currentIndex()]  # 将当前选择付给子图对象

    def axes_control_slot(self):
        if not self.current_subplot:
            QtWidgets.QMessageBox.warning(
                self.canvas.parent(), "错误", "没有可选的子图！")
            return
        Ui_Form_Manager(self.current_subplot, self.canvas)

    def show(self):
        super().show()


class FigureManagerPyMiner(FigureManagerBase):
    def show(self):
        canvas = self.canvas
        app = QtWidgets.QApplication(sys.argv)
        main = Window(canvas.figure)
        main.setWindowTitle('Powered by PyMiner')
        main.show()
        app.exec_()
        # main.callback_pb_load()
        # app.quit()
        # app.exit(app.exec_())
        # sys.exit(app.exec_())


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
