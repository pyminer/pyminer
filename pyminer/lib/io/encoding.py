import os

from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QMessageBox

from widgets import PMGPanel
import utils
from utils import file_encoding_convert


class EncodingConversionWidget(QDialog):
    def __init__(self, parent=None):
        super(EncodingConversionWidget, self).__init__(parent=parent)
        views = [
            ('file_ctrl', 'input_file', '读取文件名', '', '',
             utils.get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR")),
            ('file_ctrl', 'output_file', '输出为文件', '', '',
             utils.get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR"), 'save'),
            [
                ('combo_ctrl', 'input_encoding', '读取编码方式', 'UTF8', ['UTF8', 'GBK', 'ASCII']),
                ('combo_ctrl', 'output_encoding', '输出编码方式', 'UTF8', ['UTF8', 'GBK', 'ASCII'])
            ]

        ]
        self.panel = PMGPanel(parent=self, views=views)
        self.text_view = QTextBrowser()
        self.button_preview = QPushButton('预览')
        self.button_convert = QPushButton('转换')
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(self.panel)
        self.layout().addWidget(self.text_view)
        button_layout = QHBoxLayout()
        self.layout().addLayout(button_layout)
        button_layout.addWidget(self.button_preview)
        button_layout.addWidget(self.button_convert)

        self.button_preview.clicked.connect(self.preview)
        self.button_convert.clicked.connect(self.convert)

    def preview(self):
        info = self.panel.get_value()
        size = os.path.getsize(info['input_file'])
        with open(info['input_file'], 'r', encoding=info['input_encoding'], errors='replace')as f:
            if size > 1000:
                text = f.read(1000)
            else:
                text = f.read()
        self.text_view.setText(text)

    def convert(self):
        info = self.panel.get_value()
        try:
            file_encoding_convert(info['input_file'], info['input_encoding'], info['output_file'],
                                  info['output_encoding'])
            QMessageBox.information(self, '提示', '转换完成！', QMessageBox.Ok, QMessageBox.Ok)
        except FileNotFoundError:
            QMessageBox.information(self, '未找到输出文件', '未找到输出文件', QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication([])
    w = EncodingConversionWidget()
    w.show()
    app.exec_()
