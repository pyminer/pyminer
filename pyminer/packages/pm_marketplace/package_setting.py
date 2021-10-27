# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_setting.ui'
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
        Form.resize(600, 400)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(120, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.widget_2)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.listWidget)

        self.splitter.addWidget(self.widget_2)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBox_source = QComboBox(self.page)
        self.comboBox_source.addItem("")
        self.comboBox_source.addItem("")
        self.comboBox_source.addItem("")
        self.comboBox_source.addItem("")
        self.comboBox_source.addItem("")
        self.comboBox_source.addItem("")
        self.comboBox_source.setObjectName(u"comboBox_source")
        self.comboBox_source.setEnabled(True)
        self.comboBox_source.setMinimumSize(QSize(100, 0))
        self.comboBox_source.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.comboBox_source)

        self.lineEdit_source = QLineEdit(self.page)
        self.lineEdit_source.setObjectName(u"lineEdit_source")
        self.lineEdit_source.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lineEdit_source.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_source)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox_dir = QComboBox(self.page)
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.setObjectName(u"comboBox_dir")
        self.comboBox_dir.setMinimumSize(QSize(100, 0))
        self.comboBox_dir.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.comboBox_dir)

        self.lineEdit_dir = QLineEdit(self.page)
        self.lineEdit_dir.setObjectName(u"lineEdit_dir")
        self.lineEdit_dir.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_dir)

        self.toolButton = QToolButton(self.page)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_3.addWidget(self.toolButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.comboBox_dir_2 = QComboBox(self.page)
        self.comboBox_dir_2.addItem("")
        self.comboBox_dir_2.addItem("")
        self.comboBox_dir_2.addItem("")
        self.comboBox_dir_2.addItem("")
        self.comboBox_dir_2.setObjectName(u"comboBox_dir_2")
        self.comboBox_dir_2.setMinimumSize(QSize(100, 0))
        self.comboBox_dir_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.comboBox_dir_2)

        self.lineEdit_dir_2 = QLineEdit(self.page)
        self.lineEdit_dir_2.setObjectName(u"lineEdit_dir_2")
        self.lineEdit_dir_2.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_dir_2)

        self.toolButton_2 = QToolButton(self.page)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout_4.addWidget(self.toolButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_5 = QHBoxLayout(self.page_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.page_2)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.horizontalLayout_5.addWidget(self.tableWidget)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_browser = QPushButton(self.page_2)
        self.pushButton_browser.setObjectName(u"pushButton_browser")

        self.verticalLayout_4.addWidget(self.pushButton_browser)

        self.pushButton_default = QPushButton(self.page_2)
        self.pushButton_default.setObjectName(u"pushButton_default")

        self.verticalLayout_4.addWidget(self.pushButton_default)

        self.pushButton_delete = QPushButton(self.page_2)
        self.pushButton_delete.setObjectName(u"pushButton_delete")

        self.verticalLayout_4.addWidget(self.pushButton_delete)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.stackedWidget.addWidget(self.page_2)
        self.splitter.addWidget(self.stackedWidget)

        self.verticalLayout.addWidget(self.splitter)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 50))
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_help = QPushButton(self.widget)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u8bbe\u7f6e", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"\u5e38\u89c4", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"\u89e3\u91ca\u5668", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("Form", u"\u4e0b \u8f7d \u6e90:", None))
        self.comboBox_source.setItemText(0, QCoreApplication.translate("Form", u"\u817e\u8baf(\u63a8\u8350)", None))
        self.comboBox_source.setItemText(1, QCoreApplication.translate("Form", u"\u5b98\u65b9", None))
        self.comboBox_source.setItemText(2, QCoreApplication.translate("Form", u"\u6e05\u534e\u5927\u5b66", None))
        self.comboBox_source.setItemText(3, QCoreApplication.translate("Form", u"\u963f\u91cc", None))
        self.comboBox_source.setItemText(4, QCoreApplication.translate("Form", u"\u8c46\u74e3", None))
        self.comboBox_source.setItemText(5, QCoreApplication.translate("Form", u"\u81ea\u5b9a\u4e49", None))

        self.lineEdit_source.setText(QCoreApplication.translate("Form", u"https://mirrors.cloud.tencent.com/pypi/simple", None))
        self.lineEdit_source.setPlaceholderText(QCoreApplication.translate("Form", u"\u817e\u8baf\u955c\u50cf\u6e90", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5b89\u88c5\u9009\u9879:", None))
        self.comboBox_dir.setItemText(0, QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u4f4d\u7f6e", None))
        self.comboBox_dir.setItemText(1, QCoreApplication.translate("Form", u"\u7528\u6237\u76ee\u5f55", None))
        self.comboBox_dir.setItemText(2, QCoreApplication.translate("Form", u"\u4ec5\u4e0b\u8f7d", None))
        self.comboBox_dir.setItemText(3, QCoreApplication.translate("Form", u"\u81ea\u5b9a\u4e49", None))

        self.lineEdit_dir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u8def\u5f84:", None))
        self.comboBox_dir_2.setItemText(0, QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u4f4d\u7f6e", None))
        self.comboBox_dir_2.setItemText(1, QCoreApplication.translate("Form", u"\u7528\u6237\u76ee\u5f55", None))
        self.comboBox_dir_2.setItemText(2, QCoreApplication.translate("Form", u"\u4ec5\u4e0b\u8f7d", None))
        self.comboBox_dir_2.setItemText(3, QCoreApplication.translate("Form", u"\u81ea\u5b9a\u4e49", None))

        self.lineEdit_dir_2.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"...", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u8def\u5f84", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u9ed8\u8ba4", None));
        self.pushButton_browser.setText(QCoreApplication.translate("Form", u"\u6d4f\u89c8", None))
        self.pushButton_default.setText(QCoreApplication.translate("Form", u"\u8bbe\u4e3a\u9ed8\u8ba4", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

