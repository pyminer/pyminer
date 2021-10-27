# -*- coding: utf-8 -*-
# 帕累托图
import matplotlib.pyplot as plt
import pandas as pd
from utils.ui.app.pmbasicapp import PMApp
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    a = PMApp(title='帕累托图')
    btn = a.button_panel.add_button('计算')
    a.show()


    @a.pmagg_add_chart
    def draw():
        global a

        data = a.get_variable()

        if isinstance(data, (pd.DataFrame, pd.Series)):
            data = data.copy()
            data.sort_values()
            data.plot(kind='bar')

            plt.ylabel(u'值')
            p = 1.0 * data.cumsum() / data.sum()
            p.plot(color='r', secondary_y=True, style='-o', linewidth=2)
            # plt.annotate(format(p[6], '.4%'), xy=(6, p[6]), xytext=(6 * 0.9, p[6] * 0.9),
            #              arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))  # 添加注释，即85%处的标记。这里包括了指定箭头样式。
            plt.ylabel(u'比例')


    btn.clicked.connect(draw)
    app.exec_()
