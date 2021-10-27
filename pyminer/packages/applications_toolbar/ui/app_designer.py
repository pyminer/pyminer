# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_designer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from resources import resources_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(646, 557)
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        Wizard.setFont(font)
        Wizard.setAutoFillBackground(False)
        Wizard.setStyleSheet(u"")
        Wizard.setWizardStyle(QWizard.AeroStyle)
        self.intruduce = QWizardPage()
        self.intruduce.setObjectName(u"intruduce")
        self.verticalLayout = QVBoxLayout(self.intruduce)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plainTextEdit = QPlainTextEdit(self.intruduce)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.plainTextEdit)

        Wizard.setPage(1, self.intruduce)
        self.base_info = QWizardPage()
        self.base_info.setObjectName(u"base_info")
        self.horizontalLayout = QHBoxLayout(self.base_info)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.base_info)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.app_name = QLineEdit(self.widget)
        self.app_name.setObjectName(u"app_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.app_name)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.author = QLineEdit(self.widget)
        self.author.setObjectName(u"author")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.author)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.version = QLineEdit(self.widget)
        self.version.setObjectName(u"version")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.version)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.app_type = QComboBox(self.widget)
        self.app_type.addItem("")
        self.app_type.addItem("")
        self.app_type.setObjectName(u"app_type")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.app_type)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.app_display_name = QLineEdit(self.widget)
        self.app_display_name.setObjectName(u"app_display_name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.app_display_name)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.icon_path = QLineEdit(self.widget)
        self.icon_path.setObjectName(u"icon_path")

        self.horizontalLayout_8.addWidget(self.icon_path)

        self.icon_choose = QToolButton(self.widget)
        self.icon_choose.setObjectName(u"icon_choose")

        self.horizontalLayout_8.addWidget(self.icon_choose)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_7)

        self.app_desciption = QTextEdit(self.widget)
        self.app_desciption.setObjectName(u"app_desciption")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.app_desciption)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.app_class = QComboBox(self.widget)
        self.app_class.addItem("")
        self.app_class.addItem("")
        self.app_class.addItem("")
        self.app_class.addItem("")
        self.app_class.addItem("")
        self.app_class.addItem("")
        self.app_class.setObjectName(u"app_class")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.app_class)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_11)

        self.app_dev_path = QComboBox(self.widget)
        self.app_dev_path.setObjectName(u"app_dev_path")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.app_dev_path)


        self.horizontalLayout.addWidget(self.widget)

        Wizard.setPage(2, self.base_info)
        self.designer = QWizardPage()
        self.designer.setObjectName(u"designer")
        self.verticalLayout_2 = QVBoxLayout(self.designer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plainTextEdit_2 = QPlainTextEdit(self.designer)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit_2.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.plainTextEdit_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_qtdesigner = QPushButton(self.designer)
        self.btn_qtdesigner.setObjectName(u"btn_qtdesigner")

        self.horizontalLayout_2.addWidget(self.btn_qtdesigner)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        Wizard.setPage(3, self.designer)
        self.code = QWizardPage()
        self.code.setObjectName(u"code")
        self.verticalLayout_3 = QVBoxLayout(self.code)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit_3 = QPlainTextEdit(self.code)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setBackgroundVisible(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_open_folder = QPushButton(self.code)
        self.btn_open_folder.setObjectName(u"btn_open_folder")

        self.horizontalLayout_3.addWidget(self.btn_open_folder)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        Wizard.setPage(4, self.code)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"App Developing Wizard", None))
        self.intruduce.setTitle(QCoreApplication.translate("Wizard", u"Introduction", None))
        self.intruduce.setSubTitle("")
        self.plainTextEdit.setPlainText(QCoreApplication.translate("Wizard", u"PyMiner makes it easier to develop  applications by PyQt5. \n"
"\n"
"The applications can only run on your machine or release to application market to used by more users. \n"
"\n"
"The applications are of two types: Toolbox Application and Embedded Application.\n"
"\n"
"Toolbox Application is suitable for scientific calculation. You can start it by double clicking the buttons in Application toolbar.\n"
"\n"
"Embedded Application will be displayed on PyMiner MainWindow, which strengthens the PyMiner platform.\n"
"\n"
"Let's start our tour on developing Applications! \n"
"", None))
        self.base_info.setTitle(QCoreApplication.translate("Wizard", u"App Information", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"App Name:", None))
        self.app_name.setText(QCoreApplication.translate("Wizard", u"demo_app", None))
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Author:", None))
        self.author.setText(QCoreApplication.translate("Wizard", u"demo", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"Version:", None))
#if QT_CONFIG(tooltip)
        self.version.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>\u7248\u672c\u53f7\u683c\u5f0f\u8bf7\u53c2\u8003\uff1ax.y.z</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.version.setText(QCoreApplication.translate("Wizard", u"1.0.1", None))
        self.label_4.setText(QCoreApplication.translate("Wizard", u"App Type:", None))
        self.app_type.setItemText(0, QCoreApplication.translate("Wizard", u"Toolbox Application", None))
        self.app_type.setItemText(1, QCoreApplication.translate("Wizard", u"Embedded Application", None))

        self.label_5.setText(QCoreApplication.translate("Wizard", u"Text:", None))
        self.app_display_name.setText(QCoreApplication.translate("Wizard", u"Test Application", None))
        self.label_6.setText(QCoreApplication.translate("Wizard", u"Icon:", None))
        self.icon_choose.setText(QCoreApplication.translate("Wizard", u"...", None))
        self.label_7.setText(QCoreApplication.translate("Wizard", u"Description:", None))
        self.label_8.setText(QCoreApplication.translate("Wizard", u"Field:", None))
        self.app_class.setItemText(0, QCoreApplication.translate("Wizard", u"Math&Statistics", None))
        self.app_class.setItemText(1, QCoreApplication.translate("Wizard", u"Economics&Finance", None))
        self.app_class.setItemText(2, QCoreApplication.translate("Wizard", u"Electronics&Communication Engineering", None))
        self.app_class.setItemText(3, QCoreApplication.translate("Wizard", u"Biology&Medical", None))
        self.app_class.setItemText(4, QCoreApplication.translate("Wizard", u"Civil Engineerings", None))
        self.app_class.setItemText(5, QCoreApplication.translate("Wizard", u"Mechanical Engineerings", None))

        self.label_11.setText(QCoreApplication.translate("Wizard", u"Dev Path:", None))
        self.designer.setTitle(QCoreApplication.translate("Wizard", u"Start Designing", None))
        self.plainTextEdit_2.setPlainText(QCoreApplication.translate("Wizard", u"Well done! Now we have created the project folder, and your application is right here.\n"
"\n"
"However your application needs a GUI with some code. In PyMiner, we develop GUI with Qt Designer and write code in the editor of PyMiner.", None))
        self.btn_qtdesigner.setText(QCoreApplication.translate("Wizard", u"Qt Designer", None))
        self.plainTextEdit_3.setPlainText(QCoreApplication.translate("Wizard", u"Now your applications has been initialized, and you can enter the App folder to develop it.", None))
        self.btn_open_folder.setText(QCoreApplication.translate("Wizard", u"Open App Folder", None))
    # retranslateUi

