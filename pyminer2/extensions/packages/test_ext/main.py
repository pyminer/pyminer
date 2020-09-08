from PyQt5.QtWidgets import QTextEdit


class Extension:
    def on_load(self):
        print("被加载!")

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class Interface:
    def __init__(self):
        self.ui_inserters = {
            'test_inserter': self.insert_to_test
        }
    
    def insert_to_test(self, widget_class: 'QWidget', config=None):
        pass


class WidgetTest(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setup_ui(self):
        self.setText('这是一个测试用插件，这个插件被插入到工具栏中。')
