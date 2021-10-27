# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_sample.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_10 = QVBoxLayout(self.tab)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.listWidget_var = QListWidget(self.widget_2)
        self.listWidget_var.setObjectName(u"listWidget_var")

        self.verticalLayout_3.addWidget(self.listWidget_var)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_5.addWidget(self.widget_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_selected_add_2 = QPushButton(self.tab)
        self.pushButton_selected_add_2.setObjectName(u"pushButton_selected_add_2")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/arrow_right_hover.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_add_2.setIcon(icon)

        self.verticalLayout_4.addWidget(self.pushButton_selected_add_2)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.pushButton_weight_add_2 = QPushButton(self.tab)
        self.pushButton_weight_add_2.setObjectName(u"pushButton_weight_add_2")
        self.pushButton_weight_add_2.setIcon(icon)

        self.verticalLayout_16.addWidget(self.pushButton_weight_add_2)


        self.verticalLayout.addLayout(self.verticalLayout_16)


        self.horizontalLayout_5.addLayout(self.verticalLayout)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_8.addWidget(self.label_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.listWidget_selected = QListWidget(self.tab)
        self.listWidget_selected.setObjectName(u"listWidget_selected")

        self.horizontalLayout_6.addWidget(self.listWidget_selected)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_selected_add = QPushButton(self.tab)
        self.pushButton_selected_add.setObjectName(u"pushButton_selected_add")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_add.setIcon(icon1)

        self.verticalLayout_6.addWidget(self.pushButton_selected_add)

        self.pushButton_selected_up = QPushButton(self.tab)
        self.pushButton_selected_up.setObjectName(u"pushButton_selected_up")
        self.pushButton_selected_up.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_up.setIcon(icon2)

        self.verticalLayout_6.addWidget(self.pushButton_selected_up)

        self.pushButton_selected_down = QPushButton(self.tab)
        self.pushButton_selected_down.setObjectName(u"pushButton_selected_down")
        self.pushButton_selected_down.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_down.setIcon(icon3)

        self.verticalLayout_6.addWidget(self.pushButton_selected_down)

        self.pushButton_selected_del = QPushButton(self.tab)
        self.pushButton_selected_del.setObjectName(u"pushButton_selected_del")
        self.pushButton_selected_del.setMaximumSize(QSize(50, 16777215))
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_selected_del.setIcon(icon4)

        self.verticalLayout_6.addWidget(self.pushButton_selected_del)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_5.addWidget(self.label_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.listWidget_weight = QListWidget(self.tab)
        self.listWidget_weight.setObjectName(u"listWidget_weight")

        self.horizontalLayout_7.addWidget(self.listWidget_weight)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_weight_add = QPushButton(self.tab)
        self.pushButton_weight_add.setObjectName(u"pushButton_weight_add")
        self.pushButton_weight_add.setIcon(icon1)

        self.verticalLayout_7.addWidget(self.pushButton_weight_add)

        self.pushButton_weight_up = QPushButton(self.tab)
        self.pushButton_weight_up.setObjectName(u"pushButton_weight_up")
        self.pushButton_weight_up.setMaximumSize(QSize(50, 16777215))
        self.pushButton_weight_up.setIcon(icon2)

        self.verticalLayout_7.addWidget(self.pushButton_weight_up)

        self.pushButton_weight_down = QPushButton(self.tab)
        self.pushButton_weight_down.setObjectName(u"pushButton_weight_down")
        self.pushButton_weight_down.setMaximumSize(QSize(50, 16777215))
        self.pushButton_weight_down.setIcon(icon3)

        self.verticalLayout_7.addWidget(self.pushButton_weight_down)

        self.pushButton_weight_del = QPushButton(self.tab)
        self.pushButton_weight_del.setObjectName(u"pushButton_weight_del")
        self.pushButton_weight_del.setMaximumSize(QSize(50, 16777215))
        self.pushButton_weight_del.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.pushButton_weight_del)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.verticalLayout_9.addLayout(self.verticalLayout_5)


        self.horizontalLayout_5.addLayout(self.verticalLayout_9)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_12 = QLabel(self.tab_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_12)

        self.lineEdit_dataset_name = QLineEdit(self.tab_2)
        self.lineEdit_dataset_name.setObjectName(u"lineEdit_dataset_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_dataset_name)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.comboBox_replace = QComboBox(self.tab_2)
        self.comboBox_replace.addItem("")
        self.comboBox_replace.addItem("")
        self.comboBox_replace.setObjectName(u"comboBox_replace")

        self.horizontalLayout_12.addWidget(self.comboBox_replace)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_12)

        self.label_14 = QLabel(self.tab_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.spinBox_random_state = QSpinBox(self.tab_2)
        self.spinBox_random_state.setObjectName(u"spinBox_random_state")
        self.spinBox_random_state.setMaximum(999999999)
        self.spinBox_random_state.setValue(12345)

        self.horizontalLayout_15.addWidget(self.spinBox_random_state)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_13)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_15)

        self.label_15 = QLabel(self.tab_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.radioButton_size = QRadioButton(self.tab_2)
        self.radioButton_size.setObjectName(u"radioButton_size")
        self.radioButton_size.setChecked(True)

        self.horizontalLayout_16.addWidget(self.radioButton_size)

        self.spinBox_size = QSpinBox(self.tab_2)
        self.spinBox_size.setObjectName(u"spinBox_size")
        self.spinBox_size.setMaximum(999999999)
        self.spinBox_size.setValue(100)

        self.horizontalLayout_16.addWidget(self.spinBox_size)

        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_16.addWidget(self.label_5)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_14)


        self.verticalLayout_11.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.radioButton_ratio = QRadioButton(self.tab_2)
        self.radioButton_ratio.setObjectName(u"radioButton_ratio")

        self.horizontalLayout_17.addWidget(self.radioButton_ratio)

        self.doubleSpinBox_ratio = QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_ratio.setObjectName(u"doubleSpinBox_ratio")
        self.doubleSpinBox_ratio.setMinimumSize(QSize(104, 0))
        self.doubleSpinBox_ratio.setMaximum(100.000000000000000)

        self.horizontalLayout_17.addWidget(self.doubleSpinBox_ratio)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_17.addWidget(self.label)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_15)


        self.verticalLayout_11.addLayout(self.horizontalLayout_17)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.verticalLayout_11)

        self.label_16 = QLabel(self.tab_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_16)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.comboBox_axis = QComboBox(self.tab_2)
        self.comboBox_axis.addItem("")
        self.comboBox_axis.addItem("")
        self.comboBox_axis.setObjectName(u"comboBox_axis")

        self.horizontalLayout_13.addWidget(self.comboBox_axis)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_13)


        self.horizontalLayout_3.addLayout(self.formLayout)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_code = QPushButton(self.widget)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon5 = QIcon()
        icon5.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon5)

        self.horizontalLayout.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_save = QPushButton(self.widget)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u968f\u673a\u62bd\u6837", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.pushButton_selected_add_2.setText("")
        self.pushButton_weight_add_2.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.pushButton_selected_add.setText("")
        self.pushButton_selected_up.setText("")
        self.pushButton_selected_down.setText("")
        self.pushButton_selected_del.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6743\u91cd\u53d8\u91cf:", None))
        self.pushButton_weight_add.setText("")
        self.pushButton_weight_up.setText("")
        self.pushButton_weight_down.setText("")
        self.pushButton_weight_del.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u53d8\u91cf", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6\uff1a", None))
        self.lineEdit_dataset_name.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"\u62bd\u6837\u65b9\u6cd5:", None))
        self.comboBox_replace.setItemText(0, QCoreApplication.translate("Form", u"\u65e0\u653e\u56de\u62bd\u6837", None))
        self.comboBox_replace.setItemText(1, QCoreApplication.translate("Form", u"\u6709\u653e\u56de\u62bd\u6837", None))

        self.label_14.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u79cd\u5b50:", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u6837\u672c\u65b9\u6cd5:", None))
        self.radioButton_size.setText(QCoreApplication.translate("Form", u"\u6837\u672c\u5927\u5c0f", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u884c", None))
        self.radioButton_ratio.setText(QCoreApplication.translate("Form", u"\u6837\u672c\u6bd4\u4f8b", None))
        self.label.setText(QCoreApplication.translate("Form", u"%", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"\u62bd\u53d6\u884c/\u5217:", None))
        self.comboBox_axis.setItemText(0, QCoreApplication.translate("Form", u"\u884c", None))
        self.comboBox_axis.setItemText(1, QCoreApplication.translate("Form", u"\u5217", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u62bd\u6837", None))
        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

