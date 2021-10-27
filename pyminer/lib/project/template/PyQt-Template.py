# --coding:utf-8--
import sys
from PySide2.QtWidgets import QApplication, QDialog


class CallPyQtTemplate(object):
    def __init__(self):
        super(CallPyQtTemplate, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CallPyQtTemplate()
    form.show()
    sys.exit(app.exec())
