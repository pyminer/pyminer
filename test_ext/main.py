class Extension:
    def on_load(self):
        print("被加载!")
    def on_install(self):
        print('被安装')
    def on_uninstall(self):
        print("被卸载")

class Interface:
    def hello(self):
        print("Hello")