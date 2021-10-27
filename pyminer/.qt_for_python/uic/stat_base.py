# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stat_base.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)
import stats_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(749, 557)
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_5 = QHBoxLayout(self.tab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 0)
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listWidget_var = QListWidget(self.widget_2)
        self.listWidget_var.setObjectName(u"listWidget_var")

        self.verticalLayout_2.addWidget(self.listWidget_var)


        self.horizontalLayout_5.addWidget(self.widget_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.vbox_right_up = QVBoxLayout()
        self.vbox_right_up.setObjectName(u"vbox_right_up")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.vbox_right_up.addWidget(self.label)

        self.listWidget_selected = QListWidget(self.tab)
        self.listWidget_selected.setObjectName(u"listWidget_selected")

        self.vbox_right_up.addWidget(self.listWidget_selected)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.vbox_right_up.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.vbox_right_up)

        self.vbox_right_down = QVBoxLayout()
        self.vbox_right_down.setSpacing(0)
        self.vbox_right_down.setObjectName(u"vbox_right_down")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.vbox_right_down.addWidget(self.label_2)

        self.listWidget_group = QListWidget(self.tab)
        self.listWidget_group.setObjectName(u"listWidget_group")

        self.vbox_right_down.addWidget(self.listWidget_group)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.vbox_right_down.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.vbox_right_down)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_12 = QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.radioButton_all = QRadioButton(self.tab_2)
        self.radioButton_all.setObjectName(u"radioButton_all")

        self.verticalLayout_12.addWidget(self.radioButton_all)

        self.radioButton_custom = QRadioButton(self.tab_2)
        self.radioButton_custom.setObjectName(u"radioButton_custom")

        self.verticalLayout_12.addWidget(self.radioButton_custom)

        self.hbox_stat_option = QHBoxLayout()
        self.hbox_stat_option.setObjectName(u"hbox_stat_option")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.checkBox_total_cnt = QCheckBox(self.tab_2)
        self.checkBox_total_cnt.setObjectName(u"checkBox_total_cnt")
        self.checkBox_total_cnt.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_total_cnt)

        self.checkBox_valid_cnt = QCheckBox(self.tab_2)
        self.checkBox_valid_cnt.setObjectName(u"checkBox_valid_cnt")
        self.checkBox_valid_cnt.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_valid_cnt)

        self.checkBox_valid_ratio = QCheckBox(self.tab_2)
        self.checkBox_valid_ratio.setObjectName(u"checkBox_valid_ratio")

        self.verticalLayout_9.addWidget(self.checkBox_valid_ratio)

        self.checkBox_miss_cnt = QCheckBox(self.tab_2)
        self.checkBox_miss_cnt.setObjectName(u"checkBox_miss_cnt")
        self.checkBox_miss_cnt.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_miss_cnt)

        self.checkBox_miss_ratio = QCheckBox(self.tab_2)
        self.checkBox_miss_ratio.setObjectName(u"checkBox_miss_ratio")
        self.checkBox_miss_ratio.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_miss_ratio)

        self.checkBox_unique = QCheckBox(self.tab_2)
        self.checkBox_unique.setObjectName(u"checkBox_unique")

        self.verticalLayout_9.addWidget(self.checkBox_unique)

        self.checkBox_max = QCheckBox(self.tab_2)
        self.checkBox_max.setObjectName(u"checkBox_max")
        self.checkBox_max.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_max)

        self.checkBox_min = QCheckBox(self.tab_2)
        self.checkBox_min.setObjectName(u"checkBox_min")
        self.checkBox_min.setChecked(True)

        self.verticalLayout_9.addWidget(self.checkBox_min)


        self.hbox_stat_option.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.checkBox_sum = QCheckBox(self.tab_2)
        self.checkBox_sum.setObjectName(u"checkBox_sum")

        self.verticalLayout_10.addWidget(self.checkBox_sum)

        self.checkBox_mean = QCheckBox(self.tab_2)
        self.checkBox_mean.setObjectName(u"checkBox_mean")
        self.checkBox_mean.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_mean)

        self.checkBox_mode = QCheckBox(self.tab_2)
        self.checkBox_mode.setObjectName(u"checkBox_mode")

        self.verticalLayout_10.addWidget(self.checkBox_mode)

        self.checkBox_kurt = QCheckBox(self.tab_2)
        self.checkBox_kurt.setObjectName(u"checkBox_kurt")

        self.verticalLayout_10.addWidget(self.checkBox_kurt)

        self.checkBox_skew = QCheckBox(self.tab_2)
        self.checkBox_skew.setObjectName(u"checkBox_skew")

        self.verticalLayout_10.addWidget(self.checkBox_skew)

        self.checkBox_var = QCheckBox(self.tab_2)
        self.checkBox_var.setObjectName(u"checkBox_var")

        self.verticalLayout_10.addWidget(self.checkBox_var)

        self.checkBox_std = QCheckBox(self.tab_2)
        self.checkBox_std.setObjectName(u"checkBox_std")
        self.checkBox_std.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_std)

        self.checkBox_se_mean = QCheckBox(self.tab_2)
        self.checkBox_se_mean.setObjectName(u"checkBox_se_mean")

        self.verticalLayout_10.addWidget(self.checkBox_se_mean)


        self.hbox_stat_option.addLayout(self.verticalLayout_10)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.checkBox_q1 = QCheckBox(self.tab_2)
        self.checkBox_q1.setObjectName(u"checkBox_q1")
        self.checkBox_q1.setChecked(True)

        self.verticalLayout_11.addWidget(self.checkBox_q1)

        self.checkBox_median = QCheckBox(self.tab_2)
        self.checkBox_median.setObjectName(u"checkBox_median")
        self.checkBox_median.setChecked(True)

        self.verticalLayout_11.addWidget(self.checkBox_median)

        self.checkBox_q3 = QCheckBox(self.tab_2)
        self.checkBox_q3.setObjectName(u"checkBox_q3")
        self.checkBox_q3.setChecked(True)

        self.verticalLayout_11.addWidget(self.checkBox_q3)

        self.checkBox_qrange = QCheckBox(self.tab_2)
        self.checkBox_qrange.setObjectName(u"checkBox_qrange")

        self.verticalLayout_11.addWidget(self.checkBox_qrange)

        self.checkBox_range = QCheckBox(self.tab_2)
        self.checkBox_range.setObjectName(u"checkBox_range")

        self.verticalLayout_11.addWidget(self.checkBox_range)

        self.checkBox_cv = QCheckBox(self.tab_2)
        self.checkBox_cv.setObjectName(u"checkBox_cv")

        self.verticalLayout_11.addWidget(self.checkBox_cv)

        self.checkBox_sum_of_squares = QCheckBox(self.tab_2)
        self.checkBox_sum_of_squares.setObjectName(u"checkBox_sum_of_squares")

        self.verticalLayout_11.addWidget(self.checkBox_sum_of_squares)


        self.hbox_stat_option.addLayout(self.verticalLayout_11)


        self.verticalLayout_12.addLayout(self.hbox_stat_option)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.spinBox_precision = QSpinBox(self.tab_2)
        self.spinBox_precision.setObjectName(u"spinBox_precision")
        self.spinBox_precision.setValue(2)

        self.horizontalLayout_3.addWidget(self.spinBox_precision)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_12.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 277, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_15 = QVBoxLayout(self.tab_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.checkBoxhist = QCheckBox(self.tab_3)
        self.checkBoxhist.setObjectName(u"checkBoxhist")

        self.verticalLayout_14.addWidget(self.checkBoxhist)

        self.checkBox_normal = QCheckBox(self.tab_3)
        self.checkBox_normal.setObjectName(u"checkBox_normal")

        self.verticalLayout_14.addWidget(self.checkBox_normal)

        self.checkBox_value = QCheckBox(self.tab_3)
        self.checkBox_value.setObjectName(u"checkBox_value")

        self.verticalLayout_14.addWidget(self.checkBox_value)

        self.checkBox_boxplot = QCheckBox(self.tab_3)
        self.checkBox_boxplot.setObjectName(u"checkBox_boxplot")

        self.verticalLayout_14.addWidget(self.checkBox_boxplot)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_4)


        self.verticalLayout_15.addLayout(self.verticalLayout_14)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_13.addWidget(self.tabWidget)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.widget_3.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_help = QPushButton(self.widget_3)
        self.pushButton_help.setObjectName(u"pushButton_help")

        self.horizontalLayout.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(467, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget_3)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.widget_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout_13.addWidget(self.widget_3)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u663e\u793a\u63cf\u8ff0\u6027\u7edf\u8ba1\u91cf", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u53d8\u91cf:", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u53d8\u91cf:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5206\u7ec4\u53d8\u91cf(\u53ef\u9009)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u57fa\u672c", None))
        self.radioButton_all.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.radioButton_custom.setText(QCoreApplication.translate("Form", u"\u81ea\u5b9a\u4e49", None))
        self.checkBox_total_cnt.setText(QCoreApplication.translate("Form", u"\u8ba1\u6570", None))
        self.checkBox_valid_cnt.setText(QCoreApplication.translate("Form", u"\u975e\u7f3a\u5931\u503c\u8ba1\u6570", None))
        self.checkBox_valid_ratio.setText(QCoreApplication.translate("Form", u"\u975e\u7f3a\u5931\u503c\u5360\u6bd4", None))
        self.checkBox_miss_cnt.setText(QCoreApplication.translate("Form", u"\u7f3a\u5931\u503c\u8ba1\u6570", None))
        self.checkBox_miss_ratio.setText(QCoreApplication.translate("Form", u"\u7f3a\u5931\u503c\u5360\u6bd4", None))
        self.checkBox_unique.setText(QCoreApplication.translate("Form", u"\u552f\u4e00\u503c", None))
        self.checkBox_max.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u503c", None))
        self.checkBox_min.setText(QCoreApplication.translate("Form", u"\u6700\u5c0f\u503c", None))
        self.checkBox_sum.setText(QCoreApplication.translate("Form", u"\u603b\u548c", None))
        self.checkBox_mean.setText(QCoreApplication.translate("Form", u"\u5747\u503c", None))
        self.checkBox_mode.setText(QCoreApplication.translate("Form", u"\u4f17\u6570", None))
        self.checkBox_kurt.setText(QCoreApplication.translate("Form", u"\u5cf0\u5ea6", None))
        self.checkBox_skew.setText(QCoreApplication.translate("Form", u"\u504f\u5ea6", None))
        self.checkBox_var.setText(QCoreApplication.translate("Form", u"\u65b9\u5dee", None))
        self.checkBox_std.setText(QCoreApplication.translate("Form", u"\u6807\u51c6\u5dee", None))
        self.checkBox_se_mean.setText(QCoreApplication.translate("Form", u"\u5747\u503c\u6807\u51c6\u8bef", None))
        self.checkBox_q1.setText(QCoreApplication.translate("Form", u"\u4e0b\u56db\u5206\u4f4d\u6570Q1", None))
        self.checkBox_median.setText(QCoreApplication.translate("Form", u"\u4e2d\u4f4d\u6570", None))
        self.checkBox_q3.setText(QCoreApplication.translate("Form", u"\u4e0a\u56db\u5206\u4f4d\u6570Q3", None))
        self.checkBox_qrange.setText(QCoreApplication.translate("Form", u"\u56db\u5206\u4f4d\u95f4\u8ddd", None))
        self.checkBox_range.setText(QCoreApplication.translate("Form", u"\u6781\u5dee", None))
        self.checkBox_cv.setText(QCoreApplication.translate("Form", u"\u53d8\u5f02\u7cfb\u6570", None))
        self.checkBox_sum_of_squares.setText(QCoreApplication.translate("Form", u"\u5e73\u65b9\u548c", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7cbe\u5ea6:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.checkBoxhist.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u76f4\u65b9\u56fe", None))
        self.checkBox_normal.setText(QCoreApplication.translate("Form", u"\u5e26\u6b63\u6001\u66f2\u7ebf\u7684\u6570\u636e\u76f4\u65b9\u56fe", None))
        self.checkBox_value.setText(QCoreApplication.translate("Form", u"\u5355\u503c\u56fe", None))
        self.checkBox_boxplot.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7bb1\u7ebf\u56fe", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\u56fe\u5f62", None))
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

