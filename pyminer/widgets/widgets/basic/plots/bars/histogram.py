# -*- coding: utf-8 -*-
"""
In this example we draw two different kinds of histogram.
"""
import numpy as np
import pyqtgraph as pg
import sys
from PySide2.QtWidgets import QApplication
from widgets.widgets.basic.plots import PMGPyQtGraphWidget
from widgets import color_str2tup


class PMGBarWidget(PMGPyQtGraphWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.plot_widget = pg.PlotWidget(self)
        self.v_layout.addWidget(self.plot_widget)

    def plot(self, vals):
        y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
        self.plot_widget.plot(x, y, stepMode=True, fillLevel=0, fillOutline=True,
                              pen=pg.mkPen(self.border_color, width = self.border_width),
                              brush=color_str2tup(self.item_color))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PMGBarWidget()
    demo.show()
    demo.border_width = 3
    demo.border_color = '#ffff00'
    demo.plot(np.random.normal(size=500))
    sys.exit(app.exec_())
