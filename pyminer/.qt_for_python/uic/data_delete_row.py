# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_delete_row.ui'
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
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

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
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
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

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_to_right = QPushButton(self.widget_2)
        self.pushButton_to_right.setObjectName(u"pushButton_to_right")

        self.verticalLayout_4.addWidget(self.pushButton_to_right)

        self.pushButton_to_right_all = QPushButton(self.widget_2)
        self.pushButton_to_right_all.setObjectName(u"pushButton_to_right_all")

        self.verticalLayout_4.addWidget(self.pushButton_to_right_all)


        self.verticalLayout_17.addLayout(self.verticalLayout_4)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.pushButton_to_left = QPushButton(self.widget_2)
        self.pushButton_to_left.setObjectName(u"pushButton_to_left")

        self.verticalLayout_16.addWidget(self.pushButton_to_left)

        self.pushButton_to_left_all = QPushButton(self.widget_2)
        self.pushButton_to_left_all.setObjectName(u"pushButton_to_left_all")

        self.verticalLayout_16.addWidget(self.pushButton_to_left_all)


        self.verticalLayout_17.addLayout(self.verticalLayout_16)


        self.horizontalLayout.addLayout(self.verticalLayout_17)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.listWidget_selecetd = QListWidget(self.tab)
        self.listWidget_selecetd.setObjectName(u"listWidget_selecetd")

        self.verticalLayout_3.addWidget(self.listWidget_selecetd)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_8 = QVBoxLayout(self.tab_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.comboBox)

        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_4.addWidget(self.comboBox_2)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.comboBox_3 = QComboBox(self.groupBox)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_4.addWidget(self.comboBox_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_4.addWidget(self.pushButton_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.tableWidget_2 = QTableWidget(self.groupBox)
        if (self.tableWidget_2.columnCount() < 4):
            self.tableWidget_2.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget_2.rowCount() < 2):
            self.tableWidget_2.setRowCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setCheckState(Qt.Checked);
        self.tableWidget_2.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_2.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignTrailing|Qt.AlignVCenter);
        self.tableWidget_2.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_2.setItem(0, 3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setCheckState(Qt.Checked);
        self.tableWidget_2.setItem(1, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_2.setItem(1, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignTrailing|Qt.AlignVCenter);
        self.tableWidget_2.setItem(1, 2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_2.setItem(1, 3, __qtablewidgetitem13)
        self.tableWidget_2.setObjectName(u"tableWidget_2")

        self.verticalLayout_7.addWidget(self.tableWidget_2)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tableWidget = QTableWidget(self.groupBox_2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_6.addWidget(self.tableWidget)


        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tab_2, "")

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

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u5220\u9664\u884c", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_to_right.setText(QCoreApplication.translate("Form", u">", None))
        self.pushButton_to_right_all.setText(QCoreApplication.translate("Form", u">>", None))
        self.pushButton_to_left.setText(QCoreApplication.translate("Form", u"<", None))
        self.pushButton_to_left_all.setText(QCoreApplication.translate("Form", u"<<", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u57fa\u672c", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u67e5\u8be2\u6761\u4ef6", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"\u53d8\u91cf\u5217\u8868", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"\u4e0d\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Form", u"\u5c0f\u4e8e", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("Form", u"\u5c0f\u4e8e\u6216\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("Form", u"\u5927\u4e8e", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("Form", u"\u5927\u4e8e\u6216\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("Form", u"\u4e0d\u5728\u5217\u8868\u4e2d", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("Form", u"\u4ecb\u4e8e", None))
        self.comboBox_2.setItemText(8, QCoreApplication.translate("Form", u"\u4e0d\u4ecb\u4e8e", None))
        self.comboBox_2.setItemText(9, QCoreApplication.translate("Form", u"\u7f3a\u5931", None))
        self.comboBox_2.setItemText(10, QCoreApplication.translate("Form", u"\u975e\u7f3a\u5931", None))
        self.comboBox_2.setItemText(11, QCoreApplication.translate("Form", u"\u6a21\u7cca\u5339\u914d", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"AND", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"OR", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"\u65b0\u589e", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        ___qtablewidgetitem = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u53d8\u91cf", None));
        ___qtablewidgetitem1 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u67e5\u8be2\u6761\u4ef6", None));
        ___qtablewidgetitem2 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u5339\u914d\u89c4\u5219", None));
        ___qtablewidgetitem3 = self.tableWidget_2.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u6761\u4ef6\u903b\u8f91", None));
        ___qtablewidgetitem4 = self.tableWidget_2.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"1", None));
        ___qtablewidgetitem5 = self.tableWidget_2.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"2", None));

        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        ___qtablewidgetitem6 = self.tableWidget_2.item(0, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"SEX", None));
        ___qtablewidgetitem7 = self.tableWidget_2.item(0, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"\u7b49\u4e8e", None));
        ___qtablewidgetitem8 = self.tableWidget_2.item(0, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"1", None));
        ___qtablewidgetitem9 = self.tableWidget_2.item(0, 3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"AND", None));
        ___qtablewidgetitem10 = self.tableWidget_2.item(1, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"NAME", None));
        ___qtablewidgetitem11 = self.tableWidget_2.item(1, 1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"\u7b49\u4e8e", None));
        ___qtablewidgetitem12 = self.tableWidget_2.item(1, 2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"2", None));
        ___qtablewidgetitem13 = self.tableWidget_2.item(1, 3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"AND", None));
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)

        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

