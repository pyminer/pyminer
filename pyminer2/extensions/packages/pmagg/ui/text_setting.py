from PyQt5 import QtWidgets, QtGui
from .linestyles import *
from matplotlib.text import Text
import matplotlib.colors as mcolors


class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Text Setting')
        self.event_text = event
        self.text = event.artist
        self.canvas = canvas
        assert isinstance(self.text, Text)
        self.text_font_size = QtWidgets.QLineEdit()
        self.text_font_alpha = QtWidgets.QLineEdit()
        self.text_font_weight_combox = QtWidgets.QComboBox()
        self.text_font_style_combox = QtWidgets.QComboBox()
        self.text_font_color_combox = QtWidgets.QComboBox()
        self.text_content = QtWidgets.QLineEdit()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.layout = QtWidgets.QFormLayout()
        self.generate_items()
        self.layout.addRow('内容', self.text_content)
        self.layout.addRow('不透明度', self.text_font_alpha)
        self.layout.addRow('字体大小', self.text_font_size)
        self.layout.addRow('字体权重', self.text_font_weight_combox)
        self.layout.addRow('字体样式', self.text_font_style_combox)
        self.layout.addRow('字体颜色', self.text_font_color_combox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec()

    def generate_items(self):
        self.text_content.setText(self.text.get_text())
        self.text_font_size.setText(str(self.text.get_fontsize()))
        self.text_font_style_combox.addItems(font_styles)
        self.text_font_style_combox.setCurrentText(self.text.get_fontstyle())
        self.text_font_weight_combox.addItems(font_weights)
        self.text_font_weight_combox.setCurrentText(self.text.get_fontweight())
        alpha = self.text.get_alpha()
        if alpha is None:
            self.text_font_alpha.setText(str(1))
        else:
            self.text_font_alpha.setText(str(alpha))
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.text_font_color_combox.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.text_font_color_combox.model().item(index).setBackground(color)
            index += 1
        self.text_font_color_combox.setCurrentText(self.text.get_color())

    def confirm_slot(self):
        self.text.set_text(self.text_content.text())
        self.text.set_fontsize(float(self.text_font_size.text()))
        self.text.set_fontstyle(self.text_font_style_combox.currentText())
        self.text.set_fontweight(self.text_font_weight_combox.currentText())
        self.text.set_color(self.text_font_color_combox.currentText())
        self.text.set_alpha(float(self.text_font_alpha.text()))
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()
