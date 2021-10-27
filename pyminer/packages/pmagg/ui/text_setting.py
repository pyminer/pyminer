from PySide2 import QtWidgets, QtGui,QtCore
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
        self.text_rotation_lineedit = QtWidgets.QLineEdit()
        self.text_font_alpha_slider = QtWidgets.QSlider()
        self.text_font_alpha_slider.setMaximum(100)
        self.bbox_alpha_slider = QtWidgets.QSlider()
        self.bbox_alpha_slider.setMaximum(100)
        self.text_font_weight_combox = QtWidgets.QComboBox()
        self.text_font_style_combox = QtWidgets.QComboBox()
        self.text_font_color_combox = QtWidgets.QComboBox()
        self.bbox_facecolor_combox = QtWidgets.QComboBox()
        self.bbox_edgecolor_combox = QtWidgets.QComboBox()
        self.bbox_width_lineedit = QtWidgets.QLineEdit()
        self.text_bbox_combox = QtWidgets.QComboBox()
        self.text_content = QtWidgets.QLineEdit()
        self.double_validator = QtGui.QDoubleValidator()
        self.double_validator.setRange(1,100)
        self.text_font_size.setValidator(self.double_validator)
        self.bbox_width_lineedit.setValidator(self.double_validator)
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.layout = QtWidgets.QFormLayout()
        self.generate_items()
        self.layout.addRow('内容', self.text_content)
        self.layout.addRow('不透明度', self.text_font_alpha_slider)
        self.layout.addRow('旋转角/度', self.text_rotation_lineedit)
        self.layout.addRow('字体大小', self.text_font_size)
        self.layout.addRow('字体权重', self.text_font_weight_combox)
        self.layout.addRow('字体样式', self.text_font_style_combox)
        self.layout.addRow('字体颜色', self.text_font_color_combox)
        self.layout.addRow('边框样式', self.text_bbox_combox)
        self.layout.addRow('边框透明度', self.bbox_alpha_slider)
        self.layout.addRow('背景色', self.bbox_facecolor_combox)
        self.layout.addRow('边框色', self.bbox_edgecolor_combox)
        self.layout.addRow('边框宽度', self.bbox_width_lineedit)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)

        self.exec_()

    def generate_items(self):
        self.text_content.setText(self.text.get_text())
        self.text_rotation_lineedit.setText(str(self.text.get_rotation()))
        self.text_font_size.setText(str(self.text.get_fontsize()))
        self.text_font_style_combox.addItems(font_styles)
        self.text_font_style_combox.setCurrentText(self.text.get_fontstyle())
        self.text_font_weight_combox.addItems(font_weights)
        self.text_font_weight_combox.setCurrentText(self.text.get_fontweight())
        alpha = self.text.get_alpha()
        self.text_font_alpha_slider.setProperty("value", 100 if alpha is None else int(alpha * 100))
        self.text_font_alpha_slider.setOrientation(QtCore.Qt.Horizontal)
        self.text_font_alpha_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.text_font_alpha_slider.setTickInterval(10)
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.text_font_color_combox.addItem(color_name)
            self.bbox_facecolor_combox.addItem(color_name)
            self.bbox_edgecolor_combox.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.text_font_color_combox.model().item(index).setBackground(color)
            self.bbox_facecolor_combox.model().item(index).setBackground(color)
            self.bbox_edgecolor_combox.model().item(index).setBackground(color)
            index += 1
        self.text_font_color_combox.setCurrentText(self.text.get_color())
        self.text_bbox_combox.addItems(box_styles)
        self.text_bbox_combox.setCurrentText('None')
        bbox = self.text.get_bbox_patch()
        if bbox is None:
            self.text.set_bbox(rectprops=dict(alpha=0))
            bbox=self.text.get_bbox_patch()
        facecolor_hex = mcolors.to_hex(bbox.get_facecolor())
        edgecolor_hex = mcolors.to_hex(bbox.get_edgecolor())
        for k, v in self.color_dict.items():
            if v == facecolor_hex:
                self.bbox_facecolor_combox.setCurrentText(k)
            if v == edgecolor_hex:
                self.bbox_edgecolor_combox.setCurrentText(k)
        self.bbox_width_lineedit.setText(str(bbox.get_linewidth()))
        alpha = bbox.get_alpha()
        self.bbox_alpha_slider.setProperty("value", 100 if alpha is None else int(alpha * 100))
        self.bbox_alpha_slider.setOrientation(QtCore.Qt.Horizontal)
        self.bbox_alpha_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.bbox_alpha_slider.setTickInterval(10)

    def confirm_slot(self):
        self.text.set_text(self.text_content.text())
        self.text.set_rotation(float(self.text_rotation_lineedit.text()))
        self.text.set_fontsize(float(self.text_font_size.text()))
        self.text.set_fontstyle(self.text_font_style_combox.currentText())
        self.text.set_fontweight(self.text_font_weight_combox.currentText())
        self.text.set_color(self.text_font_color_combox.currentText())
        self.text.set_alpha(self.text_font_alpha_slider.value()/100)
        bbox = self.text_bbox_combox.currentText()
        if bbox != 'None':
            self.text.set_bbox(rectprops=dict(boxstyle=bbox,
                                              facecolor=self.bbox_facecolor_combox.currentText(),
                                              edgecolor=self.bbox_edgecolor_combox.currentText(),
                                              linewidth=float(self.bbox_width_lineedit.text()),
                                              alpha=self.bbox_alpha_slider.value()/100))
        else:
            bbox = self.text.get_bbox_patch()
            bbox.set_alpha(0)
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()
