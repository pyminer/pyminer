"""
作者：@吴宫幽径
说明：
dialog无需写在json里面，直接调用主界面的控件就可以了。
"""

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton, QToolButton, QTextEdit, QSizePolicy
from pyminer2.extensions.extensionlib import BaseExtension,BaseInterface


class Extension(BaseExtension):
    def on_load(self):
        self.demo_tool_button = self.widgets['DemoToolButton']
        self.demo_tool_button.main = self
        print("对话框示例被加载")

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class Interface(BaseInterface):
    def hello(self):
        print("Hello,来自对话框示例")


class DemoToolButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('显示\n插件示例\n的对话框')
        self.clicked.connect(self.show_dialog)

    def show_dialog(self):
        """
        显示一个插件示例所弹出的对话框。
        """
        self.main.demo_tool_dialog = DemoToolDialog(self, ['执行python命令\'x=123\'', '获取数据x值\n', ])
        self.main.demo_tool_dialog.main = self.main
        self.main.demo_tool_dialog.show()


class DemoToolDialog(QDialog):
    def __init__(self, parent, button_text: list):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.append('请先点击左侧按钮运行命令\'x=123\',然后点击右侧按钮获取变量空间中的x值。'
                              '\n这条命令将以用户不可见的形式执行。\n')
        layout.addWidget(self.text_edit)
        b = QToolButton(self)
        b.setText(button_text[0])
        b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        b.clicked.connect(self.run_shell_command)
        layout.addWidget(b)
        b = QToolButton(self)
        b.setText(button_text[1])
        b.clicked.connect(self.get_data)
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(b)
        self.setLayout(layout)

    def run_shell_command(self):
        console = self.main.extension_lib.get_interface('ipython_console')
        if console is None:
            raise Exception('dependency ipython console not found')
        console.run_command(command='x=123',hint_text='执行命令')
        self.text_edit.append('命令已执行，请查看工作空间。\n')
        self.main.extension_lib.UI.raise_dock_into_view('ipython_console')#调用命令，将控制台提升到窗口最上方。

    def get_data(self):
        try:
            var = self.main.extension_lib.get_var('x')
        except:
            self.text_edit.append('x变量不存在，请先点击左侧按钮对x赋值。\n')
            return
        self.text_edit.append('成功获取变量‘x’，值为' + repr(var) + '\n你可以在控制台中运行命令改变x的值，'
                                                           '并且再次点击右侧按钮获取它，查看有无变化。\n')


if __name__ == '__main__':
    '''
    这个测试只是用于调试界面，不能点击按钮
    '''
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    form = DemoToolDialog(None,['aaa','dddddd'])
    form.show()
    sys.exit(app.exec_())