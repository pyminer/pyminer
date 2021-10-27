# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_row_filter.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.radioButton_no_filter = QRadioButton(Form)
        self.radioButton_no_filter.setObjectName(u"radioButton_no_filter")
        self.radioButton_no_filter.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.radioButton_no_filter)

        self.radioButton_simple = QRadioButton(Form)
        self.radioButton_simple.setObjectName(u"radioButton_simple")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.radioButton_simple)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.spinBox_start = QSpinBox(Form)
        self.spinBox_start.setObjectName(u"spinBox_start")
        self.spinBox_start.setMinimum(1)
        self.spinBox_start.setMaximum(999999999)

        self.horizontalLayout_3.addWidget(self.spinBox_start)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.spinBox_end = QSpinBox(Form)
        self.spinBox_end.setObjectName(u"spinBox_end")
        self.spinBox_end.setMaximum(999999999)
        self.spinBox_end.setValue(100)

        self.horizontalLayout_3.addWidget(self.spinBox_end)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.radioButton_random = QRadioButton(Form)
        self.radioButton_random.setObjectName(u"radioButton_random")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.radioButton_random)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_random = QComboBox(Form)
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.setObjectName(u"comboBox_random")

        self.horizontalLayout.addWidget(self.comboBox_random)

        self.spinBox_random = QSpinBox(Form)
        self.spinBox_random.setObjectName(u"spinBox_random")
        self.spinBox_random.setMaximum(100)
        self.spinBox_random.setValue(10)

        self.horizontalLayout.addWidget(self.spinBox_random)

        self.label_random = QLabel(Form)
        self.label_random.setObjectName(u"label_random")

        self.horizontalLayout.addWidget(self.label_random)

        self.comboBox_replace = QComboBox(Form)
        self.comboBox_replace.addItem("")
        self.comboBox_replace.addItem("")
        self.comboBox_replace.setObjectName(u"comboBox_replace")

        self.horizontalLayout.addWidget(self.comboBox_replace)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.spinBox_random_state = QSpinBox(Form)
        self.spinBox_random_state.setObjectName(u"spinBox_random_state")
        self.spinBox_random_state.setMaximum(999999999)
        self.spinBox_random_state.setValue(12345)

        self.horizontalLayout.addWidget(self.spinBox_random_state)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.radioButton_column = QRadioButton(Form)
        self.radioButton_column.setObjectName(u"radioButton_column")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.radioButton_column)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_columns = QComboBox(Form)
        self.comboBox_columns.addItem("")
        self.comboBox_columns.setObjectName(u"comboBox_columns")

        self.horizontalLayout_2.addWidget(self.comboBox_columns)

        self.comboBox_col_condition = QComboBox(Form)
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.addItem("")
        self.comboBox_col_condition.setObjectName(u"comboBox_col_condition")

        self.horizontalLayout_2.addWidget(self.comboBox_col_condition)

        self.lineEdit_col_find = QLineEdit(Form)
        self.lineEdit_col_find.setObjectName(u"lineEdit_col_find")
        self.lineEdit_col_find.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_2.addWidget(self.lineEdit_col_find)

        self.horizontalSpacer_4 = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.radioButton_dtype = QRadioButton(Form)
        self.radioButton_dtype.setObjectName(u"radioButton_dtype")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.radioButton_dtype)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox_dtype = QComboBox(Form)
        self.comboBox_dtype.addItem("")
        self.comboBox_dtype.setObjectName(u"comboBox_dtype")

        self.horizontalLayout_5.addWidget(self.comboBox_dtype)

        self.horizontalSpacer_6 = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.formLayout)

        self.tableWidget_dataset = QTableWidget(Form)
        self.tableWidget_dataset.setObjectName(u"tableWidget_dataset")

        self.verticalLayout.addWidget(self.tableWidget_dataset)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_help = QPushButton(self.widget)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout_6.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_6.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_6.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u7b5b\u9009", None))
        self.radioButton_no_filter.setText(QCoreApplication.translate("Form", u"\u4e0d\u7b5b\u9009", None))
        self.radioButton_simple.setText(QCoreApplication.translate("Form", u"\u7b80\u5355", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4ece", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5230", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u884c", None))
        self.radioButton_random.setText(QCoreApplication.translate("Form", u"\u968f\u673a", None))
        self.comboBox_random.setItemText(0, QCoreApplication.translate("Form", u"\u6309\u6bd4\u4f8b\u968f\u673a\u62bd\u6837", None))
        self.comboBox_random.setItemText(1, QCoreApplication.translate("Form", u"\u6309\u884c\u6570\u968f\u673a\u62bd\u6837", None))

        self.label_random.setText(QCoreApplication.translate("Form", u"%", None))
        self.comboBox_replace.setItemText(0, QCoreApplication.translate("Form", u"\u65e0\u653e\u56de\u62bd\u6837", None))
        self.comboBox_replace.setItemText(1, QCoreApplication.translate("Form", u"\u6709\u653e\u56de\u62bd\u6837", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u79cd\u5b50", None))
        self.radioButton_column.setText(QCoreApplication.translate("Form", u"\u5217", None))
        self.comboBox_columns.setItemText(0, QCoreApplication.translate("Form", u"\u53d8\u91cf\u5217\u8868", None))

        self.comboBox_col_condition.setItemText(0, QCoreApplication.translate("Form", u"\u6a21\u7cca\u5339\u914d", None))
        self.comboBox_col_condition.setItemText(1, QCoreApplication.translate("Form", u"in", None))
        self.comboBox_col_condition.setItemText(2, QCoreApplication.translate("Form", u"not in", None))
        self.comboBox_col_condition.setItemText(3, QCoreApplication.translate("Form", u"=", None))
        self.comboBox_col_condition.setItemText(4, QCoreApplication.translate("Form", u">", None))
        self.comboBox_col_condition.setItemText(5, QCoreApplication.translate("Form", u">=", None))
        self.comboBox_col_condition.setItemText(6, QCoreApplication.translate("Form", u"<", None))
        self.comboBox_col_condition.setItemText(7, QCoreApplication.translate("Form", u"<=", None))

        self.lineEdit_col_find.setText("")
        self.radioButton_dtype.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7c7b\u578b", None))
        self.comboBox_dtype.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8", None))

        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

