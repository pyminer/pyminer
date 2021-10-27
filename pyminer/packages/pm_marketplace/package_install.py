# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_install.ui'
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
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboBox_source = QComboBox(Form)
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

        self.horizontalLayout_3.addWidget(self.comboBox_source)

        self.lineEdit_source = QLineEdit(Form)
        self.lineEdit_source.setObjectName(u"lineEdit_source")
        self.lineEdit_source.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lineEdit_source.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_source)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_dir = QComboBox(Form)
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.addItem("")
        self.comboBox_dir.setObjectName(u"comboBox_dir")
        self.comboBox_dir.setMinimumSize(QSize(100, 0))
        self.comboBox_dir.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.comboBox_dir)

        self.lineEdit_dir = QLineEdit(Form)
        self.lineEdit_dir.setObjectName(u"lineEdit_dir")
        self.lineEdit_dir.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_dir)

        self.toolButton = QToolButton(Form)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.horizontalLayout_7.addWidget(self.lineEdit_name)

        self.checkBox_version = QCheckBox(Form)
        self.checkBox_version.setObjectName(u"checkBox_version")

        self.horizontalLayout_7.addWidget(self.checkBox_version)

        self.comboBox_version = QComboBox(Form)
        self.comboBox_version.addItem("")
        self.comboBox_version.setObjectName(u"comboBox_version")
        self.comboBox_version.setEnabled(True)
        self.comboBox_version.setMinimumSize(QSize(0, 0))
        self.comboBox_version.setMaximumSize(QSize(16777215, 16777215))
        self.comboBox_version.setEditable(False)

        self.horizontalLayout_7.addWidget(self.comboBox_version)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_7)


        self.horizontalLayout_4.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textEdit_desc = QTextEdit(self.groupBox)
        self.textEdit_desc.setObjectName(u"textEdit_desc")

        self.horizontalLayout_5.addWidget(self.textEdit_desc)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.textEdit_log = QTextEdit(self.groupBox_2)
        self.textEdit_log.setObjectName(u"textEdit_log")

        self.horizontalLayout_6.addWidget(self.textEdit_log)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_2.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_2.addWidget(self.pushButton_cancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5b89\u88c5", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5305\u540d:", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u6e90:", None))
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
        self.lineEdit_name.setText("")
        self.checkBox_version.setText(QCoreApplication.translate("Form", u"\u6307\u5b9a\u7248\u672c", None))
        self.comboBox_version.setItemText(0, QCoreApplication.translate("Form", u"\u6700\u65b0\u7248\u672c", None))

        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u8be6\u60c5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6267\u884c\u8bb0\u5f55", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

