from PySide2 import QtWidgets, QtGui
import matplotlib.colors as mcolors
from matplotlib.offsetbox import OffsetImage


class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Image Setting')
        self.canvas = canvas
        self.event = event
        self.zoom_lineedit = QtWidgets.QLineEdit()
        self.zoom = 1
        for item in self.event.artist.get_children():
            if type(item) == OffsetImage:
                self.offset_image=item
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.zoom_lineedit.setText(str(self.offset_image._zoom))
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('缩放值', self.zoom_lineedit)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec_()

    def confirm_slot(self):
        self.offset_image.set_zoom(float(self.zoom_lineedit.text()))
        self.canvas.draw()

    def cancel_slot(self):
        self.close()
