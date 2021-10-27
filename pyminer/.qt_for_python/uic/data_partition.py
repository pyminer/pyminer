# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_partition.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QToolBox, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(0, 0))
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setContentsMargins(9, 0, 0, 0)
        self.label_username = QLabel(self.widget)
        self.label_username.setObjectName(u"label_username")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_username)

        self.lineEdit_dataset_name = QLineEdit(self.widget)
        self.lineEdit_dataset_name.setObjectName(u"lineEdit_dataset_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_dataset_name)

        self.label_username_3 = QLabel(self.widget)
        self.label_username_3.setObjectName(u"label_username_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_username_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox_type = QComboBox(self.widget)
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.setObjectName(u"comboBox_type")

        self.horizontalLayout_5.addWidget(self.comboBox_type)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_username_4 = QLabel(self.widget)
        self.label_username_4.setObjectName(u"label_username_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_username_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_partition_label = QLineEdit(self.widget)
        self.lineEdit_partition_label.setObjectName(u"lineEdit_partition_label")

        self.horizontalLayout_2.addWidget(self.lineEdit_partition_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_username_5 = QLabel(self.widget)
        self.label_username_5.setObjectName(u"label_username_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_username_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spinBox_random_state = QSpinBox(self.widget)
        self.spinBox_random_state.setObjectName(u"spinBox_random_state")
        self.spinBox_random_state.setMaximum(999999999)
        self.spinBox_random_state.setValue(12345)

        self.horizontalLayout_3.addWidget(self.spinBox_random_state)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_partition_label = QLabel(self.widget)
        self.label_partition_label.setObjectName(u"label_partition_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_partition_label)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.spinBox_partition_count = QSpinBox(self.widget)
        self.spinBox_partition_count.setObjectName(u"spinBox_partition_count")
        self.spinBox_partition_count.setMinimum(1)
        self.spinBox_partition_count.setMaximum(4)

        self.horizontalLayout_6.addWidget(self.spinBox_partition_count)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.label_describe = QLabel(self.widget)
        self.label_describe.setObjectName(u"label_describe")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_describe)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 100))
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolBox_2 = QToolBox(self.widget_2)
        self.toolBox_2.setObjectName(u"toolBox_2")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 659, 362))
        self.verticalLayout_13 = QVBoxLayout(self.page_3)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.widget_6 = QWidget(self.page_3)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMinimumSize(QSize(100, 150))
        self.verticalLayout_14 = QVBoxLayout(self.widget_6)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(9, 9, 9, 9)
        self.widget_part_13 = QWidget(self.widget_6)
        self.widget_part_13.setObjectName(u"widget_part_13")
        self.horizontalLayout_19 = QHBoxLayout(self.widget_part_13)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.label_24 = QLabel(self.widget_part_13)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_19.addWidget(self.label_24)

        self.doubleSpinBox_part_13 = QDoubleSpinBox(self.widget_part_13)
        self.doubleSpinBox_part_13.setObjectName(u"doubleSpinBox_part_13")
        self.doubleSpinBox_part_13.setMinimum(0.010000000000000)
        self.doubleSpinBox_part_13.setMaximum(1.000000000000000)
        self.doubleSpinBox_part_13.setValue(0.700000000000000)

        self.horizontalLayout_19.addWidget(self.doubleSpinBox_part_13)

        self.horizontalSpacer_31 = QSpacerItem(411, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_31)


        self.verticalLayout_14.addWidget(self.widget_part_13)

        self.widget_part_14 = QWidget(self.widget_6)
        self.widget_part_14.setObjectName(u"widget_part_14")
        self.horizontalLayout_20 = QHBoxLayout(self.widget_part_14)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.widget_part_14)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_20.addWidget(self.label_25)

        self.doubleSpinBox_part_14 = QDoubleSpinBox(self.widget_part_14)
        self.doubleSpinBox_part_14.setObjectName(u"doubleSpinBox_part_14")
        self.doubleSpinBox_part_14.setMinimum(0.000000000000000)
        self.doubleSpinBox_part_14.setMaximum(1.000000000000000)
        self.doubleSpinBox_part_14.setValue(0.700000000000000)

        self.horizontalLayout_20.addWidget(self.doubleSpinBox_part_14)

        self.horizontalSpacer_32 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_32)


        self.verticalLayout_14.addWidget(self.widget_part_14)

        self.widget_part_15 = QWidget(self.widget_6)
        self.widget_part_15.setObjectName(u"widget_part_15")
        self.horizontalLayout_21 = QHBoxLayout(self.widget_part_15)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.widget_part_15)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_21.addWidget(self.label_26)

        self.doubleSpinBox_part_15 = QDoubleSpinBox(self.widget_part_15)
        self.doubleSpinBox_part_15.setObjectName(u"doubleSpinBox_part_15")
        self.doubleSpinBox_part_15.setMinimum(0.000000000000000)
        self.doubleSpinBox_part_15.setMaximum(1.000000000000000)
        self.doubleSpinBox_part_15.setValue(0.700000000000000)

        self.horizontalLayout_21.addWidget(self.doubleSpinBox_part_15)

        self.horizontalSpacer_33 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_33)


        self.verticalLayout_14.addWidget(self.widget_part_15)

        self.widget_part_16 = QWidget(self.widget_6)
        self.widget_part_16.setObjectName(u"widget_part_16")
        self.horizontalLayout_22 = QHBoxLayout(self.widget_part_16)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.widget_part_16)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_22.addWidget(self.label_27)

        self.doubleSpinBox_part_16 = QDoubleSpinBox(self.widget_part_16)
        self.doubleSpinBox_part_16.setObjectName(u"doubleSpinBox_part_16")
        self.doubleSpinBox_part_16.setMinimum(0.000000000000000)
        self.doubleSpinBox_part_16.setMaximum(1.000000000000000)
        self.doubleSpinBox_part_16.setValue(0.700000000000000)

        self.horizontalLayout_22.addWidget(self.doubleSpinBox_part_16)

        self.horizontalSpacer_34 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_34)


        self.verticalLayout_14.addWidget(self.widget_part_16)

        self.widget_part_other_4 = QWidget(self.widget_6)
        self.widget_part_other_4.setObjectName(u"widget_part_other_4")
        self.horizontalLayout_27 = QHBoxLayout(self.widget_part_other_4)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.widget_part_other_4)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_27.addWidget(self.label_35)

        self.doubleSpinBox_26 = QDoubleSpinBox(self.widget_part_other_4)
        self.doubleSpinBox_26.setObjectName(u"doubleSpinBox_26")
        self.doubleSpinBox_26.setMinimum(0.000000000000000)
        self.doubleSpinBox_26.setMaximum(1.000000000000000)
        self.doubleSpinBox_26.setValue(0.010000000000000)

        self.horizontalLayout_27.addWidget(self.doubleSpinBox_26)

        self.horizontalSpacer_41 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_41)


        self.verticalLayout_14.addWidget(self.widget_part_other_4)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_7)


        self.verticalLayout_13.addWidget(self.widget_6)

        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/arrow-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox_2.addItem(self.page_3, icon, u"\u5206\u533a\u6bd4\u4f8b\u8bbe\u7f6e")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 659, 362))
        self.verticalLayout_15 = QVBoxLayout(self.page_4)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.widget_7 = QWidget(self.page_4)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(100, 150))
        self.verticalLayout_16 = QVBoxLayout(self.widget_7)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(9, 9, 9, 9)
        self.widget_label_name_4 = QWidget(self.widget_7)
        self.widget_label_name_4.setObjectName(u"widget_label_name_4")
        self.horizontalLayout_43 = QHBoxLayout(self.widget_label_name_4)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.widget_label_name_4)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_43.addWidget(self.label_36)

        self.lineEdit_partition_name_5 = QLineEdit(self.widget_label_name_4)
        self.lineEdit_partition_name_5.setObjectName(u"lineEdit_partition_name_5")

        self.horizontalLayout_43.addWidget(self.lineEdit_partition_name_5)

        self.horizontalSpacer_57 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_43.addItem(self.horizontalSpacer_57)


        self.verticalLayout_16.addWidget(self.widget_label_name_4)

        self.widget_label_16 = QWidget(self.widget_7)
        self.widget_label_16.setObjectName(u"widget_label_16")
        self.horizontalLayout_44 = QHBoxLayout(self.widget_label_16)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.label_50 = QLabel(self.widget_label_16)
        self.label_50.setObjectName(u"label_50")

        self.horizontalLayout_44.addWidget(self.label_50)

        self.lineEdit_partition_name_21 = QLineEdit(self.widget_label_16)
        self.lineEdit_partition_name_21.setObjectName(u"lineEdit_partition_name_21")

        self.horizontalLayout_44.addWidget(self.lineEdit_partition_name_21)

        self.horizontalSpacer_58 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_44.addItem(self.horizontalSpacer_58)


        self.verticalLayout_16.addWidget(self.widget_label_16)

        self.widget_label_17 = QWidget(self.widget_7)
        self.widget_label_17.setObjectName(u"widget_label_17")
        self.horizontalLayout_45 = QHBoxLayout(self.widget_label_17)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.label_51 = QLabel(self.widget_label_17)
        self.label_51.setObjectName(u"label_51")

        self.horizontalLayout_45.addWidget(self.label_51)

        self.lineEdit_partition_name_22 = QLineEdit(self.widget_label_17)
        self.lineEdit_partition_name_22.setObjectName(u"lineEdit_partition_name_22")

        self.horizontalLayout_45.addWidget(self.lineEdit_partition_name_22)

        self.horizontalSpacer_59 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_59)


        self.verticalLayout_16.addWidget(self.widget_label_17)

        self.widget_label_18 = QWidget(self.widget_7)
        self.widget_label_18.setObjectName(u"widget_label_18")
        self.horizontalLayout_46 = QHBoxLayout(self.widget_label_18)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(0, 0, 0, 0)
        self.label_52 = QLabel(self.widget_label_18)
        self.label_52.setObjectName(u"label_52")

        self.horizontalLayout_46.addWidget(self.label_52)

        self.lineEdit_partition_name_23 = QLineEdit(self.widget_label_18)
        self.lineEdit_partition_name_23.setObjectName(u"lineEdit_partition_name_23")

        self.horizontalLayout_46.addWidget(self.lineEdit_partition_name_23)

        self.horizontalSpacer_60 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_46.addItem(self.horizontalSpacer_60)


        self.verticalLayout_16.addWidget(self.widget_label_18)

        self.widget_label_19 = QWidget(self.widget_7)
        self.widget_label_19.setObjectName(u"widget_label_19")
        self.horizontalLayout_47 = QHBoxLayout(self.widget_label_19)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalLayout_47.setContentsMargins(0, 0, 0, 0)
        self.label_53 = QLabel(self.widget_label_19)
        self.label_53.setObjectName(u"label_53")

        self.horizontalLayout_47.addWidget(self.label_53)

        self.lineEdit_partition_name_24 = QLineEdit(self.widget_label_19)
        self.lineEdit_partition_name_24.setObjectName(u"lineEdit_partition_name_24")

        self.horizontalLayout_47.addWidget(self.lineEdit_partition_name_24)

        self.horizontalSpacer_61 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_47.addItem(self.horizontalSpacer_61)


        self.verticalLayout_16.addWidget(self.widget_label_19)

        self.widget_label_20 = QWidget(self.widget_7)
        self.widget_label_20.setObjectName(u"widget_label_20")
        self.horizontalLayout_48 = QHBoxLayout(self.widget_label_20)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.label_54 = QLabel(self.widget_label_20)
        self.label_54.setObjectName(u"label_54")

        self.horizontalLayout_48.addWidget(self.label_54)

        self.lineEdit_partition_name_25 = QLineEdit(self.widget_label_20)
        self.lineEdit_partition_name_25.setObjectName(u"lineEdit_partition_name_25")

        self.horizontalLayout_48.addWidget(self.lineEdit_partition_name_25)

        self.horizontalSpacer_62 = QSpacerItem(411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_62)


        self.verticalLayout_16.addWidget(self.widget_label_20)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_8)


        self.verticalLayout_15.addWidget(self.widget_7)

        self.toolBox_2.addItem(self.page_4, icon, u"\u5206\u533a\u8f93\u51fa\u8bbe\u7f6e")

        self.verticalLayout.addWidget(self.toolBox_2)


        self.verticalLayout_6.addWidget(self.widget_2)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.verticalLayout_6)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Form)

        self.toolBox_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e--\u6570\u636e\u5206\u533a", None))
        self.label_username.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6:", None))
        self.lineEdit_dataset_name.setText("")
        self.label_username_3.setText(QCoreApplication.translate("Form", u"\u5206\u533a\u7c7b\u578b:", None))
        self.comboBox_type.setItemText(0, QCoreApplication.translate("Form", u"\u65b0\u589e\u4e00\u5217\u6807\u8bb0\u6240\u6709\u5206\u533a", None))
        self.comboBox_type.setItemText(1, QCoreApplication.translate("Form", u"\u6bcf\u4e2a\u5206\u533a\u5355\u72ec\u4e00\u4e2a\u6570\u636e\u96c6", None))

        self.label_username_4.setText(QCoreApplication.translate("Form", u"\u5206\u533a\u5b57\u6bb5\u6807\u8bb0:", None))
        self.lineEdit_partition_label.setText(QCoreApplication.translate("Form", u"partition_", None))
        self.label_username_5.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u79cd\u5b50:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_random_state.setToolTip(QCoreApplication.translate("Form", u"\u8f93\u5165\u4e00\u4e2a\u5927\u4e8e 0 \u4e14\u5c0f\u4e8e\u7b49\u4e8e999999999\u7684\u6574\u6570\u4f5c\u4e3a\u968f\u673a\u79cd\u5b50", None))
#endif // QT_CONFIG(tooltip)
        self.label_partition_label.setText(QCoreApplication.translate("Form", u"\u5206\u533a\u6570:", None))
        self.label_describe.setText(QCoreApplication.translate("Form", u"\u5206\u533a\u8be6\u60c5:", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"\u5206\u533a1\u7684\u89c2\u6d4b\u6240\u5360\u6bd4\u4f8b", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"\u5206\u533a2\u7684\u89c2\u6d4b\u6240\u5360\u6bd4\u4f8b", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"\u5206\u533a3\u7684\u89c2\u6d4b\u6240\u5360\u6bd4\u4f8b", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"\u5206\u533a4\u7684\u89c2\u6d4b\u6240\u5360\u6bd4\u4f8b", None))
        self.label_35.setText(QCoreApplication.translate("Form", u"\u5176\u4ed6\u6570\u636e\u6240\u5360\u6bd4\u4f8b", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3), QCoreApplication.translate("Form", u"\u5206\u533a\u6bd4\u4f8b\u8bbe\u7f6e", None))
        self.label_36.setText(QCoreApplication.translate("Form", u"\u5206\u533a\u503c\u7684\u53d8\u91cf\u540d", None))
        self.lineEdit_partition_name_5.setText(QCoreApplication.translate("Form", u"_partition_", None))
        self.label_50.setText(QCoreApplication.translate("Form", u"\u5206\u533a1\u7684\u6807\u8bc6", None))
        self.lineEdit_partition_name_21.setText(QCoreApplication.translate("Form", u"part_1", None))
        self.label_51.setText(QCoreApplication.translate("Form", u"\u5206\u533a2\u7684\u6807\u8bc6", None))
        self.lineEdit_partition_name_22.setText(QCoreApplication.translate("Form", u"part_2", None))
        self.label_52.setText(QCoreApplication.translate("Form", u"\u5206\u533a3\u7684\u6807\u8bc6", None))
        self.lineEdit_partition_name_23.setText(QCoreApplication.translate("Form", u"part_3", None))
        self.label_53.setText(QCoreApplication.translate("Form", u"\u5206\u533a4\u7684\u6807\u8bc6", None))
        self.lineEdit_partition_name_24.setText(QCoreApplication.translate("Form", u"part_4", None))
        self.label_54.setText(QCoreApplication.translate("Form", u"\u5176\u4ed6\u6570\u636e\u6807\u8bc6", None))
        self.lineEdit_partition_name_25.setText(QCoreApplication.translate("Form", u"other", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), QCoreApplication.translate("Form", u"\u5206\u533a\u8f93\u51fa\u8bbe\u7f6e", None))
    # retranslateUi

