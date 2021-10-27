# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_merge_horizontal.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(0, 0))
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_username_3 = QLabel(Form)
        self.label_username_3.setObjectName(u"label_username_3")

        self.verticalLayout_3.addWidget(self.label_username_3)

        self.listWidget_dataset = QListWidget(Form)
        self.listWidget_dataset.setObjectName(u"listWidget_dataset")

        self.verticalLayout_3.addWidget(self.listWidget_dataset)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_username_5 = QLabel(Form)
        self.label_username_5.setObjectName(u"label_username_5")

        self.verticalLayout_4.addWidget(self.label_username_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_start_add = QPushButton(Form)
        self.pushButton_start_add.setObjectName(u"pushButton_start_add")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_add.setIcon(icon)

        self.verticalLayout_6.addWidget(self.pushButton_start_add)

        self.pushButton_start_up = QPushButton(Form)
        self.pushButton_start_up.setObjectName(u"pushButton_start_up")
        self.pushButton_start_up.setMaximumSize(QSize(50, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_up.setIcon(icon1)

        self.verticalLayout_6.addWidget(self.pushButton_start_up)

        self.pushButton_start_down = QPushButton(Form)
        self.pushButton_start_down.setObjectName(u"pushButton_start_down")
        self.pushButton_start_down.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_down.setIcon(icon2)

        self.verticalLayout_6.addWidget(self.pushButton_start_down)

        self.pushButton_start_del = QPushButton(Form)
        self.pushButton_start_del.setObjectName(u"pushButton_start_del")
        self.pushButton_start_del.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_del.setIcon(icon3)

        self.verticalLayout_6.addWidget(self.pushButton_start_del)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.listWidget_start = QListWidget(Form)
        self.listWidget_start.setObjectName(u"listWidget_start")

        self.horizontalLayout_3.addWidget(self.listWidget_start)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_username_4 = QLabel(Form)
        self.label_username_4.setObjectName(u"label_username_4")

        self.verticalLayout_2.addWidget(self.label_username_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget_append = QListWidget(Form)
        self.listWidget_append.setObjectName(u"listWidget_append")

        self.horizontalLayout_2.addWidget(self.listWidget_append)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_append_add = QPushButton(Form)
        self.pushButton_append_add.setObjectName(u"pushButton_append_add")
        self.pushButton_append_add.setIcon(icon)

        self.verticalLayout_5.addWidget(self.pushButton_append_add)

        self.pushButton_append_up = QPushButton(Form)
        self.pushButton_append_up.setObjectName(u"pushButton_append_up")
        self.pushButton_append_up.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_up.setIcon(icon1)

        self.verticalLayout_5.addWidget(self.pushButton_append_up)

        self.pushButton_append_down = QPushButton(Form)
        self.pushButton_append_down.setObjectName(u"pushButton_append_down")
        self.pushButton_append_down.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_down.setIcon(icon2)

        self.verticalLayout_5.addWidget(self.pushButton_append_down)

        self.pushButton_append_del = QPushButton(Form)
        self.pushButton_append_del.setObjectName(u"pushButton_append_del")
        self.pushButton_append_del.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_del.setIcon(icon3)

        self.verticalLayout_5.addWidget(self.pushButton_append_del)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 50))
        self.widget_2.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_code = QPushButton(self.widget_2)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget_2)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon4)

        self.horizontalLayout.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget_2)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_save = QPushButton(self.widget_2)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u5408\u5e76-\u6a2a\u5411\u5408\u5e76", None))
        self.label_username_3.setText(QCoreApplication.translate("Form", u"\u53ef\u9009\u6570\u636e\u96c6:", None))
        self.label_username_5.setText(QCoreApplication.translate("Form", u"\u8d77\u59cb\u6570\u636e\u96c6\uff1a", None))
        self.pushButton_start_add.setText("")
        self.pushButton_start_up.setText("")
        self.pushButton_start_down.setText("")
        self.pushButton_start_del.setText("")
        self.label_username_4.setText(QCoreApplication.translate("Form", u"\u7528\u6765\u6a2a\u5411\u5408\u5e76\u7684\u6570\u636e\u96c6\uff1a", None))
        self.pushButton_append_add.setText("")
        self.pushButton_append_up.setText("")
        self.pushButton_append_down.setText("")
        self.pushButton_append_del.setText("")
        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

