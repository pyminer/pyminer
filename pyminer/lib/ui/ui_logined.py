# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_logined.ui'
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
        Form.resize(407, 361)
        Form.setMinimumSize(QSize(407, 361))
        Form.setMaximumSize(QSize(407, 361))
        Form.setBaseSize(QSize(407, 361))
        Form.setStyleSheet(u"QPushButton{\n"
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
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 0, 391, 341))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Plain)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMargin(0)

        self.horizontalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout.addItem(self.verticalSpacer_2)

        self.usernameLabel = QLabel(self.layoutWidget)
        self.usernameLabel.setObjectName(u"usernameLabel")
        self.usernameLabel.setCursor(QCursor(Qt.IBeamCursor))
        self.usernameLabel.setLayoutDirection(Qt.LeftToRight)
        self.usernameLabel.setWordWrap(True)
        self.usernameLabel.setMargin(0)
        self.usernameLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.usernameLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.loginOutButton = QPushButton(self.layoutWidget)
        self.loginOutButton.setObjectName(u"loginOutButton")
        self.loginOutButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.loginOutButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7528\u6237\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7528  \u6237   \u540d", None))
        self.usernameLabel.setText("")
        self.loginOutButton.setText(QCoreApplication.translate("Form", u"\u6ce8  \u9500", None))
    # retranslateUi

