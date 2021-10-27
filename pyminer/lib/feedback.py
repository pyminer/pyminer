# -*- coding: utf-8 -*-
# @Time    : 2021/2/12 16:24
# @Author  : jcl
# @Email   : 2195932461@qq.com
# @File    : feedback.py
# @Software: PyCharm
import requests
from PySide2.QtWidgets import QDialog, QTextEdit, QLabel, QVBoxLayout, QApplication, QPushButton, QMessageBox

from lib.settings import Setting


class FeedbackClient(QDialog):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.text_edit = QTextEdit()
        self.setWindowTitle(self.tr('Feedback'))
        self.label = QLabel(
            self.tr('You can give feedback through issue on suggestions or problems encountered in use! (<200 words)'))
        self.confirm_button = QPushButton(self.tr('confirm'))
        self.confirm_button.setFixedWidth(75)
        self.confirm_button.clicked.connect(self.post)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.text_edit)
        self.vbox.addWidget(self.confirm_button)
        setting = Setting()
        self.version = setting.get_system_version()
        self.exec_()

    def post(self):
        text = self.text_edit.toPlainText()
        version = self.version
        url = 'http://www.pyminer.com/api/v1/feedback/'
        data = {'core': version, 'feedback': text}
        r = requests.post(url, data)
        if r.status_code == 201:
            QMessageBox.about(self, self.tr('result'), self.tr('Submitted successfully!'))
        else:
            QMessageBox.warning(self, self.tr('result'), r.text, QMessageBox.Yes)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    FeedbackClient()
