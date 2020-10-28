from PyQt5 import QtWidgets, QtGui
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from .linestyles import norms


class Window(QtWidgets.QDialog):
    def __init__(self, ax, canvas):
        super().__init__()
        self.setWindowTitle('Colorbar Setting')
        self.ax = ax
        if not ax.collections:
            QtWidgets.QMessageBox.warning(
                self, "错误", "当前子图并没有Mappable对象！")
            return
        self.canvas = canvas
        self.collections_combox = QtWidgets.QComboBox()
        self.colormaps_combox = QtWidgets.QComboBox()
        self.norms_combox = QtWidgets.QComboBox()
        self.min_lineedit = QtWidgets.QLineEdit()
        self.max_lineedit = QtWidgets.QLineEdit()
        self.clip_checkbox = QtWidgets.QCheckBox()
        self.center_lineedit = QtWidgets.QLineEdit()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.collections_combox.addItems(list(map(str, range(len(self.ax.collections)))))
        self.colormaps_combox.addItems(sorted(plt.colormaps(), key=lambda x: x.lower()))
        self.norms_combox.addItems(norms)
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('Mappable', self.collections_combox)
        self.layout.addRow('Colormaps', self.colormaps_combox)
        self.layout.addRow('Norms', self.norms_combox)
        self.layout.addRow('最小(可空)', self.min_lineedit)
        self.layout.addRow('最大(可空)', self.max_lineedit)
        self.layout.addRow('映射0-1', self.clip_checkbox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.setLayout(self.layout)
        self.colorbar = None
        self.collection = None
        self.exec()

    def confirm_slot(self):
        cmap = plt.get_cmap(self.colormaps_combox.currentText())
        vmin = float(self.min_lineedit.text()) if self.min_lineedit.text() != '' else None
        vmax = float(self.max_lineedit.text()) if self.max_lineedit.text() != '' else None
        clip = self.clip_checkbox.isChecked()
        if self.collection:
            vmax = self.collection.norm.vmax if vmax is None else vmax
            vmin = self.collection.norm.vmin if vmin is None else vmin
        if clip:
            vmin, vmax = None, None
        if self.norms_combox.currentText() == 'Normalize':
            norm = mcolors.Normalize(vmin, vmax, clip)
        if self.norms_combox.currentText() == 'LogNorm':
            norm = mcolors.LogNorm(vmin, vmax, clip)
        if self.norms_combox.currentText() == 'NoNorm':
            norm = mcolors.NoNorm(vmin, vmax, clip)
        # self.ax.set_autoscale_on(True)
        if not self.colorbar:
            self.collection = self.ax.collections[self.collections_combox.currentIndex()]
            self.collection.cmap = cmap
            self.collection.norm = norm
            self.colorbar = self.canvas.figure.colorbar(self.ax.collections[self.collections_combox.currentIndex()],
                                                        ax=self.ax)
        else:
            self.collection.autoscale()
            self.collection.cmap = cmap
            self.collection.norm = norm
            self.colorbar.update_normal(self.collection)
            # self.colorbar.norm=norm
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()
