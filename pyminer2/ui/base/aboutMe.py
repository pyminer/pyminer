# -*- coding: utf-8 -*-
# 已经经过手动编辑，切勿用Qtdesigner进行覆盖!


from .. import pyqtsource_rc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from pyminer2.pmutil import get_root_dir


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setMinimumSize(QtCore.QSize(500, 400))
        Form.setMaximumSize(QtCore.QSize(500, 400))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 20, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(230, 40, 101, 16))
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(20, 70, 461, 321))
        self.textBrowser.setObjectName("textBrowser")
        self.label_logo = QtWidgets.QLabel(Form)
        self.label_logo.setGeometry(QtCore.QRect(100, 5, 64, 64))
        self.label_logo.setStyleSheet(
            "image: url(:/pyqt/source/icons/base/64.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "关于"))
        self.label.setText(_translate("Form", "PyMiner"))
        self.label_2.setText(_translate("Form", "版本号：1.0.1"))
        self.textBrowser.setHtml(_translate("Form",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                            "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style "
                                            "type=\"text/css\">\n "
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; "
                                            "font-weight:400; font-style:normal;\">\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                            "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">PyMiner 是基于 "
                                            "PyQt5 技术进行开发的Python数据分析工具，它是一个开源代码的软件，遵循GPL开源许可证书。</p>\n "
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; "
                                            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                                            "text-indent:0px;\"><br /></p>\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                            "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">作者：PyMiner "
                                            "Development Team</p>\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                            "margin-right:0px; -qt-block-indent:0; "
                                            "text-indent:0px;\">QQ：454017698</p>\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                            "margin-right:0px; -qt-block-indent:0; "
                                            "text-indent:0px;\">邮箱：aboutlong@qq.com</p>\n "
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; "
                                            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                                            "text-indent:0px;\"><br /></p></body></html>"))


class AboutMeForm(QWidget, Ui_Form):
    """
    打开"关于"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.setLogo()

    def keyPressEvent(self, evt):
        """
        按键盘Escape退出当前窗口
        @param evt:
        """
        if evt.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setLogo(self):
        pix = QPixmap(get_root_dir() + '/ui/source/icons/logo.png')
        self.label_logo.setPixmap(pix)
