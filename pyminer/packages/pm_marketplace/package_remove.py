# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_remove.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_name)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_dir = QLineEdit(Form)
        self.lineEdit_dir.setObjectName(u"lineEdit_dir")
        self.lineEdit_dir.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_dir)

        self.toolButton_open = QToolButton(Form)
        self.toolButton_open.setObjectName(u"toolButton_open")
        self.toolButton_open.setMinimumSize(QSize(0, 22))

        self.horizontalLayout.addWidget(self.toolButton_open)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)


        self.horizontalLayout_4.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textEdit_desc = QTextEdit(self.groupBox)
        self.textEdit_desc.setObjectName(u"textEdit_desc")

        self.horizontalLayout_5.addWidget(self.textEdit_desc)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.textEdit_log = QTextEdit(self.groupBox_2)
        self.textEdit_log.setObjectName(u"textEdit_log")

        self.horizontalLayout_6.addWidget(self.textEdit_log)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_2.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_2.addWidget(self.pushButton_cancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5378\u8f7d", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5305\u540d:", None))
        self.lineEdit_name.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u5b89\u88c5\u4f4d\u7f6e:", None))
        self.lineEdit_dir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.toolButton_open.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u8be6\u60c5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6267\u884c\u8bb0\u5f55", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

