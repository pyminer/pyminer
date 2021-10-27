"""
ipython的颜色不是由qss决定的，而是由自身决定的。
qss在这个文件中定义。

Created on 2020/8/24
@author: Irony
@email: 892768447@qq.com
@file: consolewidget
@description: Console Widget
"""
import os
from typing import Tuple
from widgets import PMDockObject, in_unit_test
from widgets.widgets.basic.others.console import PMGIpythonConsole
from PySide2.QtWidgets import QApplication

if QApplication.instance() is not None:
    PMGIpythonConsole.install_translator()

class ConsoleWidget(PMGIpythonConsole, PMDockObject):
    def __init__(self, *args, **kwargs):
        super(ConsoleWidget, self).__init__(*args, **kwargs)
        self.is_in_ui_start = True
        self.is_first_execution = True
        self.confirm_restart = False

    def get_widget_text(self) -> str:
        return self.tr('IPython Console')

    def _handle_kernel_died(self, since_last_heartbit):
        self.is_first_execution = True
        self.restart_kernel(None, True)
        self.initialize_ipython_builtins()
        self.execute_command('')
        return True

    def setup_ui(self):
        super().setup_ui()
        if not in_unit_test():
            style = self.lib.Program.get_theme()
            self.change_ui_theme(style)

    def connect_to_datamanager(self, data_manager):
        """绑定工作空间。

        Args:
            data_manager: 工作空间。
        """
        self.data_manager = data_manager
        self.lib = self.data_manager

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib

    def initialize_ipython_builtins(self):
        if in_unit_test():
            pwd = os.path.dirname(__file__)
        else:
            pwd = self.extension_lib.Program.get_work_dir()
        pwd = pwd.replace('\\', '\\\\')
        from utils import get_root_dir
        cmd = 'import sys;sys.path.append(r\'%s\')' % get_root_dir()
        self.execute_command(cmd, True, '')
        cdcmd = 'import os;os.chdir(\'%s\')' % pwd  # 启动时切换到当前工作路径。
        self.execute_command(cdcmd, True, '')
        ini_py = os.path.join(os.path.dirname(__file__), 'initialize.py')
        self.execute_file(ini_py, hidden=True)
        for source, hidden, hint_text in self.commands_pool:
            self.execute_command(source, hidden, hint_text)
        if not self.is_in_ui_start:  # 如果不是初次启动而是重启，那么就需要清空已有的内容。
            msgid = self.execute_command('print(\'Welcome To PyMiner!\')', True, 'Welcome To PyMiner!\n')
            self.command_callback_pool[msgid] = lambda: self.clear()
            self.clear(False)
        else:
            self.is_in_ui_start = False

    def _update_list(self):
        try:
            super(ConsoleWidget, self)._update_list()
        except BaseException:
            import traceback
            traceback.print_exc()

    def _handle_complete_reply(self, msg):
        """重写，加上trycatch，直接禁用了没有其他的变化，故不做类型标注。"""
        try:
            super()._handle_complete_reply(msg)
        except BaseException:
            import traceback
            traceback.print_exc()

    def _banner_default(self):
        """自定义控制台开始时的文字。"""
        return 'Welcome To PyMiner!\n'

    def is_source_code_legal(self, source_code: str) -> Tuple[bool, str]:
        """判断注入到控制台中的命令是否合法。

        Args:
            source_code: 注入到控制台中的命令。

        Returns:
            * 命令是否合法
            * 如不合法，返回其不合法的原因，如合法则为空字符串。
        """
        msg_ipython_not_support = 'IPython不支持运行%s的程序,请在终端中执行。'
        s = source_code.strip()
        if s != '' and s in ('%reset', 'reset'):
            return False, '命令含有reset,暂不支持在IPython中运行。'
        elif s.find('sys.exit') != -1:
            return False, msg_ipython_not_support % '含有解释器退出语句(如sys.exit)'
        elif s.find('QApplication') != -1 or s.find('tkinter') != -1:
            return False, msg_ipython_not_support % '含有图形界面'
        return super(ConsoleWidget, self).is_source_code_legal(source_code)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PySide2.QtWidgets import QApplication, QMainWindow

    app = QApplication([])
    PMGIpythonConsole.install_translator()
    mw = QMainWindow()

    w = ConsoleWidget()
    mw.setCentralWidget(w)
    mw.show()
    w.execute_command('import numpy;print(numpy)', hidden=True)
    w.setup_ui()
    print(w.font)

    sys.exit(app.exec_())
