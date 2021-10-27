# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_option.ui'
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
        Form.resize(705, 515)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listWidget = QListWidget(self.splitter)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(200, 16777215))
        self.splitter.addWidget(self.listWidget)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_general = QWidget()
        self.page_general.setObjectName(u"page_general")
        self.horizontalLayout_3 = QHBoxLayout(self.page_general)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.page_general)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabBase = QWidget()
        self.tabBase.setObjectName(u"tabBase")
        self.verticalLayout_8 = QVBoxLayout(self.tabBase)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_theme = QLabel(self.tabBase)
        self.label_theme.setObjectName(u"label_theme")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_theme)

        self.comboBox_theme = QComboBox(self.tabBase)
        self.comboBox_theme.addItem("")
        self.comboBox_theme.addItem("")
        self.comboBox_theme.addItem("")
        self.comboBox_theme.addItem("")
        self.comboBox_theme.setObjectName(u"comboBox_theme")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBox_theme)

        self.label = QLabel(self.tabBase)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.lineEdit_worksapce = QLineEdit(self.tabBase)
        self.lineEdit_worksapce.setObjectName(u"lineEdit_worksapce")

        self.horizontalLayout_14.addWidget(self.lineEdit_worksapce)

        self.toolButton_workspace = QToolButton(self.tabBase)
        self.toolButton_workspace.setObjectName(u"toolButton_workspace")

        self.horizontalLayout_14.addWidget(self.toolButton_workspace)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_14)

        self.label_15 = QLabel(self.tabBase)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_15)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.lineEdit_output = QLineEdit(self.tabBase)
        self.lineEdit_output.setObjectName(u"lineEdit_output")

        self.horizontalLayout_15.addWidget(self.lineEdit_output)

        self.toolButton_output = QToolButton(self.tabBase)
        self.toolButton_output.setObjectName(u"toolButton_output")

        self.horizontalLayout_15.addWidget(self.toolButton_output)


        self.formLayout_2.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_15)

        self.label_16 = QLabel(self.tabBase)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_16)

        self.comboBox_9 = QComboBox(self.tabBase)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.comboBox_9)

        self.label_11 = QLabel(self.tabBase)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_11)

        self.comboBox_8 = QComboBox(self.tabBase)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.comboBox_8)

        self.check_box_check_upd_on_startup = QCheckBox(self.tabBase)
        self.check_box_check_upd_on_startup.setObjectName(u"check_box_check_upd_on_startup")
        self.check_box_check_upd_on_startup.setChecked(True)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.check_box_check_upd_on_startup)

        self.checkbox_show_startpage = QCheckBox(self.tabBase)
        self.checkbox_show_startpage.setObjectName(u"checkbox_show_startpage")
        self.checkbox_show_startpage.setChecked(True)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.checkbox_show_startpage)


        self.verticalLayout_8.addLayout(self.formLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tabBase, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        self.stackedWidget.addWidget(self.page_general)
        self.page_appearance = QWidget()
        self.page_appearance.setObjectName(u"page_appearance")
        self.verticalLayout_6 = QVBoxLayout(self.page_appearance)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBox_3 = QCheckBox(self.page_appearance)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox_3)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.page_appearance)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.pushButton = QPushButton(self.page_appearance)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_11.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.page_appearance)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.page_appearance)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEdit_2)

        self.horizontalSpacer_3 = QSpacerItem(120, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.page_appearance)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.comboBox = QComboBox(self.page_appearance)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.textEdit = QTextEdit(self.page_appearance)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.textEdit)

        self.stackedWidget.addWidget(self.page_appearance)
        self.page_format = QWidget()
        self.page_format.setObjectName(u"page_format")
        self.verticalLayout_3 = QVBoxLayout(self.page_format)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.page_format)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.comboBox_2 = QComboBox(self.page_format)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_2)

        self.comboBox_3 = QComboBox(self.page_format)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_3)

        self.label_5 = QLabel(self.page_format)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.comboBox_4 = QComboBox(self.page_format)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_4)

        self.label_6 = QLabel(self.page_format)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.comboBox_5 = QComboBox(self.page_format)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBox_5)

        self.label_7 = QLabel(self.page_format)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.comboBox_6 = QComboBox(self.page_format)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboBox_6)

        self.label_8 = QLabel(self.page_format)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_8)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.stackedWidget.addWidget(self.page_format)
        self.splitter.addWidget(self.stackedWidget)

        self.verticalLayout_2.addWidget(self.splitter)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_7 = QHBoxLayout(self.widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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


        self.horizontalLayout_7.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Settings", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"\u5e38\u89c4", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"\u5916\u89c2", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Form", u"\u683c\u5f0f\u5316", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.label_theme.setText(QCoreApplication.translate("Form", u"UI Theme", None))
        self.comboBox_theme.setItemText(0, QCoreApplication.translate("Form", u"Fusion", None))
        self.comboBox_theme.setItemText(1, QCoreApplication.translate("Form", u"Qdarkstyle", None))
        self.comboBox_theme.setItemText(2, QCoreApplication.translate("Form", u"windowsvista", None))
        self.comboBox_theme.setItemText(3, QCoreApplication.translate("Form", u"Windows", None))

        self.label.setText(QCoreApplication.translate("Form", u"Work Directory", None))
        self.toolButton_workspace.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Output Directory", None))
        self.toolButton_output.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"UI Language", None))
        self.comboBox_9.setItemText(0, QCoreApplication.translate("Form", u"\u7b80\u4f53\u4e2d\u6587", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("Form", u"English", None))

        self.label_11.setText(QCoreApplication.translate("Form", u"Encoding", None))
        self.comboBox_8.setItemText(0, QCoreApplication.translate("Form", u"utf-8", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("Form", u"gb2312", None))

        self.check_box_check_upd_on_startup.setText(QCoreApplication.translate("Form", u"Check upd on startup", None))
        self.checkbox_show_startpage.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u8d77\u59cb\u9875\u9762", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBase), QCoreApplication.translate("Form", u"Basic", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"Interlaced coloring", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Table Header Background:", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Color", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Size:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"15", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Font:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Source Code Pro", None))

        self.textEdit.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Patata is a full-featured IDE</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">with a high level of usability and outstanding</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">advanced code editing and refactoring support.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-t"
                        "op:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">abcdefghijklmnopqrstuvwxyz 0123456789 (){}[]</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ABCDEFGHIJKLMNOPQRSTUVWXYZ +-*/= .,;:!? #&amp;$%@|^</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u65e5\u671f\u683c\u5f0f:", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"2020-01-01", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"2020/01/01", None))
        self.comboBox_2.setItemText(2, "")

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"15:30:01(24-\u5c0f\u65f6\u5236)", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"3:30:01 PM(12-\u5c0f\u65f6\u5236)", None))
        self.comboBox_3.setItemText(2, "")

        self.label_5.setText(QCoreApplication.translate("Form", u"\u65f6\u95f4\u683c\u5f0f:", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("Form", u"\u7f8e\u5143US Dollar", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Form", u"\u4eba\u6c11\u5e01Chinese Yuan", None))
        self.comboBox_4.setItemText(2, "")

        self.label_6.setText(QCoreApplication.translate("Form", u"\u8d27\u5e01\u5355\u4f4d:", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("Form", u"\uffe5", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("Form", u"CNY", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("Form", u"$", None))
        self.comboBox_5.setItemText(3, QCoreApplication.translate("Form", u"USD", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"\u8d27\u5e01\u7b26\u53f7:", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Form", u"\u5217\u6807\u9898\u5185", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Form", u"\u5355\u5143\u683c\u5185", None))

        self.label_8.setText(QCoreApplication.translate("Form", u"\u8d27\u5e01\u7b26\u53f7\u4f4d\u4e8e:", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"Help", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"OK", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

