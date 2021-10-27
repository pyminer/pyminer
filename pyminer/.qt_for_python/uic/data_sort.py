# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_sort.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(767, 600)
        Form.setMaximumSize(QSize(767, 16777215))
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listWidget_var = QListWidget(self.widget_2)
        self.listWidget_var.setObjectName(u"listWidget_var")

        self.verticalLayout_2.addWidget(self.listWidget_var)


        self.verticalLayout_7.addLayout(self.verticalLayout_2)


        self.horizontalLayout.addWidget(self.widget_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_add = QPushButton(self.tab)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_add.setIcon(icon)

        self.verticalLayout_4.addWidget(self.pushButton_add)

        self.pushButton_delete = QPushButton(self.tab)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_delete.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.pushButton_delete)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget_selected = QListWidget(self.tab)
        self.listWidget_selected.setObjectName(u"listWidget_selected")

        self.horizontalLayout_2.addWidget(self.listWidget_selected)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_start_add = QPushButton(self.tab)
        self.pushButton_start_add.setObjectName(u"pushButton_start_add")
        self.pushButton_start_add.setMaximumSize(QSize(50, 16777215))
        self.pushButton_start_add.setIcon(icon)

        self.verticalLayout_3.addWidget(self.pushButton_start_add)

        self.pushButton_start_up = QPushButton(self.tab)
        self.pushButton_start_up.setObjectName(u"pushButton_start_up")
        self.pushButton_start_up.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_up.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.pushButton_start_up)

        self.pushButton_start_down = QPushButton(self.tab)
        self.pushButton_start_down.setObjectName(u"pushButton_start_down")
        self.pushButton_start_down.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_down.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.pushButton_start_down)

        self.pushButton_start_del = QPushButton(self.tab)
        self.pushButton_start_del.setObjectName(u"pushButton_start_del")
        self.pushButton_start_del.setMaximumSize(QSize(50, 16777215))
        self.pushButton_start_del.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.pushButton_start_del)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_9 = QVBoxLayout(self.tab_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox_sort_column = QComboBox(self.tab_3)
        self.comboBox_sort_column.setObjectName(u"comboBox_sort_column")
        self.comboBox_sort_column.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_5.addWidget(self.comboBox_sort_column)

        self.comboBox_sort_condition = QComboBox(self.tab_3)
        self.comboBox_sort_condition.addItem("")
        self.comboBox_sort_condition.addItem("")
        self.comboBox_sort_condition.setObjectName(u"comboBox_sort_condition")

        self.horizontalLayout_5.addWidget(self.comboBox_sort_condition)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tableWidget_sort = QTableWidget(self.tab_3)
        if (self.tableWidget_sort.columnCount() < 2):
            self.tableWidget_sort.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_sort.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_sort.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget_sort.rowCount() < 1):
            self.tableWidget_sort.setRowCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_sort.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setCheckState(Qt.Checked);
        self.tableWidget_sort.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_sort.setItem(0, 1, __qtablewidgetitem4)
        self.tableWidget_sort.setObjectName(u"tableWidget_sort")

        self.horizontalLayout_6.addWidget(self.tableWidget_sort)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.pushButton_sort_add = QPushButton(self.tab_3)
        self.pushButton_sort_add.setObjectName(u"pushButton_sort_add")
        self.pushButton_sort_add.setMaximumSize(QSize(50, 16777215))
        self.pushButton_sort_add.setIcon(icon)

        self.verticalLayout_8.addWidget(self.pushButton_sort_add)

        self.pushButton_sort_up = QPushButton(self.tab_3)
        self.pushButton_sort_up.setObjectName(u"pushButton_sort_up")
        self.pushButton_sort_up.setMaximumSize(QSize(50, 16777215))
        self.pushButton_sort_up.setIcon(icon2)

        self.verticalLayout_8.addWidget(self.pushButton_sort_up)

        self.pushButton_sort_down = QPushButton(self.tab_3)
        self.pushButton_sort_down.setObjectName(u"pushButton_sort_down")
        self.pushButton_sort_down.setMaximumSize(QSize(50, 16777215))
        self.pushButton_sort_down.setIcon(icon3)

        self.verticalLayout_8.addWidget(self.pushButton_sort_down)

        self.pushButton_sort_del = QPushButton(self.tab_3)
        self.pushButton_sort_del.setObjectName(u"pushButton_sort_del")
        self.pushButton_sort_del.setMaximumSize(QSize(50, 16777215))
        self.pushButton_sort_del.setIcon(icon1)

        self.verticalLayout_8.addWidget(self.pushButton_sort_del)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_8)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.tableWidget_sort_preview = QTableWidget(self.tab_3)
        self.tableWidget_sort_preview.setObjectName(u"tableWidget_sort_preview")

        self.verticalLayout_9.addWidget(self.tableWidget_sort_preview)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_13.addWidget(self.tabWidget)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout_3.addWidget(self.pushButton_help)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineEdit_dataset_name = QLineEdit(self.widget_3)
        self.lineEdit_dataset_name.setObjectName(u"lineEdit_dataset_name")

        self.horizontalLayout_3.addWidget(self.lineEdit_dataset_name)

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
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u6392\u5e8f", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_add.setText("")
        self.pushButton_delete.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.pushButton_start_add.setText("")
        self.pushButton_start_up.setText("")
        self.pushButton_start_down.setText("")
        self.pushButton_start_del.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u57fa\u672c", None))
        self.comboBox_sort_condition.setItemText(0, QCoreApplication.translate("Form", u"\u9012\u589e", None))
        self.comboBox_sort_condition.setItemText(1, QCoreApplication.translate("Form", u"\u9012\u51cf", None))

        ___qtablewidgetitem = self.tableWidget_sort.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u53d8\u91cf", None));
        ___qtablewidgetitem1 = self.tableWidget_sort.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u6392\u5e8f\u89c4\u5219", None));
        ___qtablewidgetitem2 = self.tableWidget_sort.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"1", None));

        __sortingEnabled = self.tableWidget_sort.isSortingEnabled()
        self.tableWidget_sort.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.tableWidget_sort.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"SEX", None));
        ___qtablewidgetitem4 = self.tableWidget_sort.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u9012\u589e", None));
        self.tableWidget_sort.setSortingEnabled(__sortingEnabled)

        self.pushButton_sort_add.setText("")
        self.pushButton_sort_up.setText("")
        self.pushButton_sort_down.setText("")
        self.pushButton_sort_del.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\u6392\u5e8f", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5904\u7406\u540e\u6570\u636e\u96c6\u540d\u79f0", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

