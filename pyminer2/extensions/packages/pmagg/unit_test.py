import unittest
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D
current_path=os.getcwd()
sys.path.append(current_path)
# matplotlib.use('QT5Agg')
matplotlib.use('module://PMAgg')
class MyTestCase(unittest.TestCase):
    def f(self,t):
        return np.exp(-1*t) * np.cos(2 * np.pi * t)
    def test_MainWindow(self):
        t1 = np.arange(0, 5, 0.1)
        t2 = np.arange(0, 5, 0.02)

        fig=plt.figure()
        plt.subplot(221)
        # plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'r--',pickradius=5,picker=True)
        plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'r--')
        plt.xlabel('xxx')

        ax=plt.subplot(222)
        x = np.random.randn(100000)
        y = np.random.randn(100000) + 5
        ax.hist2d(x, y, bins=40, norm=LogNorm())
        # h=ax.hist2d(x, y, bins=40, norm=LogNorm())
        # fig.colorbar(h[3],ax=ax)

        plt.subplot(223)
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.plot([1, 2, 3, 4], [2, 4, 7, 9])

        # plt.subplot(224)
        ax = fig.add_subplot(224, projection='3d')
        X = np.arange(-4, 4, 0.25)
        Y = np.arange(-4, 4, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    unittest.main()
