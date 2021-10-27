from widgets import PMDockObject
from widgets import PMGWebBrowser, PMGWebEngineView


def createWindow(self:PMGWebEngineView, QWebEnginePage_WebWindowType) -> PMGWebEngineView:
    new_window = PMWebBrowser()
    self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
    self.signal_new_window_created.emit(new_window)
    new_window.webview.loadStarted.connect(lambda :new_window.webview.signal_load_url.emit(new_window.webview.url().toString()))
    new_window.webview.signal_load_url.connect(lambda x: print('url is!', x))
    new_window.webview.signal_load_url.connect(lambda text: new_window.url_input.setText(text))
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
        """回调函数，用于子类添加事件。

        Args:
            browser_id: 浏览器编号。
        """
        pass

    def on_dock_widget_deleted(self) -> None:
        self.on_browser_deleted(self.browser_id)
        super(PMWebBrowser, self).deleteLater()

    def get_widget_text(self) -> str:
        return self.tr('Browser')
