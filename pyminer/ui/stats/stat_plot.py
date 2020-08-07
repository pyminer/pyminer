# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stat_plot.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 250)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxhist = QtWidgets.QCheckBox(Form)
        self.checkBoxhist.setObjectName("checkBoxhist")
        self.verticalLayout.addWidget(self.checkBoxhist)
        self.checkBox_normal = QtWidgets.QCheckBox(Form)
        self.checkBox_normal.setObjectName("checkBox_normal")
        self.verticalLayout.addWidget(self.checkBox_normal)
        self.checkBox_value = QtWidgets.QCheckBox(Form)
        self.checkBox_value.setObjectName("checkBox_value")
        self.verticalLayout.addWidget(self.checkBox_value)
        self.checkBox_boxplot = QtWidgets.QCheckBox(Form)
        self.checkBox_boxplot.setObjectName("checkBox_boxplot")
        self.verticalLayout.addWidget(self.checkBox_boxplot)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_help = QtWidgets.QPushButton(Form)
        self.pushButton_help.setObjectName("pushButton_help")
        self.horizontalLayout.addWidget(self.pushButton_help)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pushButton_ok = QtWidgets.QPushButton(Form)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "显示描述性统计量"))
        self.checkBoxhist.setText(_translate("Form", "数据直方图"))
        self.checkBox_normal.setText(_translate("Form", "带正态曲线的数据直方图"))
        self.checkBox_value.setText(_translate("Form", "单值图"))
        self.checkBox_boxplot.setText(_translate("Form", "数据箱线图"))
        self.pushButton_help.setText(_translate("Form", "帮助"))
        self.pushButton_ok.setText(_translate("Form", "确定"))
        self.pushButton_cancel.setText(_translate("Form", "取消"))
