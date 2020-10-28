"""
作者：@吴宫幽径
说明：
dialog无需写在json里面，直接调用主界面的控件就可以了。
"""

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QToolButton, QTextEdit, QSizePolicy

from communication import Client

class DemoToolDialog(QDialog):
    def __init__(self, parent, button_text: list):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.append('请先点击左侧按钮,向工作空间注入数据\'mat=[[1,2,3],[3,2,1]]\',然后点击右侧按钮获取变量空间中的mat值。'
                              '\n这条命令将以用户不可见的形式执行。\n')
        layout.addWidget(self.text_edit)
        b = QToolButton(self)
        b.setText(button_text[0])
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        b.clicked.connect(self.inject_var_to_workspace)
        layout.addWidget(b)
        b = QToolButton(self)
        b.setText(button_text[1])
        b.clicked.connect(self.get_data)
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(b)
        self.setLayout(layout)

    def inject_var_to_workspace(self):
        c = Client()
        c.write('mat', {'type': 'Matrix', 'value': [[1, 2, 3], [3, 2, 1]]}, 'user')
        self.text_edit.append('命令已执行，请查看工作空间。\n')

    def get_data(self):
        c = Client()

        try:
            mat = c.read('mat')
        except BaseException:
            self.text_edit.append('mat变量不存在，请先点击左侧按钮对mat赋值。\n')
            return
        self.text_edit.append('成功获取变量‘mat’，值为' + repr(mat) + '\n你可以在控制台中运行命令改变mat的值，'
                                                           '并且再次点击右侧按钮获取它，查看有无变化。\n')


if __name__ == '__main__':
    """
    这个测试只是用于调试界面，不能点击按钮
    """
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    form = DemoToolDialog(None, ['注入变量\'mat\'', '读取变量\'mat\''])
    form.show()
    sys.exit(app.exec_())
