# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_first_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(620, 580)
        Form.setMinimumSize(QSize(620, 580))
        Form.setMaximumSize(QSize(620, 580))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(28)
        self.label_3.setFont(font)
        self.label_3.setPixmap(QPixmap(u":/resources/images/bg.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_3)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 270))
        self.widget.setMaximumSize(QSize(16777215, 270))
        self.widget.setStyleSheet(u"background-color: rgb(33, 33, 33);")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_24 = QLabel(self.widget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(20, 0))
        self.label_24.setMaximumSize(QSize(20, 16777215))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_24.setFont(font1)
        self.label_24.setStyleSheet(u"color: rgb(229, 229, 229);")

        self.horizontalLayout_7.addWidget(self.label_24)

        self.label_23 = QLabel(self.widget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)
        self.label_23.setStyleSheet(u"color: rgb(229, 229, 229);")

        self.horizontalLayout_7.addWidget(self.label_23)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(300, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.toolButton_2 = QToolButton(self.widget_3)
        self.toolButton_2.setObjectName(u"toolButton_2")
        icon = QIcon()
        icon.addFile(u":/resources/icons/python.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QSize(18, 18))

        self.horizontalLayout_4.addWidget(self.toolButton_2)

        self.btn_open_python = QToolButton(self.widget_3)
        self.btn_open_python.setObjectName(u"btn_open_python")
        self.btn_open_python.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_open_python.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.btn_open_python)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButton_3 = QToolButton(self.widget_3)
        self.toolButton_3.setObjectName(u"toolButton_3")
        icon1 = QIcon()
        icon1.addFile(u":/resources/icons/csv.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_3.setIcon(icon1)
        self.toolButton_3.setIconSize(QSize(18, 18))

        self.horizontalLayout_5.addWidget(self.toolButton_3)

        self.btn_open_csv = QToolButton(self.widget_3)
        self.btn_open_csv.setObjectName(u"btn_open_csv")
        self.btn_open_csv.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_open_csv.setAutoRaise(True)

        self.horizontalLayout_5.addWidget(self.btn_open_csv)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.toolButton_4 = QToolButton(self.widget_3)
        self.toolButton_4.setObjectName(u"toolButton_4")
        icon2 = QIcon()
        icon2.addFile(u":/resources/icons/excel.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_4.setIcon(icon2)
        self.toolButton_4.setIconSize(QSize(18, 18))

        self.horizontalLayout_6.addWidget(self.toolButton_4)

        self.btn_open_excel = QToolButton(self.widget_3)
        self.btn_open_excel.setObjectName(u"btn_open_excel")
        self.btn_open_excel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_open_excel.setAutoRaise(True)

        self.horizontalLayout_6.addWidget(self.btn_open_excel)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.toolButton_10 = QToolButton(self.widget_3)
        self.toolButton_10.setObjectName(u"toolButton_10")
        icon3 = QIcon()
        icon3.addFile(u":/resources/icons/E-matlab.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_10.setIcon(icon3)
        self.toolButton_10.setIconSize(QSize(18, 18))

        self.horizontalLayout_14.addWidget(self.toolButton_10)

        self.btn_open_matlab = QToolButton(self.widget_3)
        self.btn_open_matlab.setObjectName(u"btn_open_matlab")
        self.btn_open_matlab.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_open_matlab.setAutoRaise(True)

        self.horizontalLayout_14.addWidget(self.btn_open_matlab)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_6.addWidget(self.widget_3)

        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_5 = QVBoxLayout(self.widget_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolButton = QToolButton(self.widget_6)
        self.toolButton.setObjectName(u"toolButton")
        icon4 = QIcon()
        icon4.addFile(u":/resources/icons/open_folder.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon4)
        self.toolButton.setIconSize(QSize(18, 18))

        self.horizontalLayout_3.addWidget(self.toolButton)

        self.btn_open_folder = QToolButton(self.widget_6)
        self.btn_open_folder.setObjectName(u"btn_open_folder")
        self.btn_open_folder.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_open_folder.setAutoRaise(True)

        self.horizontalLayout_3.addWidget(self.btn_open_folder)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addWidget(self.widget_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_25 = QLabel(self.widget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(20, 0))
        self.label_25.setMaximumSize(QSize(20, 16777215))
        self.label_25.setFont(font1)
        self.label_25.setStyleSheet(u"color: rgb(229, 229, 229);")

        self.horizontalLayout_8.addWidget(self.label_25)

        self.label_26 = QLabel(self.widget)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)
        self.label_26.setStyleSheet(u"color: rgb(229, 229, 229);")

        self.horizontalLayout_8.addWidget(self.label_26)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_10 = QVBoxLayout(self.widget_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.toolButton_5 = QToolButton(self.widget_8)
        self.toolButton_5.setObjectName(u"toolButton_5")
        icon5 = QIcon()
        icon5.addFile(u":/resources/icons/website.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_5.setIcon(icon5)
        self.toolButton_5.setIconSize(QSize(18, 18))

        self.horizontalLayout_9.addWidget(self.toolButton_5)

        self.btn_manual = QToolButton(self.widget_8)
        self.btn_manual.setObjectName(u"btn_manual")
        self.btn_manual.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_manual.setAutoRaise(True)

        self.horizontalLayout_9.addWidget(self.btn_manual)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout_10.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.toolButton_6 = QToolButton(self.widget_8)
        self.toolButton_6.setObjectName(u"toolButton_6")
        self.toolButton_6.setIcon(icon5)
        self.toolButton_6.setIconSize(QSize(18, 18))

        self.horizontalLayout_10.addWidget(self.toolButton_6)

        self.btn_website = QToolButton(self.widget_8)
        self.btn_website.setObjectName(u"btn_website")
        self.btn_website.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_website.setAutoRaise(True)

        self.horizontalLayout_10.addWidget(self.btn_website)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.toolButton_7 = QToolButton(self.widget_8)
        self.toolButton_7.setObjectName(u"toolButton_7")
        self.toolButton_7.setIcon(icon5)
        self.toolButton_7.setIconSize(QSize(18, 18))

        self.horizontalLayout_11.addWidget(self.toolButton_7)

        self.btn_source = QToolButton(self.widget_8)
        self.btn_source.setObjectName(u"btn_source")
        self.btn_source.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_source.setAutoRaise(True)

        self.horizontalLayout_11.addWidget(self.btn_source)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)


        self.verticalLayout_10.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)


        self.verticalLayout_9.addWidget(self.widget_8)

        self.widget_9 = QWidget(self.widget)
        self.widget_9.setObjectName(u"widget_9")
        self.verticalLayout_11 = QVBoxLayout(self.widget_9)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.toolButton_8 = QToolButton(self.widget_9)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setIcon(icon5)
        self.toolButton_8.setIconSize(QSize(18, 18))

        self.horizontalLayout_12.addWidget(self.toolButton_8)

        self.btn_member = QToolButton(self.widget_9)
        self.btn_member.setObjectName(u"btn_member")
        self.btn_member.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_member.setAutoRaise(True)

        self.horizontalLayout_12.addWidget(self.btn_member)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)


        self.verticalLayout_11.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.toolButton_9 = QToolButton(self.widget_9)
        self.toolButton_9.setObjectName(u"toolButton_9")
        icon6 = QIcon()
        icon6.addFile(u":/resources/icons/donate.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_9.setIcon(icon6)
        self.toolButton_9.setIconSize(QSize(18, 18))

        self.horizontalLayout_13.addWidget(self.toolButton_9)

        self.btn_donate = QToolButton(self.widget_9)
        self.btn_donate.setObjectName(u"btn_donate")
        self.btn_donate.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.btn_donate.setAutoRaise(True)

        self.horizontalLayout_13.addWidget(self.btn_donate)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_9)


        self.verticalLayout_11.addLayout(self.horizontalLayout_13)


        self.verticalLayout_9.addWidget(self.widget_9)


        self.horizontalLayout_2.addLayout(self.verticalLayout_9)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText("")
        self.label_24.setText("")
        self.label_23.setText(QCoreApplication.translate("Form", u"Open File", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_open_python.setText(QCoreApplication.translate("Form", u"Python File", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_open_csv.setText(QCoreApplication.translate("Form", u"CSV File", None))
        self.toolButton_4.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_open_excel.setText(QCoreApplication.translate("Form", u"Excel File", None))
        self.toolButton_10.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_open_matlab.setText(QCoreApplication.translate("Form", u"MATLAB File", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_open_folder.setText(QCoreApplication.translate("Form", u"Open Folder...", None))
        self.label_25.setText("")
        self.label_26.setText(QCoreApplication.translate("Form", u"Quick Start", None))
        self.toolButton_5.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_manual.setText(QCoreApplication.translate("Form", u"Use Manual", None))
        self.toolButton_6.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_website.setText(QCoreApplication.translate("Form", u"Official Site", None))
        self.toolButton_7.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_source.setText(QCoreApplication.translate("Form", u"Gitee Repo", None))
        self.toolButton_8.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_member.setText(QCoreApplication.translate("Form", u"Join Us", None))
        self.toolButton_9.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_donate.setText(QCoreApplication.translate("Form", u"Donate", None))
    # retranslateUi

