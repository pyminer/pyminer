# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_column_name.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(824, 600)
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_8 = QHBoxLayout(self.tab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listWidget_var = QListWidget(self.widget_2)
        self.listWidget_var.setObjectName(u"listWidget_var")

        self.verticalLayout_2.addWidget(self.listWidget_var)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_8.addWidget(self.widget_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_add = QPushButton(self.tab)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_add.setIcon(icon)

        self.verticalLayout_4.addWidget(self.pushButton_add)

        self.pushButton_delete = QPushButton(self.tab)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_delete.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.pushButton_delete)


        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.listWidget_selected = QListWidget(self.tab)
        self.listWidget_selected.setObjectName(u"listWidget_selected")

        self.horizontalLayout_4.addWidget(self.listWidget_selected)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_selected_add = QPushButton(self.tab)
        self.pushButton_selected_add.setObjectName(u"pushButton_selected_add")
        self.pushButton_selected_add.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_add.setIcon(icon2)

        self.verticalLayout_6.addWidget(self.pushButton_selected_add)

        self.pushButton_selected_up = QPushButton(self.tab)
        self.pushButton_selected_up.setObjectName(u"pushButton_selected_up")
        self.pushButton_selected_up.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_up.setIcon(icon3)

        self.verticalLayout_6.addWidget(self.pushButton_selected_up)

        self.pushButton_selected_down = QPushButton(self.tab)
        self.pushButton_selected_down.setObjectName(u"pushButton_selected_down")
        self.pushButton_selected_down.setMaximumSize(QSize(50, 16777215))
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_down.setIcon(icon4)

        self.verticalLayout_6.addWidget(self.pushButton_selected_down)

        self.pushButton_selected_del = QPushButton(self.tab)
        self.pushButton_selected_del.setObjectName(u"pushButton_selected_del")
        self.pushButton_selected_del.setMaximumSize(QSize(50, 16777215))
        icon5 = QIcon()
        icon5.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_del.setIcon(icon5)

        self.verticalLayout_6.addWidget(self.pushButton_selected_del)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_8.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.comboBox_columns = QComboBox(self.tab_2)
        self.comboBox_columns.addItem("")
        self.comboBox_columns.setObjectName(u"comboBox_columns")
        self.comboBox_columns.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_9.addWidget(self.comboBox_columns)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_9.addWidget(self.label)

        self.lineEdit_replace = QLineEdit(self.tab_2)
        self.lineEdit_replace.setObjectName(u"lineEdit_replace")
        self.lineEdit_replace.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_9.addWidget(self.lineEdit_replace)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lineEdit_prefix_add = QLineEdit(self.tab_2)
        self.lineEdit_prefix_add.setObjectName(u"lineEdit_prefix_add")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_prefix_add)

        self.checkBox_prefix_del = QCheckBox(self.tab_2)
        self.checkBox_prefix_del.setObjectName(u"checkBox_prefix_del")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.checkBox_prefix_del)

        self.lineEdit_prefix_del = QLineEdit(self.tab_2)
        self.lineEdit_prefix_del.setObjectName(u"lineEdit_prefix_del")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_prefix_del)

        self.checkBox_suffix_add = QCheckBox(self.tab_2)
        self.checkBox_suffix_add.setObjectName(u"checkBox_suffix_add")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.checkBox_suffix_add)

        self.lineEdit_suffix_add = QLineEdit(self.tab_2)
        self.lineEdit_suffix_add.setObjectName(u"lineEdit_suffix_add")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_suffix_add)

        self.checkBox_suffix_del = QCheckBox(self.tab_2)
        self.checkBox_suffix_del.setObjectName(u"checkBox_suffix_del")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.checkBox_suffix_del)

        self.lineEdit_suffix_del = QLineEdit(self.tab_2)
        self.lineEdit_suffix_del.setObjectName(u"lineEdit_suffix_del")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_suffix_del)

        self.checkBox_prefix_add = QCheckBox(self.tab_2)
        self.checkBox_prefix_add.setObjectName(u"checkBox_prefix_add")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.checkBox_prefix_add)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_preview = QPushButton(self.tab_2)
        self.pushButton_preview.setObjectName(u"pushButton_preview")

        self.horizontalLayout_2.addWidget(self.pushButton_preview)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget_dataset = QTableWidget(self.tab_2)
        self.tableWidget_dataset.setObjectName(u"tableWidget_dataset")

        self.verticalLayout.addWidget(self.tableWidget_dataset)

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
        self.pushButton_code = QPushButton(self.widget_3)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout_3.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon6 = QIcon()
        icon6.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon6)

        self.horizontalLayout_3.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget_3)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_3.addWidget(self.pushButton_ok)

        self.pushButton_save = QPushButton(self.widget_3)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_3.addWidget(self.pushButton_save)

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
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u5217\u540d\u5904\u7406", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_add.setText("")
        self.pushButton_delete.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.pushButton_selected_add.setText("")
        self.pushButton_selected_up.setText("")
        self.pushButton_selected_down.setText("")
        self.pushButton_selected_del.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u53d8\u91cf", None))
        self.comboBox_columns.setItemText(0, QCoreApplication.translate("Form", u"\u53d8\u91cf\u5217\u8868", None))

        self.label.setText(QCoreApplication.translate("Form", u"\u4fee\u6539\u4e3a", None))
        self.checkBox_prefix_del.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u524d\u7f00", None))
        self.checkBox_suffix_add.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u540e\u7f00", None))
        self.checkBox_suffix_del.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u540e\u7f00", None))
        self.checkBox_prefix_add.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u524d\u7f00", None))
        self.pushButton_preview.setText(QCoreApplication.translate("Form", u"\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u5217\u540d\u5904\u7406", None))
        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

