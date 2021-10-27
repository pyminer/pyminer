# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_info.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_path = QLineEdit(Form)
        self.lineEdit_path.setObjectName(u"lineEdit_path")
        self.lineEdit_path.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_path)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_row = QLineEdit(Form)
        self.lineEdit_row.setObjectName(u"lineEdit_row")
        self.lineEdit_row.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_row)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_col = QLineEdit(Form)
        self.lineEdit_col.setObjectName(u"lineEdit_col")
        self.lineEdit_col.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_col)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.lineEdit_file_size = QLineEdit(Form)
        self.lineEdit_file_size.setObjectName(u"lineEdit_file_size")
        self.lineEdit_file_size.setReadOnly(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEdit_file_size)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_9)

        self.lineEdit_memory_usage = QLineEdit(Form)
        self.lineEdit_memory_usage.setObjectName(u"lineEdit_memory_usage")
        self.lineEdit_memory_usage.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lineEdit_memory_usage)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.lineEdit_create_time = QLineEdit(Form)
        self.lineEdit_create_time.setObjectName(u"lineEdit_create_time")
        self.lineEdit_create_time.setReadOnly(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lineEdit_create_time)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_update_time = QLineEdit(Form)
        self.lineEdit_update_time.setObjectName(u"lineEdit_update_time")
        self.lineEdit_update_time.setReadOnly(True)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.lineEdit_update_time)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_dataset_name = QLineEdit(Form)
        self.lineEdit_dataset_name.setObjectName(u"lineEdit_dataset_name")
        self.lineEdit_dataset_name.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_dataset_name)

        self.toolButton_dataset_name = QToolButton(Form)
        self.toolButton_dataset_name.setObjectName(u"toolButton_dataset_name")

        self.horizontalLayout.addWidget(self.toolButton_dataset_name)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout)

        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_help = QPushButton(self.widget)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout_2.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_2.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_2.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u57fa\u672c\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6\u540d\u79f0:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u8def\u5f84\uff1a", None))
        self.lineEdit_path.setText(QCoreApplication.translate("Form", u"c:/demo.csv", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u884c\uff1a", None))
        self.lineEdit_row.setText(QCoreApplication.translate("Form", u"30000", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5217\uff1a", None))
        self.lineEdit_col.setText(QCoreApplication.translate("Form", u"20", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u5927\u5c0f\uff1a", None))
        self.lineEdit_file_size.setText(QCoreApplication.translate("Form", u"1024 kb", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u5185\u5b58\u5360\u7528\uff1a", None))
        self.lineEdit_memory_usage.setText(QCoreApplication.translate("Form", u"1024 kb", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u65f6\u95f4\uff1a", None))
        self.lineEdit_create_time.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0\u65f6\u95f4\uff1a", None))
        self.lineEdit_update_time.setText("")
        self.lineEdit_dataset_name.setText(QCoreApplication.translate("Form", u"demo.csv", None))
        self.toolButton_dataset_name.setText(QCoreApplication.translate("Form", u"...", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

