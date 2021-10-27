# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_import_mysql.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .password import PasswordEdit

from resources import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(681, 450)
        Form.setMinimumSize(QSize(500, 400))
        Form.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/resources/icons/MySQL.svg", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_nettype = QLabel(Form)
        self.label_nettype.setObjectName(u"label_nettype")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_nettype)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.comboBox_database = QComboBox(Form)
        self.comboBox_database.addItem("")
        self.comboBox_database.setObjectName(u"comboBox_database")
        self.comboBox_database.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_8.addWidget(self.comboBox_database)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.label_username = QLabel(Form)
        self.label_username.setObjectName(u"label_username")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_username)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lineEdit_user = QLineEdit(Form)
        self.lineEdit_user.setObjectName(u"lineEdit_user")

        self.horizontalLayout_7.addWidget(self.lineEdit_user)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.label_password = QLabel(Form)
        self.label_password.setObjectName(u"label_password")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_password)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit_passwd = PasswordEdit(Form)
        self.lineEdit_passwd.setObjectName(u"lineEdit_passwd")

        self.horizontalLayout_6.addWidget(self.lineEdit_passwd)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(7, QFormLayout.FieldRole, self.verticalSpacer)

        self.label_ip = QLabel(Form)
        self.label_ip.setObjectName(u"label_ip")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_ip)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_host = QLineEdit(Form)
        self.lineEdit_host.setObjectName(u"lineEdit_host")

        self.horizontalLayout_4.addWidget(self.lineEdit_host)

        self.label_port = QLabel(Form)
        self.label_port.setObjectName(u"label_port")

        self.horizontalLayout_4.addWidget(self.label_port)

        self.spinBox_port = QSpinBox(Form)
        self.spinBox_port.setObjectName(u"spinBox_port")
        self.spinBox_port.setMaximum(999999)
        self.spinBox_port.setValue(3306)

        self.horizontalLayout_4.addWidget(self.spinBox_port)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_database = QLabel(Form)
        self.label_database.setObjectName(u"label_database")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_database)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_db = QLineEdit(Form)
        self.lineEdit_db.setObjectName(u"lineEdit_db")

        self.horizontalLayout_3.addWidget(self.lineEdit_db)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_database_2 = QLabel(Form)
        self.label_database_2.setObjectName(u"label_database_2")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_database_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_table = QLineEdit(Form)
        self.lineEdit_table.setObjectName(u"lineEdit_table")

        self.horizontalLayout_2.addWidget(self.lineEdit_table)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_test = QLabel(Form)
        self.label_test.setObjectName(u"label_test")

        self.verticalLayout.addWidget(self.label_test)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_test = QPushButton(self.widget)
        self.pushButton_test.setObjectName(u"pushButton_test")

        self.horizontalLayout.addWidget(self.pushButton_test)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4ece\u6570\u636e\u5e93\u5bfc\u5165", None))
        self.label_nettype.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u5e93\u7c7b\u578b\uff1a", None))
        self.comboBox_database.setItemText(0, QCoreApplication.translate("Form", u"MySQL", None))

        self.label_username.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d\uff1a", None))
        self.lineEdit_user.setInputMask("")
        self.lineEdit_user.setText(QCoreApplication.translate("Form", u"root", None))
        self.lineEdit_user.setPlaceholderText(QCoreApplication.translate("Form", u"\u8d26\u6237\u540d\u79f0", None))
        self.label_password.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\uff1a", None))
        self.lineEdit_passwd.setPlaceholderText(QCoreApplication.translate("Form", u"\u8d26\u6237\u5bc6\u7801", None))
        self.label_ip.setText(QCoreApplication.translate("Form", u"\u4e3b\u673a\u540d/IP\u5730\u5740\uff1a", None))
        self.lineEdit_host.setText(QCoreApplication.translate("Form", u"127.0.0.1", None))
        self.lineEdit_host.setPlaceholderText(QCoreApplication.translate("Form", u"\u6570\u636e\u5e93\u5730\u5740", None))
        self.label_port.setText(QCoreApplication.translate("Form", u"\u7aef\u53e3\uff1a", None))
        self.label_database.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u5e93\uff1a", None))
        self.lineEdit_db.setText("")
        self.lineEdit_db.setPlaceholderText(QCoreApplication.translate("Form", u"\u6570\u636e\u5e93\u540d", None))
        self.label_database_2.setText(QCoreApplication.translate("Form", u"\u8868\u540d\uff1a", None))
        self.lineEdit_table.setText("")
        self.lineEdit_table.setPlaceholderText(QCoreApplication.translate("Form", u"\u8981\u5bfc\u5165\u7684\u8868\u540d", None))
        self.label_test.setText(QCoreApplication.translate("Form", u"\u7b49\u5f85\u8fde\u63a5", None))
        self.pushButton_test.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u8fde\u63a5", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

