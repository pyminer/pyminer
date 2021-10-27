import sys
from typing import List, Union, Tuple
from widgets import PMGFlowContent
import numpy as np
import matplotlib.pyplot as plt


class LinePlot(PMGFlowContent):
    """
    根据输入的数据，绘制一条直线。
    允许输入的数据类型：多个端口的直线。

    """

    def __init__(self):
        super(LinePlot, self).__init__()
        self.input_args_labels = ['in1']
        self.output_ports_labels = []
        self.class_name = 'LinePlot'
        self.text = '折线图'
        self.icon_path = ''
        self.agg = None

        # self.info = {'gen_array': False, 'size': (1, 2, 3),
        #              'type': 'normal'}  # 命名为self.info的变量会被自动保存，下一次会调用load_info方法进行读取。

    def process(self, *args) -> List:
        """

        Args:
            *args:

        Returns:

        """
        from packages.pmagg import PMAgg
        for arg in args:
            pass
        if self.agg is None:
            self.agg = PMAgg.Window()

        plt.plot([1, 2, 3, 4, 5])
        fig = plt.gcf()
        self.agg.get_canvas(fig)
        self.agg.show()

        return []

    def check_data(self, data):
        pass

    def load_info(self, info: dict):
        print('load info!!!!!!!!!!')
        self.info = info
        print(self.info)


class HistPlot(PMGFlowContent):
    """
    根据输入的数据，绘制一条直线。
    允许输入的数据类型：多个端口的直线。

    """

    def __init__(self):
        super(HistPlot, self).__init__()
        self.input_args_labels = ['in1']
        self.output_ports_labels = []
        self.class_name = 'HistPlot'
        self.text = '条形图'
        self.icon_path = ''
        self.agg = None

    def process(self, *args) -> List:
        """

        Args:
            *args:

        Returns:

        """
        from packages.pmagg import PMAgg
        if self.agg is None:
            self.agg = PMAgg.Window()

        plt.hist(x=args, bins=20, color='steelblue', edgecolor='black')
        fig = plt.gcf()
        self.agg.get_canvas(fig)
        self.agg.show()

        return []

    def check_data(self, data):
        pass

    def load_info(self, info: dict):
        print('load info!!!!!!!!!!')
        self.info = info
        print(self.info)
