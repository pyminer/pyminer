class BaseInterface:
    pass

class ConsoleInterface(BaseInterface):
    def __init__(self):
        widget: 'ConsoleWidget' = None

    def run_command(self, command: str, hint_text=''):
        '''run command
        '''
        if self.widget is not None:
            self.widget.execute_command(command, True, hint_text=hint_text)

    def run_file(self, file: str):
        if self.widget is not None:
            self.widget.execute_file(file, True)

    def test_func(self, a, b=1, *c, **d):
        pass

    def test_func1(self, a, b=1, **d):
        pass

    def test_func2(self, a, b=1, *c):
        pass