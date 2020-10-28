import logging

logger = logging.getLogger(__name__)

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface
from .webbrowser import PMWebBrowser
from typing import Dict


class Extension(BaseExtension):
    def on_load(self):
        self.current_browser_id = 0
        self.web_browsers: Dict[int, 'PMWebBrowser'] = {}
        logger.debug(self.settings)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.bind_html_file_shown)

    def bind_html_file_shown(self):
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.html', self.open_url)

    def new_id(self) -> int:
        if len(self.web_browsers.keys()) != 0:
            m = max(self.web_browsers.keys())
            return m + 1
        else:
            return 0

    def open_url(self, url='', browser_id: int = -1, side='right') -> int:
        """
        :param url:
        :param browser_id: int.默认为-1.当<0的时候，创建一个新的；当存在对应浏览器的时候就在对应浏览器打开；
        当不存在对应浏览器的时候，也是新建一个浏览器。
        :param side:str,为'left','right','top'和'bottom',默认为‘right’。
        :return: 浏览器对应的id。
        """
        if browser_id < 0:
            browser_id = self.new_id()
        web_browser = self.web_browsers.get(browser_id)

        if web_browser is None:
            self.data_viewer_cls = PMWebBrowser
            browser_name = "_temp_web_browser#%d" % browser_id
            web_browser: 'PMWebBrowser' = \
                self.extension_lib.insert_widget(self.data_viewer_cls,
                                                 'new_dock_window', {
                                                     "name": browser_name,
                                                     "side": side,
                                                     "text": "WebBrowser"})
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
        """
        当浏览器控件被删除的时候触发的函数。
        :param browser_id:
        :return:
        """
        logger.warning('browser id:%s is deleted!' % browser_id)
        self.web_browsers[browser_id] = None

    def insert_browser(self, browser: PMWebBrowser, side='right') -> 'PMWebBrowser':
        browser_id = self.new_id()
        browser_name = "_temp_web_browser#%d" % browser_id
        web_browser: 'PMWebBrowser' = \
            self.extension_lib.insert_widget(browser,
                                             'new_dock_window_obj', {
                                                 "name": browser_name,
                                                 "side": side,
                                                 "text": "WebBrowser"})
        web_browser.browser_name = browser_name
        web_browser.browser_id = browser_id
        web_browser.on_browser_deleted = self.on_web_browser_deleted

        self.web_browsers[browser_id] = web_browser
        return web_browser


class Interface(BaseInterface):

    def open_url(self, url: str, browser_id: int = -1, side: str = 'right') -> int:
        return self.extension.open_url(url, browser_id=browser_id, side=side)
