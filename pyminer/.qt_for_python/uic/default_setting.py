# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'default_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFontComboBox, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(373, 233)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_44 = QLabel(Form)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout.addWidget(self.label_44, 5, 0, 1, 1)

        self.fontComboBox = QFontComboBox(Form)
        self.fontComboBox.setObjectName(u"fontComboBox")

        self.gridLayout.addWidget(self.fontComboBox, 4, 1, 1, 1)

        self.label_46 = QLabel(Form)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout.addWidget(self.label_46, 4, 0, 1, 1)

        self.label_17 = QLabel(Form)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 2, 0, 1, 1)

        self.comboBox_gui_language = QComboBox(Form)
        self.comboBox_gui_language.setObjectName(u"comboBox_gui_language")

        self.gridLayout.addWidget(self.comboBox_gui_language, 0, 1, 1, 1)

        self.comboBox_14 = QComboBox(Form)
        self.comboBox_14.setObjectName(u"comboBox_14")

        self.gridLayout.addWidget(self.comboBox_14, 5, 1, 1, 1)

        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_8.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_8.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_8.addWidget(self.pushButton_3)


        self.gridLayout.addLayout(self.horizontalLayout_8, 7, 1, 1, 1)

        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 1, 0, 1, 1)

        self.comboBox_3 = QComboBox(Form)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout.addWidget(self.comboBox_3, 3, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 3, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.comboBox_coord = QComboBox(Form)
        self.comboBox_coord.addItem("")
        self.comboBox_coord.addItem("")
        self.comboBox_coord.addItem("")
        self.comboBox_coord.addItem("")
        self.comboBox_coord.setObjectName(u"comboBox_coord")

        self.gridLayout.addWidget(self.comboBox_coord, 6, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 2, 4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.label_44.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u7ed8\u56fe\u98ce\u683c\u91c7\u7528SciencePlots\u5305\uff0c\u53ea\u4f1a\u5728\u91cd\u65b0plt.show()\u540e\u624d\u4f1a\u751f\u6548\uff0c\u6587\u5b57\u4e2d\u542b\u6709 \u4e2d\u6587\u53ef\u80fd\u4f1a\u62a5\u9519\uff0c\u9ed8\u8ba4\u5b57\u4f53\u7684\u8bbe\u7f6e\u5c06\u4f1a\u65e0\u6548</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_44.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.label_44.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_44.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u9ed8\u8ba4\u7ed8\u56fe\u98ce\u683c\uff1a", None))
        self.label_46.setText(QCoreApplication.translate("Form", u"\u5207\u6362\u754c\u9762\u5b57\u4f53", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"\u82f1\u6587\u5b57\u4f53\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\u5e94\u7528", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"\u4e2d\u6587\u5b57\u4f53\uff1a", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf\u8bed\u8a00:", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"\u4e2d\u82f1\u6587\u6df7\u5408\u5b57\u4f53\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5207\u6362\u6ce8\u91ca\u7684\u5750\u6807\u7cfb", None))
        self.comboBox_coord.setItemText(0, QCoreApplication.translate("Form", u"data", None))
        self.comboBox_coord.setItemText(1, QCoreApplication.translate("Form", u"axes", None))
        self.comboBox_coord.setItemText(2, QCoreApplication.translate("Form", u"figure", None))
        self.comboBox_coord.setItemText(3, QCoreApplication.translate("Form", u"pixel", None))

    # retranslateUi

