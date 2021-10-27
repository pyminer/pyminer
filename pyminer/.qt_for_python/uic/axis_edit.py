# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'axis_edit.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(635, 480)
        Dialog.setMinimumSize(QSize(635, 480))
        Dialog.setMaximumSize(QSize(635, 480))
        self.treeWidget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(10, 10, 121, 421))
        self.treeWidget.setMaximumSize(QSize(150, 16777215))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(140, 10, 491, 461))
        self.gridGroupBox_2 = QGroupBox(self.groupBox)
        self.gridGroupBox_2.setObjectName(u"gridGroupBox_2")
        self.gridGroupBox_2.setGeometry(QRect(10, 20, 471, 407))
        self.gridLayout_2 = QGridLayout(self.gridGroupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.comboBox_4 = QComboBox(self.gridGroupBox_2)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout_2.addWidget(self.comboBox_4, 0, 3, 1, 1)

        self.checkBox_3 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_2.addWidget(self.checkBox_3, 12, 1, 1, 1)

        self.label_9 = QLabel(self.gridGroupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 1, 2, 1, 1)

        self.label = QLabel(self.gridGroupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_25 = QLabel(self.gridGroupBox_2)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_2.addWidget(self.label_25, 5, 2, 1, 1)

        self.checkBox = QCheckBox(self.gridGroupBox_2)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 11, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_2.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.checkBox_5 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout_2.addWidget(self.checkBox_5, 14, 1, 1, 1)

        self.checkBox_8 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.gridLayout_2.addWidget(self.checkBox_8, 15, 1, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self.gridGroupBox_2)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(0.000000000000000)
        self.doubleSpinBox.setMaximum(100.000000000000000)
        self.doubleSpinBox.setSingleStep(0.500000000000000)
        self.doubleSpinBox.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox, 4, 3, 1, 1)

        self.lineEdit = QLineEdit(self.gridGroupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_12 = QLabel(self.gridGroupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 2, 2, 1, 1)

        self.lineEdit_5 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout_2.addWidget(self.lineEdit_5, 4, 1, 1, 1)

        self.label_19 = QLabel(self.gridGroupBox_2)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 9, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_2.addWidget(self.checkBox_2, 10, 1, 1, 1)

        self.comboBox_5 = QComboBox(self.gridGroupBox_2)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.gridLayout_2.addWidget(self.comboBox_5, 1, 3, 1, 1)

        self.lineEdit_4 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_2.addWidget(self.lineEdit_4, 3, 1, 1, 1)

        self.label_16 = QLabel(self.gridGroupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 12, 0, 1, 1)

        self.label_18 = QLabel(self.gridGroupBox_2)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_2.addWidget(self.label_18, 14, 0, 1, 1)

        self.label_3 = QLabel(self.gridGroupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_10 = QLabel(self.gridGroupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 5, 0, 1, 1)

        self.checkBox_6 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.gridLayout_2.addWidget(self.checkBox_6, 9, 1, 1, 1)

        self.label_7 = QLabel(self.gridGroupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 15, 0, 1, 1)

        self.label_14 = QLabel(self.gridGroupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 11, 0, 1, 1)

        self.horizontalSlider = QSlider(self.gridGroupBox_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)

        self.gridLayout_2.addWidget(self.horizontalSlider, 3, 3, 1, 1)

        self.comboBox_6 = QComboBox(self.gridGroupBox_2)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.gridLayout_2.addWidget(self.comboBox_6, 2, 3, 1, 1)

        self.comboBox_2 = QComboBox(self.gridGroupBox_2)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout_2.addWidget(self.comboBox_2, 8, 1, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.gridGroupBox_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setDecimals(1)
        self.doubleSpinBox_2.setMinimum(0.000000000000000)
        self.doubleSpinBox_2.setMaximum(100.000000000000000)
        self.doubleSpinBox_2.setSingleStep(0.500000000000000)
        self.doubleSpinBox_2.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_2, 5, 3, 1, 1)

        self.label_2 = QLabel(self.gridGroupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_13 = QLabel(self.gridGroupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 8, 0, 1, 1)

        self.label_5 = QLabel(self.gridGroupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_8 = QLabel(self.gridGroupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)

        self.label_29 = QLabel(self.gridGroupBox_2)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_2.addWidget(self.label_29, 3, 2, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.gridGroupBox_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setDecimals(1)
        self.doubleSpinBox_3.setMinimum(0.000000000000000)
        self.doubleSpinBox_3.setMaximum(100.000000000000000)
        self.doubleSpinBox_3.setSingleStep(0.500000000000000)
        self.doubleSpinBox_3.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_3, 6, 3, 1, 1)

        self.label_22 = QLabel(self.gridGroupBox_2)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_2.addWidget(self.label_22, 4, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.checkBox_4 = QCheckBox(self.gridGroupBox_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_2.addWidget(self.checkBox_4, 13, 1, 1, 1)

        self.label_24 = QLabel(self.gridGroupBox_2)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_2.addWidget(self.label_24, 6, 2, 1, 1)

        self.label_17 = QLabel(self.gridGroupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_2.addWidget(self.label_17, 13, 0, 1, 1)

        self.label_4 = QLabel(self.gridGroupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_15 = QLabel(self.gridGroupBox_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 10, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_7 = QComboBox(self.gridGroupBox_2)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.horizontalLayout_2.addWidget(self.comboBox_7)

        self.lineEdit_7 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.horizontalLayout_2.addWidget(self.lineEdit_7)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)

        self.label_21 = QLabel(self.gridGroupBox_2)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_2.addWidget(self.label_21, 6, 0, 1, 1)

        self.lineEdit_8 = QLineEdit(self.gridGroupBox_2)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout_2.addWidget(self.lineEdit_8, 6, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(240, 430, 239, 25))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5750\u6807\u8f74\u7f16\u8f91\u5668", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.checkBox_3.setText("")
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u663e\u793a\u4f4d\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6700\u5c0f\u503c", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"\u8f74\u6807\u7b7e\u5b57\u4f53\u5927\u5c0f", None))
        self.checkBox.setText("")
        self.checkBox_5.setText("")
        self.checkBox_8.setText("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u6837\u5f0f", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u8f74", None))
        self.checkBox_2.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u5bf9\u8fb9\u8f74", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u5bf9\u8fb9\u8f74\u523b\u5ea6\u6807\u7b7e", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u4e3b\u523b\u5ea6\u95f4\u9694", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u5750\u6807\u8f74\u4f4d\u7f6e", None))
        self.checkBox_6.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u7f51\u683c", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u8f74\u523b\u5ea6\u6807\u7b7e", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u6700\u5927\u503c", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u523b\u5ea6\u4f4d\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u5750\u6807\u8f74\u6807\u7b7e", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u989c\u8272", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u900f\u660e\u5ea6", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u5bbd\u5ea6", None))
        self.checkBox_4.setText("")
        self.label_24.setText(QCoreApplication.translate("Dialog", u"\u523b\u5ea6\u6807\u7b7e\u5b57\u4f53\u5927\u5c0f ", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u5bf9\u8fb9\u8f74\u523b\u5ea6", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u6b21\u523b\u5ea6\u95f4\u9694", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u663e\u793a\u8f74\u523b\u5ea6", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"\u65cb\u8f6c\u8f74\u523b\u5ea6\u6807\u7b7e/\u00b0", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"\u5e94\u7528", None))
    # retranslateUi

