#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QToolButton, QGraphicsDropShadowEffect


class PMToolButton(QToolButton):
    shadow = QGraphicsDropShadowEffect()  # 实例阴影
    def __init__(self,parent=None):
        super().__init__(parent)
        self.shadow.setColor(QColor(63, 72, 204))  # 设置阴影颜色
        self.shadow.setOffset(0, 0)  # 设置阴影方向

        self.clicked.connect(self.set_btn_clicked_effect)

    def set_btn_clicked_effect(self):
        # 设置模糊度并为按钮添加阴影
        self.shadow.setBlurRadius(20)
        self.setGraphicsEffect(self.shadow)

    def unset_btn_clicked_effect(self):
        # 设置模糊度为0 间接取消阴影
        self.shadow.setBlurRadius(0)

