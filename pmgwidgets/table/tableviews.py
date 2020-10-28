"""
这是一个利用QT的MVC架构进行数据查看的表格。这个表格十分适合大量数据的查看，1000*1000规模的数据集可以做到秒开。
其中定义了若干类。可以直接显示pd.DataFrame,np.array和list的TableView。

目前增加了切片索引查看功能和編輯功能。对dataframe而言，切片时可以编辑
但是array在切片的时候编辑。
"""
import sys

import typing
from PyQt5.QtWidgets import QTableView, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMessageBox, QInputDialog
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, pyqtSignal
from PyQt5.QtCore import Qt
import numpy as np

def to_decimal_str(cell_data: 'np.ndarray', decimals: int = 6):
    try:
        rounded_data = np.around(cell_data, decimals)
        return repr(rounded_data)
    except:
        return repr(cell_data)


def dataformat(val, decimals=6, sci=False):
    """
    这只是暂时的strformat函数。如有可能，应当使用cython重写并且部署在动态链接库中,从而提升性能。
    Args:
        val:
        decimals:
        sci:

    Returns:

    """
    global type_float_set
    return to_decimal_str(val, decimals)


class BaseAbstractTableModel(QAbstractTableModel):
    @property
    def default_slicing_statement(self):
        raise NotImplementedError


class TableModelForList(BaseAbstractTableModel):
    """
    输入为list的table model
    """

    def __init__(self, data: list):
        super(TableModelForList, self).__init__()
        self._data: np.ndarray = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return dataformat(self._data[index.row()][index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class TableModelForNumpyArray(BaseAbstractTableModel):
    """
    输入为pandas.DataFram的TableModel，用于在表格中显示数据。
    """

    def __init__(self, data):
        super(QAbstractTableModel, self).__init__()
        self._data = data
        self.horizontal_start: int = 0
        self.vertical_start: int = 0

    def setData(self, index: 'QModelIndex', value: object = None, role='Qt.EditRole'):
        """
        # View中编辑后，View会调用这个方法修改Model中的数据
        :param index:
        :param value:
        :param role:
        :return:
        """

        if index.isValid() and 0 <= index.row() < self._data.shape[0] and value:
            col = index.column()
            row = index.row()

            if len(self._data.shape) == 1:
                self.beginResetModel()
                self._data[row] = value
                self.dirty = True
                self.endResetModel()
                return True
            else:
                if 0 <= col < self._data.shape[1]:
                    self.beginResetModel()
                    self._data[row, col] = value
                    self.dirty = True
                    self.endResetModel()
                    return True
        return False

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if len(self._data.shape) >= 2:
                value = self._data[index.row(), index.column()]
            else:
                value = self._data[index.row()]
            return dataformat(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        if len(self._data.shape) == 1:
            return 1
        else:
            return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if role == Qt.DisplayRole:
                if orientation == Qt.Horizontal:
                    return str(self.horizontal_start + section)
                if orientation == Qt.Vertical:
                    return str(self.vertical_start + section)

    @property
    def default_slicing_statement(self):
        """
        默认切片数组
        :return:
        """
        data_dim = len(self._data.shape)
        if data_dim in (1, 2):

            return '[%s]' % (':,' * data_dim).strip(',')
        else:
            return '[%s]' % (':,:,' + '0,' * (data_dim - 2)).strip(',')


class TableModelForPandasDataframe(BaseAbstractTableModel):
    """
    输入为pandas.DataFram的TableModel，用于在表格中显示数据。
    """

    def __init__(self, data, original_data):
        super(QAbstractTableModel, self).__init__()
        self._data: 'pd.DataFrame' = data
        self.original_data = original_data

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

    @property
    def default_slicing_statement(self):
        """
        默认切片数组
        :return:
        """
        data_dim = len(self._data.shape)
        return '.iloc[%s]' % (':,' * data_dim).strip(',')

    def setData(self, index, value=None, role=Qt.EditRole):
        # 编辑后更新模型中的数据 View中编辑后，View会调用这个方法修改Model中的数据
        if index.isValid() and 0 <= index.row() < self._data.shape[0] and value:
            col = index.column()
            row = index.row()

            if 0 <= col < self._data.shape[1]:
                self.beginResetModel()
                col_label = self._data.columns[col]
                row_label = self._data.index[row]
                self.original_data.loc[row_label, col_label] = value
                self._data.loc[row_label, col_label] = value
                self.dirty = True
                self.endResetModel()
                return True
        return False


class PMTableView(QTableView):
    """
    基类，用于显示数据。输入数据类型为列表。
    """

    def __init__(self, data=None):
        super().__init__()
        self.data = None

        if data is not None:
            self.set_data(data)

    def set_data(self, data):
        self.data = data
        self.show_data(data)

    def show_data(self, data):
        import pandas as pd
        import numpy as np
        if isinstance(data, pd.DataFrame):
            self.model = TableModelForPandasDataframe(data, self.data)
        elif isinstance(data, np.ndarray):
            self.model = TableModelForNumpyArray(data)
        elif isinstance(data, list):
            self.model = TableModelForList(data)
        else:
            raise Exception("data type %s is not supported in PMTableView.\
                            \n Supported Types are: numpy.array,list and pandas.DataFrame." % type(data))
        self.setModel(self.model)

    def get_default_slicing_statement(self):
        return self.model.default_slicing_statement

    # def currentChanged(self, current: 'QModelIndex', previous: 'QModelIndex') -> None:
    #     self.edit(current)

    def mouseDoubleClickEvent(self, e: 'QMouseEvent') -> None:

        index = self.currentIndex()
        curr_data = self.model.data(index, role=Qt.DisplayRole)

        input_dialog = QInputDialog(self)
        input_dialog.setTextValue(curr_data)
        input_dialog.exec_()
        text = input_dialog.textValue()
        try:
            try:
                if text.find('.'):
                    val = float(text)
                else:
                    val = int(text)
            except:
                val = str(text)
        except:
            import traceback
            traceback.print_exc()
            return

        self.model.setData(index, val)
        # self.set_data(self.model._data)


class PMGTableViewer(QWidget):
    """
    一个含有QTableView的控件。
    """
    data_modified_signal = pyqtSignal()

    def __init__(self, parent=None, table_view: 'PMTableView' = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.top_layout = QHBoxLayout()
        self.layout().addLayout(self.top_layout)
        self.table_view = table_view
        self.slice_input = QLineEdit()

        self.slice_refresh_button = QPushButton(self.tr('Slice'))
        self.save_change_button = QPushButton(self.tr('Save'))
        self.save_change_button.clicked.connect(self.data_modified_signal.emit)
        self.slice_refresh_button.clicked.connect(self.slice)
        self.top_layout.addWidget(self.slice_input)
        self.top_layout.addWidget(self.slice_refresh_button)
        self.top_layout.addWidget(self.save_change_button)
        if table_view is not None:
            self.layout().addWidget(self.table_view)

    def set_data(self, data: object) -> None:
        """
        set_data方法在初次调用时，设置其内部的data参数；
        当后面调用的时候，不会更改内部的data参数。
        get_default_slicing_statement的意思是可以获取默认的切片索引。
        这是因为表格一般只能显示二维的数据，当数组维数超过二维的时候，就需要尽可能地利用切片进行显示了。
        比如对于四维np.array张量，返回的默认就是[:,:,0,0]。用户可以根据自己的需要进行切片。
        :param data:
        :return:
        """
        if self.table_view is not None:
            self.table_view.set_data(data)
            self.slice_input.setText(self.table_view.get_default_slicing_statement())
            self.slice()

    def get_data(self):
        return self.table_view.data

    def slice(self):
        """
        切片操作。同时屏蔽可能出现的非法字符。
        目前做不到对array数组进行索引。
        :return:
        """
        data = self.table_view.data
        text = self.slice_input.text().strip()
        for char in text:
            if not char in "[]:,.1234567890iloc":
                QMessageBox.warning(self, self.tr('Invalid Input'),
                                    self.tr("invalid character \"%s\" in slicing statement." % char))
                return
        try:
            data = eval('data' + text)
        except Exception as e:

            QMessageBox.warning(self, self.tr('Invalid Input'),
                                self.tr(str(e)))

        self.table_view.show_data(data)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        super().closeEvent(a0)



if __name__ == '__main__':
    import pandas as pd

    app = QApplication(sys.argv)
    table = PMGTableViewer(table_view=PMTableView())

    data = np.random.random((5, 3, 3, 3))
    data = pd.DataFrame(np.random.random((5, 3)))
    table.show()

    table.set_data(data)

    app.exec_()
