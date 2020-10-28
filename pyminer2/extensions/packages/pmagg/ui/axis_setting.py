from PyQt5 import QtWidgets, QtGui
from .linestyles import *
from matplotlib.text import Text
import matplotlib.colors as mcolors


class Window(QtWidgets.QDialog):
    def __init__(self, event, canvas):
        super().__init__()
        self.setWindowTitle('Axis Setting')
        self.axes = event.artist
        self.canvas = canvas
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')

        # 创建列表窗口，添加条目
        self.leftlist =QtWidgets.QListWidget()
        self.leftlist.insertItem(0, 'X轴设置：')
        self.leftlist.insertItem(1, 'Y轴设置：')
        self.leftlist.insertItem(2, 'Z轴设置：')

        # 创建三个小控件
        self.stackX = QtWidgets.QWidget()
        self.stackY = QtWidgets.QWidget()
        self.stackZ = QtWidgets.QWidget()

        self.stackXUI()
        self.stackYUI()
        self.stackZUI()

        # 在QStackedWidget对象中填充了三个子控件
        self.stack = QtWidgets.QStackedWidget(self)

        self.stack.addWidget(self.stackX)
        self.stack.addWidget(self.stackY)
        self.stack.addWidget(self.stackZ)

        self.leftlist.currentRowChanged.connect(self.display)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)

        self.layout = QtWidgets.QFormLayout()
        self.generate_items()
        self.layout.addRow(self.leftlist, self.stack)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.exec()


    def stackXUI(self):
        layout =QtWidgets.QFormLayout()
        layout.addRow('姓名', QtWidgets.QLineEdit())
        layout.addRow('地址', QtWidgets.QLineEdit())
        self.stackX.setLayout(layout)

    def stackYUI(self):
        # zhu表单布局，次水平布局
        layout = QtWidgets.QFormLayout()
        sex = QtWidgets.QHBoxLayout()

        # 水平布局添加单选按钮
        sex.addWidget(QtWidgets.QRadioButton('男'))
        sex.addWidget(QtWidgets.QRadioButton('女'))

        # 表单布局添加控件
        layout.addRow(QtWidgets.QLabel('性别'), sex)
        layout.addRow('生日', QtWidgets.QLineEdit())

        self.stackY.setLayout(layout)

    def stackZUI(self):
        # 水平布局
        layout = QtWidgets.QHBoxLayout()

        # 添加控件到布局中
        layout.addWidget(QtWidgets.QLabel('科目'))
        layout.addWidget(QtWidgets.QCheckBox('物理'))
        layout.addWidget(QtWidgets.QCheckBox('高数'))

        self.stackZ.setLayout(layout)

    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

    def generate_items(self):
        pass

    def confirm_slot(self):
        pass

    def cancel_slot(self):
        self.close()