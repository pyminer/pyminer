"""
作者：侯展意
协议：GPL
"""
import time

t0 = time.time()
import json
import os
import sys

path = os.path.dirname(__file__)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
root_path = os.path.dirname(root_path)

sys.path.append(root_path)
import traceback
import matplotlib.pyplot as plt
import sys
from typing import TYPE_CHECKING, Tuple, List, Dict, Union
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSizePolicy, QApplication, QHBoxLayout, QDialog, QVBoxLayout, QTextBrowser, QSpacerItem, \
    QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from widgets import PMGPanel, center_window, set_closable, set_minimizable, set_always_on_top
from utils import bind_combo_with_workspace
from lib.comm import get_var, get_var_names

if not TYPE_CHECKING:
    import algorithm
    # from algorithm import predefined_functions
    from algorithm import loadVariables
else:
    import algorithm
    # from .algorithm import loadVariables
    from .algorithm import predefined_functions
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
t1 = time.time()
print(t1 - t0)


class ControlPanel(PMGPanel):

    def __init__(self, parent=None):
        args = [
            ('combo_ctrl', 'x_axis', 'x variable', 'a', ['a', 'b', 'cc', 'myvar']),
            ('combo_ctrl', 'y_axis', 'y variable', 'a', ['a', 'b', 'cc', 'myvar']),
            ('combo_ctrl', 'z_axis', 'z variable', 'a', ['None', 'a']),
            ('combo_ctrl', 'func_type', 'Function Type', 'linear', list(algorithm.predefined_functions.keys())),
            ('line_ctrl', 'vars', 'variables', 'a,b'),
            ('line_ctrl', 'func', 'function', 'a*x+b'),
            ]
        super(ControlPanel, self).__init__(parent=parent, views=args)
        self.signal_settings_changed.connect(self.handle_settings_change)
        # self.client.signal_data_changed.connect(self.on_data_changed)
        self.refresh_variables()
        bind_combo_with_workspace(self.widgets_dic['x_axis'].check)
        bind_combo_with_workspace(self.widgets_dic['y_axis'].check)
        bind_combo_with_workspace(self.widgets_dic['z_axis'].check)

    def handle_settings_change(self, settings: Dict[str, Union[str, int, list]]):
        if settings['func_type'] == 'customized':
            self.widgets_dic['vars'].setEnabled(True)
            self.widgets_dic['func'].setEnabled(True)
        else:
            self.widgets_dic['vars'].setEnabled(False)
            self.widgets_dic['func'].setEnabled(False)

    def on_data_changed(self, data_name: str):
        print('data_changed!!!!!!!!')
        # print(packet)
        # if packet.get('message') == 'data_changed':
        self.refresh_variables()

    def refresh_variables(self):
        """
        从数据服务器取回全部的可迭代类型变量名称，然后显示在标签上。
        """
        name_list = get_var_names()
        list_x, list_y, list_z = name_list, name_list, ['None'] + name_list

        self.widgets_dic['x_axis'].set_choices(list_x)
        self.widgets_dic['y_axis'].set_choices(list_y)
        self.widgets_dic['z_axis'].set_choices(list_z)

    def get_variables(self) -> Tuple:
        """
        获取数值。当然，由于目前网络通信还没有做，所以暂时还做不了。
        """
        x_var_name = self.widgets_dic['x_axis'].check.currentText()  # get_value()
        y_var_name = self.widgets_dic['y_axis'].check.currentText()  ##get_value()
        z_var_name = self.widgets_dic['z_axis'].check.currentText()  # et_value()
        print(y_var_name, x_var_name)
        x = get_var(x_var_name)
        y = get_var(y_var_name)
        return x, y
#        else:
#            x = get_var(x_var_name)
#            y = get_var(y_var_name)
#            z = get_var(z_var_name)
#            return x, y, z

    def get_variables_string(self) -> str:
        return self.widgets_dic['vars'].get_value()

    def get_function_string(self) -> str:
        return self.widgets_dic['func'].get_value()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=6, height=4):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self):
        n = np.random.rand(100)
        data = np.sin(10 * n)
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_title('PyQt Matplotlib Example')
        ax.grid()
        ax.plot(data, 'r-')
        ax.plot(data, '*')


class CurveFitDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.initUI()

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        self.control_panel.client.shut_down()
        print('shut down!')
        super(CurveFitDialog, self).closeEvent(a0)

    def initUI(self):
        self.setWindowTitle('Pyminer Curve Fitting Tool')
        self.setGeometry(10, 10, 600, 400)
        self.outer_layout = QHBoxLayout()
        self.setLayout(self.outer_layout)
        self.control_layout = QVBoxLayout()

        m = PlotCanvas(self)
        self.outer_layout.addWidget(m)

        self.control_panel = ControlPanel()

        self.text_show = QTextBrowser()
        self.control_layout.addWidget(self.text_show)
        self.control_layout.addWidget(self.control_panel)
        self.text_show.setMinimumWidth(200)

        self.button_refresh = QPushButton('Fit')
        self.control_layout.addWidget(self.button_refresh)
        self.button_refresh.clicked.connect(self.fit)

        self.control_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.outer_layout.addLayout(self.control_layout)
        self.canvas = m
        self.figure = m.figure

    def showFitResult(self, popt, pcov, argsStr):
        st = ''
        stdevErr = np.sqrt(np.diag(pcov))
        print('stdevErr', stdevErr)

        argsList = argsStr.split(',')
        for i in range(len(popt)):
            st += '%s = %f, cov:%f\n' % (argsList[i], popt[i], stdevErr[i])
        print(pcov)
        self.reportStatus(st, 'result')

    def reportStatus(self, text: str, stat: str = 'result'):
        """
        报告状态或者其他信息。
        stat:error或者result两种选择。
        """
        if (stat == 'error'):
            l = text.split('\n')
            html = ''
            for st in l:
                st = st.strip()
                html += '<p style="color:red;">' + st + '</p>'
        elif stat == 'result':
            l = text.split('\n')
            html = ''
            for st in l:
                st = st.strip()
                print(st)
                html += '<p style="color:black;">' + st + '</p>'

        self.text_show.setHtml(html)

    def fit(self):
        """
        拟合时调用的方法
        """
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        try:
            x, y = self.control_panel.get_variables()  # np.array([1, 2, 3]), np.array([1.1, 1.8, 2.2])
            if self.control_panel.widgets_dic['func_type'].get_value() == 'customized':
                argsStr, funcStr = self.control_panel.get_variables_string(), self.control_panel.get_function_string()
            else:
                func: str = self.control_panel.get_value()['func_type']
                argsStr = algorithm.predefined_functions[func]['vars']
                funcStr = algorithm.predefined_functions[func]['function']
            result, message = algorithm.check_identifiers(argsStr, funcStr)
            if result == False:
                self.reportStatus(message, 'error')
                return
            popt, pcov, xvals, yvals = algorithm.fit(x, y, argsStr, funcStr)
            self.showFitResult(popt, pcov, argsStr)
            plot1 = ax.plot(x, y, 's', label='original values')
            argsor = np.argsort(xvals, axis=0)
            plot2 = ax.plot(xvals[argsor], yvals[argsor], 'r', label='fit values')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend(loc=4)  # 指定legend的位置右下角
            ax.set_title('curve_fit')
            ax.grid()

            self.canvas.draw()
            self.canvas.flush_events()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            e = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback.print_exc()
            st = ''
            for s in e:
                st += s


def run():
    global t0
    app = QApplication(sys.argv)
    ex = CurveFitDialog()
    ex.show()
    center_window(ex)
    print(time.time() - t0, 'start_time')
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
