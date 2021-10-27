"""
这是一个利用QT的MVC架构进行数据查看的表格。这个表格十分适合大量数据的查看，1000*1000规模的数据集可以做到秒开。
其中定义了若干类。可以直接显示pd.DataFrame,np.array和list的TableView。

目前增加了切片索引查看功能和編輯功能。对dataframe而言，切片时可以编辑
但是array在切片的时候编辑。

作者：侯展意
"""
import os
import sys

import typing
import logging
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QSpacerItem, QComboBox, QSpinBox, QLabel
from PySide2.QtWidgets import QTableView, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMessageBox, QInputDialog, QMenu, QDialog, QDialogButtonBox, QShortcut, QSizePolicy
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Signal, QLocale, QCoreApplication
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QContextMenuEvent, QKeyEvent, QKeySequence

from widgets.utilities.source.translation import create_translator
from widgets.widgets.basic.dialogs.textdialog import TextShowDialog

if typing.TYPE_CHECKING:
    import numpy as np

logger = logging.getLogger(__name__)


class InputValueDialog(QDialog):
    UP = -1
    DOWN = 1
    signal_move_cursor = Signal(int)
    signal_edit_finished = Signal(str)

    def __init__(self, parent):
        super(InputValueDialog, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.edit = QLineEdit()
        self.layout().addWidget(self.edit)
        self.edit.returnPressed.connect(self.edit_finished)
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.button_box)
        self.button_box.rejected.connect(self.close)
        self.button_box.accepted.connect(self.edit_finished)

    def edit_finished(self):
        self.close()
        self.signal_edit_finished.emit(self.edit.text())

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Up:
            self.close()
            self.signal_move_cursor.emit(self.UP)
            e.accept()
        elif e.key() == Qt.Key_Down:
            self.close()
            self.signal_move_cursor.emit(self.DOWN)
            e.accept()

        super(InputValueDialog, self).keyPressEvent(e)


def to_decimal_str(cell_data: 'np.ndarray', decimals: int = 6):
    import numpy as np
    try:
        rounded_data = np.around(cell_data, decimals)
        return repr(rounded_data)
    except:
        return str(cell_data)


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
        import numpy as np
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
        super(TableModelForNumpyArray, self).__init__()
        self._data = data
        self.horizontal_start: int = 0
        self.vertical_start: int = 0

    def setData(self, index: 'QModelIndex', value: typing.Any = None, role='Qt.EditRole'):
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

            if len(self._data.shape) == 1:  # 一维矩阵
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
                value = self._data[index.column()]
            return dataformat(value)

    def rowCount(self, index):
        if len(self._data.shape) >= 2:
            return self._data.shape[0]
        else:
            return 1
        # return self._data.shape[0]

    def columnCount(self, index):
        if len(self._data.shape) == 1:
            return self._data.shape[0]
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
        super(TableModelForPandasDataframe, self).__init__()
        self._data: 'pd.DataFrame' = data
        self.original_data = original_data
        self.colors = {'int': QColor(0, 0, 128, 100), 'bool': QColor(0, 200, 200, 100),
                       'float': QColor(0, 64, 128, 100), 'str': QColor(200, 200, 0, 100),
                       'timestamp': QColor(0, 200, 0, 100),
                       'complex': QColor(100, 0, 128, 100)
                       }

    def get_color(self, data):
        import numpy as np
        import pandas as pd
        if isinstance(data, (np.bool_, bool)):
            return self.colors['bool']
        elif isinstance(data, (np.integer, int)):
            return self.colors['int']
        elif isinstance(data, (np.inexact, float)):
            if isinstance(data, np.complex_):
                return self.colors['complex']
            return self.colors['float']
        elif isinstance(data, (str)):
            return self.colors['str']
        elif isinstance(data, (pd.Timestamp)):
            return self.colors['timestamp']
        elif data == np.nan:
            return QColor(0, 0, 50, 100)
        elif data == pd.NaT:
            return QColor(0, 50, 0, 100)

        return QColor(0, 0, 0, 80)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return dataformat(value)
        if role == Qt.BackgroundRole:
            data = self._data.iloc[index.row(), index.column()]
            return self.get_color(data)

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
    INSERT_ROW = 0
    DELETE_ROW = 1
    INSERT_COLUMN = 2
    DELETE_COLUMN = 3

    signal_need_save = Signal(bool)

    def __init__(self, data=None):
        super().__init__()
        self.translator = create_translator(
            path=os.path.join(os.path.dirname(__file__), 'translations',
                              'qt_{0}.qm'.format(QLocale.system().name())))  # translator
        self.data = None
        self.menu = QMenu()
        self.action_insert_row = self.menu.addAction(QCoreApplication.translate('PMTableView', 'Insert Row'))
        self.action_insert_row.triggered.connect(lambda: self.on_change_row_col(self.INSERT_ROW))
        self.action_delete_row = self.menu.addAction(QCoreApplication.translate('PMTableView', 'Delete Row'))
        self.action_delete_row.triggered.connect(lambda: self.on_change_row_col(self.DELETE_ROW))
        self.action_insert_col = self.menu.addAction(QCoreApplication.translate('PMTableView', 'Insert Column'))
        self.action_insert_col.triggered.connect(lambda: self.on_change_row_col(self.INSERT_COLUMN))
        self.action_delete_col = self.menu.addAction(QCoreApplication.translate('PMTableView', 'Delete Column'))
        self.action_delete_col.triggered.connect(lambda: self.on_change_row_col(self.DELETE_COLUMN))
        # self.menu.addAction("aaaaaa")
        if data is not None:
            self.set_data(data)

    def on_change_row_col(self, operation: int):
        """
        The slot for editting row or columns
        Args:
            operation:

        Returns:

        """
        import pandas as pd
        import numpy as np
        pd_data: pd.DataFrame = self.model._data
        current_index = self.currentIndex()
        row, column = current_index.row(), current_index.column()
        if operation == self.INSERT_ROW:
            prev = pd_data.iloc[:row]
            lat = pd_data.iloc[row:]
            self.model._data = pd.concat([prev, pd.DataFrame([[]]), lat])
        elif operation == self.DELETE_ROW:
            prev = pd_data.iloc[:row]
            lat = pd_data.iloc[row + 1:]
            self.model._data = pd.concat([prev, lat])
        elif operation == self.INSERT_COLUMN:
            col_name: str = ''
            col_name, _ = QInputDialog.getText(self, QCoreApplication.translate('PMTableView', 'Input Column Title'),
                                               QCoreApplication.translate('PMTableView', 'Title'))
            if _:
                if col_name.isdigit():
                    col_name = int(col_name)
                    # if col_name in pd_data.columns:
                    #     QMessageBox.warning(self, QCoreApplication.translate("PMTableView", "Warning"),
                    #                     QCoreApplication.translate("PMTableView",
                    #                                                "Input value was integer, however the value will be converted to string." % col_name))
                    #     return
                try:
                    pd_data.insert(column, col_name, np.nan)
                except ValueError:
                    QMessageBox.warning(self, QCoreApplication.translate("PMTableView", "Error"),
                                        QCoreApplication.translate("PMTableView",
                                                                   "Column name \'%s\', type\'%s\' duplicated with existing column!" % (
                                                                       col_name, type(col_name))))

        elif operation == self.DELETE_COLUMN:
            # prev = pd_data.iloc[:row]
            # lat = pd_data.iloc[row + 1:]
            # self.model._data = pd.concat([prev, lat])
            self.model._data = pd_data.drop(columns=[column], axis=0)
        else:
            raise NotImplementedError
        self.model.layoutChanged.emit()
        self.signal_need_save.emit(True)

    def set_data(self, data):
        self.data = data
        self.show_data(data)

    def get_data(self):
        return self.model._data

    def show_data(self, data):
        """
        data可能是self.data，也可能是self.data的一部分。
        Args:
            data:

        Returns:

        """
        import pandas as pd
        import numpy as np
        if isinstance(data, pd.DataFrame):
            self.model = TableModelForPandasDataframe(data, self.data)
        elif isinstance(data, np.ndarray):
            self.model = TableModelForNumpyArray(data)
            self.menu.setEnabled(False)
        elif isinstance(data, list):
            self.model = TableModelForList(data)
            self.menu.setEnabled(True)
        else:
            raise Exception("data type %s is not supported in PMTableView.\
                            \n Supported Types are: numpy.array,list and pandas.DataFrame." % type(data))
        self.setModel(self.model)

    def get_default_slicing_statement(self):
        return self.model.default_slicing_statement

    def mouseDoubleClickEvent(self, event: 'QMouseEvent') -> None:
        """
        Args:
            event:

        Returns:

        """
        super().mouseDoubleClickEvent(event)
        self.show_edit_dialog(self.currentIndex().row(), self.currentIndex().column())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super(PMTableView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.show_edit_dialog(self.currentIndex().row(), self.currentIndex().column())

    def show_edit_dialog(self, row, col):
        import pandas as pd
        import numpy as np
        data = self.model._data
        if isinstance(data, (pd.DataFrame, np.ndarray)):
            def on_edited(text):
                from pandas import Timestamp, Period, Interval
                try:
                    result = eval(text)
                    if isinstance(data, pd.DataFrame):
                        data.iloc[row, col] = result
                    elif isinstance(data, np.ndarray):
                        data[row, col] = result
                    self.signal_need_save.emit(True)
                except:
                    import traceback
                    QMessageBox.warning(self, QCoreApplication.translate('PMTableView', 'Warning'),
                                        traceback.format_exc())
                    return

            def on_move_current_cell(direction: int):
                target_row = row + direction
                if 0 <= target_row < self.model.rowCount(col):
                    self.setCurrentIndex(self.model.index(target_row, col))
                    self.show_edit_dialog(target_row, col)

            if isinstance(data, pd.DataFrame):
                original_data = data.iloc[row, col]
            elif isinstance(data, np.ndarray):
                original_data = data[row, col]
            else:
                raise NotImplementedError

            dlg = InputValueDialog(self)
            dlg.setWindowTitle(QCoreApplication.translate('PMTableView', 'Input New Value'))
            dlg.edit.setText(repr(original_data))
            dlg.signal_edit_finished.connect(on_edited)
            dlg.signal_move_cursor.connect(on_move_current_cell)
            global_pos = self.mapToGlobal(
                QPoint(self.columnViewportPosition(col) + 50, self.rowViewportPosition(row) + 50))
            dlg.setGeometry(global_pos.x(), global_pos.y(), dlg.width(), dlg.height())
            dlg.exec_()
            # QInputDialog.getText(self, QCoreApplication.translate('PMTableView','Input New Value'), '', QLineEdit.Normal,
            # text=repr(original_data))

    def contextMenuEvent(self, event: QContextMenuEvent):
        import pandas as pd
        if isinstance(self.model._data, pd.DataFrame):
            self.menu.exec_(event.globalPos())

    def on_goto_index(self, row: int, col: int = 0):
        import pandas as pd
        import numpy as np

        if isinstance(self.data, (pd.DataFrame, np.ndarray)):
            assert 0 <= row <= self.model.rowCount(None)
        self.setCurrentIndex(self.model.index(row, col))


class PMGTableViewer(QWidget):
    """
    一个含有QTableView的控件。
    有切片和保存两个按钮。点击Slice的时候可以切片查看，点击Save保存。
    """
    data_modified_signal = Signal()
    signal_need_save = Signal(bool)

    def __init__(self, parent=None, table_view: 'PMTableView' = None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        self.top_layout = QHBoxLayout()
        self.layout().addLayout(self.top_layout)
        self.table_view = table_view
        self.slice_input = QLineEdit()
        self.help_button = QPushButton(QCoreApplication.translate('PMGTableViewer', '帮助'))
        self.slice_refresh_button = QPushButton(QCoreApplication.translate('PMGTableViewer', '切片'))
        self.save_change_button = QPushButton(QCoreApplication.translate('PMGTableViewer', '保存'))
        self.goto_cell_button = QPushButton(QCoreApplication.translate('PMGTableViewer', '前往单元格'))

        self.label_slice_axis2 = QLabel("高度索引：")

        self.slice_axis2 = QSpinBox()
        self.slice_axis2.setMinimum(0)
        self.slice_axis2.setSingleStep(1)
        self.slice_axis2.setMaximum(0)
        self.slice_axis2.valueChanged.connect(self.on_axis2_value_changed)

        self.save_change_button.clicked.connect(self.on_save)
        self.slice_refresh_button.clicked.connect(self.slice)
        self.help_button.clicked.connect(self.on_help)
        self.goto_cell_button.clicked.connect(self.on_goto_cell)
        self.slice_input.hide()
        self.slice_refresh_button.hide()

        self.table_view.signal_need_save.connect(self.signal_need_save.emit)
        self.signal_need_save.connect(self.on_signal_need_save)

        self.top_layout.addWidget(self.label_slice_axis2)
        self.top_layout.addWidget(self.slice_axis2)

        self.label_slice_axis2.hide()
        self.slice_axis2.hide()

        self.top_layout.addWidget(self.goto_cell_button)
        self.top_layout.addWidget(self.save_change_button)
        self.top_layout.addWidget(self.help_button)
        self.top_layout.addWidget(self.slice_input)
        self.top_layout.addWidget(self.slice_refresh_button)
        self.top_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        if table_view is not None:
            self.layout().addWidget(self.table_view)

        self.shortcut_save = QShortcut(QKeySequence.Save, self.table_view, context=Qt.WidgetShortcut)
        self.shortcut_save.activated.connect(self.on_save)

        self.shortcut_goto = QShortcut(QKeySequence('Ctrl+G'), self.table_view, context=Qt.WidgetShortcut)
        self.shortcut_goto.activated.connect(self.on_goto_cell)

    def on_axis2_value_changed(self):
        """
        当显示多维数组时，如果改变第三维的索引，就调用这个函数
        Returns:

        """
        import numpy as np
        if isinstance(self.table_view.data, np.ndarray):
            if len(self.table_view.data.shape) > 2:
                self.table_view.show_data(self.table_view.data[self.slice_axis2.value(), :, :])

    def on_high_dimensional_array(self, high_dimensional: bool):
        self.label_slice_axis2.setVisible(high_dimensional)
        self.slice_axis2.setVisible(high_dimensional)

    def on_help(self):
        dlg = TextShowDialog(title=QCoreApplication.translate('PMGTableViewer', '帮助'))
        with open(os.path.join(os.path.dirname(__file__), 'help', 'help.md'), 'r', encoding='utf8',
                  errors='replace') as f:
            dlg.set_markdown(f.read())
        dlg.exec_()

    def on_signal_need_save(self, need_save: str):
        title = self.windowTitle()
        if need_save:
            if not title.startswith('*'):
                self.setWindowTitle('*' + title)
        else:
            if title.startswith('*'):
                self.setWindowTitle(title.strip('*'))

    def on_save(self):
        self.signal_need_save.emit(False)
        self.data_modified_signal.emit()

    def set_data(self, data: typing.Any) -> bool:
        """
        set_data方法在初次调用时，设置其内部的data参数；
        当后面调用的时候，不会更改内部的data参数。
        get_default_slicing_statement的意思是可以获取默认的切片索引。
        这是因为表格一般只能显示二维的数据，当数组维数超过二维的时候，就需要尽可能地利用切片进行显示了。
        比如对于四维np.array张量，返回的默认就是[:,:,0,0]。用户可以根据自己的需要进行切片。
        :param data:
        :return:
        """
        import numpy as np
        if isinstance(data, np.ndarray):
            if len(data.shape) > 3:
                QMessageBox.warning(self, "提示", "目前只支持三维及以下数组的查看")
                return False
            elif len(data.shape) == 3:
                self.slice_axis2.setMaximum(data.shape[0] - 1)
            self.on_high_dimensional_array(len(data.shape) == 3)

        if self.table_view is not None:
            self.table_view.set_data(data)
            self.slice_input.setText(self.table_view.get_default_slicing_statement())

        if isinstance(data, np.ndarray):
            if len(data.shape) > 2:
                self.on_axis2_value_changed()  # 如果维度小于3，则默认进行以下切片操作。
        return True

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
                QMessageBox.warning(self, QCoreApplication.translate('PMGTableViewer', 'Invalid Input'),
                                    QCoreApplication.translate('PMGTableViewer',
                                                               "invalid character \"%s\" in slicing statement.") % char)
                return
        try:
            data = eval('data' + text)
        except Exception as exeption:

            QMessageBox.warning(self, QCoreApplication.translate('PMGTableViewer', 'Invalid Input'),
                                QCoreApplication.translate('PMGTableViewer', str(exeption)))

        self.table_view.show_data(data)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        super().closeEvent(a0)

    def on_goto_cell(self):
        if isinstance(self.table_view.model, (TableModelForPandasDataframe, TableModelForNumpyArray)):
            min_row, max_row = 1, self.table_view.model.rowCount(None)
            current_row = self.table_view.currentIndex().row() + 1
            current_col = self.table_view.currentIndex().column() + 1
            row, _ = QInputDialog.getInt(self, QCoreApplication.translate('PMGTableViewer', '输入行'),
                                         QCoreApplication.translate('PMGTableViewer',
                                                                    'Target Row No.:({min}~{max})').format(min=min_row,
                                                                                                           max=max_row),
                                         current_row,
                                         min_row, max_row, step=1)
            if _:
                self.table_view.on_goto_index(row - 1, 0)
        else:
            raise NotImplementedError


if __name__ == '__main__':
    import datetime
    import numpy as np
    import pandas as pd

    app = QApplication(sys.argv)

    table = PMGTableViewer(table_view=PMTableView())
    data = np.arange(1, 17).reshape(2, 2, 4)
    table.show()
    ret = table.set_data(data)

    table2 = PMGTableViewer(table_view=PMTableView())
    data = np.arange(1, 17).reshape(2, 8)
    table2.show()
    ret = table2.set_data(data)

    table3 = PMGTableViewer(table_view=PMTableView())
    data = np.arange(1, 17)
    table3.show()
    ret = table3.set_data(data)

    if not ret:
        table.close()
    else:
        app.exec_()
    # table.setWindowTitle('Pandas数据集 显示多种数据')

    # data2 = pd.DataFrame(np.array([1 + 1j, 1 + 2j, 1 + 2.0j]))
    # table2 = PMGTableViewer(table_view=PMTableView())
    # # table2.show()
    # table2.setWindowTitle('Pandas数据集复数显示')
    # table2.set_data(data2)
    # print(data.dtypes)
