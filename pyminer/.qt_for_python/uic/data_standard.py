# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_standard.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

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
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(10, 100, 161, 16))
        self.checkBox_3.setChecked(False)
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(12, 22, 212, 48))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.checkBox)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.checkBox_2 = QCheckBox(self.layoutWidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.checkBox_2)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)


        self.verticalLayout_6.addWidget(self.groupBox)

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u6807\u51c6\u5316", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_to_right.setText(QCoreApplication.translate("Form", u">", None))
        self.pushButton_to_right_all.setText(QCoreApplication.translate("Form", u">>", None))
        self.pushButton_to_left.setText(QCoreApplication.translate("Form", u"<", None))
        self.pushButton_to_left_all.setText(QCoreApplication.translate("Form", u"<<", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u57fa\u672c", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"\u7528\u5217\u5747\u503c\u66ff\u6362\u7f3a\u5931\u503c", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"\u65b0\u5747\u503c", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"0", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"\u65b0\u6807\u51c6\u5dee", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u6807\u51c6\u5316", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

