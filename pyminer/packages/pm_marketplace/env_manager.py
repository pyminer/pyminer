# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'env_manager.ui'
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
        Form.resize(800, 500)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listWidget = QListWidget(self.widget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_new = QPushButton(self.widget)
        self.pushButton_new.setObjectName(u"pushButton_new")

        self.horizontalLayout_2.addWidget(self.pushButton_new)

        self.pushButton_copy = QPushButton(self.widget)
        self.pushButton_copy.setObjectName(u"pushButton_copy")

        self.horizontalLayout_2.addWidget(self.pushButton_copy)

        self.pushButton_from = QPushButton(self.widget)
        self.pushButton_from.setObjectName(u"pushButton_from")

        self.horizontalLayout_2.addWidget(self.pushButton_from)

        self.pushButton_delete = QPushButton(self.widget)
        self.pushButton_delete.setObjectName(u"pushButton_delete")

        self.horizontalLayout_2.addWidget(self.pushButton_delete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout.addWidget(self.widget)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.horizontalLayout_5 = QHBoxLayout(self.page_1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_install = QPushButton(self.page_1)
        self.pushButton_install.setObjectName(u"pushButton_install")

        self.horizontalLayout_4.addWidget(self.pushButton_install)

        self.pushButton_import = QPushButton(self.page_1)
        self.pushButton_import.setObjectName(u"pushButton_import")

        self.horizontalLayout_4.addWidget(self.pushButton_import)

        self.pushButton_export = QPushButton(self.page_1)
        self.pushButton_export.setObjectName(u"pushButton_export")

        self.horizontalLayout_4.addWidget(self.pushButton_export)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.lineEdit_find = QLineEdit(self.page_1)
        self.lineEdit_find.setObjectName(u"lineEdit_find")
        self.lineEdit_find.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_4.addWidget(self.lineEdit_find)

        self.comboBox = QComboBox(self.page_1)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.tableWidget = QTableWidget(self.page_1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_3.addWidget(self.tableWidget)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.pushButton = QPushButton(self.page_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(500, 250, 75, 23))
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Python\u73af\u5883\u7ba1\u7406", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u73af\u5883", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton_new.setText(QCoreApplication.translate("Form", u"\u65b0\u5efa", None))
        self.pushButton_copy.setText(QCoreApplication.translate("Form", u"\u590d\u5236", None))
        self.pushButton_from.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.pushButton_install.setText(QCoreApplication.translate("Form", u"\u5b89\u88c5", None))
        self.pushButton_import.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
        self.pushButton_export.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        self.lineEdit_find.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u5305\u540d", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"\u5df2\u5b89\u88c5", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"\u53ef\u66f4\u65b0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"\u6e90", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

