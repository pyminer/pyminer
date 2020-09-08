# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'package_remove.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_name = QtWidgets.QLineEdit(Form)
        self.lineEdit_name.setText("")
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_dir = QtWidgets.QLineEdit(Form)
        self.lineEdit_dir.setReadOnly(True)
        self.lineEdit_dir.setObjectName("lineEdit_dir")
        self.horizontalLayout.addWidget(self.lineEdit_dir)
        self.toolButton_open = QtWidgets.QToolButton(Form)
        self.toolButton_open.setMinimumSize(QtCore.QSize(0, 22))
        self.toolButton_open.setObjectName("toolButton_open")
        self.horizontalLayout.addWidget(self.toolButton_open)
        self.formLayout.setLayout(
            1,
            QtWidgets.QFormLayout.FieldRole,
            self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textEdit_desc = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_desc.setObjectName("textEdit_desc")
        self.horizontalLayout_5.addWidget(self.textEdit_desc)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.textEdit_log = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_log.setObjectName("textEdit_log")
        self.horizontalLayout_6.addWidget(self.textEdit_log)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_ok = QtWidgets.QPushButton(self.widget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_2.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self.widget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_2.addWidget(self.pushButton_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "卸载"))
        self.label_2.setText(_translate("Form", "包名:"))
        self.label_3.setText(_translate("Form", "当前安装位置:"))
        self.lineEdit_dir.setPlaceholderText(_translate("Form", "默认"))
        self.toolButton_open.setText(_translate("Form", "打开"))
        self.groupBox.setTitle(_translate("Form", "详情"))
        self.groupBox_2.setTitle(_translate("Form", "执行记录"))
        self.pushButton_ok.setText(_translate("Form", "确定"))
        self.pushButton_cancel.setText(_translate("Form", "取消"))
