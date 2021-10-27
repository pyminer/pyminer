# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login.ui'
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
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(407, 361)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(407, 361))
        Form.setMaximumSize(QSize(407, 361))
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(407, 361))
        self.widget.setSizeIncrement(QSize(407, 361))
        self.widget.setBaseSize(QSize(407, 361))
        self.widget.setStyleSheet(u"QPushButton{\n"
"	padding: 8px 20px;\n"
"    font-size: 13px;\n"
"    line-height: 1.65;\n"
"    border-radius: 20px;\n"
"	display: inline-block;\n"
"    margin-bottom: 0;\n"
"    font-weight: 600;\n"
"    text-align: center;\n"
"    vertical-align: middle;\n"
"    touch-action: manipulation;\n"
"    cursor: pointer;\n"
"    background-image: none;\n"
"    border: 1px solid transparent;\n"
"    white-space: nowrap;\n"
"	font-family: inherit;\n"
"	text-transform: none;\n"
"	background-color: #00a6fd;\n"
"	border-color: #00a6fd;\n"
"	color: #fff;\n"
"	\n"
"}")
        self.layoutWidget = QWidget(self.widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 452, 331))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.usernameError = QLabel(self.layoutWidget)
        self.usernameError.setObjectName(u"usernameError")
        self.usernameError.setEnabled(True)
        self.usernameError.setMinimumSize(QSize(380, 32))
        self.usernameError.setMaximumSize(QSize(380, 32))
        font = QFont()
        font.setFamily(u"18thCentury")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.usernameError.setFont(font)
        self.usernameError.setAutoFillBackground(False)
        self.usernameError.setStyleSheet(u"*{\n"
"color:red;\n"
"}")
        self.usernameError.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.usernameError)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(70, 0))
        self.label.setMaximumSize(QSize(70, 16777215))
        self.label.setBaseSize(QSize(70, 0))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.usernameLineEdit = QLineEdit(self.layoutWidget)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        self.usernameLineEdit.setMinimumSize(QSize(300, 32))
        self.usernameLineEdit.setMaximumSize(QSize(300, 32))
        self.usernameLineEdit.setStyleSheet(u"QLineEdit{\n"
"background-color: white;\n"
"selection-color: white;\n"
"selection-background-color: blue;\n"
"}")
        self.usernameLineEdit.setMaxLength(64)

        self.horizontalLayout_2.addWidget(self.usernameLineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.passwordError = QLabel(self.layoutWidget)
        self.passwordError.setObjectName(u"passwordError")
        self.passwordError.setMinimumSize(QSize(380, 32))
        self.passwordError.setMaximumSize(QSize(380, 32))
        self.passwordError.setFont(font)
        self.passwordError.setStyleSheet(u"*{\n"
"color:red;\n"
"}")
        self.passwordError.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.passwordError)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 0))
        self.label_2.setMaximumSize(QSize(70, 16777215))
        self.label_2.setBaseSize(QSize(70, 0))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.passwordLineEdit = QLineEdit(self.layoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setMinimumSize(QSize(300, 0))
        self.passwordLineEdit.setMaximumSize(QSize(300, 32))
        self.passwordLineEdit.setBaseSize(QSize(300, 32))
        self.passwordLineEdit.setStyleSheet(u"QLineEdit{\n"
"background-color: white;\n"
"selection-color: white;\n"
"selection-background-color: blue;\n"
"}")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.passwordLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loginButton = QPushButton(self.layoutWidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(150, 16777215))
        self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginButton.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.loginButton)

        self.forgetPwdButton = QPushButton(self.layoutWidget)
        self.forgetPwdButton.setObjectName(u"forgetPwdButton")
        self.forgetPwdButton.setMaximumSize(QSize(150, 16777215))
        self.forgetPwdButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.forgetPwdButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7528\u6237\u767b\u5f55", None))
        self.usernameError.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u7528 \u6237 \u540d", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u7528\u6237\u540d", None))
        self.passwordError.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5bc6   \u7801", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
        self.loginButton.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.forgetPwdButton.setText(QCoreApplication.translate("Form", u"\u5fd8\u8bb0\u5bc6\u7801\uff1f", None))
    # retranslateUi

