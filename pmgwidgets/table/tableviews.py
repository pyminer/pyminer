'''
这是一个利用QT的MVC架构进行数据查看的表格。这个表格十分适合大量数据的查看，1000*1000规模的数据集可以做到秒开。
其中定义了若干类。可以直接显示pd.DataFrame,np.array和list的TableView。
'''
import sys
import time

import typing
from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
import numpy as np


def to_decimal_str(cell_data: 'np.ndarray', decimals: int = 6):
    try:
        rounded_data = np.around(cell_data,decimals)
        return repr(rounded_data)
    except:
        return repr(cell_data)


def dataformat(val, decimals=6, sci=False):
    '''
    这只是暂时的strformat函数。如有可能，应当使用cython重写并且部署在动态链接库中,从而提升性能。
    Args:
        val:
        decimals:
        sci:

    Returns:

    '''
    global type_float_set
    return to_decimal_str(val,decimals)
    value_str = repr(val)

    if hasattr(val, 'dtype'):
        if np.issubdtype(val, np.inexact):
            if not sci:
                return str(np.around(val, decimals=decimals))
            else:
                return '%e' % np.around(val, decimals=decimals)
    elif isinstance(val, int):
        if sci:
            return '%e' % val
        return str(val)
    elif isinstance(val, float):
        if sci:
            return '%e' % round(val, decimals)
        return str(val)
    elif isinstance(val, complex):
        if sci:
            return '%e+%ej' % (round(val.real), round(val.imag))
        else:
            return '%f+%fj' % (round(val.real), round(val.imag))
    else:
        return str(val)


class TableModelForList(QAbstractTableModel):
    '''
    输入为list的table model
    '''

    def __init__(self, data: list):
        super(TableModelForList, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return dataformat(self._data[index.row()][index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class TableModelForNumpyArray(QAbstractTableModel):
    '''
    输入为pandas.DataFram的TableModel，用于在表格中显示数据。
    '''

    def __init__(self, data):
        super(QAbstractTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row(), index.column()]
            return dataformat(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]


class TableModelForPandasDataframe(QAbstractTableModel):
    '''
    输入为pandas.DataFram的TableModel，用于在表格中显示数据。
    '''

    def __init__(self, data):
        super(QAbstractTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return dataformat(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if role == Qt.DisplayRole:
                if orientation == Qt.Horizontal:
                    return str(self._data.columns[section])
                if orientation == Qt.Vertical:
                    return str(self._data.index[section])


class PMTableView(QTableView):
    '''
    基类，用于显示数据。输入数据类型为列表。
    '''

    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            self.set_data(data)

    def set_data(self, data):
        import pandas as pd
        import numpy as np
        if isinstance(data, pd.DataFrame):
            self.model = TableModelForPandasDataframe(data)
        elif isinstance(data, np.ndarray):
            self.model = TableModelForNumpyArray(data)
        elif isinstance(data, list):
            self.model = TableModelForList(data)
        else:
            raise Exception("data type %s is not supported in PMTableView.\
                            \n Supported Types are: numpy.array,list and pandas.DataFrame." % type(data))
        self.setModel(self.model)


if __name__ == '__main__':
    import pandas as pd

    app = QApplication(sys.argv)
    table = PMTableView()
    import numpy as np

    data = pd.DataFrame(np.random.random((1000, 1000)), columns=['a' + str(i) for i in range(1000)],
                        index=['row' + str(i) for i in range(1000)])
    table.show()
    table.set_data(data.values)

    app.exec_()
