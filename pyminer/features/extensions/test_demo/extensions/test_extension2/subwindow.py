from extensionlib import SubWindow

class YourSubWindow1(SubWindow):
    def test(self):
        super().test()
        print('this is subwindow 1')

class YourSubWindow2(SubWindow):
    def test(self):
        super().test()
        print('this is subwindow 2')