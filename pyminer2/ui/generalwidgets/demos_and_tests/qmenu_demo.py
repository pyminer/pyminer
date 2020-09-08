import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QToolButton,QMenu,QAction
from PyQt5.QtCore import Qt

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(100,100)
        self.button = QToolButton(self)  # 实例化按钮
        self.button.move(50,30)
        self.button.setIcon(QIcon('大象.ico'))  #设置图标,也可以是png图片
        self.button.setToolTip('提示文本')    #设置提示文本
        self.button.setToolButtonStyle(Qt.ToolButtonFollowStyle)#设置按钮风格
        #Qt.ToolButtonIconOnly    仅显示图标-默认
        #Qt.ToolButtonTextOnly    仅显示文字
        #Qt.ToolButtonTextBesideIcon    文本显示在图标旁边
        #Qt.ToolButtonTextUnderIcon    文本显示在图标下方
        #Qt.ToolButtonFollowStyle   遵循风格

        #toolButtonStyle()   #获取样式风格

        self.button.setArrowType(Qt.UpArrow)   #设置箭头
        #Qt.NoArrow     无箭头
        #Qt.UpArrow     向上箭头
        #Qt.DownArrow    向下箭头
        #Qt.LeftArrow    向左箭头
        #Qt.RightArrow    向右箭头

        #arrowType()   获取箭头类型

        self.button.setAutoRaise(True)  #设置是否自动提升-鼠标在上面时会自动凸起
        #autoRaise()    返回是否自动凸起

        menu=QMenu(self)
        action1=QAction(menu)
        action1.setText('新建')
        action1.setData([1,2,3])  #给行为绑定数据
        action1.triggered.connect(self.A)
        menu.addAction(action1)
        self.button.setMenu(menu)   #给按钮设置菜单
        self.button.setPopupMode(QToolButton.MenuButtonPopup)  #设置菜单弹出模式
        #QToolButton.DelayedPopup    鼠标按住一会才显示-默认
        #QToolButton.MenuButtonPopup    有一个专门的指示箭头,点击箭头才显示
        #QToolButton.InstantPopup    点了按钮就显示,点击信号不会发射

        self.button.triggered.connect(self.B)  #点击行为时发出这个信号
        #会向槽函数传递被点击的行为

    def A(self):
        print('点击了新建行为')
    def B(self,action):
        print('点击了行为',action,action.data())  #action.data() 获取行为绑定的数据


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())