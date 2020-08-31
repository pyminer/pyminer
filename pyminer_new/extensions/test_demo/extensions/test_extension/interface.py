class MyInterface:
    def _link_(self, entry):
        self.entry = entry

    def method(self):
        print(f'interface of {self.entry}')