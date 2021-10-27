import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.ui.app.pmbasicapp import PMApp
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    a = PMApp(params=[('check_ctrl', 'check', '标注异常值文字', False)], data_type_filter='dataframe', title='异常值检查')
    btn = a.button_panel.add_button('计算')
    a.show()


    @a.pmagg_add_chart
    def draw():
        global a
        data = a.get_variable()
        if isinstance(data, (pd.DataFrame, pd.Series)):
            arr = data.values
            data = arr[np.logical_not(np.isnan(arr))]

        if data is not None:
            p = plt.boxplot(data)
            if a.get_params()['check']:
                x, y = p['fliers'][0].get_xdata(), p['fliers'][0].get_ydata()
                y.sort()
                for i in range(len(x)):
                    if i > 0:
                        plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.05 - 0.8 / (y[i] - y[i - 1]), y[i]))
                    else:
                        plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.08, y[i]))


    btn.clicked.connect(draw)
    app.exec_()
