# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_project_wizard.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPlainTextEdit, QSizePolicy, QSpacerItem,
    QToolButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget, QWizard, QWizardPage)
import pyqtsource_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(736, 505)
        Wizard.setWizardStyle(QWizard.ModernStyle)
        Wizard.setOptions(QWizard.HelpButtonOnRight|QWizard.NoBackButtonOnStartPage)
        self.wizardPage1 = QWizardPage()
        self.wizardPage1.setObjectName(u"wizardPage1")
        self.horizontalLayout = QHBoxLayout(self.wizardPage1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.widget_left = QWidget(self.wizardPage1)
        self.widget_left.setObjectName(u"widget_left")
        self.widget_left.setMinimumSize(QSize(200, 0))
        self.widget_left.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget_left)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.label = QLabel(self.widget_left)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(self.widget_left)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.listWidget = QListWidget(self.widget_left)
        font = QFont()
        font.setBold(True)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setFont(font);
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"border:0px;")

        self.verticalLayout.addWidget(self.listWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget_left)

        self.widget_right = QWidget(self.wizardPage1)
        self.widget_right.setObjectName(u"widget_right")
        self.verticalLayout_4 = QVBoxLayout(self.widget_right)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_11 = QLabel(self.widget_right)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(15, 15))
        self.label_11.setPixmap(QPixmap(u":/resources/icons/search.svg"))
        self.label_11.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_11)

        self.label_2 = QLabel(self.widget_right)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.widget_right)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.widget_3 = QWidget(self.widget_right)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.treeWidget = QTreeWidget(self.widget_3)
        icon = QIcon()
        icon.addFile(u":/resources/icons/folder_yellow.svg", QSize(), QIcon.Normal, QIcon.Off)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem.setIcon(0, icon);
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.treeWidget)


        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_right)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.file_list = QListWidget(self.widget_4)
        icon1 = QIcon()
        icon1.addFile(u":/resources/icons/python.svg", QSize(), QIcon.Normal, QIcon.Off)
        __qlistwidgetitem1 = QListWidgetItem(self.file_list)
        __qlistwidgetitem1.setIcon(icon1);
        __qlistwidgetitem2 = QListWidgetItem(self.file_list)
        __qlistwidgetitem2.setIcon(icon1);
        __qlistwidgetitem3 = QListWidgetItem(self.file_list)
        __qlistwidgetitem3.setIcon(icon1);
        __qlistwidgetitem4 = QListWidgetItem(self.file_list)
        __qlistwidgetitem4.setIcon(icon1);
        self.file_list.setObjectName(u"file_list")

        self.verticalLayout_3.addWidget(self.file_list)


        self.horizontalLayout_3.addWidget(self.widget_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.plainTextEdit = QPlainTextEdit(self.widget_right)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMaximumSize(QSize(16777215, 90))
        self.plainTextEdit.setStyleSheet(u"background-color: rgb(243, 243, 243);")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.plainTextEdit)


        self.horizontalLayout.addWidget(self.widget_right)

        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QWizardPage()
        self.wizardPage2.setObjectName(u"wizardPage2")
        self.horizontalLayout_6 = QHBoxLayout(self.wizardPage2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.widget_left_2 = QWidget(self.wizardPage2)
        self.widget_left_2.setObjectName(u"widget_left_2")
        self.widget_left_2.setMinimumSize(QSize(200, 0))
        self.widget_left_2.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.widget_left_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.label_5 = QLabel(self.widget_left_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_5.addWidget(self.label_5)

        self.line_2 = QFrame(self.widget_left_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_2)

        self.listWidget_2 = QListWidget(self.widget_left_2)
        font1 = QFont()
        font1.setBold(False)
        __qlistwidgetitem5 = QListWidgetItem(self.listWidget_2)
        __qlistwidgetitem5.setFont(font1);
        __qlistwidgetitem6 = QListWidgetItem(self.listWidget_2)
        __qlistwidgetitem6.setFont(font);
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setStyleSheet(u"border:0px;")

        self.verticalLayout_5.addWidget(self.listWidget_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addWidget(self.widget_left_2)

        self.widget_right_2 = QWidget(self.wizardPage2)
        self.widget_right_2.setObjectName(u"widget_right_2")
        self.verticalLayout_6 = QVBoxLayout(self.widget_right_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_9 = QLabel(self.widget_right_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_6.addWidget(self.label_9)

        self.line_3 = QFrame(self.widget_right_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line_3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.projectNameText = QLabel(self.widget_right_2)
        self.projectNameText.setObjectName(u"projectNameText")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.projectNameText)

        self.projectNameLineEdit = QLineEdit(self.widget_right_2)
        self.projectNameLineEdit.setObjectName(u"projectNameLineEdit")
        self.projectNameLineEdit.setClearButtonEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.projectNameLineEdit)

        self.projectDirectory = QLabel(self.widget_right_2)
        self.projectDirectory.setObjectName(u"projectDirectory")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.projectDirectory)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.projectDirectoryEditLine = QLineEdit(self.widget_right_2)
        self.projectDirectoryEditLine.setObjectName(u"projectDirectoryEditLine")
        self.projectDirectoryEditLine.setStyleSheet(u"")
        self.projectDirectoryEditLine.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.projectDirectoryEditLine)

        self.toolButton = QToolButton(self.widget_right_2)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_4.addWidget(self.toolButton)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.absoluteDirectory = QLabel(self.widget_right_2)
        self.absoluteDirectory.setObjectName(u"absoluteDirectory")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.absoluteDirectory)

        self.absoluteDirectoryEditLine = QLineEdit(self.widget_right_2)
        self.absoluteDirectoryEditLine.setObjectName(u"absoluteDirectoryEditLine")
        self.absoluteDirectoryEditLine.setStyleSheet(u"")
        self.absoluteDirectoryEditLine.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.absoluteDirectoryEditLine)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout_2.setItem(4, QFormLayout.LabelRole, self.verticalSpacer_3)

        self.warningLabel = QLabel(self.widget_right_2)
        self.warningLabel.setObjectName(u"warningLabel")
        self.warningLabel.setFont(font)
        self.warningLabel.setCursor(QCursor(Qt.IBeamCursor))
        self.warningLabel.setStyleSheet(u"color: rgb(255, 102, 0);")
        self.warningLabel.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.warningLabel)


        self.verticalLayout_6.addLayout(self.formLayout_2)


        self.horizontalLayout_6.addWidget(self.widget_right_2)

        Wizard.addPage(self.wizardPage2)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"New Project", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"Steps", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Wizard", u"1. Select Project Type", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Wizard", u"2. Configure Project", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.label_11.setText("")
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Search", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"Language", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Wizard", u"Type", None));

        __sortingEnabled1 = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Wizard", u"Python", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled1)

        self.label_4.setText(QCoreApplication.translate("Wizard", u"Project Type", None))

        __sortingEnabled2 = self.file_list.isSortingEnabled()
        self.file_list.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.file_list.item(0)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Wizard", u"Python-Empty", None));
        ___qlistwidgetitem3 = self.file_list.item(1)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Wizard", u"Python-Template-Basic", None));
        ___qlistwidgetitem4 = self.file_list.item(2)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Wizard", u"Python-Template-Plot", None));
        ___qlistwidgetitem5 = self.file_list.item(3)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Wizard", u"Python-Template-PySide2", None));
        self.file_list.setSortingEnabled(__sortingEnabled2)

        self.plainTextEdit.setPlainText("")
        self.label_5.setText(QCoreApplication.translate("Wizard", u"Steps", None))

        __sortingEnabled3 = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        ___qlistwidgetitem6 = self.listWidget_2.item(0)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Wizard", u"1. Select Project Type", None));
        ___qlistwidgetitem7 = self.listWidget_2.item(1)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Wizard", u"2. Configure Project", None));
        self.listWidget_2.setSortingEnabled(__sortingEnabled3)

        self.label_9.setText(QCoreApplication.translate("Wizard", u"Project Configuration", None))
        self.projectNameText.setText(QCoreApplication.translate("Wizard", u"Project Name:", None))
        self.projectNameLineEdit.setText(QCoreApplication.translate("Wizard", u"PyMinerProject", None))
        self.projectDirectory.setText(QCoreApplication.translate("Wizard", u"Project Directory:", None))
        self.toolButton.setText(QCoreApplication.translate("Wizard", u"...", None))
        self.absoluteDirectory.setText(QCoreApplication.translate("Wizard", u"Absolute Directory:", None))
        self.warningLabel.setText("")
    # retranslateUi

