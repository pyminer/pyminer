# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_repace.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(767, 511)
        Form.setMaximumSize(QSize(767, 16777215))
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout = QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_3 = QLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_12.addWidget(self.label_3)

        self.lineEdit_find = QLineEdit(self.tab_3)
        self.lineEdit_find.setObjectName(u"lineEdit_find")
        self.lineEdit_find.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_12.addWidget(self.lineEdit_find)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.checkBox_find_case = QCheckBox(self.tab_3)
        self.checkBox_find_case.setObjectName(u"checkBox_find_case")

        self.horizontalLayout_13.addWidget(self.checkBox_find_case)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.comboBox_find_columns = QComboBox(self.tab_3)
        self.comboBox_find_columns.addItem("")
        self.comboBox_find_columns.setObjectName(u"comboBox_find_columns")
        self.comboBox_find_columns.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_11.addWidget(self.comboBox_find_columns)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_10.addWidget(self.label_9)

        self.comboBox_find_search = QComboBox(self.tab_3)
        self.comboBox_find_search.addItem("")
        self.comboBox_find_search.addItem("")
        self.comboBox_find_search.setObjectName(u"comboBox_find_search")
        self.comboBox_find_search.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_10.addWidget(self.comboBox_find_search)

        self.checkBox_find_cell = QCheckBox(self.tab_3)
        self.checkBox_find_cell.setObjectName(u"checkBox_find_cell")

        self.horizontalLayout_10.addWidget(self.checkBox_find_cell)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.lineEdit_replace_find = QLineEdit(self.tab_2)
        self.lineEdit_replace_find.setObjectName(u"lineEdit_replace_find")
        self.lineEdit_replace_find.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_4.addWidget(self.lineEdit_replace_find)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEdit_replace = QLineEdit(self.tab_2)
        self.lineEdit_replace.setObjectName(u"lineEdit_replace")
        self.lineEdit_replace.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.lineEdit_replace)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.checkBox_replace_case = QCheckBox(self.tab_2)
        self.checkBox_replace_case.setObjectName(u"checkBox_replace_case")

        self.horizontalLayout_9.addWidget(self.checkBox_replace_case)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.comboBox_replace_columns = QComboBox(self.tab_2)
        self.comboBox_replace_columns.addItem("")
        self.comboBox_replace_columns.setObjectName(u"comboBox_replace_columns")
        self.comboBox_replace_columns.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_6.addWidget(self.comboBox_replace_columns)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.comboBox_replace_search = QComboBox(self.tab_2)
        self.comboBox_replace_search.addItem("")
        self.comboBox_replace_search.addItem("")
        self.comboBox_replace_search.setObjectName(u"comboBox_replace_search")
        self.comboBox_replace_search.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_7.addWidget(self.comboBox_replace_search)

        self.checkBox_replace_cell = QCheckBox(self.tab_2)
        self.checkBox_replace_cell.setObjectName(u"checkBox_replace_cell")

        self.horizontalLayout_7.addWidget(self.checkBox_replace_cell)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_13.addWidget(self.tabWidget)

        self.tableWidget_dataset = QTableWidget(Form)
        self.tableWidget_dataset.setObjectName(u"tableWidget_dataset")

        self.verticalLayout_13.addWidget(self.tableWidget_dataset)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.combo_var_name = QComboBox(self.widget_3)
        self.combo_var_name.addItem("")
        self.combo_var_name.setObjectName(u"combo_var_name")

        self.horizontalLayout_3.addWidget(self.combo_var_name)

        self.pushButton_code = QPushButton(self.widget_3)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout_3.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_find = QPushButton(self.widget_3)
        self.pushButton_find.setObjectName(u"pushButton_find")

        self.horizontalLayout_3.addWidget(self.pushButton_find)

        self.pushButton_replace = QPushButton(self.widget_3)
        self.pushButton_replace.setObjectName(u"pushButton_replace")

        self.horizontalLayout_3.addWidget(self.pushButton_replace)

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
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u67e5\u627e\u548c\u66ff\u6362", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u67e5\u627e\u5185\u5bb9:", None))
        self.checkBox_find_case.setText(QCoreApplication.translate("Form", u"\u533a\u5206\u5927\u5c0f\u5199", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u8303\u56f4:", None))
        self.comboBox_find_columns.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8\u5217", None))

        self.label_9.setText(QCoreApplication.translate("Form", u"\u641c\u7d22:", None))
        self.comboBox_find_search.setItemText(0, QCoreApplication.translate("Form", u"\u6309\u5217", None))
        self.comboBox_find_search.setItemText(1, QCoreApplication.translate("Form", u"\u6309\u884c", None))

        self.checkBox_find_cell.setText(QCoreApplication.translate("Form", u"\u5355\u5143\u683c\u5339\u914d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\u67e5\u627e", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u67e5\u627e\u5185\u5bb9:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u66ff\u6362\u4e3a:  ", None))
        self.checkBox_replace_case.setText(QCoreApplication.translate("Form", u"\u533a\u5206\u5927\u5c0f\u5199", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u8303\u56f4:", None))
        self.comboBox_replace_columns.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8\u5217", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"\u641c\u7d22:", None))
        self.comboBox_replace_search.setItemText(0, QCoreApplication.translate("Form", u"\u6309\u5217", None))
        self.comboBox_replace_search.setItemText(1, QCoreApplication.translate("Form", u"\u6309\u884c", None))

        self.checkBox_replace_cell.setText(QCoreApplication.translate("Form", u"\u5355\u5143\u683c\u5339\u914d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u66ff\u6362", None))
        self.combo_var_name.setItemText(0, QCoreApplication.translate("Form", u"\u9009\u62e9\u53d8\u91cf", None))

        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_find.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u67e5\u627e", None))
        self.pushButton_replace.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u66ff\u6362", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

