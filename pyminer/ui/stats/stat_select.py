# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stat_select.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listWidget_var = QtWidgets.QListWidget(Form)
        self.listWidget_var.setObjectName("listWidget_var")
        self.verticalLayout_2.addWidget(self.listWidget_var)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.listWidget_selecetd = QtWidgets.QListWidget(Form)
        self.listWidget_selecetd.setObjectName("listWidget_selecetd")
        self.verticalLayout_3.addWidget(self.listWidget_selecetd)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.listWidget_group = QtWidgets.QListWidget(Form)
        self.listWidget_group.setObjectName("listWidget_group")
        self.verticalLayout_3.addWidget(self.listWidget_group)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_option = QtWidgets.QPushButton(Form)
        self.pushButton_option.setObjectName("pushButton_option")
        self.verticalLayout.addWidget(self.pushButton_option)
        self.pushButton_plot = QtWidgets.QPushButton(Form)
        self.pushButton_plot.setObjectName("pushButton_plot")
        self.verticalLayout.addWidget(self.pushButton_plot)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(0, 50))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_help = QtWidgets.QPushButton(self.widget)
        self.pushButton_help.setObjectName("pushButton_help")
        self.horizontalLayout.addWidget(self.pushButton_help)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_ok = QtWidgets.QPushButton(self.widget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self.widget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.widget)

        self.retranslateUi(Form)
        self.pushButton_cancel.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "显示描述性统计量"))
        self.label_3.setText(_translate("Form", "全部变量:"))
        self.label.setText(_translate("Form", "已选变量:"))
        self.label_2.setText(_translate("Form", "分组变量:(可选)"))
        self.pushButton_option.setText(_translate("Form", "选项"))
        self.pushButton_plot.setText(_translate("Form", "图形"))
        self.pushButton_help.setText(_translate("Form", "帮助"))
        self.pushButton_ok.setText(_translate("Form", "确定"))
        self.pushButton_cancel.setText(_translate("Form", "取消"))
