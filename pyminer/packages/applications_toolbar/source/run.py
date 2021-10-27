import os
import sys
from PySide2.QtWidgets import QWidget, QApplication


class MyMainForm(QWidget):
    """
    docstring
    """

    def __init__(self):
        super(MyMainForm, self).__init__()
        # 在这里完善你的应用


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
