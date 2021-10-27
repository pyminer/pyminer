# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formeditor.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FormEditor(object):
    def setupUi(self, FormEditor):
        FormEditor.setObjectName("FormEditor")
        FormEditor.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(FormEditor)
        self.gridLayout.setContentsMargins(0, 0, 0, 3)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label_status_length = QtWidgets.QLabel(FormEditor)
        self.label_status_length.setObjectName("label_status_length")
        self.gridLayout.addWidget(self.label_status_length, 1, 1, 1, 1)
        self.label_status_encoding = QtWidgets.QLabel(FormEditor)
        self.label_status_encoding.setObjectName("label_status_encoding")
        self.gridLayout.addWidget(self.label_status_encoding, 1, 5, 1, 1)
        self.label_status_sel = QtWidgets.QLabel(FormEditor)
        self.label_status_sel.setObjectName("label_status_sel")
        self.gridLayout.addWidget(self.label_status_sel, 1, 3, 1, 1)
        self.label_status_ln_col = QtWidgets.QLabel(FormEditor)
        self.label_status_ln_col.setObjectName("label_status_ln_col")
        self.gridLayout.addWidget(self.label_status_ln_col, 1, 2, 1, 1)
        self.label_status_eol = QtWidgets.QLabel(FormEditor)
        self.label_status_eol.setObjectName("label_status_eol")
        self.gridLayout.addWidget(self.label_status_eol, 1, 4, 1, 1)
        self.textEdit = PMGQsciWidget(FormEditor)
        self.textEdit.setToolTip("")
        self.textEdit.setWhatsThis("")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)
        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(FormEditor)
        QtCore.QMetaObject.connectSlotsByName(FormEditor)

    def retranslateUi(self, FormEditor):
        _translate = QtCore.QCoreApplication.translate
        FormEditor.setWindowTitle(_translate("FormEditor", "Form"))
        self.label_status_length.setText(_translate("FormEditor", "Length:{0}  Lines:{1}"))
        self.label_status_encoding.setText(_translate("FormEditor", "UTF-8"))
        self.label_status_sel.setText(_translate("FormEditor", "Sel:{0} | {1}"))
        self.label_status_ln_col.setText(_translate("FormEditor", "Ln:{0}  Col:{1}"))
        self.label_status_eol.setText(_translate("FormEditor", "Unix(LF)"))

from widgets import PMGQsciWidget
