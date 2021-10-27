"""
有无办法通过迭代器方式递归实现流程图的迭代仿真？
"""
import os
import sys
import time
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable
from widgets import PMGFlowContent, PMGPanelDialog

if TYPE_CHECKING:
    import pandas as pd


class ListDirs(PMGFlowContent):

    def __init__(self):
        super(ListDirs, self).__init__()
        self.input_args_labels = []
        self.output_ports_labels = ['路径']  # , '检验']
        self.class_name = 'ListDirs'
        self.text = '文件列举'
        self.icon_path = ''
        self.info = {
            'ext_filter': '.csv',
            'dir': ''
        }

    def process(self, *args) -> List:
        """
        基础迭代器
        Args:
            *args:

        Returns:

        """
        ext = self.info['ext_filter']
        files = [path for path in os.listdir(self.info['dir']) if os.path.splitext(path)[1] == ext]
        for file_path in files:
            path = os.path.normcase(os.path.join(self.info['dir'], file_path))
            yield [path]

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
        views = [
            ('folder_ctrl', 'dir', '选取路径', self.info['dir']),
            ('line_ctrl', 'ext_filter', '扩展名类型', self.info['ext_filter']),
        ]
        dlg = PMGPanelDialog(parent=parent, views=views)

        dlg.setMinimumSize(600, 480)
        dlg.exec_()

        self.info = dlg.panel.get_value()


if __name__ == '__main__':
    import sys

    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # r.load_info({'gen_array': False, 'size': (1, 2, 3), 'type': 'normal'})
    # r.process()
    info = {
        'ext_filter': '.csv',
        'dir': '/home/'
    }
    r = ListDirs()
    r.load_info(info)
    r.on_settings_requested(None)
    print(r.info)
    sys.exit(app.exec_())
