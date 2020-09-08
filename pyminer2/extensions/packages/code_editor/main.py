from .editor import PMCodeEditTabWidget
from .toolbar import PMEditorToolbar
from pyminer2.extensions.extensionlib import BaseInterface,BaseExtension

class Extension(BaseExtension):
    def on_load(self):
        print("被加载!")

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class Interface(BaseInterface):
    def hello(self):
        print("Hello")


class EditorToolBar(PMEditorToolbar):
    pass


class WidgetTest(PMCodeEditTabWidget):
    pass
