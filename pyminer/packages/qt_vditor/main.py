# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 20:47
# @Author  : 别着急慢慢来
# @FileName: main.py
import logging
logger = logging.getLogger('qt_vditor')
from lib.extensions.extensionlib import BaseExtension, BaseInterface
from lib.localserver.server import server
from .route import qt_vditor

class Extension(BaseExtension):
    def on_load(self):
        server.register_blueprint(qt_vditor) # 注册蓝图
        logger.info('默认使用 qt vditor')


class Interface(BaseInterface):
    def hello(self):
        print("Hello")
