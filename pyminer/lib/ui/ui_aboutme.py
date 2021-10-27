# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_aboutme.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        Form.setMaximumSize(QSize(800, 600))
        font = QFont()
        font.setFamily(u"Albany AMT")
        Form.setFont(font)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(85, 85))
        self.label_3.setMaximumSize(QSize(85, 85))
        self.label_3.setPixmap(QPixmap(u":/logo/icons/logo.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_3)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamily(u"Microsoft YaHei UI")
        font1.setPointSize(24)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setFamily(u"\u9ed1\u4f53")
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.label_version_show = QLabel(Form)
        self.label_version_show.setObjectName(u"label_version_show")
        self.label_version_show.setFont(font2)
        self.label_version_show.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.horizontalLayout.addWidget(self.label_version_show)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        font3 = QFont()
        font3.setFamily(u"\u9ed1\u4f53")
        font3.setPointSize(11)
        self.tabWidget.setFont(font3)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textedit_about = QTextEdit(self.tab)
        self.textedit_about.setObjectName(u"textedit_about")
        self.textedit_about.setFont(font3)
        self.textedit_about.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.textedit_about)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.feedback = QPlainTextEdit(self.tab_2)
        self.feedback.setObjectName(u"feedback")
        font4 = QFont()
        font4.setFamily(u"Microsoft YaHei UI")
        font4.setPointSize(11)
        self.feedback.setFont(font4)
        self.feedback.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_3.addWidget(self.feedback)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit_2 = QPlainTextEdit(self.tab_3)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setFont(font3)
        self.plainTextEdit_2.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_4.addWidget(self.plainTextEdit_2)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.tab_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u":/resources/images/weixin.png"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.tab_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u":/resources/images/zhifubao.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"About", None))
        self.label_3.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"PyMiner", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Version:", None))
        self.label_version_show.setText(QCoreApplication.translate("Form", u"v2.0 Beta", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"About", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"System", None))
        self.plainTextEdit_2.setPlainText(QCoreApplication.translate("Form", u"\u4faf\u5c55\u610f\n"
"py2cn\n"
"Junruoyu-Zheng\n"
"\u5fc3\u968f\u98ce\n"
"nihk\n"
"cl-jiang\n"
"Irony\n"
"\u51b0\u4e2d\u706b\n"
"houxinluo\n"
"\u5f00\u59cb\u8bf4\u6545\u4e8b\n"
"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Credit", None))
        self.label_4.setText("")
        self.label_5.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Form", u"Donate", None))
    # retranslateUi

