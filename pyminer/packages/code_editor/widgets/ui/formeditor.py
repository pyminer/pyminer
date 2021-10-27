# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formeditor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets import PMGQsciWidget


class Ui_FormEditor(object):
    def setupUi(self, FormEditor):
        if not FormEditor.objectName():
            FormEditor.setObjectName(u"FormEditor")
        FormEditor.resize(800, 600)
        self.gridLayout = QGridLayout(FormEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setContentsMargins(0, 0, 0, 3)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.label_status_length = QLabel(FormEditor)
        self.label_status_length.setObjectName(u"label_status_length")

        self.gridLayout.addWidget(self.label_status_length, 1, 1, 1, 1)

        self.label_status_encoding = QLabel(FormEditor)
        self.label_status_encoding.setObjectName(u"label_status_encoding")

        self.gridLayout.addWidget(self.label_status_encoding, 1, 5, 1, 1)

        self.label_status_sel = QLabel(FormEditor)
        self.label_status_sel.setObjectName(u"label_status_sel")

        self.gridLayout.addWidget(self.label_status_sel, 1, 3, 1, 1)

        self.label_status_ln_col = QLabel(FormEditor)
        self.label_status_ln_col.setObjectName(u"label_status_ln_col")

        self.gridLayout.addWidget(self.label_status_ln_col, 1, 2, 1, 1)

        self.label_status_eol = QLabel(FormEditor)
        self.label_status_eol.setObjectName(u"label_status_eol")

        self.gridLayout.addWidget(self.label_status_eol, 1, 4, 1, 1)

        self.textEdit = PMGQsciWidget(FormEditor)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)

        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(FormEditor)

        QMetaObject.connectSlotsByName(FormEditor)
    # setupUi

    def retranslateUi(self, FormEditor):
        FormEditor.setWindowTitle(QCoreApplication.translate("FormEditor", u"Form", None))
        self.label_status_length.setText(QCoreApplication.translate("FormEditor", u"Length:{0}  Lines:{1}", None))
        self.label_status_encoding.setText(QCoreApplication.translate("FormEditor", u"UTF-8", None))
        self.label_status_sel.setText(QCoreApplication.translate("FormEditor", u"Sel:{0} | {1}", None))
        self.label_status_ln_col.setText(QCoreApplication.translate("FormEditor", u"Ln:{0}  Col:{1}", None))
        self.label_status_eol.setText(QCoreApplication.translate("FormEditor", u"Unix(LF)", None))
#if QT_CONFIG(tooltip)
        self.textEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.textEdit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

