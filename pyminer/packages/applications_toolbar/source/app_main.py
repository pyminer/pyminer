"""
作者:demo
创建日期:2020-01-01
说明:示例描述信息
"""
from lib.comm import get_var, set_var
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel


def set_variable():
    set_var("x", [1, 2, 3, 4, 5])


def get_variable():
    global label
    x = get_var("x")
    label.setText('x = ' + repr(x))


if __name__ == '__main__':
    app = QApplication([])
    w = QWidget()
    layout = QVBoxLayout()
    w.setLayout(layout)

    button_send_var = QPushButton("发送变量x=[1,2,3,4,5]")
    button_get_var = QPushButton("获取变量x")

    button_send_var.clicked.connect(set_variable)
    button_get_var.clicked.connect(get_variable)

    label = QLabel()
    layout.addWidget(label)
    layout.addWidget(button_send_var)
    layout.addWidget(button_get_var)
    w.show()
    app.exec_()
