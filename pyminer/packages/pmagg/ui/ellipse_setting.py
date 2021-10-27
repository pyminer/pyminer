from PySide2 import QtWidgets, QtGui
import matplotlib.colors as mcolors


class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Ellipse Setting')
        self.legends = []
        self.event_legend = event
        self.artist = event.artist
        self.canvas = canvas
        self.width_lineedit = QtWidgets.QLineEdit()
        self.height_lineedit = QtWidgets.QLineEdit()
        self.linewidth_lineedit = QtWidgets.QLineEdit()
        self.zorder_lineedit = QtWidgets.QLineEdit()
        self.fill_checkbox = QtWidgets.QCheckBox()
        self.edge_combox = QtWidgets.QComboBox()
        self.face_combox = QtWidgets.QComboBox()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')

        self.set_combox_items()
        edgecolor = event.artist.get_edgecolor()
        if edgecolor == (0, 0, 0, 0):
            self.edge_combox.setCurrentText('None')
        else:
            for item in self.color_dict:
                if mcolors.to_hex(item) == mcolors.to_hex(edgecolor):
                    self.edge_combox.setCurrentText(item)
        facecolor = event.artist.get_facecolor()
        if facecolor == (0, 0, 0, 0):
            self.face_combox.setCurrentText('None')
        else:
            for item in self.color_dict:
                if mcolors.to_hex(item) == mcolors.to_hex(facecolor):
                    self.face_combox.setCurrentText(item)
        self.width_lineedit.setText(str(event.artist.get_width()))
        self.height_lineedit.setText(str(event.artist.get_height()))
        self.linewidth_lineedit.setText(str(event.artist.get_linewidth()))
        self.zorder_lineedit.setText(str(event.artist.zorder))
        self.fill_checkbox.setChecked(event.artist.get_fill())

        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('宽度', self.width_lineedit)
        self.layout.addRow('高度', self.height_lineedit)
        self.layout.addRow('边框宽度', self.linewidth_lineedit)
        self.layout.addRow('绘图顺序(zorder)', self.zorder_lineedit)
        self.layout.addRow('是否填充', self.fill_checkbox)
        self.layout.addRow('边框色', self.edge_combox)
        self.layout.addRow('填充色', self.face_combox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec_()

    def confirm_slot(self):
        self.artist.set_width(float(self.width_lineedit.text()))
        self.artist.set_height(float(self.height_lineedit.text()))
        self.artist.set_linewidth(float(self.linewidth_lineedit.text()))
        self.artist.set_fill(self.fill_checkbox.isChecked())
        self.artist.zorder=int(self.zorder_lineedit.text())
        self.artist.set_edgecolor(self.edge_combox.currentText())
        self.artist.set_facecolor(self.face_combox.currentText())
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