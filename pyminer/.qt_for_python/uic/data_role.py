# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_role.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 25))
        self.label.setMaximumSize(QSize(50, 25))

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_columns = QComboBox(Form)
        self.comboBox_columns.addItem("")
        self.comboBox_columns.setObjectName(u"comboBox_columns")
        self.comboBox_columns.setEnabled(True)
        self.comboBox_columns.setMinimumSize(QSize(80, 25))
        self.comboBox_columns.setMaximumSize(QSize(80, 25))

        self.horizontalLayout.addWidget(self.comboBox_columns)

        self.lineEdit_col_find = QLineEdit(Form)
        self.lineEdit_col_find.setObjectName(u"lineEdit_col_find")
        self.lineEdit_col_find.setMinimumSize(QSize(250, 25))
        self.lineEdit_col_find.setMaximumSize(QSize(250, 25))

        self.horizontalLayout.addWidget(self.lineEdit_col_find)

        self.pushButton_find = QPushButton(Form)
        self.pushButton_find.setObjectName(u"pushButton_find")
        self.pushButton_find.setMinimumSize(QSize(60, 25))
        self.pushButton_find.setMaximumSize(QSize(60, 25))

        self.horizontalLayout.addWidget(self.pushButton_find)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.tableWidget_dataset = QTableWidget(Form)
        if (self.tableWidget_dataset.columnCount() < 10):
            self.tableWidget_dataset.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_dataset.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if (self.tableWidget_dataset.rowCount() < 1):
            self.tableWidget_dataset.setRowCount(1)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_dataset.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_dataset.setItem(0, 7, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_dataset.setItem(0, 9, __qtablewidgetitem12)
        self.tableWidget_dataset.setObjectName(u"tableWidget_dataset")
        self.tableWidget_dataset.setMinimumSize(QSize(500, 400))

        self.gridLayout.addWidget(self.tableWidget_dataset, 1, 0, 1, 1)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_code = QPushButton(self.widget_3)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout_3.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.pushButton_help)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButton_ok = QPushButton(self.widget_3)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_3.addWidget(self.pushButton_ok)

        self.pushButton_export = QPushButton(self.widget_3)
        self.pushButton_export.setObjectName(u"pushButton_export")

        self.horizontalLayout_3.addWidget(self.pushButton_export)

        self.pushButton_cancel = QPushButton(self.widget_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_3.addWidget(self.pushButton_cancel)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.gridLayout.addWidget(self.widget_3, 2, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u89d2\u8272", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u67e5\u627e\u5185\u5bb9\uff1a", None))
        self.comboBox_columns.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8", None))

        self.pushButton_find.setText(QCoreApplication.translate("Form", u"\u67e5\u627e", None))
        ___qtablewidgetitem = self.tableWidget_dataset.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u53d8\u91cf\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tableWidget_dataset.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u6807\u7b7e", None));
        ___qtablewidgetitem2 = self.tableWidget_dataset.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7c7b\u578b", None));
        ___qtablewidgetitem3 = self.tableWidget_dataset.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u5bbd\u5ea6", None));
        ___qtablewidgetitem4 = self.tableWidget_dataset.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u5c0f\u6570\u4f4d\u6570", None));
        ___qtablewidgetitem5 = self.tableWidget_dataset.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"\u7f3a\u5931", None));
        ___qtablewidgetitem6 = self.tableWidget_dataset.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"\u7c7b\u522b\u6570", None));
        ___qtablewidgetitem7 = self.tableWidget_dataset.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u53c2\u4e0e", None));
        ___qtablewidgetitem8 = self.tableWidget_dataset.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"\u6d4b\u91cf\u6c34\u5e73", None));
        ___qtablewidgetitem9 = self.tableWidget_dataset.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u89d2\u8272", None));
        ___qtablewidgetitem10 = self.tableWidget_dataset.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"1", None));

        __sortingEnabled = self.tableWidget_dataset.isSortingEnabled()
        self.tableWidget_dataset.setSortingEnabled(False)
        self.tableWidget_dataset.setSortingEnabled(__sortingEnabled)

        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_export.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

