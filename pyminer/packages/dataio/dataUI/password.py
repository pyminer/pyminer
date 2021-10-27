import sys
import os
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets


class PasswordEdit(QtWidgets.QLineEdit):
    """
    Password LineEdit with icons to show/hide password entries.
    """

    def __init__(self, show_visibility=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_path=os.path.dirname(__file__)
        self.visibleIcon = QtGui.QIcon(os.path.join(current_path,"display.png"))
        self.hiddenIcon = QtGui.QIcon(os.path.join(current_path,"hide.png"))

        self.setEchoMode(QtWidgets.QLineEdit.Password)

        if show_visibility:
            # Add the password hide/shown toggle at the end of the edit box.
            self.togglepasswordAction = self.addAction(
                self.visibleIcon,
                QtWidgets.QLineEdit.TrailingPosition
            )
            self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)

        self.password_shown = False

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    psw=PasswordEdit()
    psw.show()
    sys.exit(app.exec_())


