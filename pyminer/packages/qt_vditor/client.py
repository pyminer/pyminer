import json
import os
import re
import sys
import time

import requests
from PySide2 import QtWidgets, QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView


class Window(QtWidgets.QDialog):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.view = QWebEngineView()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.pushButton = QtWidgets.QPushButton('theme=light')
        # self.pushButton2 = QtWidgets.QPushButton('theme=dark')
        # self.pushButton.clicked.connect(lambda: self.set_theme('classic', 'light'))
        # self.pushButton2.clicked.connect(lambda: self.set_theme('dark', 'dark'))
        self.setLayout(self.layout)
        # self.layout.addWidget(self.pushButton)
        # self.layout.addWidget(self.pushButton2)
        self.layout.addWidget(self.view)
        self.last_savetime = 0
        self.raw_content = ''
        self.file_path = ''

    def post(self, url, md_content, md_path):
        data = {
            'md_content': md_content,
            'md_path': md_path,
            'url': url
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response

    def load_file(self, file_path: str):
        self.file_path = file_path
        if file_path and os.path.exists(file_path):
            self.last_savetime = os.stat(self.file_path).st_mtime
            (filename, ext) = os.path.basename(file_path).split('.')
            if ext == 'md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.raw_content = f.read()
                    self.raw_content = self.convert_local_md_image(self.raw_content)  # 对图片路径进行转换
                # 使相对地址生效
                temp_html = os.path.join(os.path.dirname(file_path), filename + '.html').replace('\\', '/')
                response = self.post(url=self.url,
                                     md_content=self.raw_content,
                                     md_path=self.file_path)
                self.view.setHtml(response.text, baseUrl=QtCore.QUrl(temp_html))

    def save_file(self):
        self.view.page().runJavaScript("saveMDText(\"{}\")".format(self.file_path))
        self.last_savetime = time.time()

    def set_theme(self, theme: str, content_theme: str):
        self.view.page().runJavaScript("setTheme(\"{}|{}\")".format(theme, content_theme))

    def convert_localpics(self, m):
        result = m.group(2)
        if m.group(2)[1] == ':':  # windows下绝对路径
            result = 'file:///' + m.group(2).replace('\\', '/')
        if m.group(2)[0] == '/':  # linux下绝对路径
            result = 'file://' + m.group(2).replace('\\', '/')
        return "![{}](".format(m.group(1)) + result + ")"

    def convert_local_md_image(self, md_content):
        pattern = re.compile(r'(?:!\[(.*?)\]\((.*?)\))')  # md图片格式识别
        new_content = pattern.sub(self.convert_localpics, md_content)
        return new_content

    def get_last_save_time(self):
        return self.last_savetime


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window(url='http://127.0.0.1:5000/qt_vditor')
    win.load_file(file_path=os.path.join(os.path.dirname(__file__), "examples", "sample.md"))
    win.show()
    app.exec_()
