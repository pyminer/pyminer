import logging
import sys
import time

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
import numpy as np
from typing import List, Dict, Tuple
from widgets.display.matplotlib.qt5agg import PMMatplotlibQt5Widget

logger = logging.getLogger('display.basetimeseries')


class PMBaseTimeSeriesWidget(QWidget):
    def __init__(self, parent: 'QWidget' = None, recent_samples: int = 100, show_mode: str = '',
                 max_samples: int = 10000, sample_type: np.dtype = np.float):
        """
        运用循环队进行数据刷新
        :param parent:
        :param recent_samples:
        :param show_mode: "recently":最近的 recent_points个点,"all":显示全部
        :param max_samples:最多采样数目。如果采样数量太多，就舍弃前面的数据。
        """
        super().__init__(parent=parent)
        self.recent_sample_num = recent_samples
        self.max_samples = max_samples
        self.buffer_length = int(max_samples * 1.5)
        self.bottom_pointers: Dict[str, int] = {}
        self.top_pointers: Dict[str, int] = {}
        self.time: Dict[str, np.ndarray] = {}  # np.zeros(self.buffer_length, dtype=np.float)
        self.data: Dict[str, np.ndarray] = {}
        self.last_plot_time: float = 0
        # self.init_plot()

    def add_data(self, data_name, data_type):
        self.data[data_name] = np.zeros(self.buffer_length, dtype=data_type)
        self.time[data_name] = np.zeros(self.buffer_length, dtype=np.float)
        self.top_pointers[data_name] = 0
        self.bottom_pointers[data_name] = 0

    def add_sample(self, data_name: str, value: float, sample_time: float = -1):
        """
        增加一个采样点
        :param data_name:
        :param value:
        :return:
        """
        if sample_time < 0:
            sample_time = time.time()
        top_pointer = self.top_pointers[data_name]

        if top_pointer == self.buffer_length:
            self.trim_data(data_name)

        top_pointer = self.top_pointers[data_name]
        self.data[data_name][top_pointer] = value
        self.time[data_name][top_pointer] = sample_time
        self.top_pointers[data_name] = self.top_pointers[data_name] + 1
        self.refresh()

    def trim_data(self, data_name: str):
        self.data[data_name][:self.max_samples] = self.data[data_name][
                                                  self.buffer_length - self.max_samples:self.buffer_length]
        self.data[data_name][self.max_samples:] = np.zeros(self.buffer_length - self.max_samples)
        self.time[data_name][:self.max_samples] = self.time[data_name][
                                                  self.buffer_length - self.max_samples:self.buffer_length]
        self.time[data_name][self.max_samples:] = np.zeros(self.buffer_length - self.max_samples)
        self.top_pointers[data_name] = self.max_samples
        # self.bottom_pointers[data_name] = self.max_samples

    def on_length_exceed(self):
        pass

    def get_time_series(self, data_name: str) -> Tuple[np.ndarray, np.ndarray]:
        data = self.data.get(data_name)
        sample_time = self.time.get(data_name)
        assert data is not None, 'no data named %s' % data_name
        if self.top_pointers[data_name] - self.max_samples < 0:
            return sample_time[:self.top_pointers[data_name]], data[:self.top_pointers[data_name]]
        return sample_time[self.top_pointers[data_name] - self.max_samples:self.top_pointers[data_name]], \
               data[self.top_pointers[data_name] - self.max_samples:self.top_pointers[data_name]]

    def get_recent_data(self, data_name: str) -> Tuple[np.ndarray, np.ndarray]:
        data = self.data.get(data_name)
        sample_time = self.time.get(data_name)
        assert data is not None, 'no data named %s' % data_name
        if self.top_pointers[data_name] - self.recent_sample_num < 0:
            return sample_time[:self.top_pointers[data_name]], \
                   data[:self.top_pointers[data_name]]
        return sample_time[self.top_pointers[data_name] - self.recent_sample_num:self.top_pointers[data_name]], \
               data[self.top_pointers[data_name] - self.recent_sample_num:self.top_pointers[data_name]]

    def create_new_line(self):
        pass

    def refresh(self):
        """
        'It is suggested that refresh rate should lower than 10 fps for Matplotlib widget.'
        刷新帧率通常不能超过每秒钟10帧——而且点数不太多的情况下，
        :return:
        """
        self.clear()
        for k in self.time.keys():
            t, y = self.get_recent_data(k)
            self.plot(t, y)

    def init_plot(self):
        pass

    def plot(self, t, y):
        pass

    def clear(self):
        pass


class PMTimeSeriesMPLWidget(PMBaseTimeSeriesWidget):
    def __init__(self, max_samples: int = 10000, recent_samples: int = 100):
        super(PMTimeSeriesMPLWidget, self).__init__(max_samples=max_samples, recent_samples=recent_samples)

        self.setLayout(QVBoxLayout())
        self.plot_widget = PMMatplotlibQt5Widget(self)
        self.layout().addWidget(self.plot_widget)
        self.layout().addWidget(QPushButton('aaaa'))

        self.ax = None

    def plot(self, t, y):
        ax = self.plot_widget.add_subplot(111)
        ax.plot(t, y, 'r')
        ax.set_xlabel('test_x_label')
        self.plot_widget.draw()
        self.plot_widget.canvas.flush_events()

    def clear(self):
        self.plot_widget.figure.clf()


class PMTimeSeriesPGWidget(PMBaseTimeSeriesWidget):
    def __init__(self, max_samples: int = 10000, recent_samples: int = 100):
        super(PMTimeSeriesPGWidget, self).__init__(max_samples=max_samples, recent_samples=recent_samples)
        import pyqtgraph
        self.curves: Dict = {}
        self.setLayout(QVBoxLayout())
        self.plot_widget = pyqtgraph.plot()  # PMMatplotlibQt5Widget(self)
        self.layout().addWidget(self.plot_widget)
        self.layout().addWidget(QPushButton('aaaa'))

        self.ax = None

    def add_data(self, data_name, data_type):
        super().add_data(data_name, data_type)
        self.curves[data_name] = self.plot_widget.plot()

    # def plot(self, t, y):
    #     self.curves[].setData(y)
    def refresh(self):
        for k in self.time.keys():
            t, y = self.get_recent_data(k)
            self.curves[k].setData(t, y)

    def clear(self):
        pass


def time_out():
    t0 = time.time()
    global i, graphics
    i += 1
    graphics.add_sample('a', value=np.random.randint(100))
    t1 = time.time()
    logger.debug(i, 'time elapsed :', t1 - t0)


if __name__ == '__main__':
    app = QApplication(sys.argv)


    def mpl():
        global i, graphics
        graphics = PMTimeSeriesMPLWidget(max_samples=100, recent_samples=20)
        graphics.show()
        i = 0

        graphics.add_data('a', np.float)

        timer = QTimer()
        timer.start(50)
        timer.timeout.connect(time_out)


    def pg():
        global i, graphics
        graphics = PMTimeSeriesPGWidget(max_samples=2000, recent_samples=1000)
        graphics.show()
        i = 0

        graphics.add_data('a', np.float)


    timer = QTimer()

    timer.timeout.connect(time_out)

    timer.start(1)
    pg()
    # timer.start(100)
    # mpl()

    sys.exit(app.exec_())
