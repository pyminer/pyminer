from PySide2 import QtWidgets, QtGui
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from .linestyles import norms


class Window(QtWidgets.QDialog):
    def __init__(self,canvas):
        super().__init__()
        self.setWindowTitle('颜色条设置')
        self.axes = []
        self.mappable = None
        self.canvas = canvas
        self.double_validator = QtGui.QDoubleValidator()
        self.axes_combox = QtWidgets.QComboBox()
        self.axes_combox.currentIndexChanged.connect(self.switch_axes_slot)
        self.colormaps_combox = QtWidgets.QComboBox()
        self.min_lineedit = QtWidgets.QLineEdit()
        self.max_lineedit = QtWidgets.QLineEdit()
        self.pad_lineedit = QtWidgets.QLineEdit()
        self.update_radio = QtWidgets.QRadioButton()
        self.update_radio.setChecked(True)
        self.add_radio = QtWidgets.QRadioButton()
        self.pad_lineedit.setValidator(self.double_validator)
        self.center_lineedit = QtWidgets.QLineEdit()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.colormaps_combox.addItems(sorted(plt.colormaps(), key=lambda x: x.lower()))
        self.layout = QtWidgets.QFormLayout()
        self.set_combox_items()
        self.layout.addRow('能添加颜色条的子图', self.axes_combox)
        self.layout.addRow('样式', self.colormaps_combox)
        self.layout.addRow('最小(可空)', self.min_lineedit)
        self.layout.addRow('最大(可空)', self.max_lineedit)
        self.layout.addRow('仅更新样式', self.update_radio)
        self.layout.addRow('添加颜色条', self.add_radio)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.setLayout(self.layout)
        self.colorbar = None
        self.exec_()

    def confirm_slot(self):
        cmap = plt.get_cmap(self.colormaps_combox.currentText())  # 根据名称获取cmap
        vmin = float(self.min_lineedit.text()) if self.min_lineedit.text() != '' else None
        vmax = float(self.max_lineedit.text()) if self.max_lineedit.text() != '' else None
        norm = mcolors.Normalize(vmin, vmax)
        if self.add_radio.isChecked():
            self.mappable.cmap = cmap
            self.mappable.norm = norm
            self.canvas.figure.colorbar(self.mappable, ax=self.current_subplot)
        else:
            self.mappable.autoscale()
            self.mappable.cmap = cmap
            self.mappable.norm = norm
            if self.mappable.colorbar:
                self.mappable.colorbar.norm = norm
                self.mappable.colorbar.update_normal(self.mappable)
        self.canvas.draw_idle()

    def switch_axes_slot(self):
        self.current_subplot = self.axes[self.axes_combox.currentIndex()]
        if len(self.current_subplot.collections) == 1:
            self.mappable = self.current_subplot.collections[0]
        if len(self.current_subplot.images) == 1:
            self.mappable = self.current_subplot.images[0]
        vmin = '' if self.mappable.norm.vmin is None else str(self.mappable.norm.vmin)
        vmax = '' if self.mappable.norm.vmax is None else str(self.mappable.norm.vmax)
        self.min_lineedit.setText(vmin)
        self.max_lineedit.setText(vmax)

    def set_combox_items(self):
        index = 1
        for ax in self.canvas.figure.get_axes():
            bbox = ax.get_window_extent().transformed(self.canvas.figure.dpi_scale_trans.inverted())
            width, height = bbox.width, bbox.height
            if len(ax.collections) == 1 or len(ax.images) == 1:
                if height/width<10: # 利用图像像素长宽比区分colorbar和正常的图形，因为很难判断了
                    self.axes.append(ax)
                    self.axes_combox.addItem('图' + str(index))
                    index += 1
        if self.axes == []:
            self.confirm_button.setEnabled(False)

    def cancel_slot(self):
        self.close()
