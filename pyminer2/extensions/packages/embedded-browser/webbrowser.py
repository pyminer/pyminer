from PyQt5.QtCore import pyqtSignal
from pmgwidgets import PMGWebBrowser, PMGWebEngineView
from pmgwidgets import PMDockObject


def createWindow(self, QWebEnginePage_WebWindowType):
    # new_webview = WebEngineView()
    new_window = PMWebBrowser()
    # new_window.setCentralWidget(new_webview)
    # new_window.show()
    self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
    self.signal_new_window_created.emit(new_window)
    return new_window.webview


PMGWebEngineView.createWindow = createWindow


class PMWebBrowser(PMGWebBrowser, PMDockObject):

    def __init__(self, parent=None, toolbar='standard'):
        super(PMWebBrowser, self).__init__(parent, toolbar)
        PMDockObject.__init__(self)
        self.on_closed_action = 'delete'
        self.browser_name = ''
        self.browser_id = -1

    def is_temporary(self):
        return True

    def on_browser_deleted(self, browser_id: int):
        """
        回调函数
        目的就是防止在子类中添加事件时加不进去。
        :param browser_id:
        :return:
        """
        pass

    def on_dock_widget_deleted(self) -> None:
        self.on_browser_deleted(self.browser_id)
        super(PMWebBrowser, self).deleteLater()
