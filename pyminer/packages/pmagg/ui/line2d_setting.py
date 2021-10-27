from PySide2 import QtWidgets, QtGui, QtCore
import matplotlib.colors as mcolors
from .linestyles import *

class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Line2D Setting')
        self.legends = []
        self.artist = event.artist
        self.canvas = canvas
        self.linewidth_lineedit = QtWidgets.QLineEdit()
        self.markersize_lineedit = QtWidgets.QLineEdit()
        self.markeredgesize_lineedit = QtWidgets.QLineEdit()
        self.linestyle_combox = QtWidgets.QComboBox()
        self.marker_combox = QtWidgets.QComboBox()
        self.color_combox = QtWidgets.QComboBox()
        self.markeredgecolor_combox = QtWidgets.QComboBox()
        self.markerfacecolor_combox = QtWidgets.QComboBox()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')

        self.set_combox_items()
        self.horizontalSlider = QtWidgets.QSlider()
        self.horizontalSlider.setMaximum(100)
        alpha=event.artist.get_alpha()
        self.horizontalSlider.setProperty("value",100 if alpha is None else int(alpha*100))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)
        validator=QtGui.QDoubleValidator()
        validator.setRange(0,100)
        self.linewidth_lineedit.setValidator(validator)
        self.markersize_lineedit.setValidator(validator)
        self.markeredgesize_lineedit.setValidator(validator)
        self.linewidth_lineedit.setText(str(event.artist.get_linewidth()))
        self.markersize_lineedit.setText(str(event.artist.get_markersize()))
        self.markeredgesize_lineedit.setText(str(event.artist.get_markeredgewidth()))
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('线宽', self.linewidth_lineedit)
        self.layout.addRow('颜色', self.color_combox)
        self.layout.addRow('线型', self.linestyle_combox)
        self.layout.addRow('点状', self.marker_combox)
        self.layout.addRow('点大小', self.markersize_lineedit)
        self.layout.addRow('点边缘宽度', self.markeredgesize_lineedit)
        self.layout.addRow('点内部颜色', self.markerfacecolor_combox)
        self.layout.addRow('点边缘色', self.markeredgecolor_combox)
        self.layout.addRow('透明度', self.horizontalSlider)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec_()

    def confirm_slot(self):
        self.artist.set_color(self.color_combox.currentText())
        self.artist.set_markeredgecolor(self.markeredgecolor_combox.currentText())
        self.artist.set_markerfacecolor(self.markerfacecolor_combox.currentText())
        self.artist.set_linestyle(self.linestyle_combox.currentText())
        self.artist.set_linewidth(float(self.linewidth_lineedit.text()))
        self.artist.set_markeredgewidth(float(self.markeredgesize_lineedit.text()))
        self.artist.set_markersize(float(self.markersize_lineedit.text()))
        self.artist.set_marker(self.marker_combox.currentText())
        self.artist.set_alpha(self.horizontalSlider.value()/100)
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()

    def set_combox_items(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.color_combox.addItem(color_name)
            self.markerfacecolor_combox.addItem(color_name)
            self.markeredgecolor_combox.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.color_combox.model().item(index).setBackground(color)
            self.markerfacecolor_combox.model().item(index).setBackground(color)
            self.markeredgecolor_combox.model().item(index).setBackground(color)
            index += 1
        self.linestyle_combox.addItems(linestyles)
        self.linestyle_combox.setCurrentText(self.artist.get_linestyle())
        self.marker_combox.addItems(markers)
        self.marker_combox.setCurrentText(self.artist.get_marker())
        self.color_combox.setCurrentText(self.artist.get_color())
        self.markeredgecolor_combox.setCurrentText(self.artist.get_markeredgecolor())
        self.markerfacecolor_combox.setCurrentText(self.artist.get_markerfacecolor())
