# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 20:47
# @Author  : 别着急慢慢来
# @FileName: main.py
# from pyminer2.extensions.packages.ipython_console.main import ConsoleInterface
# from pyminer2.extensions.extensionlib import extension_lib
import os


class Extension:
    def on_load(self):
        console = self.extension_lib.get_interface('ipython_console')
        if console is None:
            raise Exception('console not found')
        console.run_command(command="import sys")
        console.run_command(command=f"sys.path.append(r'{os.path.dirname(__file__)}')")
        console.run_command(command="import matplotlib")
        console.run_command(command="matplotlib.use('module://PMAgg')")
        self.extension_lib.Signal.get_events_ready_signal().connect(
            lambda: self.extension_lib.UI.raise_dock_into_view('ipython_console'))

        print("默认使用PMAgg")

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class Interface:
    def hello(self):
        print("Hello")
