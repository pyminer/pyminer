# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'ConsoleHistoryDialog.ui'
##
# Created by: Qt User Interface Compiler version 6.1.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConsoleHistoryDialog(object):
    def setupUi(self, ConsoleHistoryDialog):
        if not ConsoleHistoryDialog.objectName():
            ConsoleHistoryDialog.setObjectName(u"ConsoleHistoryDialog")
        ConsoleHistoryDialog.resize(540, 506)
        ConsoleHistoryDialog.setSizeGripEnabled(True)
        self.gridLayout = QGridLayout(ConsoleHistoryDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.historyList = QListWidget(ConsoleHistoryDialog)
        self.historyList.setObjectName(u"historyList")
        font = QFont()
        font.setFamilies([u"Monospace"])
        self.historyList.setFont(font)
        self.historyList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.historyList.setAlternatingRowColors(True)
        self.historyList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.historyList.setWordWrap(True)

        self.gridLayout.addWidget(self.historyList, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.deleteButton = QPushButton(ConsoleHistoryDialog)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setEnabled(False)

        self.verticalLayout.addWidget(self.deleteButton)

        self.copyButton = QPushButton(ConsoleHistoryDialog)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setEnabled(False)

        self.verticalLayout.addWidget(self.copyButton)

        self.executeButton = QPushButton(ConsoleHistoryDialog)
        self.executeButton.setObjectName(u"executeButton")
        self.executeButton.setEnabled(False)

        self.verticalLayout.addWidget(self.executeButton)

        self.reloadButton = QPushButton(ConsoleHistoryDialog)
        self.reloadButton.setObjectName(u"reloadButton")

        self.verticalLayout.addWidget(self.reloadButton)

        self.verticalSpacer = QSpacerItem(
            72, 208, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(ConsoleHistoryDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        QWidget.setTabOrder(self.historyList, self.deleteButton)
        QWidget.setTabOrder(self.deleteButton, self.copyButton)
        QWidget.setTabOrder(self.copyButton, self.executeButton)
        QWidget.setTabOrder(self.executeButton, self.reloadButton)
        QWidget.setTabOrder(self.reloadButton, self.buttonBox)

        self.retranslateUi(ConsoleHistoryDialog)
        self.buttonBox.accepted.connect(ConsoleHistoryDialog.accept)
        self.buttonBox.rejected.connect(ConsoleHistoryDialog.reject)

        QMetaObject.connectSlotsByName(ConsoleHistoryDialog)
    # setupUi

    def retranslateUi(self, ConsoleHistoryDialog):
        ConsoleHistoryDialog.setWindowTitle(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"Shell History", None))
# if QT_CONFIG(tooltip)
        self.deleteButton.setToolTip(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"Delete the selected entries", None))
#endif // QT_CONFIG(tooltip)
        self.deleteButton.setText(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"&Delete", None))
# if QT_CONFIG(tooltip)
        self.copyButton.setToolTip(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"Copy the selected entries to the current editor", None))
#endif // QT_CONFIG(tooltip)
        self.copyButton.setText(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"C&opy", None))
# if QT_CONFIG(tooltip)
        self.executeButton.setToolTip(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"Execute the selected entries", None))
#endif // QT_CONFIG(tooltip)
        self.executeButton.setText(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"&Execute", None))
# if QT_CONFIG(tooltip)
        self.reloadButton.setToolTip(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"Reload the history", None))
#endif // QT_CONFIG(tooltip)
        self.reloadButton.setText(QCoreApplication.translate(
            "ConsoleHistoryDialog", u"&Reload", None))
    # retranslateUi
