# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_role_edit.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listWidget = QListWidget(self.groupBox_2)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_3.addWidget(self.listWidget)

        self.splitter.addWidget(self.groupBox_2)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 25))
        self.lineEdit.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.comboBox_3 = QComboBox(self.groupBox)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setMinimumSize(QSize(0, 25))
        self.comboBox_3.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_3)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.spinBox_2 = QSpinBox(self.groupBox)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimumSize(QSize(0, 25))
        self.spinBox_2.setMaximumSize(QSize(150, 16777215))
        self.spinBox_2.setValue(8)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinBox_2)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(0, 25))
        self.spinBox.setMaximumSize(QSize(150, 16777215))
        self.spinBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.spinBox.setValue(2)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spinBox)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_6)

        self.comboBox_6 = QComboBox(self.groupBox)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setMinimumSize(QSize(0, 25))
        self.comboBox_6.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboBox_6)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_7)

        self.comboBox_7 = QComboBox(self.groupBox)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setMinimumSize(QSize(0, 25))
        self.comboBox_7.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.comboBox_7)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.comboBox_8 = QComboBox(self.groupBox)
        icon = QIcon()
        icon.addFile(u":/pyqt/source/image/lc_datasort.png", QSize(), QIcon.Normal, QIcon.On)
        self.comboBox_8.addItem(icon, "")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/image/lc_dbsortingandgrouping.png", QSize(), QIcon.Normal, QIcon.On)
        self.comboBox_8.addItem(icon1, "")
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/image/lc_insertsymbol.png", QSize(), QIcon.Normal, QIcon.On)
        self.comboBox_8.addItem(icon2, "")
        self.comboBox_8.setObjectName(u"comboBox_8")
        self.comboBox_8.setMinimumSize(QSize(0, 25))
        self.comboBox_8.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboBox_8)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_9)

        self.comboBox_9 = QComboBox(self.groupBox)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")
        self.comboBox_9.setMinimumSize(QSize(0, 25))
        self.comboBox_9.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.comboBox_9)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.splitter.addWidget(self.groupBox)

        self.verticalLayout.addWidget(self.splitter)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u89d2\u8272\u7f16\u8f91", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u53d8\u91cf\u5217\u8868", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u53d8\u91cf\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6807\u7b7e\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7c7b\u578b\uff1a", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"int", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"string", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Form", u"double", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("Form", u"float", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"\u5bbd\u5ea6\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5c0f\u6570\u4f4d\u6570\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u7f3a\u5931\u503c\uff1a", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Form", u"\u9ed8\u8ba4", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Form", u"NULL", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("Form", u"NA", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u53c2\u4e0e\uff1a", None))
        self.comboBox_7.setItemText(0, QCoreApplication.translate("Form", u"\u662f", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("Form", u"\u5426", None))

        self.label_8.setText(QCoreApplication.translate("Form", u"\u6d4b\u91cf\u6c34\u5e73\uff1a", None))
        self.comboBox_8.setItemText(0, QCoreApplication.translate("Form", u"\u6807\u5ea6", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("Form", u"\u6709\u5e8f", None))
        self.comboBox_8.setItemText(2, QCoreApplication.translate("Form", u"\u540d\u4e49", None))

        self.label_9.setText(QCoreApplication.translate("Form", u"\u6d4b\u91cf\u6c34\u5e73\uff1a", None))
        self.comboBox_9.setItemText(0, QCoreApplication.translate("Form", u"\u8f93\u5165", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("Form", u"\u76ee\u6807", None))
        self.comboBox_9.setItemText(2, QCoreApplication.translate("Form", u"\u4e24\u8005", None))
        self.comboBox_9.setItemText(3, QCoreApplication.translate("Form", u"\u65e0", None))
        self.comboBox_9.setItemText(4, QCoreApplication.translate("Form", u"\u5206\u533a", None))
        self.comboBox_9.setItemText(5, QCoreApplication.translate("Form", u"\u62c6\u5206", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"\u5e2e\u52a9", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

