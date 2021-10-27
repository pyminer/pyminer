# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_normal.ui'
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
        Dialog.resize(458, 405)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setObjectName(u"tableWidget")

        self.horizontalLayout.addWidget(self.tableWidget)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.spinBox_precison = QSpinBox(Dialog)
        self.spinBox_precison.setObjectName(u"spinBox_precison")
        self.spinBox_precison.setValue(2)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spinBox_precison)

        self.spinBox_count = QSpinBox(Dialog)
        self.spinBox_count.setObjectName(u"spinBox_count")
        self.spinBox_count.setValue(30)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinBox_count)

        self.doubleSpinBox_std = QDoubleSpinBox(Dialog)
        self.doubleSpinBox_std.setObjectName(u"doubleSpinBox_std")
        self.doubleSpinBox_std.setValue(1.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_std)

        self.doubleSpinBox_mean = QDoubleSpinBox(Dialog)
        self.doubleSpinBox_mean.setObjectName(u"doubleSpinBox_mean")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_mean)


        self.horizontalLayout.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u6570\u636e\u751f\u6210-\u6b63\u6001\u5206\u5e03", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5747\u503c:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u6807\u51c6\u5dee:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u6570\u91cf:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u7cbe\u5ea6:", None))
    # retranslateUi

