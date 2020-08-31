#!/usr/bin/env python
# -*- coding:utf-8 -*-



import datetime
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QInputDialog

from .PMDialog import PMDialog
from pyminer.ui.data.data_transpose import Ui_Form as DataTranspose_Ui_Form

class DataTransposeForm(PMDialog, DataTranspose_Ui_Form):
    """
    打开"数据-转置"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改当前数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()

        self.current_dataset_columns = ''
        self.current_dataset_name = ''
        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.dataset_alter = pd.DataFrame()  # 修改后的数据集
        self.all_dataset = dict()
        # 按钮事件
        self.listWidget_var.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为按住ctrl可以多选
        self.listWidget_selected.setAcceptDrops(True)

        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_cancel.clicked.connect(self.close)

        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)

        self.pushButton_add.clicked.connect(self.var_selected_add)
        self.pushButton_delete.clicked.connect(self.var_selected_add)


    def var_selected_del(self):
        current_row = self.listWidget_selected.currentRow()
        self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(current_row))

    def var_selected_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        row = self.listWidget_selected.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_selected.clear()
        # 重新添加新项
        self.listWidget_selected.addItems(var_list)

    def var_selected_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        row = self.listWidget_selected.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_selected.clear()
        # 重新添加新项
        self.listWidget_selected.addItems(var_list)

    def var_selected_add(self):
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_selected.addItem(selected_item.text())

    def dataset_transpose(self):
        dataset_name = self.listWidget_selected.item(0).text()
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        self.dataset_alter = self.current_dataset.loc[:, var_list].T  # 使用pandas DataFrame.T转置数据
        self.dataset_alter.columns = [str(x) for x in self.dataset_alter.columns]  # 将索引转化为字符串
        print("数据集转置成功")

    def dataset_update(self):
        self.dataset_transpose()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(self.current_dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()

    def dataset_save(self):
        self.dataset_transpose()
        default_name = self.current_dataset_name.split('.')[0] + '_transpose'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()
