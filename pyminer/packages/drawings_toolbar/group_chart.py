"""
生成组合图前变量选择
"""
import sys
from PySide2.QtWidgets import QDialog, QPushButton, QComboBox, QApplication, QLabel, QSizePolicy
from matplotlib import rcParams, use
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

use('Qt5Agg')


class MatplotlibWidget(FigureCanvas):
    """
    Implements a Matplotlib figure inside a QWidget.
    Use getFigure() and redraw() to interact with matplotlib.

    Example::

        mw = MatplotlibWidget()
        subplot = mw.getFigure().add_subplot(111)
        subplot.plot(x,y)
        mw.draw()
    """

    def __init__(self, parent=None, size=(5, 4), dpi=100):
        rcParams['font.family'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        self.fig = Figure(figsize=size, dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def get_figure(self):
        return self.fig


class DialogGroup(QDialog):
    def __init__(self, parent=None):
        super(DialogGroup, self).__init__(parent)
        self.setWindowTitle('组合图设置')
        self.resize(450, 530)
        self.lbl1 = QLabel(self)
        self.lbl1.setText('绘制折线图的变量:')
        self.lbl1.move(20, 30)
        self.draw_line_widget = MatplotlibWidget(self)
        self.draw_line_widget.move(25, 55)
        self.draw_line_widget.resize(400, 190)
        self.draw_bar_widget = MatplotlibWidget(self)
        self.draw_bar_widget.move(25, 285)
        self.draw_bar_widget.resize(400, 190)
        self.lbl2 = QLabel(self)
        self.lbl2.setText('绘制柱状图的变量:')
        self.lbl2.move(20, 260)
        self.cb_select1 = QComboBox(self)
        self.cb_select1.move(155, 26)
        self.cb_select2 = QComboBox(self)
        self.cb_select2.move(155, 256)
        self.btn_combin = QPushButton('组合绘图', self)
        self.btn_combin.move(260, 490)
        self.btn_quit = QPushButton('取消', self)
        self.btn_quit.move(350, 490)
        self.btn_quit.clicked.connect(self.close)
        self.lbl_mess = QLabel(self)
        self.lbl_mess.setFixedWidth(200)
        self.lbl_mess.setStyleSheet('color:red')
        self.lbl_mess.move(20, 500)
        self.cb_select1.currentIndexChanged.connect(self.dial_cb_changed)
        self.cb_select2.currentIndexChanged.connect(self.dial_cb_changed)

    def dial_cb_changed(self):
        line_var_name = self.cb_select1.currentText()
        bar_var_name = self.cb_select2.currentText()
        if line_var_name == bar_var_name:
            self.lbl_mess.setText('建议选择两个不一样的变量')
            self.cb_select2.setFocus()
        else:
            self.lbl_mess.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DialogGroup()
    demo.cb_select1.addItems(['j', 'b'])
    demo.cb_select2.addItems(['j', 'b'])
    ax = demo.draw_line_widget.axes
    ax.plot([1, 2, 3, 4])
    demo.draw_line_widget.draw()
    ax1 = demo.draw_bar_widget.axes
    ax1.bar([1,2,3,4],[2,5,4,3])
    demo.draw_bar_widget.draw()
    demo.show()
    sys.exit(app.exec_())
