# -*- coding: utf-8 -*-
"""
Demonstrates very basic use of ImageItem to display image data inside a ViewBox.
"""

## Add path to library (just for examples; you do not need this)
# from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt
import time
from typing import TYPE_CHECKING
from PIL import Image

if TYPE_CHECKING:
    import numpy as np


class PMGImageViewer(QWidget):
    def __init__(self, parent=None):
        """
        这是一个可以用多种方式和数据类型设置、获取图片的控件。
        Args:
            parent:
        """
        super(QWidget, self).__init__(parent)

        self.setLayout(QVBoxLayout())
        self.img_show = QLabel()
        self.img_show.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scroll_widget = QScrollArea()
        self.layout().addWidget(self.scroll_widget)
        self.scroll_widget.setWidget(self.img_show)

    def set_image_qpixmap(self, pixmap):
        self.img_show.setPixmap(pixmap)
        self.img_show.setMinimumSize(pixmap.width() + 100, pixmap.height() + 100)

    def set_image_array(self, arr: 'np.ndarray'):
        from PIL import Image
        image2 = Image.fromarray(arr)
        self.set_image_qpixmap(image2.toqpixmap())

    def open_image(self, image_path):
        from PIL import Image
        img = Image.open(image_path)
        # img.topixmap()
        self.set_image_qpixmap(img.toqpixmap())

    def get_image_qpixmap(self) -> QPixmap:
        return self.img_show.pixmap()

    def get_image_array(self) -> 'np.ndarray':
        from PIL import Image
        img = Image.fromqpixmap(self.get_image_qpixmap())
        return np.array(img)


if __name__ == '__main__':

    from pyqtgraph.Qt import QtCore, QtGui
    import numpy as np
    import pyqtgraph as pg
    import pyqtgraph.ptime as ptime

    app = QtGui.QApplication([])
    # read_figure()

    ## Create window with GraphicsView widget
    win = PMGImageViewer()
    win.showMaximized()  ## show widget alone in its own window
    win.setWindowTitle('pyqtgraph example: ImageItem')

    # updateData()
    image = Image.open(
        r'C:\Users\12957\Documents\Developing\Python\PyMiner_dev_kit\bin\widgets\doc_figures\pmflowarea_1.png')
    # image = np.array(image)
    # image2 = Image.fromarray(image)
    # win.set_image(image2.toqpixmap())
    win.open_image(
        r'C:\Users\12957\Documents\Developing\Python\PyMiner_dev_kit\bin\widgets\doc_figures\pmflowarea_1.png')
    ## Start Qt event loop unless running in interactive mode.
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
