from PyQt5.QtGui import QCloseEvent
from pmgwidgets import PMDockObject

from pyminer2.ui.common.open_process_with_pyqt import PMGProcessConsoleWidget
from PyQt5.QtWidgets import QTabWidget, QMessageBox


class PMProcessConsoleTabWidget(QTabWidget, PMDockObject):
    def __init__(self, parent=None):
        super(PMProcessConsoleTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.slot_tab_close_request)

    def create_process(self, text: str, args: list, auto_run=True):
        w = PMGProcessConsoleWidget(args)
        if auto_run:
            w.start_process()
        self.addTab(w, text)

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
        super(PMProcessConsoleTabWidget, self).closeEvent(a0)
