import os
from typing import Callable

from PyQt5.QtCore import QLocale

from .file_tree import PMFilesTree
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface


class Extension(BaseExtension):
    def on_loading(self):
        self.extension_lib.UI.add_translation_file(
            os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name())))
        self.extension_lib.Program.add_translation('zh_CN', {'File Tree': '文件'})

    def on_load(self):
        files_tree: 'PMFilesTree' = self.widgets['PMFilesTree']
        files_tree.extension_lib = self.extension_lib
        self.interface.file_widget = files_tree
        settings = self.extension_lib.Program.get_settings()
        self.extension_lib.Signal.get_settings_changed_signal().connect(# 当主界面设置改变信号发出时，改变工作路径。
            lambda: files_tree.change_current_path(settings['work_dir']))


class Interface(BaseInterface):
    file_widget: PMFilesTree = None

    def add_open_file_callback(self, file_ext: str, callback: Callable):
        if not file_ext.startswith('.'):
            file_ext = '.' + file_ext
        if self.file_widget is not None:
            if self.file_widget.open_methods_dic.get(file_ext) is None:
                self.file_widget.open_methods_dic[file_ext] = [callback]
            else:
                self.file_widget.open_methods_dic[file_ext].append(callback)
