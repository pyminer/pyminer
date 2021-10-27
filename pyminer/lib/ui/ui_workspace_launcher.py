# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_workspace_launcher.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(444, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 9)
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.widget)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.widget_2 = QWidget(Dialog)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(self.widget_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.toolButton_3 = QToolButton(self.widget_2)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout_3.addWidget(self.toolButton_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.checkBox = QCheckBox(self.widget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_4.addWidget(self.checkBox)

        self.buttonBox = QDialogButtonBox(self.widget_2)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Workspace launcher", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Select a workspace", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"PyMiner stores your projects in a folder called a workspace.", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Choose a workspace folder to use for this session.", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Workspace", None))
        self.toolButton_3.setText(QCoreApplication.translate("Dialog", u"Browse...", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Use this as the default and do not ask again", None))
    # retranslateUi

