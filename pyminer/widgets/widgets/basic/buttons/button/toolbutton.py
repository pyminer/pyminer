#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PySide2.QtCore import QEvent, QTimer
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QToolButton, QGraphicsDropShadowEffect, QMenu, QWidget, QHBoxLayout


class PMMenu(QMenu):
    def __init__(self, tool_button: 'PMGToolButton' = None):
        super().__init__()
        self.tool_button = tool_button

    def leaveEvent(self, a0: QEvent) -> None:
        print('leave menu', self.underMouse(), self.tool_button.underMouse())

        QTimer.singleShot(50, self.tool_button.hide_menu)



class PMGToolButton(QToolButton):
    shadow = QGraphicsDropShadowEffect()  # 实例阴影

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow.setColor(QColor(63, 72, 204))  # 设置阴影颜色
        self.shadow.setOffset(0, 0)  # 设置阴影方向
        self.setMinimumWidth(60)
        self.setMinimumHeight(40)
        self.clicked.connect(self.set_btn_clicked_effect)
        self.menu = PMMenu(tool_button=self)
        self.setMenu(self.menu)
        self.menu.addAction('新建行')
        self.menu.addAction('新建列')
        self.menu.addAction('删除行')
        self.menu.addAction('删除列')

    def set_btn_clicked_effect(self):
        # 设置模糊度并为按钮添加阴影
        self.shadow.setBlurRadius(20)
        self.setGraphicsEffect(self.shadow)

    def unset_btn_clicked_effect(self):
        # 设置模糊度为0 间接取消阴影
        self.shadow.setBlurRadius(0)

    def show_menu(self):
        if self.underMouse() or self.menu.underMouse():
            self.menu.popup(self.mapToGlobal(self.pos()))
            self.grabMouse()

    def hide_menu(self):
        if not (self.underMouse() or self.menu.underMouse()):
            self.menu.hide()


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = QWidget()
    layout = QHBoxLayout()
    w.setLayout(layout)
    for i in range(3):
        w1 = PMGToolButton()
        layout.addWidget(w1)
        w1.setText('aaa')
    w.show()
    sys.exit(app.exec_())
