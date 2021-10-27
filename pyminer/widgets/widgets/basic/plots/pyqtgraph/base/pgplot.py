"""
相关的元素设置

线:
颜色--line_color
线型--line_style
粗细--line_width

图元item
边缘线的颜色--border_color
边缘线粗细--border_width
形状--symbol
颜色--item_color

图窗颜色
face_color

['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star']
    #     r_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
"""
import sys
from typing import Union

import pyqtgraph as pg
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from widgets.utilities.source.graphicsitemutils import PMGPlotCustomizer

symbols_dic = {'o': 'o', 's': 's', 't': 't', 't1': 't1', 't2': 't2', 't3': 't3',
               'd': 'd', '+': '+', 'x': 'x', 'p': 'p', 'h': 'h', 'star': 'star',
               '圆': 'o', '方': 's', '正三角': 't1', '倒三角': 't', '五边形': 'p', '六边形': 'h', '星': 'star',
               '五星': 'star', '菱形': 'd'}
random_symbols = [
    dict(pen=(0, 0, 200), symbolBrush=(0, 0, 200), symbolPen='w', symbol='o', symbolSize=8),
    dict(pen=(0, 128, 0), symbolBrush=(0, 128, 0), symbolPen='w', symbol='t', symbolSize=8),
    dict(pen=(19, 234, 201), symbolBrush=(19, 234, 201), symbolPen='w', symbol='t1', symbolSize=8),
    dict(pen=(195, 46, 212), symbolBrush=(195, 46, 212), symbolPen='w', symbol='t2', symbolSize=8),
    dict(pen=(250, 194, 5), symbolBrush=(250, 194, 5), symbolPen='w', symbol='t3', symbolSize=8),
    dict(pen=(54, 55, 55), symbolBrush=(55, 55, 55), symbolPen='w', symbol='s', symbolSize=8),
    dict(pen=(0, 114, 189), symbolBrush=(0, 114, 189), symbolPen='w', symbol='p', symbolSize=8),
    dict(pen=(217, 83, 25), symbolBrush=(217, 83, 25), symbolPen='w', symbol='h', symbolSize=8),
    dict(pen=(237, 177, 32), symbolBrush=(237, 177, 32), symbolPen='w', symbol='star', symbolSize=8),
    dict(pen=(126, 47, 142), symbolBrush=(126, 47, 142), symbolPen='w', symbol='+', symbolSize=8),
    dict(pen=(119, 172, 48), symbolBrush=(119, 172, 48), symbolPen='w', symbol='d', symbolSize=8),
]


class PMGPyQtGraphWidget(QWidget, PMGPlotCustomizer):
    def __init__(self, parent=None, text_color=None):
        super(PMGPyQtGraphWidget, self).__init__(parent)
        self._symbols_dic = symbols_dic
        self._symbols = random_symbols
        self.resize(600, 600)
        self.lines = []
        pg.setConfigOptions(leftButtonPan=False)
        text_color = 'k' if text_color is None else text_color
        pg.setConfigOption('foreground', text_color)
        self.plot_widget: pg.PlotWidget = None
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.v_layout)

    def plot(self, *args, **kwargs):
        pass

    def baseplot(self, x, ylist):
        for line in self.lines:
            line.clear()
        for y in ylist:
            plot_data = self.plot_widget.plot(x, y, pen=None, symbol='+', symbolBrush='r')
            self.lines.append(plot_data)

    def draw(self):
        pass

    def clear(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PMGPyQtGraphWidget()
    demo.show()
    sys.exit(app.exec_())
