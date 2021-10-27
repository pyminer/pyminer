# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pm_marketplace.ui'
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
        self.toolButton = QToolButton(Form)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        self.toolButton_6 = QToolButton(Form)
        self.toolButton_6.setObjectName(u"toolButton_6")

        self.horizontalLayout.addWidget(self.toolButton_6)

        self.toolButton_2 = QToolButton(Form)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)

        self.toolButton_3 = QToolButton(Form)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout.addWidget(self.toolButton_3)

        self.toolButton_4 = QToolButton(Form)
        self.toolButton_4.setObjectName(u"toolButton_4")

        self.horizontalLayout.addWidget(self.toolButton_4)

        self.toolButton_5 = QToolButton(Form)
        self.toolButton_5.setObjectName(u"toolButton_5")

        self.horizontalLayout.addWidget(self.toolButton_5)

        self.toolButton_7 = QToolButton(Form)
        self.toolButton_7.setObjectName(u"toolButton_7")

        self.horizontalLayout.addWidget(self.toolButton_7)

        self.toolButton_8 = QToolButton(Form)
        self.toolButton_8.setObjectName(u"toolButton_8")

        self.horizontalLayout.addWidget(self.toolButton_8)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 4):
            self.tableWidget.setRowCount(4)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setCheckState(Qt.Unchecked);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setCheckState(Qt.Unchecked);
        self.tableWidget.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setCheckState(Qt.Unchecked);
        self.tableWidget.setItem(2, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setCheckState(Qt.Unchecked);
        self.tableWidget.setItem(3, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setItem(3, 1, __qtablewidgetitem14)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6269\u5c55\u4e2d\u5fc3", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"\u5b89\u88c5", None))
        self.toolButton_6.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"\u8be6\u60c5", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0", None))
        self.toolButton_4.setText(QCoreApplication.translate("Form", u"\u5378\u8f7d", None))
        self.toolButton_5.setText(QCoreApplication.translate("Form", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.toolButton_7.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
        self.toolButton_8.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u7248\u672c", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"1", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"2", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"3", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"4", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem7 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"numpy", None));
        ___qtablewidgetitem8 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"1.19.3", None));
        ___qtablewidgetitem9 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"pandas", None));
        ___qtablewidgetitem10 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"1.1.1", None));
        ___qtablewidgetitem11 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"matplotlib", None));
        ___qtablewidgetitem12 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"3.3.3", None));
        ___qtablewidgetitem13 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"scipy", None));
        ___qtablewidgetitem14 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Form", u"1.0.2", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

