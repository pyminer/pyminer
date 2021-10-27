from typing import Dict, Any
import time
t0 = time.time()
from widgets import BaseClient

from widgets.widgets.composited.buttonpanel import PMGButtonPanel

from widgets.widgets.composited.generalpanel import PMGPanel, PANEL_VIEW_CLASS
from utils.ui.variableselect import VariableSelect
from PySide2.QtWidgets import QWidget, QApplication, QGridLayout
t5 = time.time()

class PMApp(QWidget):
    """
    plot_widget:绘图控件

    """

    def __init__(self, parent=None, params: PANEL_VIEW_CLASS = None,
                 data_type_filter: str = '', title: str = ''):

        super().__init__(parent=parent)
        
        
        self.setFixedSize(800, 600)
        
        from packages.pmagg import PMAgg
        self.setWindowTitle(title)
        t0 = time.time()
        self.plot_widget = PMAgg.Window()
        print('init_time',time.time()-t0)
        # plt.plot([1, 2, 3, 6, 4], [1, 2, 3, 4, 5])
        # fig = plt.gcf()
        # self.plot_widget.get_canvas(fig)

        # splitter = QSplitter(self)
        self.settings_panel = PMGPanel(views=params)
        # splitter.addWidget(self.plot_widget)
        # splitter.addWidget(self.settings_panel)
        # self.setLayout(QHBoxLayout())
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # QGridLayout.addWidget()
        self.layout().addWidget(self.plot_widget, 0, 0, 2, 1)
        # right_layout = QVBoxLayout()
        self.button_panel = PMGButtonPanel()

        self.var_sel_panel = VariableSelect(type_filter=data_type_filter)
        self.layout().addWidget(self.var_sel_panel, 0, 1, 1, 1)
        self.layout().addWidget(self.settings_panel, 1, 1, 1, 1)
        self.layout().addWidget(self.button_panel, 2, 1, 1, 1)
        
#         self._init_style_sheet()
        
    def calc(self):
        pass

    def get_params(self) -> Dict[str, Any]:
        return self.settings_panel.get_value()

    def get_variable(self):
        return self.var_sel_panel.get_variable()

    def get_variable_name(self) -> str:
        return self.var_sel_panel.get_current_variable_name()

    def pmagg_add_chart(self, draw_func):
        def wrapper():
            import matplotlib.pyplot as plt
            plt.clf()
            draw_func()

            fig = plt.gcf()
            print(fig)

            self.plot_widget.get_canvas(fig)

        return wrapper

    def _init_style_sheet(self):
        try:
            import time
            
            style_sheet = BaseClient().get_style_sheet()
            
            self.setStyleSheet('')
            t0 = time.time()
            self.plot_widget.setStyleSheet(style_sheet)
            t1  = time.time()
            print(t1-t0,'style_sheet_init_time')
        except:
            import traceback
            traceback.print_exc()


def figure_to_pmagg(draw_func):
    def outer_wrapper(self):
        def wrapper():
            import matplotlib.pyplot as plt
            plt.clf()
            draw_func()
            fig = plt.gcf()
            self.plot_widget.get_canvas(fig)

        return wrapper()

    return outer_wrapper

print(t5-t0,'import and load time')

if __name__ == '__main__':
    def draw():
        import matplotlib.pyplot as plt
        from packages.pmagg import PMAgg
        global a
        plt.clf()
        data = [1, 2, 3, 2, 1, 2, 3, 1, 2, 3, 1, 100, 34]
        p = plt.boxplot(data)
        fig = plt.gcf()
        print(p['fliers'][0].get_xdata(), p['fliers'][0].get_ydata())
        a.plot_widget.get_canvas(fig)

    
    app = QApplication.instance()#([])
    t01 = time.time()
    a = PMApp(params=[
        # ('combo_ctrl', 'var_name', '选择变量', '', ['']),
        # ('combo_ctrl', 'series', '选择系列', ''),
        ('check_ctrl', 'check', '检查', True),

    ], title='缺失值检查')
    t2 = time.time()
    btn = a.button_panel.add_button('计算')
    # bind_combo_with_workspace(a.settings_panel.get_ctrl('series').ctrl)
    a.show()
    
    draw()
    
    btn.clicked.connect(draw)
    t1 = time.time()
    print('all_time',t1-t0,'objtime',t2-t01)
    app.exec_()
