import logging
import os
import types
from typing import Optional

import pyminer_algorithms
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface
from pyminer2.extensions.packages.document_server.docserver import Server

logger = logging.getLogger(__name__)


class Extension(BaseExtension):
    server = Server(os.path.dirname(pyminer_algorithms.__file__))

    def on_load(self):
        logger.info(f'帮助文档服务器：http://127.0.0.1:{self.server.port}')
        self.server.run()


class Interface(BaseInterface):
    def __init__(self):
        self.browser_id: Optional[int] = None
        # 记忆上次打开的浏览器id，这样可以保证下次打开帮助文档的时候和上次打开的是同一个内置浏览器，从而节省内存+方便交互。

    def open_by_function_name(self, name: str):
        """
        对于`pyminer_algorithms`内的函数，按函数名打开文档
        :param name: 需要打开的`algorithms`内的函数
        :return:
        """
        import pyminer_algorithms
        attr_list = dir(pyminer_algorithms)
        if name in attr_list:
            func = getattr(pyminer_algorithms, name)
            self.open_by_function_object(func)

    def open_external_search_result(self, word_to_search: str):
        """
        打开外部搜索链接
        :param word_to_search:
        :return:
        """
        path = 'https://cn.bing.com/search?q=%s' % word_to_search
        if self.browser_id is None:
            self.browser_id = self.extension.extension_lib.get_interface('embedded-browser').open_url(url=path,
                                                                                                      side='right')
        else:
            self.browser_id = self.extension.extension_lib.get_interface('embedded-browser').open_url(
                url=path, browser_id=self.browser_id, side='right')

    def open_by_function_object(self, function: types.FunctionType):
        """
        传入一个函数，就可以在浏览器中打开帮助文档。
        :param function: 这是一个函数，是Callable的函数，不是函数名
        :return:
        """

        # 关于path的处理说明：将模块路径转换为文件路径
        # >>> array.__module__
        # 'pyminer_algorithms.linear_algebra.array'
        # >>> array.__module__.split('.', maxsplit=1)[1]
        # 'linear_algebra.array'
        # >>> array.__module__.split('.', maxsplit=1)[1].replace('.', '/')
        # 'linear_algebra/array'

        path = function.__module__.split('.', maxsplit=1)[1]
        path = path.replace('.', '/')
        path = f'{path}.md'

        # 以下这4行代码看起来似乎是没用的
        if path.startswith('/'):
            path = path[1:]
        if path.startswith('\\'):
            path = path[1:]

        # 在内置浏览器中打开帮助文档
        port = Extension.server.port
        path = f'http://127.0.0.1:{port}/{path}'
        embedded_browser = self.extension.extension_lib.get_interface('embedded-browser')
        if self.browser_id is None:
            self.browser_id = embedded_browser.open_url(url=path, side='right')
        else:
            self.browser_id = embedded_browser.open_url(url=path, browser_id=self.browser_id, side='right')
