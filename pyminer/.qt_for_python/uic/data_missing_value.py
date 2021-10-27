# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_missing_value.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout_7 = QVBoxLayout(Form)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
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
        self.widget_2.setMaximumSize(QSize(200, 16777215))
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


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pushButton_add = QPushButton(self.tab)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_add.setIcon(icon)

        self.verticalLayout_9.addWidget(self.pushButton_add)

        self.pushButton_delete = QPushButton(self.tab)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_delete.setIcon(icon1)

        self.verticalLayout_9.addWidget(self.pushButton_delete)


        self.horizontalLayout_2.addLayout(self.verticalLayout_9)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.listWidget_selected = QListWidget(self.tab)
        self.listWidget_selected.setObjectName(u"listWidget_selected")

        self.horizontalLayout_7.addWidget(self.listWidget_selected)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_selected_add = QPushButton(self.tab)
        self.pushButton_selected_add.setObjectName(u"pushButton_selected_add")
        self.pushButton_selected_add.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_add.setIcon(icon2)

        self.verticalLayout_10.addWidget(self.pushButton_selected_add)

        self.pushButton_selected_up = QPushButton(self.tab)
        self.pushButton_selected_up.setObjectName(u"pushButton_selected_up")
        self.pushButton_selected_up.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_up.setIcon(icon3)

        self.verticalLayout_10.addWidget(self.pushButton_selected_up)

        self.pushButton_selected_down = QPushButton(self.tab)
        self.pushButton_selected_down.setObjectName(u"pushButton_selected_down")
        self.pushButton_selected_down.setMaximumSize(QSize(50, 16777215))
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_down.setIcon(icon4)

        self.verticalLayout_10.addWidget(self.pushButton_selected_down)

        self.pushButton_selected_del = QPushButton(self.tab)
        self.pushButton_selected_del.setObjectName(u"pushButton_selected_del")
        self.pushButton_selected_del.setMaximumSize(QSize(50, 16777215))
        icon5 = QIcon()
        icon5.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_del.setIcon(icon5)

        self.verticalLayout_10.addWidget(self.pushButton_selected_del)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_2)


        self.horizontalLayout_7.addLayout(self.verticalLayout_10)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.radioButton = QRadioButton(self.tab_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.verticalLayout_6.addWidget(self.radioButton)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_2 = QRadioButton(self.tab_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)

        self.lineEdit_3 = QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_missing_preview = QPushButton(self.tab_2)
        self.pushButton_missing_preview.setObjectName(u"pushButton_missing_preview")

        self.horizontalLayout_8.addWidget(self.pushButton_missing_preview)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.tableWidget_missing = QTableWidget(self.tab_2)
        self.tableWidget_missing.setObjectName(u"tableWidget_missing")

        self.verticalLayout_6.addWidget(self.tableWidget_missing)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_8 = QVBoxLayout(self.tab_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.tableWidget_dataset = QTableWidget(self.tab_4)
        self.tableWidget_dataset.setObjectName(u"tableWidget_dataset")

        self.verticalLayout_8.addWidget(self.tableWidget_dataset)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButton_none = QRadioButton(self.tab_3)
        self.radioButton_none.setObjectName(u"radioButton_none")
        self.radioButton_none.setChecked(True)

        self.verticalLayout_4.addWidget(self.radioButton_none)

        self.radioButton_mean = QRadioButton(self.tab_3)
        self.radioButton_mean.setObjectName(u"radioButton_mean")

        self.verticalLayout_4.addWidget(self.radioButton_mean)

        self.radioButton_median = QRadioButton(self.tab_3)
        self.radioButton_median.setObjectName(u"radioButton_median")

        self.verticalLayout_4.addWidget(self.radioButton_median)

        self.radioButton_mode = QRadioButton(self.tab_3)
        self.radioButton_mode.setObjectName(u"radioButton_mode")

        self.verticalLayout_4.addWidget(self.radioButton_mode)

        self.radioButton_drop_col = QRadioButton(self.tab_3)
        self.radioButton_drop_col.setObjectName(u"radioButton_drop_col")

        self.verticalLayout_4.addWidget(self.radioButton_drop_col)

        self.radioButton_drop = QRadioButton(self.tab_3)
        self.radioButton_drop.setObjectName(u"radioButton_drop")

        self.verticalLayout_4.addWidget(self.radioButton_drop)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_replace = QRadioButton(self.tab_3)
        self.radioButton_replace.setObjectName(u"radioButton_replace")

        self.horizontalLayout_5.addWidget(self.radioButton_replace)

        self.lineEdit_missing_replace = QLineEdit(self.tab_3)
        self.lineEdit_missing_replace.setObjectName(u"lineEdit_missing_replace")

        self.horizontalLayout_5.addWidget(self.lineEdit_missing_replace)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radioButton_drop_ratio = QRadioButton(self.tab_3)
        self.radioButton_drop_ratio.setObjectName(u"radioButton_drop_ratio")

        self.horizontalLayout_6.addWidget(self.radioButton_drop_ratio)

        self.doubleSpinBox_missing_ratio = QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_missing_ratio.setObjectName(u"doubleSpinBox_missing_ratio")
        self.doubleSpinBox_missing_ratio.setMaximum(1.000000000000000)
        self.doubleSpinBox_missing_ratio.setValue(0.500000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_missing_ratio)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushbutton_refresh = QPushButton(self.tab_3)
        self.pushbutton_refresh.setObjectName(u"pushbutton_refresh")

        self.horizontalLayout_9.addWidget(self.pushbutton_refresh)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.tableWidget_replace = QTableWidget(self.tab_3)
        self.tableWidget_replace.setObjectName(u"tableWidget_replace")

        self.verticalLayout_4.addWidget(self.tableWidget_replace)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_7.addWidget(self.tabWidget)

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

        self.combo_var_name = QComboBox(self.widget_3)
        self.combo_var_name.setObjectName(u"combo_var_name")

        self.horizontalLayout_3.addWidget(self.combo_var_name)

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


        self.verticalLayout_7.addWidget(self.widget_3)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e-\u7f3a\u5931\u503c\u5904\u7406", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_add.setText("")
        self.pushButton_delete.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.pushButton_selected_add.setText("")
        self.pushButton_selected_up.setText("")
        self.pushButton_selected_down.setText("")
        self.pushButton_selected_del.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u53d8\u91cf", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"\u81ea\u5b9a\u4e49", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Form", u"-99999", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u591a\u4e2a\u503c\u7528\u5206\u53f7\u9694\u5f00", None))
        self.pushButton_missing_preview.setText(QCoreApplication.translate("Form", u"\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u7f3a\u5931\u503c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Form", u"\u63cf\u8ff0\u7edf\u8ba1", None))
        self.radioButton_none.setText(QCoreApplication.translate("Form", u"\u65e0", None))
        self.radioButton_mean.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528\u5217\u5747\u503c\u66ff\u6362", None))
        self.radioButton_median.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528\u5217\u4e2d\u4f4d\u6570\u66ff\u6362", None))
        self.radioButton_mode.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528\u5217\u4f17\u6570\u66ff\u6362", None))
        self.radioButton_drop_col.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u5168\u90e8\u4e3a\u7f3a\u5931\u503c\u7684\u5217", None))
        self.radioButton_drop.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u6709\u7f3a\u5931\u503c\u7684\u884c", None))
        self.radioButton_replace.setText(QCoreApplication.translate("Form", u"\u66ff\u6362\u4e3a", None))
        self.lineEdit_missing_replace.setText(QCoreApplication.translate("Form", u"-99999", None))
        self.radioButton_drop_ratio.setText(QCoreApplication.translate("Form", u"\u7f3a\u5931\u503c\u5927\u4e8e\u6307\u5b9a\u767e\u5206\u6bd4\u65f6\u5220\u9664\u5bf9\u5e94\u8bb0\u5f55", None))
        self.pushbutton_refresh.setText(QCoreApplication.translate("Form", u"\u5237\u65b0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

