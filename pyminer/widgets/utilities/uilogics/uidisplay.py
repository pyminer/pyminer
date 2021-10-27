# -*- coding:utf-8 -*-
# @Time: 2021/3/29 10:55
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: uidisplay.py
from PySide2.QtCore import QObject, QCoreApplication


class TextDisplayUtil(QObject):
    @staticmethod
    def get_display_type(obj: object):
        """
        获取显示的类型
        :param obj:
        :return:
        """
        _translate = QCoreApplication.translate
        if type(obj) == type(True):
            return _translate("TextDisplayUtil", "bool")
        elif type(obj) == type(0):
            return _translate("TextDisplayUtil", "integer")
        elif type(obj) == type(""):
            return _translate("TextDisplayUtil", "integer")
        elif type(obj) == type(1.0):
            return _translate("TextDisplayUtil", "float")
        else:
            raise TypeError("Unrecognized type  for var %s" % (obj,))
