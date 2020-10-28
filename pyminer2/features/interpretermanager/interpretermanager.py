"""
settings['interpreters'] =
{'base':{'name':'base',
         'info':'pypy3 python 3.6 compatible',
         'path':'/home/.../python3.8'}
}
"""


class Interpreter():
    def __init__(self, absolute_path: str, name: str):
        self.path = ''


class InterpreterManager():
    interpreter_paths = []

    def __init__(self):
        pass
