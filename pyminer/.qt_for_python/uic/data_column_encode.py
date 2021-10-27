# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_column_encode.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_5 = QHBoxLayout(self.tab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(300, 16777215))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listWidget_var = QListWidget(self.widget_2)
        self.listWidget_var.setObjectName(u"listWidget_var")

        self.verticalLayout_2.addWidget(self.listWidget_var)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_5.addWidget(self.widget_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget_selecetd = QListWidget(self.groupBox_2)
        self.listWidget_selecetd.setObjectName(u"listWidget_selecetd")
        self.listWidget_selecetd.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.listWidget_selecetd)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.comboBox_6 = QComboBox(self.groupBox_3)
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_10.addWidget(self.comboBox_6)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableWidget = QTableWidget(self.groupBox_4)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_3.addWidget(self.tableWidget)


        self.verticalLayout_6.addWidget(self.groupBox_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_13.addWidget(self.tabWidget)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout_3.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget_3)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_3.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_3.addWidget(self.pushButton_cancel)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_13.addWidget(self.widget_3)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u91cd\u7f16\u7801\u503c", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u7f16\u7801\u65b9\u6848:", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Form", u"OneHot", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"\u9884\u89c8", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u91cd\u7f16\u7801\u540e\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u57fa\u672c", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

