# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gotoline.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogGoto(object):
    def setupUi(self, DialogGoto):
        if not DialogGoto.objectName():
            DialogGoto.setObjectName(u"DialogGoto")
        DialogGoto.resize(300, 94)
        self.gridLayout = QGridLayout(DialogGoto)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 18, -1, -1)
        self.lineEdit = QLineEdit(DialogGoto)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label = QLabel(DialogGoto)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogGoto)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)


        self.retranslateUi(DialogGoto)

        QMetaObject.connectSlotsByName(DialogGoto)
    # setupUi

    def retranslateUi(self, DialogGoto):
        DialogGoto.setWindowTitle(QCoreApplication.translate("DialogGoto", u"Go to Line", None))
        self.label.setText(QCoreApplication.translate("DialogGoto", u"Line\uff1a", None))
    # retranslateUi

