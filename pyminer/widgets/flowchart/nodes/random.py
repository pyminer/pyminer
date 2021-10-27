import sys
from typing import List, Union, Tuple

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit
from widgets import PMGFlowContent, PMGPanelDialog
import numpy as np


class Random(PMGFlowContent):
    """
    随机数生成的类
    可以切换生成的数据类型是整数/浮点还是矩阵。

    """

    def __init__(self):
        super(Random, self).__init__()
        self.input_args_labels = []
        self.output_ports_labels = ['output1']
        self.class_name = 'Random'
        self.text = '随机数生成'
        self.icon_path = ''

        self.info = {'gen_array': False, 'size': (1, 2, 3),
                     'type': 'normal'}  # 命名为self.info的变量会被自动保存，下一次会调用load_info方法进行读取。

    def process(self, *args) -> List[Union[int, float, np.ndarray]]:
        """
        事件处理的方法。
        Args:
            *args:

        Returns:

        """
        if self.info['gen_array']:
            if self.info['type'] == 'uniform':
                return [np.random.random(size=self.info['size'])]
            elif self.info['type'] == 'normal':
                return [np.random.randn(*self.info['size'])]
        else:
            if self.info['type'] == 'uniform':
                return [np.random.random()]
            elif self.info['type'] == 'normal':
                return [np.random.randn()]

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
        assert len(self.info.keys()) > 0, 'info is empty.there maybe no information stored.'
        views = [
            ('check_ctrl', 'gen_array', 'Generate Array', self.info['gen_array']),
            ('eval_ctrl', 'size', 'Size', self.info['size'], 'safe'),
            ('combo_ctrl', 'type', 'Type', self.info['type'], ['uniform', 'normal'], ['均匀分布', '正态分布'])
        ]
        dlg = PMGPanelDialog(parent=parent, views=views)
        dlg.panel.set_param_changed_callback('gen_array',
                                             lambda params: dlg.panel.get_ctrl('size').setEnabled(params['gen_array']))
        dlg.exec_()
        value = dlg.panel.get_value()
        self.load_info(value)

    def format_param(self) -> str:
        return '模式:' + str(self.info['type'])

    def load_info(self, info: dict):
        self.info = info
        print(self.info)
