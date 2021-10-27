"""
ipython的颜色不是由qss决定的，而是由自身决定的。
它的样式在这个文件中定义。

Created on 2020/8/24
@author: Irony
@email: 892768447@qq.com
@file: console.py
@description: Console Widget
"""
import json
import logging
import os
import sys
from typing import Tuple, Dict, Callable

from PySide2.QtCore import QObject, Signal, QThread, QWaitCondition, QMutex, QPoint, QCoreApplication, QTranslator, \
    QLocale
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QMessageBox, QMenu, QApplication, QDialog
from qtconsole import styles
from qtconsole.manager import QtKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.styles import default_light_syntax_style, default_light_style_sheet

from lib.io import settings

default_dark_style_template = styles.default_template + """\
    .in-prompt { color: #ff00ff; }
    .out-prompt { color: #ff0000; }
"""
default_dark_style_sheet = default_dark_style_template % dict(
    bgcolor='#19232d', fgcolor='white', select="#ccc")
default_dark_syntax_style = 'monokai'  # 'default'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConsoleInitThread(QObject):
    initialized = Signal(object, object)

    def __init__(self, *args, **kwargs):
        super(ConsoleInitThread, self).__init__(*args, **kwargs)
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()

    def run(self):
        self.mutex.lock()
        kernel_manager = QtKernelManager(kernel_name="python3")
        logger.debug("installed kernel start method")

        # kernel_manager.kernel_spec.argv[0] = r"C:\Users\12957\AppData\Local\Programs\Python\Python38\python.exe"
        kernel_manager.kernel_spec.argv[0] = sys.executable
        # 这一步的目的是，指明要连接到的解释器。
        kernel_manager.start_kernel()

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        # notify to update ui
        self.initialized.emit(kernel_manager, kernel_client)

        # wait for exit
        self.wait_condition.wait(self.mutex)
        self.mutex.unlock()

        # stop channels and kernel
        kernel_client.stop_channels()
        kernel_manager.shutdown_kernel(now=True)  # add now=True; Fix exit error;  200924 liugang

    def stop(self):
        self.wait_condition.wakeAll()


class PMGIpythonConsole(RichJupyterWidget):

    def __init__(self, *args, **kwargs):
        super(PMGIpythonConsole, self).__init__(*args, **kwargs)
        self.is_first_execution = True
        self.confirm_restart = False

        self.history_path = os.path.join(settings.get_pyminer_data_path(), 'console_history.json')
        self.history = []
        self.commands_pool = []
        self.command_callback_pool: Dict[str, Callable] = {}

    def change_ui_theme(self, style: str):
        """
        改变界面主题颜色
        :param style:
        :return:
        """
        style = style.lower()
        if style == 'fusion':
            self.style_sheet = default_light_style_sheet
            self.syntax_style = default_light_syntax_style

        elif style == 'qdarkstyle':
            self.style_sheet = default_dark_style_sheet
            self.syntax_style = default_dark_syntax_style

        elif style.lower() == 'windowsvista':
            self.style_sheet = default_light_style_sheet
            self.syntax_style = default_light_syntax_style

        elif style.lower() == 'windows':
            self.style_sheet = default_light_style_sheet
            self.syntax_style = default_light_syntax_style

    def _handle_kernel_died(self, since_last_heartbit):
        self.is_first_execution = True
        self.restart_kernel(None, True)
        self.initialize_ipython_builtins()
        self.execute_command('')
        return True

    def _handle_execute_input(self, msg):
        super()._handle_execute_result(msg)

    def setup_ui(self):
        self.kernel_manager = None
        self.kernel_client = None
        # initialize by thread
        self.init_thread = QThread(self)
        self.console_object = ConsoleInitThread()
        self.console_object.moveToThread(self.init_thread)
        self.console_object.initialized.connect(self.slot_initialized)
        self.init_thread.finished.connect(self.console_object.deleteLater)
        self.init_thread.finished.connect(self.init_thread.deleteLater)
        self.init_thread.started.connect(self.console_object.run)
        self.init_thread.start()
        logger.debug("setup--ui")
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)

    def _context_menu_make(self, pos: 'QPoint') -> QMenu:
        menu = super(PMGIpythonConsole, self)._context_menu_make(pos)
        _translate = QCoreApplication.translate
        trans_dic = {'Cut': _translate("PMGIpythonConsole", 'Cut'), 'Copy': _translate("PMGIpythonConsole", 'Copy'),
                     'Copy (Raw Text)': _translate("PMGIpythonConsole", 'Copy(Raw Text)'),
                     'Paste': _translate("PMGIpythonConsole", 'Paste'),
                     'Select All': _translate("PMGIpythonConsole", 'Select All'),
                     'Save as HTML/XML': _translate("PMGIpythonConsole", 'Save as HTML/XML'),
                     'Print': _translate("PMGIpythonConsole", 'Print')
                     }
        for action in menu.actions():
            trans = trans_dic.get(action.text())
            trans = trans if trans is not None else action.text()
            action.setText(trans)
        history_action = menu.addAction(
            _translate("PMGIpythonConsole", 'History'))
        history_action.triggered.connect(self.show_history)

        restart_action = menu.addAction(
            _translate("PMGIpythonConsole", 'Restart'))
        restart_action.triggered.connect(self.slot_restart_kernel)

        stop_action = menu.addAction(
            _translate("PMGIpythonConsole", 'Interrupt'))
        # stop_action.triggered.connect(self.request_interrupt_kernel)
        stop_action.triggered.connect(self.on_interrupt_kernel)
        # stop_action.setEnabled(self._executing)

        return menu

    def show_history(self):
        """
        Public slot to show the shell history dialog.
        """
        from .ConsoleHistoryDialog import ConsoleHistoryDialog
        # import readline
        dlg = ConsoleHistoryDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.history = dlg.get_history()
            super()._set_history(self.history)

    def on_interrupt_kernel(self):
        """
        当点击中断执行时。
        IPython会出现一个奇怪的问题——当中断执行时，可能_executing恒为False。
        因此干脆不屏蔽了。
        Returns:

        """
        self.interrupt_kernel()

    def _custom_context_menu_requested(self, pos):
        super(PMGIpythonConsole, self)._custom_context_menu_requested(pos)

    def slot_restart_kernel(self, arg):
        ret = QMessageBox.warning(self, '提示', '是否要重启控制台？\n一切变量都将被重置。', QMessageBox.Ok | QMessageBox.Cancel,
                                  QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            self._restart_kernel(arg)

    def _restart_kernel(self, arg1):

        self.is_first_execution = True
        self.restart_kernel(None, True)
        self.initialize_ipython_builtins()
        self.execute_command('')
        return True

    def slot_initialized(self, kernel_manager, kernel_client):
        """
        Args:
            kernel_manager: `qtconsole.manager.QtKernelManager`
            kernel_client: `qtconsole.manager.QtKernelManager.client`

        Returns:
        """
        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client
        self.initialize_ipython_builtins()

    def initialize_ipython_builtins(self):
        return

    def _update_list(self):
        try:
            super(PMGIpythonConsole, self)._update_list()
        except BaseException:
            import traceback
            traceback.print_exc()

    def _banner_default(self):
        """
        自定义控制台开始的文字
        Returns:
        """
        return 'Welcome To widgets Ipython Console!\n'

    def closeEvent(self, event):
        self.history = self.history_tail(0)
        self.save_history()
        if self.init_thread.isRunning():
            self.console_object.stop()
            self.init_thread.quit()
            self.init_thread.wait(500)
        super(PMGIpythonConsole, self).closeEvent(event)

    def execute_file(self, file: str, hidden: bool = False):
        if not os.path.exists(file) or not file.endswith('.py'):
            raise FileNotFoundError(f'{file} not found or invalid')
        base = os.path.basename(file)
        cmd = os.path.splitext(base)[0]
        with open(file, 'r', encoding='utf-8') as f:
            source = f.read()

        self.execute_command(source, hidden=hidden, hint_text=cmd)

    def execute_command(self, source, hidden: bool = False, hint_text: str = '') -> str:
        """

        :param source:
        :param hidden:
        :param hint_text: 运行代码前显示的提示
        :return: str 执行命令的 msgid
        """
        self.hint_command(hint_text)
        if self.kernel_client is None:
            self.commands_pool.append((source, hidden, hint_text))
            return ''
        else:
            return self.pmexecute(source, hidden)

    def hint_command(self, hint_text: str = '') -> str:
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)
        # 运行文件时,显示文件名,无换行符,执行选中内容时,包含换行符
        # 检测换行符,在ipy console中显示执行脚本内容
        hint_row_list = hint_text.split("\n")
        for hint in hint_row_list:
            if hint != "":
                cursor.insertText('%s\n' % hint)
                self._insert_continuation_prompt(cursor)
        else:
            # 删除多余的continuation_prompt
            self.undo()

        # display input string buffer in console.
        self._finalize_input_request()
        cursor.movePosition(QTextCursor.End)

    def _handle_stream(self, msg):
        parent_header = msg.get('parent_header')
        if parent_header is not None:
            msg_id = parent_header.get('msg_id')  # 'fee0bee5-074c00d093b1455be6d166b1_10'']
            if msg_id in self.command_callback_pool.keys():
                callback = self.command_callback_pool.pop(msg_id)
                assert callable(callback)
                callback()
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)
        super()._handle_stream(msg)

    def append_stream(self, text):
        """重写的方法。原本before_prompt属性是False。"""
        self._append_plain_text(text, before_prompt=False)

    def pmexecute(self, source: str, hidden: bool = False) -> str:
        """
        执行代码并且返回Msgid
        :param source:
        :param hidden:
        :return:
        """
        is_legal, msg = self.is_source_code_legal(source)
        if not is_legal:
            QMessageBox.warning(self, '警告', msg)
            source = ''
        msg_id = self.kernel_client.execute(source, hidden)
        self._request_info['execute'][msg_id] = self._ExecutionRequest(msg_id, 'user')
        self._hidden = hidden
        if not hidden:
            self.executing.emit(source)
        return msg_id

    def is_source_code_legal(self, source_code: str) -> Tuple[bool, str]:
        """判断注入到shell中的命令是否合法。

        如果命令不合法，应当避免执行该命令。

        Args:
            source_code: 注入到shell中的命令。

        Returns:
            * 是否合法；
            * 如不合法，返回原因；如合法，返回空字符串。

        """
        return True, ''

    @staticmethod
    def install_translator():
        global _trans
        app = QApplication.instance()
        assert app is not None
        _trans = QTranslator()
        _trans.load(QLocale.system(), 'qt_zh_CN.qm',
                    directory=os.path.join(os.path.dirname(__file__), 'translations'))
        app.installTranslator(_trans)

    def _set_history(self, history):
        """ 重写的方法。重新管理历史记录。
        """
        self.load_history()
        super()._set_history(self.history)

    def load_history(self):
        if os.path.exists(self.history_path):
            with open(self.history_path) as f:
                history = json.load(f)
                self.history = history['history']

    def save_history(self):
        history = {'history': self.history}
        with open(self.history_path, 'w') as f:
            json.dump(history, f)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    app = QApplication([])
    # os.environ['IPYTHON_AS_PYMINER_NODE'] = '1'
    PMGIpythonConsole.install_translator()
    w = PMGIpythonConsole()
    w.show()
    w.setup_ui()
    sys.exit(app.exec_())
