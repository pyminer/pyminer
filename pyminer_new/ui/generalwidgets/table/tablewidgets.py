# 通用表格控件
# 作者：侯展意
# 带有加载数据集等等的功能，相对来讲比较方便。
# 所有的控件都是以PMG作为名字开头的。名字开头普
import profile
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView


class Grid():
    def __init__(self, master):
        super().__init__(master)

    def set_data(self, data):
        columns = [''] + list(data.columns.values)

        self.set_widgets(columns)
        self.treeview.bind('<ButtonRelease-1>', self.treeview_click)
        for col in columns:
            self.treeview.column(col, anchor="center")
            self.treeview.heading(col, text=col)

        for i in range(data.shape[0]):
            row = data.iloc[i]
            # print(row[0],list(row))
            self.treeview.insert('', i, values=[i] + list(row))
            i += 1

    def treeview_click(event):  # 单击
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)

    def selectTree(event):
        for item in tree.selection():
            item_text = tree.item(item, "values")
            print(item_text)


class MGrid():
    def __init__(self, parent=None, autofit=False):
        ttk.Frame.__init__(self, parent)
        ##        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        ##
        ##        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        sizer = ttk.Frame(self)  # wx.BoxSizer( wx.VERTICAL )
        sizer.pack(expand=True, fill=tk.BOTH)
        self.lab_info = ttk.Label(sizer, text='information')
        self.lab_info.pack()

        ##        self.Bind(wx.EVT_IDLE, self.on_idle)
        ##        sizer.Add( self.lab_info, 0, wx.EXPAND, 0 )
        ##
        self.grid = Grid(self)
        self.grid.pack(fill=tk.BOTH, expand=True)
        ##        sizer.Add( self.grid, 1, wx.EXPAND |wx.ALL, 0 )
        ##        self.SetSizer(sizer)
        self.select = self.grid.select
        self.set_data = self.grid.set_data

    @property
    def table(self):
        return self.grid.table

    @property
    def name(self):
        return self.grid.table.name

    def on_idle(self, event):
        if self.table.data is None: return
        if self.lab_info.GetLabel() != self.table.info:
            self.lab_info.SetLabel(self.table.info)


class GridFrame():
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        sizer = ttk.Frame(self)
        sizer.pack(expand=True, fill=tk.BOTH)
        self.grid = MGrid(sizer)
        self.set_data = self.grid.set_data

    ##        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_idle(self, event):
        if self.GetTitle() != self.grid.table.name:
            self.SetTitle(self.grid.table.name)

    def set_title(self, tab): self.SetTitle(tab.name)

    def on_valid(self, event): event.Skip()

    def on_close(self, event): event.Skip()

    def Show(self):
        self.Fit()
        wx.Frame.Show(self)


class PMGTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setRowCount(10)
        self.setColumnCount(3)
        self.set_widgets()

    def set_widgets(self):
        self.setRowCount(10000)
        self.setColumnCount(10)
        for i in range(10000):
            for j in range(10):
                self.setItem(i, j, QTableWidgetItem(''))

    def set_data(self, data):  # 传统算法，大约需要0.1秒时间进行处理。100*100的数据.
        print(t0 := time.time())
        # 获取已经导入页面获取的数据集
        self.setColumnCount(len(data.columns))
        self.setRowCount(len(data.index))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        s = data.columns.values.tolist()  # 不创建新的list对象，直接在原对象上面进行操作，可以起到加速作用。
        for i, s0 in enumerate(s):
            s[i] = str(s0)
        self.setHorizontalHeaderLabels(s)

        # 以下将循环中用到的全局变量改做局部变量。这样可以减小开销。以10000行10列表格为例，原函数大约需要1.45~1.5秒，
        # 这样处理之后,可以稳定在1.4秒以下。

        data_iat = data.iat  # 将其引用作为局部变量，速度会快一些。
        int2str = str  # 引用作为局部变量，可能加速。
        table_set_item = self.setItem
        # Table_widget_item = QTableWidgetItem
        item = self.item
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                # print(i, j, self.item(i, j))
                item(i, j).setText(int2str(data_iat[i, j]))
                # table_set_item(i, j, QTableWidgetItem(int2str(data_iat[i, j])))

        print(time.time() - t0)

        # for i in range(len(data.index)):
        #     for j in range(len(data.columns)):
        #         self.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))
        # print(time.time() - t0)

        # for x in range(self.tableWidget_dataset.columnCount()):
        #     headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
        #
        #     headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


class PMGTableTabWidget(QTabWidget):
    def __init__(self):
        super(PMGTableTabWidget, self).__init__()
        self.tab1 = PMGTable()  # 1
        self.tab2 = QWidget()
        self.tab3 = QTextEdit()

        # self.tab1_init()  # 2
        self.tab2_init()

        self.addTab(self.tab1, 'Basic Info')  # 3
        self.addTab(self.tab2, 'Contact Info')
        self.addTab(self.tab3, QIcon('info.ico'), 'More Info')

        self.currentChanged.connect(lambda: print(self.currentIndex()))  # 4

    def tab2_init(self):
        tel_label = QLabel('Tel:', self.tab2)
        mobile_label = QLabel('Mobile:', self.tab2)
        add_label = QLabel('Address:', self.tab2)

        tel_line = QLineEdit(self.tab2)
        mobile_line = QLineEdit(self.tab2)
        add_line = QLineEdit(self.tab2)

        g_layout = QGridLayout()
        g_layout.addWidget(tel_label, 0, 0, 1, 1)
        g_layout.addWidget(tel_line, 0, 1, 1, 1)
        g_layout.addWidget(mobile_label, 1, 0, 1, 1)
        g_layout.addWidget(mobile_line, 1, 1, 1, 1)
        g_layout.addWidget(add_label, 2, 0, 1, 1)
        g_layout.addWidget(add_line, 2, 1, 1, 1)

        self.tab2.setLayout(g_layout)


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    import cProfile

    from line_profiler import LineProfiler

    app = QApplication(sys.argv)

    n = 10000
    a = pd.DataFrame(np.random.random((n, 10)))

    demo = PMGTableTabWidget()
    # demo.tab1.set_data(a)

    # demo.tab1.clear()
    # demo.tab1.set_data_traditional(a)
    # demo.tab1.clear()
    # demo.tab1.set_data(a)

    # 这里使用vsm模型进行测试
    demo.tab1.set_data(a)
    # lp = LineProfiler()
    # lp_vsm = lp(demo.tab1.set_data)
    # lp_vsm(a)
    # lp.print_stats()
    demo.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     from scitk.grid.grid import Grid
#     import pandas as pd
#     import numpy as np
#
#     window = tk.Tk()
#     gnf = GridNoteFrame(window)
#     nb = gnf.notebook
#     grid2 = Grid(nb)
#     nb.add_grid(Grid(nb))
#     nb.add_grid(grid2)
#     nb.add_grid(Grid(nb))
#     nb.add_grid(Grid(nb))
#     nb.delete_tab('current')
#     nb.grid(1).set_data(pd.DataFrame(np.random.randn(100, 5) * 100))
#     window.mainloop()
