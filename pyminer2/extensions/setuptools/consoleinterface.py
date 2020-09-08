class ConsoleInterface(BaseInterface):

    def run_command(self, command, hint_text=''):
        """run command
        """
        pass

    def run_file(self, file):
        pass

    def test_func(self, a, b=1, *c, **d):
        pass

    def test_func1(self, a, b=1, **d):
        pass

    def test_func2(self, a, b=1, *c):
        pass

