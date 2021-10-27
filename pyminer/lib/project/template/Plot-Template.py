# --coding:utf-8--

"""
Please make sure the content of the file is complete.
If you customize the template, please make sure it can be executed correctly
by the interpreter after modification.
Do not delete the file and the directory where the file is located.
请确保文件内容完整。
若自定义模板，请在修改后确保能够被解释器正确执行。
【请勿删除】该文件以及文件所在目录
"""
import matplotlib.pyplot as plt
import numpy as np


def demoTemplate():
    x = np.linspace(0, 5, 200)
    y1 = x + 1
    y2 = x - 1
    plt.figure()
    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(axis="both", linestyle='-.', c='b')
    plt.plot(x, y1, 'c--')
    plt.plot(x, y2, 'r-.')
    plt.text(1, 0.5, "text")
    plt.legend(["y1", "y2"])
    plt.xlabel("xlabel")
    plt.ylabel("ylabel")
    plt.title("title")
    plt.show()


if __name__ == '__main__':
    demoTemplate()
