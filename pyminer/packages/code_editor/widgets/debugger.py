import sys

# 导入Qt 相关模块
from PySide2.QtCore import Signal
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QTabWidget, QMessageBox

from widgets import PMDockObject
from lib.ui.common.debug_process_with_pyqt import PMGDebugConsoleWidget

class PMDebugConsoleTabWidget(QTabWidget, PMDockObject):
    signal_goto_file = Signal(str, int)
    extension_lib = None

    def __init__(self, parent=None):
        super(PMDebugConsoleTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.slot_tab_close_request)

    def get_widget_text(self) -> str:
        return self.tr('Debugger')

    def new_debug(self, text, file, editor_tab_widget):
        """
        create a new debug process.
        """
        args = [sys.executable, '-u', '-m', 'pdb', file]
        self.create_process(text,
                            args,
                            auto_run=True, editor_tab_widget=editor_tab_widget)

    def create_process(self, text: str, args: list, auto_run=True, editor_tab_widget=None):
        """
        创建一个新的进程
        :param text:
        :param args:
        :param auto_run:
        :param editor_tab_widget:
        :return:
        """
        assert editor_tab_widget is not None, 'editor is None!'
        w = PMGDebugConsoleWidget(args, editor_tab_widget=editor_tab_widget)
        w.set_extension_lib(self.extension_lib)
        if auto_run:
            w.start_process()
        w.process_console.signal_goto_file.connect(lambda path, row: self.signal_goto_file.emit(path, row))
        self.addTab(w, text)
        self.setCurrentIndex(self.indexOf(w))

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
        widget: 'PMGDebugConsoleWidget' = self.widget(index)
        if not widget:
            return
        if widget.is_process_running():
            if self.slot_about_close() == QMessageBox.Ok:
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

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        for i in range(self.count()):
            self.widget(i).closeEvent(a0)
        super(PMDebugConsoleTabWidget, self).closeEvent(a0)
