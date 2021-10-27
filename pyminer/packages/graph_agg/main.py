# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 20:47
# @Author  : 别着急慢慢来
# @FileName: main.py
# from packages.ipython_console.main import ConsoleInterface
# from features.extensions.extensionlib import extension_lib
import os
import logging
logger = logging.getLogger('graph_agg')
from features.extensions.extensionlib import BaseExtension, BaseInterface

class Extension(BaseExtension):
    def on_load(self):
        console = self.extension_lib.get_interface('ipython_console')
        if console is None:
            raise Exception('console not found')
        logger.info('默认使用 graph agg')
        self.extension_lib.Signal.get_events_ready_signal().connect(
            lambda: self.extension_lib.UI.raise_dock_into_view('ipython_console'))


class Interface(BaseInterface):
    def hello(self):
        print("Hello")
