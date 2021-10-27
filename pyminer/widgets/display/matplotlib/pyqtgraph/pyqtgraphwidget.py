import sys
import random
import numpy as np
import pyqtgraph as pg
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class PMPyQtGraphWidget(QWidget):
    def __init__(self, parent=None):
        super(PMPyQtGraphWidget, self).__init__(parent)
        self.resize(600, 600)
        self.lines = []
        # 1
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # 2
        # x = np.random.normal(size=1000)
        # y = np.random.normal(size=1000)
        # r_symbol = random.choice(['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star'])
        # r_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])

        # 3
        self.pw = pg.PlotWidget(self,axisItems = {'bottom': pg.DateAxisItem()})
        # self.plot_data = self.pw.plot(x, y, pen=None, symbol=r_symbol, symbolBrush=r_color)

        # 4
        # self.plot_btn = QPushButton('Replot', self)
        # # self.plot_btn.clicked.connect(self.plot_slot)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        # self.v_layout.addWidget(self.plot_btn)
        self.setLayout(self.v_layout)

    def plot(self, x, ylist):
        self.baseplot(x, ylist)
        # self.timer2 = QTimer()
        # self.timer2.singleShot(5000, lambda: self.baseplot(np.array(x)+2, ylist))
        # self.baseplot(x, ylist)

    def baseplot(self, x, ylist):
        # print('baseplot!')
        for line in self.lines:
            line.clear()
        for y in ylist:
            plot_data = self.pw.plot(x, y, pen=None, symbol='+', symbolBrush='r')
            self.lines.append(plot_data)

    def draw(self):
        pass

    def clear(self):
        pass
    # def plot_slot(self):
    #     x = np.random.normal(size=1000)
    #     y = np.random.normal(size=1000)
    #     r_symbol = random.choice(['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star'])
    #     r_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
    #     self.plot_data.setData(x, y, pen=None, symbol=r_symbol, symbolBrush=r_color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PMPyQtGraphWidget()
    demo.show()
    sys.exit(app.exec_())
