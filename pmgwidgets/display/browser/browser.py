"""
代码来源：
https://www.cnblogs.com/taostaryu/p/9772492.html

"""
import sys

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QToolBar, QLineEdit


class PMGWebBrowser(QWidget):
    def __init__(self, parent=None, toolbar='standard'):
        """

        :param parent:
        :param toolbar:多种选项：‘no’,‘standard’,'no_url_input'
        """
        super().__init__(parent)
        self.webview = PMGWebEngineView()
        # self.webview.load(QUrl("https://cn.bing.com"))
        self.setLayout(QVBoxLayout())
        self.toolbar = QToolBar()
        self.url_input = QLineEdit()
        # self.url_input.setText('https://cn.bing.com')
        # self.load_url()
        self.toolbar.addWidget(self.url_input)
        self.toolbar.addAction('go').triggered.connect(lambda b: self.load_url())
        self.toolbar.addAction('back').triggered.connect(self.webview.back)
        self.toolbar.addAction('forward').triggered.connect(self.webview.forward)
        self.layout().addWidget(self.toolbar)
        if toolbar == 'no':
            self.toolbar.hide()
        elif toolbar == 'no_url_input':
            self.url_input.hide()

        self.layout().addWidget(self.webview)
        self.setWindowTitle('My Browser')
        self.showMaximized()

        # command:>
        # jupyter notebook --port 5000 --no-browser --ip='*' --NotebookApp.token=''
        # --NotebookApp.password='' c:\users\12957\

        # self.webview.load(QUrl("http://127.0.0.1:5000/notebooks/desktop/Untitled.ipynb"))  # 直接请求页面。
        # self.webview.load(QUrl("E:\Python\pyminer_bin\PyMiner\bin\pmgwidgets\display\browser\show_formula.html"))  # 直接请求页面。
        # self.setCentralWidget(self.webview)

    def load_url(self, url: str = ''):
        if url == '':
            url = self.url_input.text().strip()
        # print('',url)
        else:
            self.url_input.setText(url)
        self.webview.load(QUrl(url))


class PMGWebEngineView(QWebEngineView):
    windowList = []
    signal_new_window_created = pyqtSignal(PMGWebBrowser)

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        # new_webview = WebEngineView()
        new_window = PMGWebBrowser()
        # new_window.setCentralWidget(new_webview)
        # new_window.show()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        self.signal_new_window_created.emit(new_window)
        return new_window.webview


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = PMGWebBrowser()
    w.show()
    sys.exit(app.exec_())
