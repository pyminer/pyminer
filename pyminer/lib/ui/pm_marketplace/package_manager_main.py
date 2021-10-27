# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_manager_main.ui'
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
        Form.resize(978, 664)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton_install = QToolButton(Form)
        self.toolButton_install.setObjectName(u"toolButton_install")
        self.toolButton_install.setEnabled(True)

        self.horizontalLayout.addWidget(self.toolButton_install)

        self.toolButton_update = QToolButton(Form)
        self.toolButton_update.setObjectName(u"toolButton_update")
        self.toolButton_update.setEnabled(True)

        self.horizontalLayout.addWidget(self.toolButton_update)

        self.toolButton_uninstall = QToolButton(Form)
        self.toolButton_uninstall.setObjectName(u"toolButton_uninstall")
        self.toolButton_uninstall.setEnabled(True)

        self.horizontalLayout.addWidget(self.toolButton_uninstall)

        self.toolButton_install_requirements = QToolButton(Form)
        self.toolButton_install_requirements.setObjectName(u"toolButton_install_requirements")
        self.toolButton_install_requirements.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_install_requirements)

        self.toolButton_freeze_requirements = QToolButton(Form)
        self.toolButton_freeze_requirements.setObjectName(u"toolButton_freeze_requirements")
        self.toolButton_freeze_requirements.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_freeze_requirements)

        self.toolButton_downloan = QToolButton(Form)
        self.toolButton_downloan.setObjectName(u"toolButton_downloan")
        self.toolButton_downloan.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_downloan)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget.rowCount() < 100):
            self.tableWidget.setRowCount(100)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setRowCount(100)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Package Manager", None))
        self.toolButton_install.setText(QCoreApplication.translate("Form", u"Install", None))
        self.toolButton_update.setText(QCoreApplication.translate("Form", u"Update", None))
        self.toolButton_uninstall.setText(QCoreApplication.translate("Form", u"Uninstall", None))
        self.toolButton_install_requirements.setText(QCoreApplication.translate("Form", u"Import", None))
        self.toolButton_freeze_requirements.setText(QCoreApplication.translate("Form", u"Export", None))
        self.toolButton_downloan.setText(QCoreApplication.translate("Form", u"Download", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Version", None));
    # retranslateUi

