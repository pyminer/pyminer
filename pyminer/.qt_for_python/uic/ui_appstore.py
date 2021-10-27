# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_appstore.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)
import pyqtsource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1300, 809)
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.widget.setStyleSheet(u"background-color: rgb(49, 70,95);")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(849, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.toolButton_help = QToolButton(self.widget)
        self.toolButton_help.setObjectName(u"toolButton_help")
        self.toolButton_help.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.toolButton_help.setAutoRaise(True)

        self.horizontalLayout.addWidget(self.toolButton_help)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.toolButton_manage = QToolButton(self.widget)
        self.toolButton_manage.setObjectName(u"toolButton_manage")
        self.toolButton_manage.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.toolButton_manage.setAutoRaise(True)

        self.horizontalLayout.addWidget(self.toolButton_manage)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.widget_3.setStyleSheet(u"background-color: rgb(49, 70, 95);")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toolButton_4 = QToolButton(self.widget_3)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setEnabled(False)
        icon = QIcon()
        icon.addFile(u":/resources/icons/useLeftAll.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_4.setIcon(icon)
        self.toolButton_4.setAutoRaise(True)

        self.horizontalLayout_3.addWidget(self.toolButton_4)

        self.toolButton_5 = QToolButton(self.widget_3)
        self.toolButton_5.setObjectName(u"toolButton_5")
        icon1 = QIcon()
        icon1.addFile(u":/resources/icons/mIconModelLayer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_5.setIcon(icon1)
        self.toolButton_5.setIconSize(QSize(35, 35))
        self.toolButton_5.setAutoRaise(True)

        self.horizontalLayout_3.addWidget(self.toolButton_5)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(436, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.lineEdit = QLineEdit(self.widget_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(500, 35))
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);border:0px groove gray;border-radius:5px;padding:2px 4px")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.toolButton_3 = QToolButton(self.widget_3)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setMaximumSize(QSize(40, 40))
        icon2 = QIcon()
        icon2.addFile(u":/resources/icons/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_3.setIcon(icon2)
        self.toolButton_3.setIconSize(QSize(30, 30))
        self.toolButton_3.setAutoRaise(True)

        self.horizontalLayout_3.addWidget(self.toolButton_3)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"PyMiner App Store", None))
        self.toolButton_help.setText(QCoreApplication.translate("Form", u"Help", None))
        self.toolButton_manage.setText(QCoreApplication.translate("Form", u"Manage Apps", None))
        self.toolButton_4.setText(QCoreApplication.translate("Form", u"...", None))
        self.toolButton_5.setText(QCoreApplication.translate("Form", u"...", None))
        self.label.setText(QCoreApplication.translate("Form", u"App Store", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Search in sotre...", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi

