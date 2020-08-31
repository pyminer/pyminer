from extensionlib import SubWindow

class MySubWindow1(SubWindow):
    def test(self):
        super().test()
        print('this is subwindow 1')

class MySubWindow2(SubWindow):
    def test(self):
        super().test()
        print('this is subwindow 2')