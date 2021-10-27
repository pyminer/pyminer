import time
from random import randint

from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from typing import List, Union, Tuple
import pyqtgraph as pg
from PySide2.QtWidgets import QVBoxLayout, QWidget, QSpinBox
from widgets.widgets.basic.plots.pyqtgraph.base.pgplot import PMGPyQtGraphWidget
from widgets import color_str2tup, TYPE_RANGE
from widgets import iter_isinstance


def convert_time(time_stamp: Union[float, int]):
    return time.strftime('%H:%M:%S', time.localtime(time_stamp))


class TimeSeriesPGWidget(PMGPyQtGraphWidget):
    """
    性能很好的监视面板，300个点每分钟刷新一次，可以保持
    """

    def __init__(self, parent=None, face_color=None, text_color=None):
        super().__init__(parent, text_color=text_color)
        self.face_color = face_color
        self.text_color = text_color
        self.plot_widget = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()}, background=self.face_color)

        self.legend = self.plot_widget.addLegend(brush=QBrush(QColor(255, 255, 255)), offset=(-10, 10),
                                                 labelTextColor=self.text_color, labelTextSize=8)
        self.v_layout.addWidget(self.plot_widget)
        # self.setMinimumSize(300, 200)
        # self.setMaximumSize(450, 300)
        self.xlabel: str = ''
        self.ylabel: str = ''
        self.threshold_range: TYPE_RANGE = None
        self.x_range: Tuple[float, float] = None
        self.y_range: Tuple[float, float] = None
        self.title: str = ''
        self.ticks = 5
        self.show_data_num = 10
        self.max_data = 200
        self.timestamp_list = []
        self.value_list = []
        self.repaint_all = False

    def show_time_series(self, timestamps: List[float], values: List[List[float]], tags=None):
        self.clear()
        for value_list in values:
            if value_list is not None:
                assert len(timestamps) == len(value_list)
        if tags is not None:
            assert len(tags) == len(values)
        else:
            tags = [i + 1 for i in range(len(values))]
        self.plot_widget.plotItem.setTitle(self.title)
        self.plot(timestamps, values, tags)

    def gen_threshold_line(self, x):
        return [self.threshold_range[0] for i in x], [self.threshold_range[1] for i in x]

    def get_threshold_line_num(self) -> int:
        s = 0
        if self.threshold_range is None:
            return s
        if self.threshold_range[0] is not None:
            s += 1
        if self.threshold_range[1] is not None:
            s += 1
        return s

    def plot(self, x, ylist, tags: List = None):
        """
        绘图方法
        :param x:
        :param ylist:
        :param tags: 标签
        :return:
        """
        if (len(ylist) + self.get_threshold_line_num() != len(self.lines) and self.threshold_range is not None) or \
                (len(ylist) != len(self.lines) and self.threshold_range is None):

            if tags is None:
                tags = [None] * len(ylist)

            for line in self.lines:
                line.clear()
            self.lines = []
            if self.y_range is not None:
                self.plot_widget.setYRange(*self.y_range)
            self.legend.clear()
            # if self.threshold_range
            if self.threshold_range is not None:
                threshold_lower, threshold_upper = self.gen_threshold_line(x)
                if self.threshold_range[0] is not None:
                    l1 = self.plot_widget.plot(x, threshold_lower, pen='#ff0000')
                    self.lines.append(l1)
                if self.threshold_range[1] is not None:
                    l2 = self.plot_widget.plot(x, threshold_upper, pen='#ff0000')
                    self.lines.append(l2)
            assert len(self._symbols) >= len(ylist), 'Too much lines for monitor!'
            for i, y in enumerate(ylist):
                plot_data = self.plot_widget.plot(x, y, **self._symbols[i], name=tags[i])
                self.lines.append(plot_data)
            self.legend.setBrush(QColor(*color_str2tup(self.legend_face_color), 100))
            # TODO add opacity settings choices!
        else:
            if self.threshold_range is not None:

                threshold_lower, threshold_upper = self.gen_threshold_line(x)
                if self.threshold_range is not None:
                    threshold_lower, threshold_upper = self.gen_threshold_line(x)
                    if self.threshold_range[0] is not None and self.threshold_range[1] is not None:
                        self.lines[0].setData(x, threshold_lower)
                        self.lines[1].setData(x, threshold_upper)
                    else:
                        if self.threshold_range[1] is not None:
                            self.lines[0].setData(x, threshold_upper, pen='#ff0000')

                        if self.threshold_range[0] is not None:
                            self.lines[0].setData(x, threshold_lower, pen='#ff0000')

                for i, y in enumerate(ylist):
                    self.lines[i + self.get_threshold_line_num()].setData(x, y)
            else:
                for i, y in enumerate(ylist):
                    self.lines[i].setData(x, y)


class PMGTimeSeriesPlot(QWidget):
    def __init__(self, parent: QWidget = None,
                 threshold_range: TYPE_RANGE = None, face_color=None, text_color=None):
        super(PMGTimeSeriesPlot, self).__init__(parent)

        self.threshold_range = threshold_range
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.control_layout = QHBoxLayout()
        self.control_layout.setContentsMargins(0, 0, 0, 0)

        self.time_series = TimeSeriesPGWidget(face_color=face_color, text_color=text_color)
        self.layout().addWidget(self.time_series)
        self.layout().addLayout(self.control_layout)

    def set_data(self, timestamps: List[float], values: List[List[float]], tags: List[str] = None):
        self.time_series.show_time_series(timestamps, values, tags)

    def insert_data(self, timestamp: float, values: List[float], tags: List[float]):
        raise NotImplementedError
        self.time_series.insert_data(timestamp, values)

    def config_chart_text(self, title: str, xlabel: str, ylabel: str):
        self.time_series.title = title
        self.time_series.xlabel = xlabel
        self.time_series.ylabel = ylabel

    def alert(self, alert_level: int):
        if alert_level == 1:
            self.time_series.face_color = '#dc321e'
        elif alert_level == 2:
            self.time_series.face_color = '#c86428'
        else:
            self.time_series.face_color = '#ffffff'


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import QTimer

    app = QApplication(sys.argv)
    pmqt5mplwgt = PMGTimeSeriesPlot()
    pmqt5mplwgt.time_series.line_color = '#ff0000'
    pmqt5mplwgt.time_series.border_color = '#ff0000'
    pmqt5mplwgt.time_series.symbol = '圆'
    pmqt5mplwgt.time_series.y_range = (0, 100)
    pmqt5mplwgt.time_series.threshold_line = 0.8 * 100
    pmqt5mplwgt.config_chart_text(title='时间序列数据', xlabel='时间', ylabel='')
    timer = QTimer()


    def f():
        n = 300
        pmqt5mplwgt.set_data([i + 1 for i in range(n)],
                             [[randint(0, 30) for i in range(n)], [randint(0, 100) for i in range(n)]],
                             ['Cpu1', 'Cpu2'])


    timer.timeout.connect(f)
    timer.start(33)
    pmqt5mplwgt.show()
    app.exec_()
