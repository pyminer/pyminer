from PySide2 import QtWidgets
from .linestyles import *


class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Legend Setting')
        self.legends = []
        self.event_legend = event
        self.legend = event.artist
        self.canvas = canvas
        self.loc_combox = QtWidgets.QComboBox()
        self.shadow_checkbox = QtWidgets.QCheckBox()
        self.frameon_checkbox = QtWidgets.QCheckBox()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.layout = QtWidgets.QFormLayout()
        self.generate_items()
        self.layout.addRow('位置', self.loc_combox)
        self.layout.addRow('阴影', self.shadow_checkbox)
        self.layout.addRow('边框', self.frameon_checkbox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.loc_combox.addItems(locations)
        self.loc_combox.setCurrentText('best')
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec_()

    def generate_items(self):
        for index, item in enumerate(self.legend.get_texts()):
            line = QtWidgets.QLineEdit()
            line.setText(item.get_text())
            self.layout.addRow('legend ' + str(index + 1), line)
            self.legends.append(line)

    def confirm_slot(self):
        legend = self.event_legend.mouseevent.inaxes.legend(self.legend.get_lines(),
                                                            self.get_legends(),
                                                            shadow=self.shadow_checkbox.isChecked(),
                                                            frameon=self.frameon_checkbox.isChecked(),
                                                            loc=self.loc_combox.currentText())
        legend.set_picker(True)
        legend.set_draggable(True)
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()

    def get_legends(self):
        legend_texts = []
        for item in self.legends:
            legend_texts.append(item.text())
        return legend_texts
