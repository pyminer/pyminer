import logging
from typing import Dict

from PySide2.QtCore import QCoreApplication
from lib.extensions.extensionlib import BaseExtension, BaseInterface
from .webbrowser import PMWebBrowser

logger = logging.getLogger(__name__)


class Extension(BaseExtension):
    current_browser_id: int
    web_browsers: Dict[int, PMWebBrowser]
    data_viewer_cls: PMWebBrowser

    def __init__(self):
        self._last_inserted_side = ''

    def on_load(self):
        self.current_browser_id = 0
        self.web_browsers = {}
        logger.debug(self.settings)
        # self.extension_lib.Signal.get_events_ready_signal().connect(self.bind_html_file_shown)



    def new_id(self) -> int:
        if len(self.web_browsers.keys()) != 0:
            m = max(self.web_browsers.keys())
            return m + 1
        else:
            return 0

    def open_url(self, url='', browser_id: int = -1, side='right', toolbar='standard', text="WebBrowser") -> int:
        """根据URL在内置浏览器中打开页面。

        通过 ``browser_id`` 指定需要打开的浏览器：

        #. 如果编号为负（默认情况），则创建一个新浏览器；
        #. 如果存在相应的编号，则在相应的浏览器中打开该页面；
        #. 如果不存在相应的编号，则创建一个新浏览器。

        Args:
            url: 页面路径。
            browser_id: 浏览器的编号；
            side: ``left`` , ``right`` , ``top`` , ``bottom`` 中的一个。
            toolbar:`standard`,`no`,`no_url_input`中的一个。
        Returns:
            所使用的浏览器的编号。
        """
        print("text", text)
        if browser_id < 0:
            browser_id = self.new_id()
        web_browser = self.web_browsers.get(browser_id)
        self._last_inserted_side = side
        print("browser", web_browser)
        if web_browser is None:
            class _Browser(PMWebBrowser):
                def get_widget_text(self) -> str:
                    return text
            self.data_viewer_cls = _Browser
            browser_name = "_temp_web_browser#%d" % browser_id
            web_browser: 'PMWebBrowser' = self.extension_lib.insert_widget(
                self.data_viewer_cls, 'new_dock_window', {
                    "name": browser_name,
                    "side": side})
            web_browser.browser_name = browser_name
            web_browser.browser_id = browser_id
            web_browser.webview.signal_new_window_created.connect(self.insert_browser)
            web_browser.on_browser_deleted = self.on_web_browser_deleted
            self.web_browsers[browser_id] = web_browser
        web_browser.load_url(url)
        if not web_browser.isVisible():
            dock = web_browser.parent()
            dock.setVisible(True)
        self.extension_lib.UI.raise_dock_into_view(web_browser.browser_name)
        return browser_id

    def on_web_browser_deleted(self, browser_id: int):
        """浏览嚣控件被删除时所触发的回调函数。

        Args:
            browser_id: 浏览器的编号。
        """
        logger.warning('browser id:%s is deleted!' % browser_id)
        self.web_browsers[browser_id] = None

    def insert_browser(self, browser: PMWebBrowser, side='', text: str = "") -> 'PMWebBrowser':
        """
        调用extension_lib，在窗口中插入新的浏览器。

        Args:
            browser:
            side:
            text:

        Returns:

        """
        if text == "":
            text = QCoreApplication.translate("Webbrowser_Extension", text)
        if side == '':
            side = self._last_inserted_side if self._last_inserted_side != '' else 'right'
        self._last_inserted_side = side
        browser_id = self.new_id()
        browser_name = "_temp_web_browser#%d" % browser_id
        web_browser: 'PMWebBrowser' = \
            self.extension_lib.insert_widget(browser,
                                             'new_dock_window_obj', {
                                                 "name": browser_name,
                                                 "side": side,
                                                 "text": text})
        web_browser.browser_name = browser_name
        web_browser.browser_id = browser_id
        web_browser.on_browser_deleted = self.on_web_browser_deleted

        self.web_browsers[browser_id] = web_browser
        return web_browser


class Interface(BaseInterface):
    extension: Extension = None

    def open_url(self, url: str, browser_id: int = -1, side: str = 'right', toolbar='standard',
                 text: str = "WebBrowser") -> int:
        return self.extension.open_url(url, browser_id=browser_id, side=side, toolbar=toolbar, text=text)
