#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

from .PMDialog import PMDialog
from pyminer.ui.data.data_sample import Ui_Form as DataSample_Ui_Form

class DataSampleForm(PMDialog, DataSample_Ui_Form):
    """
    打开"数据抽样"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()
        self.dataset_alter = pd.DataFrame()
        self.dataset_edit = pd.DataFrame()
        self.current_dataset_name = ''
        self.all_dataset = {}
        self.current_dataset_columns = []

        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_selected_add_2.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_weight_add_2.clicked.connect(self.var_weight_add)
        self.pushButton_weight_add.clicked.connect(self.var_weight_add)
        self.pushButton_weight_up.clicked.connect(self.var_weight_up)
        self.pushButton_weight_down.clicked.connect(self.var_weight_down)
        self.pushButton_weight_del.clicked.connect(self.var_weight_del)


    def var_selected_del(self):
        # 移除选中的item
        current_row = self.listWidget_selected.currentRow()
        self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(current_row))
        # 修改当前数据集
        var_list = []
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        self.dataset_edit = self.current_dataset[var_list]

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
        current_item = self.listWidget_var.currentItem()
        if current_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            if_exist = 0  # 检查是否已存在同名变量
            for i in range(self.listWidget_selected.count()):
                if self.listWidget_selected.item(i).text() == self.listWidget_var.currentItem().text():
                    if_exist = 1

            if if_exist != 1:
                self.listWidget_selected.addItem(current_item.text())
                # 修改当前数据集
                var_list = []
                for i in range(self.listWidget_selected.count()):
                    var_list.append(self.listWidget_selected.item(i).text())
                self.dataset_edit = self.current_dataset[var_list]
            else:
                QMessageBox.information(self, "注意", "变量已存在", QMessageBox.Yes)

    def var_weight_del(self):
        current_row = self.listWidget_weight.currentRow()
        self.listWidget_weight.removeItemWidget(self.listWidget_weight.takeItem(current_row))

    def var_weight_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_weight.count()
        for i in range(count):
            var_list.append(self.listWidget_weight.item(i).text())
        row = self.listWidget_weight.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_weight.clear()
        # 重新添加新项
        self.listWidget_weight.addItems(var_list)

    def var_weight_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_weight.count()
        for i in range(count):
            var_list.append(self.listWidget_weight.item(i).text())
        row = self.listWidget_weight.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_weight.clear()
        # 重新添加新项
        self.listWidget_weight.addItems(var_list)

    def var_weight_add(self):
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_weight.addItem(selected_item.text())

    def dataset_sample(self):
        if self.comboBox_replace.currentText() == "无放回抽样":
            random_replace = True
        else:
            random_replace = False

        if self.comboBox_axis.currentText() == "行":
            random_axis = 0
            # 权重
            weight_list = []
            count = self.listWidget_weight.count()
            for i in range(count):
                weight_list.append(self.listWidget_weight.item(i).text())
        else:
            random_axis = 1

        random_state = self.spinBox_random_state.value()
        if self.radioButton_size.isChecked():
            self.dataset_alter = self.dataset_edit.sample(n=self.spinBox_size.value(),
                                                          random_state=random_state,
                                                          replace=random_replace,
                                                          axis=random_axis)
        elif self.radioButton_ratio.isChecked():
            self.dataset_alter = self.dataset_edit.sample(frac=self.doubleSpinBox_ratio.value() / 100,
                                                          random_state=random_state,
                                                          replace=random_replace,
                                                          axis=random_axis)

    def dataset_update(self):
        self.dataset_sample()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(self.current_dataset_name, self.dataset_alter.to_dict(), path,
                                             create_time, update_time, remarks, file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()

    def dataset_save(self):
        self.dataset_sample()
        default_name = self.current_dataset_name.split('.')[0] + '_sample'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = ''
                file_size = ''
                remarks = ''
                self.signal_data_change.emit(dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                logging.info("导入数据信号发射成功")
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()
