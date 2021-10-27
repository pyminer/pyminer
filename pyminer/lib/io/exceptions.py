# -*- coding:utf-8 -*-
# @Time: 2021/1/27 10:22
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: exceptions.py

from PySide2.QtCore import QObject, Signal, QCoreApplication


class PyMinerException(BaseException):
    def __init__(self, error: BaseException, solution: str, solution_command: str = ''):
        self.error = error
        self.solution = solution
        self.solution_command = solution_command

    def to_markdown(self):
        return QCoreApplication.translate('PyMinerException',
                                          """
# {error}
## Solutions:
{solution}
        """.format(error=self.error, solution=self.solution))


class PMExceptions(QObject):
    """
    单例！
    """
    signal_exception_occured = Signal(BaseException)

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self):
        super(PMExceptions, self).__init__()

    @staticmethod
    def get_instance() -> 'PMExceptions':
        return PMExceptions.instance

    def emit_exception_occured_signal(self, error: BaseException, solution: str, solution_command: str):
        self.signal_exception_occured.emit(PyMinerException(error, solution, solution_command))


pyminer_exc_mgr = PMExceptions()
