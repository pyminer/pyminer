# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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

        self.toolButton_downloan = QToolButton(Form)
        self.toolButton_downloan.setObjectName(u"toolButton_downloan")
        self.toolButton_downloan.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_downloan)

        self.toolButton_detail = QToolButton(Form)
        self.toolButton_detail.setObjectName(u"toolButton_detail")
        self.toolButton_detail.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_detail)

        self.toolButton_update = QToolButton(Form)
        self.toolButton_update.setObjectName(u"toolButton_update")
        self.toolButton_update.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_update)

        self.toolButton_uninstall = QToolButton(Form)
        self.toolButton_uninstall.setObjectName(u"toolButton_uninstall")
        self.toolButton_uninstall.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_uninstall)

        self.toolButton_check_update = QToolButton(Form)
        self.toolButton_check_update.setObjectName(u"toolButton_check_update")
        self.toolButton_check_update.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_check_update)

        self.toolButton_install_requirements = QToolButton(Form)
        self.toolButton_install_requirements.setObjectName(u"toolButton_install_requirements")
        self.toolButton_install_requirements.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_install_requirements)

        self.toolButton_freeze_requirements = QToolButton(Form)
        self.toolButton_freeze_requirements.setObjectName(u"toolButton_freeze_requirements")
        self.toolButton_freeze_requirements.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_freeze_requirements)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget.rowCount() < 9995):
            self.tableWidget.setRowCount(9995)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setRowCount(9995)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6269\u5c55\u4e2d\u5fc3", None))
        self.toolButton_install.setText(QCoreApplication.translate("Form", u"Install", None))
        self.toolButton_downloan.setText(QCoreApplication.translate("Form", u"Download", None))
        self.toolButton_detail.setText(QCoreApplication.translate("Form", u"Details", None))
        self.toolButton_update.setText(QCoreApplication.translate("Form", u"Update", None))
        self.toolButton_uninstall.setText(QCoreApplication.translate("Form", u"Uninstall", None))
        self.toolButton_check_update.setText(QCoreApplication.translate("Form", u"CheckUpdate", None))
        self.toolButton_install_requirements.setText(QCoreApplication.translate("Form", u"Import", None))
        self.toolButton_freeze_requirements.setText(QCoreApplication.translate("Form", u"Export", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Version", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Latest Version", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Type", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Update", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Uninstall", None));
    # retranslateUi

