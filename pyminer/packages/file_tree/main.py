import os
from typing import Callable

from PySide2.QtCore import QLocale, QTranslator
from PySide2.QtWidgets import QApplication

from lib.extensions.extensionlib import BaseExtension, BaseInterface
from .file_tree import PMFilesTree

file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_%s.qm' % QLocale.system().name())
app = QApplication.instance()
trans_filetree = QTranslator()
app.trans_filetree = trans_filetree
trans_filetree.load(QLocale.system(), file_name)
app.installTranslator(trans_filetree)


class Extension(BaseExtension):
    def on_loading(self):
        pass

    def on_load(self):
        files_tree: 'PMFilesTree' = self.widgets['PMFilesTree']
        files_tree.extension_lib = self.extension_lib
        self.interface.file_widget = files_tree
        def on_settings_changed():
            work_dir = self.extension_lib.Program.get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR")
            files_tree.change_current_path(work_dir)

        self.extension_lib.Signal.get_settings_changed_signal().connect(on_settings_changed)  # 当主界面设置改变信号发出时，改变工作路径。


class Interface(BaseInterface):
    file_widget: PMFilesTree = None

    def add_open_file_callback(self, file_ext: str, callback: Callable):
        """
        添加对于某个扩展名打开的事件。
        Args:
            file_ext: 扩展名。如'.csv'或者'csv'都是可以的。
            callback:

        Returns:

        """
        if not file_ext.startswith('.'):
            file_ext = '.' + file_ext
        if self.file_widget is not None:
            if self.file_widget.open_methods_dic.get(file_ext) is None:
                self.file_widget.open_methods_dic[file_ext] = [callback]
            else:
                self.file_widget.open_methods_dic[file_ext].append(callback)

    # def add_import_file_callback(self, file_ext: str, action: 'QAction'):
    #     pass
