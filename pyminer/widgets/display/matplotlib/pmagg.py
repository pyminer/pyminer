import sys
from PySide2 import QtWidgets
import matplotlib.pyplot as plt
import random
sys.path.append(r'E:\Python\pyminer_bin\PyMiner\bin\pyminer2\extensions\packages\pmagg')
import PMAgg
import os


class MainWindow(QtWidgets.QDialog):
    def __init__(self, figure, config_path):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        mpl_app = PMAgg.Window(config_path)
        # 只需要将mpl绘图产生的figure对象以及一个配置文件.cfg的路径传给PMAgg即可，配置文件可以留空。
        mpl_app.get_canvas(figure)
        layout.addWidget(mpl_app)
        # 一个额外的按钮
        self.button = QtWidgets.QPushButton('test')
        layout.addWidget(self.button)
        self.setLayout(layout)


if __name__ == '__main__':
    # matplotlib 绘图
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = [random.random() for i in range(25)]
    ax.plot(data, '*-')
    # app
    app = QtWidgets.QApplication(sys.argv)
    config_path = os.path.join(r'E:\Python\pyminer_bin\PyMiner\bin\pyminer2\extensions\packages\pmagg', 'settings.cfg')
    main = MainWindow(fig, config_path)
    main.setWindowTitle('Simple PySide2 and PMAgg example')
    main.show()
    sys.exit(app.exec_())