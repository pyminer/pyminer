# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_filter.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1024, 600)
        Form.setMinimumSize(QSize(1024, 600))
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(100, 0))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.combo_var_name = QComboBox(self.widget)
        self.combo_var_name.setObjectName(u"combo_var_name")

        self.verticalLayout_3.addWidget(self.combo_var_name)


        self.horizontalLayout_4.addWidget(self.widget)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 25))
        self.label.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_4.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEnabled(True)
        self.comboBox.setMinimumSize(QSize(80, 25))
        self.comboBox.setMaximumSize(QSize(80, 22))

        self.horizontalLayout.addWidget(self.comboBox)

        self.comboBox_3 = QComboBox(Form)
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setEnabled(True)
        self.comboBox_3.setMinimumSize(QSize(80, 25))
        self.comboBox_3.setMaximumSize(QSize(90, 22))

        self.horizontalLayout.addWidget(self.comboBox_3)

        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMinimumSize(QSize(80, 25))
        self.comboBox_2.setMaximumSize(QSize(60, 22))

        self.horizontalLayout.addWidget(self.comboBox_2)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(300, 25))
        self.lineEdit.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_4 = QComboBox(Form)
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setEnabled(True)
        self.comboBox_4.setMinimumSize(QSize(80, 25))
        self.comboBox_4.setMaximumSize(QSize(80, 22))

        self.horizontalLayout_2.addWidget(self.comboBox_4)

        self.comboBox_5 = QComboBox(Form)
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setEnabled(True)
        self.comboBox_5.setMinimumSize(QSize(80, 25))
        self.comboBox_5.setMaximumSize(QSize(90, 22))

        self.horizontalLayout_2.addWidget(self.comboBox_5)

        self.comboBox_6 = QComboBox(Form)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setMinimumSize(QSize(80, 25))
        self.comboBox_6.setMaximumSize(QSize(60, 22))

        self.horizontalLayout_2.addWidget(self.comboBox_6)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(300, 22))
        self.lineEdit_2.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(60, 25))
        self.pushButton.setMaximumSize(QSize(60, 22))
        icon = QIcon()
        icon.addFile(u":/pyqt/source/image/sc_formfiltered.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(60, 25))
        self.pushButton_2.setMaximumSize(QSize(60, 22))
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/image/lc_removefiltersort.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.pushButton_2)

        self.pushButton_export = QPushButton(Form)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setMinimumSize(QSize(60, 25))
        self.pushButton_export.setMaximumSize(QSize(60, 22))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/image/lc_exportto.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_export.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.pushButton_export)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(16, 16))
        self.label_2.setMaximumSize(QSize(20, 20))
        self.label_2.setStyleSheet(u"image: url(:/pyqt/source/image/NavOverFlow_Info.png);")

        self.horizontalLayout_4.addWidget(self.label_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tableWidget_baseStats = QTableWidget(Form)
        self.tableWidget_baseStats.setObjectName(u"tableWidget_baseStats")
        self.tableWidget_baseStats.setMinimumSize(QSize(500, 400))

        self.verticalLayout_2.addWidget(self.tableWidget_baseStats)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u7b5b\u9009", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u53d8\u91cf", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u67e5\u8be2\u6761\u4ef6\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"\u5217", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"\u4e0d\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Form", u"\u5927\u4e8e", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("Form", u"\u5927\u4e8e\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("Form", u"\u5c0f\u4e8e", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("Form", u"\u5c0f\u4e8e\u7b49\u4e8e", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("Form", u"\u6a21\u7cca\u5339\u914d", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("Form", u"\u591a\u91cd\u5339\u914d", None))

        self.comboBox_4.setItemText(0, QCoreApplication.translate("Form", u"\u884c", None))

        self.comboBox_5.setItemText(0, QCoreApplication.translate("Form", u"\u5168\u90e8", None))

        self.comboBox_6.setItemText(0, QCoreApplication.translate("Form", u"\u7b49\u4e8e", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Form", u"\u4e0d\u7b49\u4e8e", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("Form", u"\u5927\u4e8e", None))
        self.comboBox_6.setItemText(3, QCoreApplication.translate("Form", u"\u5927\u4e8e\u7b49\u4e8e", None))
        self.comboBox_6.setItemText(4, QCoreApplication.translate("Form", u"\u5c0f\u4e8e", None))
        self.comboBox_6.setItemText(5, QCoreApplication.translate("Form", u"\u5c0f\u4e8e\u7b49\u4e8e", None))
        self.comboBox_6.setItemText(6, QCoreApplication.translate("Form", u"\u6a21\u7cca\u5339\u914d", None))
        self.comboBox_6.setItemText(7, QCoreApplication.translate("Form", u"\u591a\u91cd\u5339\u914d", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"\u7b5b\u9009", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a", None))
        self.pushButton_export.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Form", u"\u9700\u8981\u4f7f\u7528\u591a\u4e2a\u6761\u4ef6\u67e5\u8be2\u65f6\uff0c\u8bf7\u4f7f\u7528\u201c\u591a\u91cd\u5339\u914d\u201d", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText("")
    # retranslateUi

