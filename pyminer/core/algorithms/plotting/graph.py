#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 13:54
# @Author  : Jiangchenglong
# @Site    : 
# @File    : graph.py
# @Software: PyCharm
from PySide2.QtWidgets import QWidget
from packages.pmagg.PMAgg import Window
from packages.graph_agg.graph_agg import GraphAgg
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, app=None, widget: QWidget = None, subplots: tuple = (1, 1), backend: str = 'mpl'):
        """
        :param widget: 将图绘制在哪个widget上，如果不提供，则默认使用pmagg的tabWidget，或其它绘图后端UI
        :param figsize: 如绘制3*3个子图
        :param backend: 选择mpl或者graph作为绘图后端
        """
        self.axes = [[None] * subplots[1]] * subplots[0]  # 二维数组，用于存储所有的子图对象
        self.backend = backend
        self.subplots = subplots
        self.widget = widget
        self.app = app
        if (app and widget) is None and backend == 'mpl':
            fig = plt.figure()
            self.axes = fig.subplots(nrows=subplots[0], ncols=subplots[1])
            if subplots == (1, 1):
                self.axes = [[self.axes]]
            else:
                self.axes = self.axes.tolist()
            self.app = Window(bg=self.backend)
            self.app.get_canvas(fig)
            self.widget = self.app.tabWidget.widget(self.app.tab_page_title_index)  # 指定widget为pmagg的tab
        if (app and widget) is None and backend == 'graph':
            self.app = GraphAgg()
            self.widget = self.app.widget
            for row in range(subplots[0]):
                for col in range(subplots[1]):
                    ax = self.widget.addPlot(row=row, col=col)
                    self.axes[row][col] = ax
        # 在初始化过程中，需要提供app,widget,axes

    def plot(self, x, y, position: tuple):
        """根据不同的绘图库，进行封装"""
        row, col = position
        if self.backend == 'mpl':
            self.axes[row][col].plot(x, y)
        if self.backend == 'graph':
            self.widget.getItem(row, col).plot(x, y)
            # 这里有一个恶心的bug，尽管将ax都存在axes中，但还是得通过self.widget.getItem(row,col)拿到对象
            # 否则绘图总是出现在最后一行

    def show(self):
        self.app.show()


if __name__ == '__main__':
    graph = Graph(subplots=(3, 3), backend='graph')
    graph.plot([1, 2, 3], [4, 5, 6], position=(0, 0))
    graph.plot([1, 2, 3], [6, 5, 4], position=(0, 1))
    graph.plot([1, 2, 3], [3, 5, 3], position=(0, 1))
    graph.plot([1, 2, 3], [6, 3, 6], position=(0, 2))
    graph.show()
