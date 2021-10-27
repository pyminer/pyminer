# --coding:utf-8--
"""
Please make sure the content of the file is complete.
If you customize the template, please make sure it can be executed correctly
by the interpreter after modification.
Do not delete the file and the directory where the file is located.
请确保文件内容完整。
若自定义模板，请在修改后确保能够被解释器正确执行。
【请勿删除】该文件以及文件所在目录。
"""
import sys
from PySide2.QtWidgets import QApplication, QDialog
from PySide2_Template import Ui_PySide2Template


class CallPySideTemplate(QDialog, Ui_PySide2Template):
    def __init__(self):
        super(CallPySideTemplate, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CallPySideTemplate()
    form.show()
    sys.exit(app.exec_())
