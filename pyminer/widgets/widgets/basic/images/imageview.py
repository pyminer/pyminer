# -*- coding: utf-8 -*-
"""
This example demonstrates the use of ImageView, which is a high-level widget for
displaying and analyzing 2D and 3D data. ImageView provides:

  1. A zoomable region (ViewBox) for displaying the image
  2. A combination histogram and gradient editor (HistogramLUTItem) for
     controlling the visual appearance of the image
  3. A timeline for selecting the currently displayed frame (for 3D data only).
  4. Tools for very basic analysis of image data (see ROI and Norm buttons)

"""
## Add path to library (just for examples; you do not need this)


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from PySide2.QtWidgets import QWidget, QVBoxLayout


class PMGImageViewer(QWidget):
    def __init__(self, parent=None):
        super(PMGImageViewer, self).__init__(parent)
        self.image_view = pg.ImageView()
        self.setLayout(QVBoxLayout())
        # QVBoxLayout.setC
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.image_view)

    def set_image(self, img, xvals=None):
        self.image_view.setImage(img)  # , xvals=xvals)

    def set_color_map(self, colormap):
        self.image_view.setColorMap(colormap=colormap)


if __name__ == '__main__':
    import numpy as np

    # Interpret image data as row-major instead of col-major
    pg.setConfigOptions(imageAxisOrder='row-major')

    app = QtGui.QApplication([])

    ## Create window with ImageView widget
    # win = QtGui.QMainWindow()
    # win.resize(800, 800)
    imv = PMGImageViewer()
    imv.show()
    imv.setWindowTitle('image view!')
    # win.setCentralWidget(imv)
    # win.show()
    # win.setWindowTitle('pyqtgraph example: ImageView')

    ## Create random 3D data set with noisy signals
    img = pg.gaussianFilter(np.random.normal(size=(200, 200)), (5, 5)) * 20 + 100
    img = img[np.newaxis, :, :]
    decay = np.exp(-np.linspace(0, 0.3, 100))[:, np.newaxis, np.newaxis]
    data = np.random.normal(size=(100, 200, 200))
    data += img * decay
    data += 2

    ## Add time-varying signal
    sig = np.zeros(data.shape[0])
    sig[30:] += np.exp(-np.linspace(1, 10, 70))
    sig[40:] += np.exp(-np.linspace(1, 10, 60))
    sig[70:] += np.exp(-np.linspace(1, 10, 30))

    sig = sig[:, np.newaxis, np.newaxis] * 3
    data[:, 50:60, 30:40] += sig
    x = np.ones((1920, 1080, 3), dtype=np.uint8) + 50
    # x[:, :, 0] = np.zeros((1920, 1080)) + 200
    # x[:, :, 1] = 0
    # x[:, :, 2] = 0
    ## Display the data and assign each frame a time value from 1.0 to 3.0
    print(x.shape,x,data,data.shape)
    imv.set_image(data)  # , xvals=np.linspace(1., 3., data.shape[0]))

    ## Set a custom color map
    colors = [
        (0, 0, 0),
        (45, 5, 61),
        (84, 42, 55),
        (150, 87, 60),
        (208, 171, 141),
        (255, 255, 255)
    ]
    # cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
    # imv.set_color_map(cmap)

    ## Start Qt event loop unless running in interactive mode.
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
