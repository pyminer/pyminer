import pyqtgraph as pg
import numpy as np
from PySide2.QtWidgets import QApplication
from widgets.widgets.basic.plots.pyqtgraph import PMGPyQtGraphWidget
from widgets import color_str2tup
import sys


class PMGScatterPlot(PMGPyQtGraphWidget):
    def __init__(self, parent=None):
        super(PMGScatterPlot, self).__init__(parent)
        self.plot_widget = pg.PlotWidget(self)
        self.v_layout.addWidget(self.plot_widget)

    def plot(self):
        n = 300
        self.s1 = pg.ScatterPlotItem(size=10,
                                     pen=pg.mkPen(self.border_color,width = self.border_width),
                                     brush=color_str2tup(self.item_color))
        pos = np.random.normal(size=(2, n), scale=1e-5)
        spots = [{'pos': pos[:, i], 'data': 1} for i in range(n)] + [{'pos': [0, 0], 'data': 1}]
        print(spots)
        self.s1.addPoints(spots)
        self.plot_widget.addItem(self.s1)
        print(self.plot_widget.getPlotItem())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pw = PMGScatterPlot()
    pw.border_color = '#ff0000'
    pw.show()
    pw.plot()
    sys.exit(app.exec_())
