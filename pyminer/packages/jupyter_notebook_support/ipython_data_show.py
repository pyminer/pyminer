# -*- coding:utf-8 -*-
# @Time: 2021/1/28 16:45
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: ipython_data_show.py
import logging

from PySide2.QtWidgets import QTableWidget, QWidget, QVBoxLayout, QComboBox, QApplication, QTableWidgetItem, \
    QHeaderView
from widgets import PMDockObject
from lib.comm.base import DataDesc
from lib.comm import get_var_names, get_var

logger = logging.getLogger(__name__)


class IPythonDataTable(QTableWidget):
    def __init__(self, parent=None):
        super(IPythonDataTable, self).__init__(parent)
        self.set_data = ''


class IPythonDataShow(QWidget, PMDockObject):
    def __init__(self):
        super(IPythonDataShow, self).__init__(None)
        self.setLayout(QVBoxLayout())
        self.data_select_combox = QComboBox()
        self.layout().addWidget(self.data_select_combox)
        self.table = QTableWidget()
        self.headers = [self.tr('Name'), self.tr('Type'), self.tr('Size'), self.tr('Value')]

        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout().addWidget(self.table)

        self.update_ipython_kernels()
        if self.data_select_combox.currentIndex() >= 0:
            self.set_data(self.data_select_combox.currentText())

    def get_widget_text(self) -> str:
        return self.tr('IPython Variables')

    def update_ipython_kernels(self):
        """
        更新IPython数据状态
        :return:
        """
        variable_names = get_var_names()
        kernel_list = []
        for name in variable_names:
            if name.startswith('IPy_'):
                kernel_list.append(name)
        current_text = self.data_select_combox.currentText()
        self.data_select_combox.clear()
        self.data_select_combox.addItems(kernel_list)
        if current_text in kernel_list:
            index = kernel_list.index(current_text)
            self.data_select_combox.setCurrentIndex(index)

    def on_combo_index_changed(self, i):
        kernel_name = self.data_select_combox.currentText()
        self.set_data(kernel_name)

    def on_data_changed(self, data_name):
        index = self.data_select_combox.findText(data_name)
        if index == -1:
            no_kernel_connected = (self.data_select_combox.count() == 0)
            self.update_ipython_kernels()
            if no_kernel_connected:
                self.set_data(self.data_select_combox.currentText())

        else:
            if data_name == self.data_select_combox.currentText():
                self.set_data(data_name)
        print('data_changed', data_name)

    def set_data(self, kernel_name):
        var: dict = get_var(kernel_name)
        # var: dict = kernel_name
        try:
            assert var is not None
            assert isinstance(var, dict)
            l = list(var.keys())
            l.sort()
            self.table.setColumnCount(4)
            self.table.setRowCount(len(l))
            for name in l:
                if not isinstance(var[name], DataDesc):
                    return
            try:
                for i, name in enumerate(l):
                    desc: DataDesc = var[name]
                    self.table.setItem(i, 0, QTableWidgetItem(name))
                    self.table.setItem(i, 1, QTableWidgetItem(desc.type))
                    self.table.setItem(i, 2, QTableWidgetItem(repr(desc.size)))
                    self.table.setItem(i, 3, QTableWidgetItem(desc.repr_value))
            except TypeError:
                import traceback
                traceback.print_exc()
                logger.warning("接受到的数据var：" + repr(var))
        except:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication([])
    ds = IPythonDataShow()
    ds.set_data({'a': DataDesc(1), 'b': DataDesc([1, 2, 3])})
    ds.show()
    app.exec_()
