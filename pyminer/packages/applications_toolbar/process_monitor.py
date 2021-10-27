import os

from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QTabWidget, QMessageBox

from widgets import PMDockObject, create_icon
from widgets import PMGProcessConsoleWidget, PMGInstantBootConsoleWidget



class PMProcessConsoleTabWidget(QTabWidget, PMDockObject):
    def __init__(self, parent=None):
        self.extension_lib = None
        super(PMProcessConsoleTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.slot_tab_close_request)

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib

    def get_widget_text(self) -> str:
        return self.tr('Run')

    def create_process(self, text: str, args: list, auto_run=True):
        w = PMGProcessConsoleWidget(args)
        w.signal_goto_file.connect(self.goto_file)
        if auto_run:
            w.start_process()
        self.addTab(w, text)

    def goto_file(self, path, row):
        """
        跳转到文件
        Args:
            path:
            row:

        Returns:

        """
        self.extension_lib.get_interface('code_editor').goto_file(path, row)

    def bind_close_events(self, extension_lib):
        extension_lib.Signals.get_main_window_close_signal().connect(self.closeEvent)

    def slot_tab_close_request(self, index: int):
        """
        关闭标签页
        要求：当标签页上的程序运行时，不应直接关闭，而应该弹出对话框，让用户确认是否终止后台进程。
        :param index: 标签当前索引
        :type index: int
        :return:
        """
        widget: 'PMGProcessConsoleWidget' = self.widget(index)
        if not widget:
            return
        if widget.is_process_running():
            if self.slot_about_close() == QMessageBox.Ok:
                widget.process_console.signal_process_stopped.disconnect(widget.on_terminated)
                widget.terminate_process()
            else:
                return
        self.removeTab(index)
        widget.close()
        widget.deleteLater()

    def slot_about_close(self) -> QMessageBox.StandardButton:
        """
        是否需要终止全部进程并且关闭
        :return:QMessageBox.StandardButton
        """
        buttons = QMessageBox.Ok | QMessageBox.Cancel

        ret = QMessageBox.question(self, self.tr('Terminate'),
                                   self.tr('Process is running, Would you like to terminate this process?'), buttons,
                                   QMessageBox.Ok)
        return ret

    def create_instant_boot_process(self, file_name: str, interpreter_path: str = '', text='', auto_run=''):
        """
        创建快速启动进程
        Args:
            file_name:
            interpreter_path:
            text:
            auto_run:

        Returns:

        """
        if text == '':
            text = os.path.basename(file_name)
        w = PMGInstantBootConsoleWidget(file_name)
        if auto_run:
            w.start_process()

        self.addTab(w, create_icon(os.path.join(os.path.dirname(__file__), 'source', 'lightening.png')), text)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        for i in range(self.count()):
            self.widget(i).closeEvent(a0)
        super(PMProcessConsoleTabWidget, self).closeEvent(a0)
