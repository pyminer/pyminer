import unittest
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from matplotlib.colors import LogNorm, NoNorm, BoundaryNorm, PowerNorm, SymLogNorm, TwoSlopeNorm, Normalize
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams

current_path = os.getcwd()
sys.path.append(current_path)
# matplotlib.use('QT5Agg')
matplotlib.use('module://PMAgg')


class MyTestCase(unittest.TestCase):
    def f(self, t):
        return np.exp(-1 * t) * np.cos(2 * np.pi * t)

    def test_MainWindow(self):
        t1 = np.arange(0, 5, 0.1)
        t2 = np.arange(0, 5, 0.01)

        fig = plt.figure()
        fig.suptitle('main title')
        plt.subplot(331)
        # plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'r--',pickradius=5,picker=True)
        plt.plot(t1, self.f(t1), 'bo', label='xxx')
        plt.plot(t2, self.f(t2), 'r--', label='curve 2')
        plt.text(2.5, 0.5, 'xxxxx')
        plt.xlabel('xxx')
        plt.legend()

        ax = plt.subplot(332)
        x = np.random.randn(100000)
        y = np.random.randn(100000) + 5
        N = 21
        cmap = plt.get_cmap('jet', N)
        h = ax.hist2d(x, y, bins=40, norm=LogNorm())
        # ax.collections[0].cmap = cmap
        # ax.collections[0].norm = Normalize()
        # x=fig.colorbar(ax.collections[0],ax=ax)
        # print(dir(ax))

        ax = plt.subplot(333)
        x = np.linspace(0, 10, 200)
        data_obj = {'x': x,
                    'y1': 2 * x + 1,
                    'y2': 3 * x + 1.2,
                    'mean': 0.5 * x * np.cos(2 * x) + 2.5 * x + 1.1}

        # 填充两条线之间的颜色
        ax.fill_between('x', 'y1', 'y2', color='yellow', data=data_obj)

        # Plot the "centerline" with `plot`
        ax.set_xscale('log')
        ax.plot('x', 'mean', color='black', data=data_obj)
        ax.plot(x, 2 * x + 1, color='blue')
        ax.plot(x, 3 * x + 1.2, color='green')

        # plt.subplot(224)
        ax = fig.add_subplot(334, projection='3d')
        X = np.arange(-4, 4, 0.25)
        Y = np.arange(-4, 4, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

        mu = 100  # mean of distribution
        sigma = 15  # standard deviation of distribution
        x = mu + sigma * np.random.randn(437)

        num_bins = 50

        ax = plt.subplot(335)

        # the histogram of the data
        n, bins, patches = ax.hist(x, num_bins, density=True)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax.plot(bins, y, '--')
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

        theta = np.arange(0, 2 * np.pi, 0.02)
        ax = plt.subplot(336, projection='polar')
        ax.plot(theta, theta / 6, '--', lw=2)

        ax = plt.subplot(337)
        slices = [7, 2, 2, 13]
        activities = ['sleeping', 'eating', 'working', 'playing']
        cols = ['c', 'm', 'r', 'b']
        ax.pie(slices,
               labels=activities,
               colors=cols,
               startangle=90,
               shadow=True,
               explode=(0, 0.1, 0, 0),
               autopct='%1.1f%%')
        ax.set_title('Interesting Graph\nCheck it out')
        ax = plt.subplot(338)
        n = 128
        X = np.random.normal(0, 1, n)  # 随机数X的生成（生成正态分布，平均数为0，方差为1，个数为128）
        Y = np.random.normal(0, 1, n)  # 随机数Y的生成（生成正态分布，平均数为0，方差为1，个数为128）
        T = np.arctan2(Y, X)
        # plt.axes([0.025,0.025,0.95,0.95]) #指定显示范围
        ax.scatter(X, Y, s=75, c=T, alpha=.5)  # 画散点图的函数scatter（其中XY表示数值的大小，s表示散点的尺寸大小，c表示颜色，alpha表示透明度)
        ax.set_xlim(-1.5, 1.5), plt.xticks([])  # x和y坐标轴的范围
        ax.set_ylim(-1.5, 1.5), plt.yticks([])  # x和y坐标轴的范围
        ax.set_title("scatter")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax = plt.subplot(339)
        x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        y1 = [6, 5, 8, 5, 6, 6, 8, 9, 8, 10]
        y2 = [5, 3, 6, 4, 3, 4, 7, 4, 4, 6]
        y3 = [4, 1, 2, 1, 2, 1, 6, 2, 3, 2]

        ax.bar(x, y1, label="label1", color='red')
        ax.bar(x, y2, label="label2", color='orange')
        ax.bar(x, y3, label="label3", color='lightgreen')

        ax.legend(loc="upper left")  # 防止label和图像重合显示不出来
        ax.set_ylabel('number')
        ax.set_xlabel('name')
        ax.set_title("title")
        plt.show()

    def test_twiny(self):
        time = np.arange(10)
        temp = np.random.random(10) * 30
        Swdown = np.random.random(10) * 100 - 10
        Rn = np.random.random(10) * 100 - 10

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(time, Swdown, '-', label='Swdown')
        ax.plot(time, Rn, '-', label='Rn')
        ax2 = ax.twinx()
        ax2.plot(time, temp, '-r', label='temp')
        ax.legend(loc=0)
        ax.grid()
        ax.set_xlabel("Time (h)")
        ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
        ax2.set_ylabel(r"Temperature ($^\circ$C)")
        ax2.set_ylim(0, 35)
        ax.set_ylim(-20, 100)
        ax2.legend(loc=0)
        plt.show()

    def test_legend(self):
        # -*- coding: utf-8 -*-
        import matplotlib.pyplot as plt
        ax = plt.subplot(111)
        ax.plot([1, 2, 3], [4, 5, 6])
        ax.legend()
        plt.show()

    def test_rotation(self):
        import numpy as np
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import random

        def fun(x, y):
            return 0.063 * x ** 2 + 0.0628 * x * y - 0.15015876 * x + 96.1659 * y ** 2 - 74.05284306 * y + 14.319143466051

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = y = np.arange(-1.0, 1.0, 0.05)
        X, Y = np.meshgrid(x, y)
        zs = np.array([fun(x, y) for x, y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)

        ax.plot_surface(X, Y, Z)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
        ax.legend([fake2Dline], ['Lyapunov function on XY plane'], numpoints=1)
        plt.show()

    def test_animation(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.show()
        for i in range(100):
            ax.plot(np.random.random(100), np.random.random(100))
            fig.canvas.draw()

    def test_axis_text(self):
        """条形图bar"""
        x = ['10/Q1', '10/Q3', '11/Q1', '11/Q3', '12/Q1', '12/Q3', '13/Q1', '13/Q3', '14/Q1', '14/Q3', '15/Q1', '15/Q3',
             '16/Q1', '16/Q3', '17/Q1', '17/Q3']
        y = [20, 35, 39, 62, 87, 114, 140, 169, 187, 211, 225, 239, 241, 247, 251, 258]

        # plt.bar([1,3,5,7,9],[5,2,7,8,2],label='Example One',color='b')#plt.bar创建条形图
        # plt.bar([2,4,6,8,10],[8,6,2,5,6],label='Example Two',color='g')

        plt.bar(range(16), y, color='lightsteelblue')
        plt.plot(range(16), y, marker='o', color='coral')  # coral
        plt.xticks(range(16), x)
        plt.legend()
        plt.show()

    def test_pie(self):
        ax = plt.subplot()
        slices = [7, 2, 2, 13]
        activities = ['sleeping', 'eating', 'working', 'playing']
        cols = ['c', 'm', 'r', 'b']
        ax.pie(slices,
               labels=activities,
               colors=cols,
               startangle=90,
               shadow=True,
               explode=(0, 0.5, 0, 0),
               autopct='%1.1f%%')
        ax.set_title('Interesting Graph\nCheck it out')
        plt.show()

    def test_colorbar(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        import numpy as np

        ax = plt.subplot(221)
        im=ax.imshow(np.arange(100).reshape((10, 10)))
        plt.colorbar(im,ax=ax)
        plt.title('中文测试')
        ax = plt.subplot(222)
        x = np.random.randn(100000)
        y = np.random.randn(100000) + 5
        ax.hist2d(x, y, bins=40, norm=LogNorm())
        ax = plt.subplot(223, projection='3d')
        X = np.arange(-4, 4, 0.25)
        Y = np.arange(-4, 4, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
        ax = plt.subplot(224)
        levels = [-1.5, -1, -0.5, 0, 0.5, 1]
        cmap = plt.cm.get_cmap("winter")
        delta = 0.025
        x = y = np.arange(-3.0, 3.01, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = np.exp(-X ** 2 - Y ** 2)
        Z2 = np.exp(-(X - 1) ** 2 - (Y - 1) ** 2)
        Z = (Z1 - Z2) * 2
        cs = ax.contour(X, Y, Z)
        dd=plt.colorbar(cs, ax=ax)
        # ax.locator_params(nbins=4)

        plt.show()

    def test_show(self):
        t1 = np.arange(0, 5, 0.1)
        t2 = np.arange(0, 5, 0.01)

        fig = plt.figure()
        fig.suptitle('main title')
        plt.subplot(221)
        # plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'r--',pickradius=5,picker=True)
        plt.plot(t1, self.f(t1), 'bo', label='xxx')
        plt.plot(t2, self.f(t2), 'r--', label='curve 2')
        plt.text(2.5, 0.5, 'xxxxx')
        plt.xlabel('xxx')
        plt.legend()

        ax = plt.subplot(222)
        x = np.random.randn(100000)
        y = np.random.randn(100000) + 5
        N = 21
        cmap = plt.get_cmap('jet', N)
        h = ax.hist2d(x, y, bins=40, norm=LogNorm())
        # ax.collections[0].cmap = cmap
        # ax.collections[0].norm = Normalize()
        # x=fig.colorbar(ax.collections[0],ax=ax)
        # print(dir(ax))

        # plt.subplot(224)
        ax = fig.add_subplot(223, projection='3d')
        X = np.arange(-4, 4, 0.25)
        Y = np.arange(-4, 4, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

        mu = 100  # mean of distribution
        sigma = 15  # standard deviation of distribution
        x = mu + sigma * np.random.randn(437)

        num_bins = 50

        ax = plt.subplot(224)

        # the histogram of the data
        n, bins, patches = ax.hist(x, num_bins, density=True)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax.plot(bins, y, '--')
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

        theta = np.arange(0, 2 * np.pi, 0.02)
        plt.show()


if __name__ == '__main__':
    unittest.main()
