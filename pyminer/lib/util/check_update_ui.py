# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_update_ui.ui'
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
        Dialog.resize(546, 173)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_detail = QPushButton(Dialog)
        self.button_detail.setObjectName(u"button_detail")
        self.button_detail.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout.addWidget(self.button_detail)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.table = QTableWidget(Dialog)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.button_confirm = QPushButton(Dialog)
        self.button_confirm.setObjectName(u"button_confirm")

        self.horizontalLayout_5.addWidget(self.button_confirm)

        self.button_close = QPushButton(Dialog)
        self.button_close.setObjectName(u"button_close")

        self.horizontalLayout_5.addWidget(self.button_close)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u66f4\u65b0\u68c0\u6d4b\u7a0b\u5e8f", None))
        self.label.setText("")
        self.button_detail.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.button_confirm.setText(QCoreApplication.translate("Dialog", u"\u66f4\u65b0", None))
        self.button_close.setText(QCoreApplication.translate("Dialog", u"\u4e0b\u6b21\u518d\u8bf4", None))
    # retranslateUi

