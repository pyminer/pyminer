"""
负责对生成的ui类绑定事件，添加交互逻辑
"""
import os
from .axis_edit import Ui_Dialog
from PySide2 import QtWidgets, QtGui
import configparser
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import LogLocator, MaxNLocator, MultipleLocator, LinearLocator, ScalarFormatter
import matplotlib.colors as mcolors
from .linestyles import *
import matplotlib as mpl


class Ui_Dialog_Manager(Ui_Dialog):
    def __init__(self, ax, canvas: FigureCanvas, path,parent):
        self.ax = ax
        self.canvas = canvas
        self.current_path = path
        self.parent=parent
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.retranslateUi(self.dialog)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(['子图'])
        self.axes = self.canvas.figure.get_axes()
        for index, item in enumerate(range(len(self.axes))):
            root = QtWidgets.QTreeWidgetItem(self.treeWidget)
            root.setText(0, '子图' + str(index + 1))
            root.setIcon(0, QtGui.QIcon(os.path.join(self.current_path, 'icons/figure.png')))
            self.treeWidget.addTopLevelItem(root)
            ax = self.axes[index]
            if hasattr(ax, 'xaxis'):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, 'X轴')
                child.setIcon(0, QtGui.QIcon(os.path.join(self.current_path, 'icons/X_axis.png')))
                root.addChild(child)
            if hasattr(ax, 'yaxis'):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, 'Y轴')
                child.setIcon(0, QtGui.QIcon(os.path.join(self.current_path, 'icons/Y_axis.png')))
                root.addChild(child)
            if hasattr(ax, 'zaxis'):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, 'Z轴')
                child.setIcon(0, QtGui.QIcon(os.path.join(self.current_path, 'icons/Z_axis.png')))
                root.addChild(child)
        self.treeWidget.clicked.connect(self.on_clicked)
        self.pushButton_3.clicked.connect(self.apply_slot)
        self.pushButton_2.clicked.connect(self.cancel_slot)
        self.pushButton.clicked.connect(self.confirm_slot)
        self.current_subplot = None
        self.current_ax = None
        self.current_ax_attribute = None  # 判断当前是X轴还是Y轴，Z轴
        self.axes_is_AxesSubplot = None
        self.axes_is_PolarAxesSubplot = None
        self.ticks_directions = ['in', 'out', 'inout']
        self.axis_positions=['axes','outward','data']
        self.comboBox_2.addItems(self.ticks_directions)
        self.comboBox_6.addItems(linestyles)
        self.comboBox_7.addItems(self.axis_positions)
        self.grid_combox_setting()
        self.comboBox_5.addItems(grid_which)
        # 输入校验
        self.double_validator = QtGui.QDoubleValidator()
        for item in [self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_7,
                     self.lineEdit_8]:
            item.setValidator(self.double_validator)
        self.dialog.exec_()  # 初始化之后再执行

    def clear_value(self):
        ax_min = ax_max = ''
        # 清除所有值
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_7.setText('')
        self.checkBox_3.setChecked(True)

    def on_clicked(self):
        self.item = self.treeWidget.currentItem()
        ax_min = ax_max = ''
        self.clear_value()
        if self.item.parent() is None:
            self.current_subplot = self.axes[int(self.item.text(0)[-1]) - 1]
            self.current_ax = self.current_subplot.xaxis
            ax_min, ax_max = self.current_subplot.get_xlim()
            self.current_ax_attribute = 'X'
            self.checkBox_6.setChecked(self.current_subplot.spines['bottom'].get_visible())
            position=self.current_subplot.spines['bottom'].get_position()
            self.lineEdit_7.setText(str(position[1]))
            self.comboBox_7.setCurrentText(str(position[0]))
        else:
            self.current_subplot = self.axes[int(self.item.parent().text(0)[-1]) - 1]
        if self.item.text(0)[0] == 'X':
            self.current_ax = self.current_subplot.xaxis
            ax_min, ax_max = self.current_subplot.get_xlim()
            self.lineEdit_5.setText(self.current_subplot.get_xlabel())
            self.current_ax_attribute = 'X'
            self.checkBox_6.setChecked(self.current_subplot.spines['bottom'].get_visible())
            position = self.current_subplot.spines['bottom'].get_position()
            self.lineEdit_7.setText(str(position[1]))
            self.comboBox_7.setCurrentText(str(position[0]))
        if self.item.text(0)[0] == 'Y':
            self.current_ax = self.current_subplot.yaxis
            ax_min, ax_max = self.current_subplot.get_ylim()
            self.current_ax_attribute = 'Y'
            self.checkBox_6.setChecked(self.current_subplot.spines['left'].get_visible())
            position = self.current_subplot.spines['left'].get_position()
            self.lineEdit_7.setText(str(position[1]))
            self.comboBox_7.setCurrentText(str(position[0]))
        if self.item.text(0)[0] == 'Z':
            self.current_ax = self.current_subplot.zaxis
            ax_min, ax_max = self.current_subplot.get_zlim()
            self.current_ax_attribute = 'Z'
        self.axes_is_AxesSubplot = self.current_subplot.__class__.__name__ == 'AxesSubplot'  # 该类是工厂生成的类，不会存在模块级别
        self.axes_is_PolarAxesSubplot = self.current_subplot.__class__.__name__ == 'PolarAxesSubplot'
        for item in [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5,
                     self.checkBox_6, self.lineEdit_8, self.lineEdit_7]:
            item.setEnabled(self.axes_is_AxesSubplot)
        self.lineEdit.setText(self.format_number(ax_min))
        self.lineEdit_2.setText(self.format_number(ax_max))
        self.scale_is_linear = self.current_ax.get_scale() == 'linear'
        self.lineEdit_3.setEnabled(self.scale_is_linear)
        self.lineEdit_4.setEnabled(self.scale_is_linear)
        self.lineEdit_5.setText(self.current_ax.get_label_text())
        self.doubleSpinBox_2.setValue(self.current_ax.label.get_fontsize())
        major_labels = self.current_ax.get_ticklabels()
        if major_labels:
            self.doubleSpinBox_3.setValue(major_labels[0].get_fontsize())
        self.linear_axis_setting()
        self.checkBox_8.setChecked(self.current_ax._major_tick_kw.get('gridOn', False))
        self.comboBox_4.setCurrentText(self.current_ax._major_tick_kw.get('grid_color'))
        grid_alpha = self.current_ax._major_tick_kw.get('grid_alpha')
        grid_alpha = 50 if grid_alpha is None else int(grid_alpha * 100)  # 默认0.5透明度
        self.horizontalSlider.setValue(grid_alpha)
        grid_linewidth = self.current_ax._major_tick_kw.get('grid_linewidth')
        if grid_linewidth is None:
            grid_linewidth = 0.5
        self.doubleSpinBox.setValue(grid_linewidth)
        grid_linestyle = self.current_ax._major_tick_kw.get('grid_linestyle')
        if grid_linestyle is None:
            grid_linestyle = '-'
        self.comboBox_6.setCurrentText(grid_linestyle)
        # 实现轴刻度和轴标签的状态更新
        self.checkBox_2.setChecked(self.current_ax._major_tick_kw.get('tick1On'))
        self.checkBox.setChecked(self.current_ax._major_tick_kw.get('label1On'))
        self.checkBox_4.setChecked(self.current_ax._major_tick_kw.get('tick2On'))
        self.checkBox_5.setChecked(self.current_ax._major_tick_kw.get('label2On'))
        direction = self.current_ax._major_tick_kw.get('tickdir')
        if direction is None:
            direction = 'out'
        self.comboBox_2.setCurrentText(direction)
        label_rotation = self.current_ax._major_tick_kw.get('labelrotation')
        if label_rotation is None:
            label_rotation = 0
        self.lineEdit_8.setText(str(label_rotation))

    def linear_axis_setting(self):
        """主刻度，次刻度间隔获取，如果刻度标签是数字则获取差值，如果不是数字，坐标轴是二维线性，获取文字位置的差值"""
        if self.current_ax is None: return
        scale_is_linear = self.current_ax.get_scale() == 'linear'
        if self.scale_is_linear:
            self.lineEdit_3.setEnabled(scale_is_linear)
            self.lineEdit_4.setEnabled(scale_is_linear)
            major_labels = self.current_ax.get_ticklabels()
            minor_labels = self.current_ax.get_ticklabels(minor=True)
            self.lineEdit_3.setText(self._get_labels_spacing(major_labels))
            self.lineEdit_4.setText(self._get_labels_spacing(minor_labels))

    def _get_labels_spacing(self, labels):
        spacing = ''
        if len(labels) >= 2:
            label1 = labels[0].get_text()
            label2 = labels[1].get_text()
            if self.is_number(label2) and self.is_number(label1):
                spacing = float(label2) - float(label1)
            elif self.axes_is_AxesSubplot or self.axes_is_PolarAxesSubplot:
                label1 = labels[0].get_position()
                label2 = labels[1].get_position()
                if self.current_ax_attribute == 'X':
                    spacing = label2[0] - label1[0]
                if self.current_ax_attribute == 'Y':
                    spacing = label2[1] - label1[1]
        return self.format_number(spacing)

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def format_number(num, decimal=12):
        if num == '': return num
        front, back = str(num * 1.0).split('.')
        if len(back) >= decimal:
            result = front + '.' + back[:decimal]
        else:
            result = front + '.' + back[:]
        return result

    def grid_combox_setting(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.comboBox_4.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.comboBox_4.model().item(index).setBackground(color)
            index += 1

    def apply_slot(self):
        if not len(self.axes) or not self.current_subplot or not self.current_ax:
            return
        if self.current_ax_attribute == 'X':
            self.current_subplot.set_xlim(float(self.lineEdit.text()), float(self.lineEdit_2.text()))
            if self.axes_is_AxesSubplot:
                self.current_subplot.spines['bottom'].set_visible(self.checkBox_6.isChecked())
                self.current_subplot.spines['top'].set_visible(self.checkBox_3.isChecked())
                self.current_subplot.spines['bottom'].set_position(
                    (self.comboBox_7.currentText(),
                     float(self.lineEdit_7.text())
                     )
                )
                self.current_ax.set_tick_params(which='both',
                                                bottom=self.checkBox_2.isChecked(),
                                                top=self.checkBox_4.isChecked(),
                                                labelbottom=self.checkBox.isChecked(),
                                                labeltop=self.checkBox_5.isChecked())
        if self.current_ax_attribute == 'Y':
            self.current_subplot.set_ylim(float(self.lineEdit.text()), float(self.lineEdit_2.text()))
            if self.axes_is_AxesSubplot:
                self.current_subplot.spines['left'].set_visible(self.checkBox_6.isChecked())
                self.current_subplot.spines['right'].set_visible(self.checkBox_3.isChecked())
                # 设置坐标轴位置
                self.current_subplot.spines['left'].set_position(
                    (self.comboBox_7.currentText(),
                     float(self.lineEdit_7.text())
                     )
                )
                self.current_ax.set_tick_params(which='both',
                                                left=self.checkBox_2.isChecked(),
                                                right=self.checkBox_4.isChecked(),
                                                labelleft=self.checkBox.isChecked(),
                                                labelright=self.checkBox_5.isChecked())
        if self.current_ax_attribute == 'Z':
            self.current_subplot.set_zlim(float(self.lineEdit.text()), float(self.lineEdit_2.text()))
        if self.scale_is_linear:
            if self.is_number(self.lineEdit_3.text()):
                major_tick_spacing = float(self.lineEdit_3.text())
                self.current_ax.set_major_locator(MultipleLocator(major_tick_spacing))
            if self.is_number(self.lineEdit_4.text()):
                minor_tick_spacing = float(self.lineEdit_4.text())
                self.current_ax.set_minor_locator(MultipleLocator(minor_tick_spacing))
        self.current_ax.set_label_text(
            self.lineEdit_5.text(),
            fontdict={'size': self.doubleSpinBox_2.value()})
        self.current_ax.set_tick_params(
            gridOn=self.checkBox_8.isChecked(),
            direction=self.comboBox_2.currentText(),
            which=self.comboBox_5.currentText(),
            labelsize=self.doubleSpinBox_3.value(),
            grid_color=self.comboBox_4.currentText(),
            grid_alpha=self.horizontalSlider.value() / 100,
            grid_linestyle=self.comboBox_6.currentText(),
            grid_linewidth=self.doubleSpinBox.value(),
            rotation=float(self.lineEdit_8.text()))
        self.parent.set_all_fonts()
        self.canvas.draw()

    def cancel_slot(self):
        self.dialog.close()

    def confirm_slot(self):
        self.apply_slot()
        self.dialog.close()
