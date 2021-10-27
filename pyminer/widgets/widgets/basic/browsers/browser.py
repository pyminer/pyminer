"""
代码来源：
https://www.cnblogs.com/taostaryu/p/9772492.html

"""
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QLineEdit
from PySide2.QtCore import QUrl, Signal
from PySide2.QtWebEngineWidgets import QWebEngineView


class PMGWebBrowser(QWidget):
    def __init__(self, parent=None, toolbar='standard'):
        """

        :param parent:
        :param toolbar:多种选项：‘no’,‘standard’,'no_url_input','refresh_only'
        """
        super().__init__(parent)
        self.webview = PMGWebEngineView()
        self.setLayout(QVBoxLayout())
        self.toolbar = QToolBar()
        self.url_input = QLineEdit()
        self.toolbar.addWidget(self.url_input)
        self.toolbar.addAction('go').triggered.connect(lambda b: self.load_url())
        back_action = self.toolbar.addAction('back')
        back_action.triggered.connect(self.webview.back)

        forward_action = self.toolbar.addAction('forward')
        forward_action.triggered.connect(self.webview.forward)
        self.layout().addWidget(self.toolbar)
        if toolbar == 'no':
            self.toolbar.hide()
        elif toolbar == 'no_url_input':
            self.url_input.hide()
        elif toolbar == 'refresh_only':
            self.url_input.hide()
            back_action.setEnabled(False)
            forward_action.setEnabled(True)

        self.layout().addWidget(self.webview)
        self.setWindowTitle('My Browser')
        self.showMaximized()

        # command:>
        # jupyter notebook --port 5000 --no-browser --ip='*' --NotebookApp.token=''
        # --NotebookApp.password='' c:\users\12957\

        # self.webview.load(QUrl("http://127.0.0.1:5000/notebooks/desktop/Untitled.ipynb"))  # 直接请求页面。
        # self.webview.load(QUrl("E:\Python\pyminer_bin\PyMiner\bin\widgets\display\browser\show_formula.html"))  # 直接请求页面。
        # self.setCentralWidget(self.webview)

    def load_url(self, url: str = ''):
        if url == '':
            url = self.url_input.text().strip()
        else:
            self.url_input.setText(url)
        self.webview.load(QUrl(url))


class PMGWebEngineView(QWebEngineView):
    windowList = []
    signal_new_window_created = Signal(PMGWebBrowser)
    signal_load_url = Signal(str)

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_window = PMGWebBrowser()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        self.signal_new_window_created.emit(new_window)
        return new_window.webview

    def load(self, request: QUrl) -> None:
        print('load url', request, request.toString())
        self.signal_load_url.emit(request.toString())
        super(PMGWebEngineView, self).load(request)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = PMGWebBrowser()
    w.show()
    sys.exit(app.exec_())
