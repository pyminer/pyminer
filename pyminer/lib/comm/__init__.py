# -*- coding:utf-8 -*-
# @Time: 2021/1/26 10:17
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: __init__.py.py
import logging

from .data_client import *
from .pyminer_client import *

logging.basicConfig(
    format="%(asctime)-15s %(name)-40s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
