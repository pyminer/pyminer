from PySide2 import QtWidgets, QtGui,QtCore
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Rectangle Setting')
        self.legends = []
        self.event_legend = event
        self.artist = event.artist
        self.canvas = canvas
        self.width_lineedit = QtWidgets.QLineEdit()
        self.height_lineedit = QtWidgets.QLineEdit()
        self.linewidth_lineedit = QtWidgets.QLineEdit()
        self.zorder_lineedit = QtWidgets.QLineEdit()
        self.fill_checkbox = QtWidgets.QCheckBox()
        self.same_color_checkbox = QtWidgets.QCheckBox()
        self.edge_combox = QtWidgets.QComboBox()
        self.face_combox = QtWidgets.QComboBox()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')

        self.set_combox_items()
        self.width_lineedit.setText(str(event.artist.get_width()))
        self.height_lineedit.setText(str(event.artist.get_height()))
        self.linewidth_lineedit.setText(str(event.artist.get_linewidth()))
        self.zorder_lineedit.setText(str(event.artist.zorder))
        edgecolor=event.artist.get_edgecolor()
        if edgecolor==(0,0,0,0):
            self.edge_combox.setCurrentText('None')
        else:
            for item in self.color_dict:
                if mcolors.to_hex(item) == mcolors.to_hex(edgecolor):
                    self.edge_combox.setCurrentText(item)
        facecolor=event.artist.get_facecolor()
        if facecolor==(0,0,0,0):
            self.face_combox.setCurrentText('None')
        else:
            for item in self.color_dict:
                if mcolors.to_hex(item) == mcolors.to_hex(facecolor):
                    self.face_combox.setCurrentText(item)
        self.fill_checkbox.setChecked(event.artist.get_fill())
        self.horizontalSlider = QtWidgets.QSlider()
        self.horizontalSlider.setMaximum(100)
        alpha=event.artist.get_alpha()
        self.horizontalSlider.setProperty("value",100 if alpha is None else int(alpha*100))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)

        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('宽度', self.width_lineedit)
        self.layout.addRow('高度', self.height_lineedit)
        self.layout.addRow('边框宽度', self.linewidth_lineedit)
        self.layout.addRow('绘图顺序(zorder)', self.zorder_lineedit)
        self.layout.addRow('边框色', self.edge_combox)
        self.layout.addRow('填充色', self.face_combox)
        self.layout.addRow('透明度', self.horizontalSlider)
        self.layout.addRow('是否填充', self.fill_checkbox)
        self.layout.addRow('是否对同色矩形操作', self.same_color_checkbox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        if self.artist.axes:
            axes=self.artist.axes
        else:
            axes=self.artist.figure
        self.rectangles=[item for item in axes.patches if type(item)==Rectangle
                         and item.get_edgecolor()==event.artist.get_edgecolor()
                         and item.get_facecolor()==event.artist.get_facecolor()]
        self.exec_()

    def confirm_slot(self):
        if self.same_color_checkbox.isChecked():
            artists=self.rectangles
        else:
            artists=[self.artist]
        for item in artists:
            item.set_width(float(self.width_lineedit.text()))
            self.artist.set_height(float(self.height_lineedit.text())) # 高度不设一样
            self.artist.zorder=int(self.zorder_lineedit.text())
            item.set_linewidth(float(self.linewidth_lineedit.text()))
            item.set_fill(self.fill_checkbox.isChecked())
            if self.edge_combox.currentText()=='None':  # 必须为None，才能透明
                item.set_edgecolor(None)
            else:
                item.set_edgecolor(self.edge_combox.currentText())
            if self.face_combox.currentText()=='None':
                item.set_facecolor(None)
            else:
                item.set_facecolor(self.face_combox.currentText())
            item.set_alpha(self.horizontalSlider.value()/100)
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
            self.edge_combox.addItem(color_name)
            self.face_combox.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.edge_combox.model().item(index).setBackground(color)
            self.face_combox.model().item(index).setBackground(color)
            index += 1
        self.edge_combox.addItem('None')
        self.face_combox.addItem('None')


