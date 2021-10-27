# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PySide2_Template.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PySide2Template(object):
    def setupUi(self, PySide2Template):
        if not PySide2Template.objectName():
            PySide2Template.setObjectName(u"PySide2Template")
        PySide2Template.resize(402, 307)
        icon = QIcon()
        icon.addFile(u"../../ui/source/icons/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        PySide2Template.setWindowIcon(icon)
        self.verticalLayoutWidget = QWidget(PySide2Template)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 19, 381, 281))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(PySide2Template)

        QMetaObject.connectSlotsByName(PySide2Template)
    # setupUi

    def retranslateUi(self, PySide2Template):
        PySide2Template.setWindowTitle(QCoreApplication.translate("PySide2Template", u"PySide2Template", None))
        self.textBrowser.setHtml(QCoreApplication.translate("PySide2Template", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">This is a PySide2 Template.</span></p></body></html>", None))
    # retranslateUi

