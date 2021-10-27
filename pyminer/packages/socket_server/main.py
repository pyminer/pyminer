import inspect
import logging
from typing import Callable

import flask.cli
from flask import Flask

from lib.extensions.extensionlib import BaseExtension, BaseInterface
from .server_by_socket import run, app

# 不显示flask的启动日志
flask.cli.show_server_banner = lambda *_, **__: None
logger = logging.getLogger(__name__)


class Extension(BaseExtension):
    def on_load(self):
        run(self.extension_lib)
        self.interface.app = app
        self.interface.extension_lib = self.extension_lib
        logger.debug(self.settings)


class Interface(BaseInterface):
    extension_lib = None
    app: Flask

    def add_handler(self, rule, callback: Callable[[], str]):
        """
        rule:比如‘/’

        :param rule:
        :param callback:
        :return:
        """
        if not isinstance(rule, str):
            raise TypeError(
                'Rule argument should be str,but your argument was %s, type %s' % (repr(rule), str(type(rule))))
        if not len(list(inspect.signature(callback).parameters.keys())) == 0:
            raise ValueError('Callback function should not have any arguments!')
        try:
            self.app.add_url_rule(rule, callback.__name__, callback)
        except AssertionError as e:
            if "overwriting an existing endpoint function" in repr(e):
                logger.error(f'Problem happened when trying register function {callback} with rule {rule}')
            raise e
            # self.extension_lib.Program.show_exception_occured_panel(e, solution='')
