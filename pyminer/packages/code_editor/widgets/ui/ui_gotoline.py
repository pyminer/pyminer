# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gotoline.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_DialogGoto(object):
    def setupUi(self, DialogGoto):
        DialogGoto.setObjectName("DialogGoto")
        DialogGoto.resize(300, 94)
        self.gridLayout = QtWidgets.QGridLayout(DialogGoto)
        self.gridLayout.setContentsMargins(-1, 18, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(DialogGoto)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(DialogGoto)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogGoto)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(DialogGoto)
        self.buttonBox.rejected.connect(DialogGoto.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogGoto)

    def retranslateUi(self, DialogGoto):
        _translate = QtCore.QCoreApplication.translate
        DialogGoto.setWindowTitle(_translate("DialogGoto", "Go to Line/Column"))
        self.label.setText(_translate("DialogGoto", "[Line] [:column]:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogGoto = QtWidgets.QDialog()
    ui = Ui_DialogGoto()
    ui.setupUi(DialogGoto)
    DialogGoto.show()
    sys.exit(app.exec_())