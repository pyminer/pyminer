# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_import_csv.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from resources import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        Form.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/resources/icons/csv.svg", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.label_8)

        self.lineEdit_filePath = QLineEdit(Form)
        self.lineEdit_filePath.setObjectName(u"lineEdit_filePath")
        self.lineEdit_filePath.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.lineEdit_filePath)

        self.pushButton_choosefile = QPushButton(Form)
        self.pushButton_choosefile.setObjectName(u"pushButton_choosefile")
        self.pushButton_choosefile.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.pushButton_choosefile)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.tableWidget_previewData = QTableWidget(Form)
        self.tableWidget_previewData.setObjectName(u"tableWidget_previewData")

        self.verticalLayout_3.addWidget(self.tableWidget_previewData)

        self.checkBox_ifColumns = QCheckBox(Form)
        self.checkBox_ifColumns.setObjectName(u"checkBox_ifColumns")
        self.checkBox_ifColumns.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_ifColumns)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_2.addWidget(self.label_6)

        self.lineEdit_datasetName = QLineEdit(Form)
        self.lineEdit_datasetName.setObjectName(u"lineEdit_datasetName")
        self.lineEdit_datasetName.setMinimumSize(QSize(150, 25))
        self.lineEdit_datasetName.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.lineEdit_datasetName)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_passHead = QLineEdit(Form)
        self.lineEdit_passHead.setObjectName(u"lineEdit_passHead")
        self.lineEdit_passHead.setMinimumSize(QSize(150, 25))
        self.lineEdit_passHead.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_passHead)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_limitRow = QLineEdit(Form)
        self.lineEdit_limitRow.setObjectName(u"lineEdit_limitRow")
        self.lineEdit_limitRow.setMinimumSize(QSize(150, 25))
        self.lineEdit_limitRow.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_4.addWidget(self.lineEdit_limitRow)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_9.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.comboBox_encode = QComboBox(Form)
        self.comboBox_encode.addItem("")
        self.comboBox_encode.addItem("")
        self.comboBox_encode.addItem("")
        self.comboBox_encode.addItem("")
        self.comboBox_encode.setObjectName(u"comboBox_encode")
        self.comboBox_encode.setMinimumSize(QSize(150, 25))
        self.comboBox_encode.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.comboBox_encode)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_6.addWidget(self.label_2)

        self.comboBox_separator = QComboBox(Form)
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.addItem("")
        self.comboBox_separator.setObjectName(u"comboBox_separator")
        self.comboBox_separator.setMinimumSize(QSize(150, 25))
        self.comboBox_separator.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_6.addWidget(self.comboBox_separator)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_7.addWidget(self.label_7)

        self.lineEdit_missValue = QLineEdit(Form)
        self.lineEdit_missValue.setObjectName(u"lineEdit_missValue")
        self.lineEdit_missValue.setMinimumSize(QSize(150, 25))
        self.lineEdit_missValue.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEdit_missValue)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_9.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(50, 0))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_10 = QHBoxLayout(self.widget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_help = QPushButton(self.widget)
        self.pushButton_help.setObjectName(u"pushButton_help")
        self.pushButton_help.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_8.addWidget(self.pushButton_help)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.pushButton_preview = QPushButton(self.widget)
        self.pushButton_preview.setObjectName(u"pushButton_preview")
        self.pushButton_preview.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_8.addWidget(self.pushButton_preview)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_8.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_8.addWidget(self.pushButton_cancel)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5bfc\u5165CSV\u6570\u636e", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6570\u636e\u96c6\uff1a", None))
        self.pushButton_choosefile.setText(QCoreApplication.translate("Form", u"\u6d4f\u89c8", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u9884\u89c8", None))
        self.checkBox_ifColumns.setText(QCoreApplication.translate("Form", u"\u9996\u884c\u5217\u540d", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6\u540d\uff1a", None))
        self.lineEdit_datasetName.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"\u524d\u7aef\u8df3\u8fc7\uff1a", None))
        self.lineEdit_passHead.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u9650\u5b9a\u884c\u6570\uff1a", None))
        self.lineEdit_limitRow.setText(QCoreApplication.translate("Form", u"\u5168\u90e8", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u7f16\u7801\uff1a", None))
        self.comboBox_encode.setItemText(0, QCoreApplication.translate("Form", u"utf8", None))
        self.comboBox_encode.setItemText(1, QCoreApplication.translate("Form", u"gb2312", None))
        self.comboBox_encode.setItemText(2, QCoreApplication.translate("Form", u"gbk", None))
        self.comboBox_encode.setItemText(3, QCoreApplication.translate("Form", u"ascii", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"\u5206 \u9694 \u7b26\uff1a", None))
        self.comboBox_separator.setItemText(0, QCoreApplication.translate("Form", u",", None))
        self.comboBox_separator.setItemText(1, QCoreApplication.translate("Form", u";", None))
        self.comboBox_separator.setItemText(2, QCoreApplication.translate("Form", u"\\s", None))
        self.comboBox_separator.setItemText(3, QCoreApplication.translate("Form", u"\\t", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"\u7f3a \u5931 \u503c\uff1a", None))
        self.lineEdit_missValue.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_preview.setText(QCoreApplication.translate("Form", u"\u9884\u89c8", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

