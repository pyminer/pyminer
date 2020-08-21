import os
import sys
import logging
import datetime
import webbrowser
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_float_dtype
from pandas.api.types import is_string_dtype

# 导入PyQt5模块
from PyQt5.Qt import *

# 导入数据相关操作模块
from pyminer.ui.data.data_filter import Ui_Form as DataFilter_Ui_Form  # 数据筛选
from pyminer.ui.data.data_role import Ui_Form as DataRole_Ui_Form  # 数据角色
from pyminer.ui.data.data_info import Ui_Form as DataInfo_Ui_Form  # 数据信息
from pyminer.ui.data.data_row_filter import Ui_Form as DataRowFilter_Ui_Form  # 数据行筛选
from pyminer.ui.data.data_column_desc import Ui_Form as Columns_desc_Ui_Form  # 数据列描述
from pyminer.ui.data.data_delete_row import Ui_Form as DataDeleteRow_Ui_Form  # 数据删除行
from pyminer.ui.data.data_delete_column import Ui_Form as DataDeleteColumn_Ui_Form
from pyminer.ui.data.data_merge_vertical import Ui_Form as DataMergeVertical_Ui_Form
from pyminer.ui.data.data_merge_horizontal import Ui_Form as DataMergeHorizontal_Ui_Form
from pyminer.ui.data.data_partition import Ui_Form as DataPartition_Ui_Form
from pyminer.ui.data.data_new_column import Ui_Form as DataNewColumn_Ui_Form
from pyminer.ui.data.data_missing_value import Ui_Form as DataMissingValue_Ui_Form
from pyminer.ui.data.data_sort import Ui_Form as DataSort_Ui_Form
from pyminer.ui.data.data_transpose import Ui_Form as DataTranspose_Ui_Form
from pyminer.ui.data.data_sample import Ui_Form as DataSample_Ui_Form
from pyminer.ui.data.data_standard import Ui_Form as DataStandard_Ui_Form
from pyminer.ui.data.data_column_encode import Ui_Form as DataColumnEncode_Ui_Form
from pyminer.ui.data.data_column_name import Ui_Form as DataColumnName_Ui_Form
from pyminer.ui.data.data_repace import Ui_Form as DataReplace_Ui_Form
from pyminer.share.exceptionhandler import exception_handler
# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)


class DataInfoForm(QDialog, DataInfo_Ui_Form):
    """
    打开"数据-数据信息"
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.all_dataset = dict()
        self.all_dataset_name = list()

        self.current_dataset_name = ''  # 当前数据集名称
        self.info = pd.DataFrame()

        # 更新数据
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_cancel.clicked.connect(self.close)
        # 帮助
        self.pushButton_help.clicked.connect(self.get_help)
        # 修改当前数据集
        self.toolButton_dataset_name.clicked.connect(self.change_dataset_name)
        # 更新当前数据信息
        self.lineEdit_dataset_name.textChanged.connect(self.change_dataset_info)

    #  ================================自定义槽函数=========================
    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def info_init(self):
        if any(self.info):
            input_table_rows = self.info.head(100).shape[0]
            input_table_colunms = self.info.shape[1]
            input_table_header = self.info.columns.values.tolist()
            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.info.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

    def change_dataset_name(self):
        # 修改当前数据集名称
        items = self.all_dataset_name
        item, ok = QInputDialog.getItem(self, "修改数据集", "请选择要查看的数据集", items, 0, False)
        if ok and item:
            self.current_dataset_name = item
            self.lineEdit_dataset_name.setText(item)

    def change_dataset_info(self):
        # 修改当前数据集的数据信息
        self.lineEdit_path.setText(self.all_dataset.get(self.current_dataset_name + ".path"))
        self.lineEdit_row.setText(self.all_dataset.get(self.current_dataset_name + ".row"))
        self.lineEdit_col.setText(self.all_dataset.get(self.current_dataset_name + ".col"))
        self.lineEdit_file_size.setText(self.all_dataset.get(self.current_dataset_name + ".file_size"))
        self.lineEdit_memory_usage.setText(
            self.all_dataset.get(self.current_dataset_name + ".memory_usage"))
        self.lineEdit_create_time.setText(
            self.all_dataset.get(self.current_dataset_name + ".create_time"))
        self.lineEdit_update_time.setText(
            self.all_dataset.get(self.current_dataset_name + ".update_time"))
        self.info = self.all_dataset.get(self.current_dataset_name + ".info")
        self.info_init()


class DataFilterForm(QWidget, DataFilter_Ui_Form):
    """
    打开"数据-筛选"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataRoleForm(QDialog, DataRole_Ui_Form):
    """
    "新建窗口"
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.current_dataset_name = ""
        self.all_dataset = dict()
        self.filter_dataset = pd.DataFrame()  # 预览筛选后内容
        self.role_dataset = pd.DataFrame()  # 预览筛选后内容

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_export.clicked.connect(self.dataset_export)
        self.pushButton_find.clicked.connect(self.change_find)
        self.lineEdit_col_find.textChanged.connect(self.change_find)
        self.comboBox_columns.currentTextChanged.connect(self.change_column)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def dataset_export(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                output_dir + r"/role.csv",  # 起始路径
                                                                "All Files (*);;CSV Files (*.csv)")

        if fileName_choose == "":
            print("\n取消选择")
            return
        else:
            self.role_dataset.to_csv(fileName_choose, index=False)
            print("\n保存成功！")

    def change_column(self):
        """
        查找指定列的数据角色
        """
        col = self.comboBox_columns.currentText()
        if col.strip() == "全部":
            self.flush_preview(self.role_dataset)
        else:
            self.filter_dataset = self.role_dataset[self.role_dataset['名称'] == col]
            self.flush_preview(self.filter_dataset)

    def change_find(self):
        """
        查找指定列的数据角色
        """
        find_text = self.lineEdit_col_find.text()
        self.filter_dataset = self.role_dataset[self.role_dataset['名称'].map(str.lower).str.contains(find_text.lower())]
        self.flush_preview(self.filter_dataset)

    def dataset_role(self):
        data = self.current_dataset
        col_name = list()
        dtype = list()
        width = list()
        precision = list()
        label = list()
        total_cnt = list()
        missing = list()
        measure = list()
        role = []
        for col in data.columns:
            col_name.append(col)
            dtype.append(str(data[col].dtypes))
            width.append(max([len(str(x)) for x in data[col]]))  # 最大宽度

            if is_float_dtype(data[col]):  # 最大精度
                precision.append(max([len(str(x).split('.')[1]) for x in data[col].dropna()]))
            else:
                precision.append("")
            label.append('')
            total_cnt.append(len(data[col]))
            missing.append(data[col].isnull().sum())

            if is_numeric_dtype(data[col]):
                measure.append("标度")
            elif is_string_dtype(data[col]):
                measure.append("名义")
            else:
                measure.append("")

            if col.lower() == "id":
                role.append("ID")
            elif col.lower() == "id" or col.lower() == "target":
                role.append("目标")
            else:
                role.append("输入")
        self.role_dataset = pd.DataFrame({"名称": col_name, "类型": dtype, "宽度": width,
                                          "精度": precision, "标签": label, "数量": total_cnt,
                                          "缺失值": missing, "测量": measure, "角色": role})

        self.flush_preview(self.role_dataset)

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)


class DataRowFilterForm(QDialog, DataRowFilter_Ui_Form):
    """
    打开"数据-行筛选"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()
        self.current_dataset_name = ''
        self.all_dataset = {}
        self.current_dataset_columns = []
        self.data_type = []
        self.filter_dataset = pd.DataFrame()
        self.comboBox_random.currentIndexChanged.connect(self.filter_random_label)  # 按比例随机抽样时，显示%，否则隐藏%
        self.lineEdit_col_find.textChanged.connect(self.filter_column_partter)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)

        # 动态刷新查询结果
        self.comboBox_random.currentIndexChanged.connect(self.exec_filter)
        self.comboBox_replace.currentIndexChanged.connect(self.exec_filter)
        self.radioButton_random.toggled.connect(self.exec_filter)
        self.radioButton_simple.toggled.connect(self.exec_filter)
        self.spinBox_end.valueChanged.connect(self.exec_filter)
        self.spinBox_start.valueChanged.connect(self.exec_filter)
        self.spinBox_random_state.valueChanged.connect(self.exec_filter)
        self.spinBox_random.valueChanged.connect(self.exec_filter)
        self.radioButton_column.toggled.connect(self.exec_filter)
        self.radioButton_dtype.toggled.connect(self.exec_filter)
        self.comboBox_columns.currentTextChanged.connect(self.exec_filter)
        self.comboBox_col_condition.currentTextChanged.connect(self.exec_filter)
        self.lineEdit_col_find.textChanged.connect(self.exec_filter)
        self.comboBox_dtype.currentIndexChanged.connect(self.exec_filter)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def dataset_init(self):
        self.filter_dataset = self.current_dataset.copy().head(100)
        self.tableWidget_dataset.setColumnCount(len(self.filter_dataset.columns))
        self.tableWidget_dataset.setRowCount(len(self.filter_dataset.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(self.filter_dataset.columns.values.tolist())

        for i in range(len(self.filter_dataset.index)):
            for j in range(len(self.filter_dataset.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(self.filter_dataset.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def data_preview(self, dataset):
        # 获取当前数据集
        data = dataset.head(100)
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def filter_simple(self):
        dataset = self.current_dataset.copy()
        # 简单过滤
        int_start = int(self.spinBox_start.value())
        int_end = int(self.spinBox_end.value())
        if 1 <= int_start <= dataset.shape[1]:
            if int_end >= 1 and int_end >= int_start:
                print(dataset.shape)
                self.filter_dataset = dataset.iloc[int_start - 1:int_end]
                self.data_preview(self.filter_dataset)
            else:
                QMessageBox.warning(self, '注意', '输入的结束位置无效', QMessageBox.Yes)
        else:
            QMessageBox.warning(self, '注意', '输入的开始位置无效', QMessageBox.Yes)

    def filter_random_label(self):
        if self.comboBox_random.currentText() == "按比例随机抽样":
            self.label_random.setHidden(False)
        elif self.comboBox_random.currentText() == "按行数随机抽样":
            self.label_random.setHidden(True)

    def filter_random(self):
        # 随机抽样
        dataset = self.current_dataset.copy()
        if self.comboBox_replace.currentText() == "有放回抽样":
            random_replace = True
        else:
            random_replace = False

        random_random_state = int(self.spinBox_random_state.value())
        if self.comboBox_random.currentText() == "按比例随机抽样":
            # 抽取行的比例
            random_func = float(self.spinBox_random.value()) / 100

            self.filter_dataset = dataset.sample(n=None,
                                                 frac=random_func,
                                                 replace=random_replace,
                                                 random_state=random_random_state)
        else:
            # 要抽取的行数
            random_func = int(self.lineEdit_random.text())
            self.filter_dataset = dataset.sample(n=random_func,
                                                 frac=None,
                                                 replace=random_replace,
                                                 random_state=random_random_state)

        self.data_preview(self.filter_dataset)  # 刷新预览数据

    def filter_column_partter(self):
        content = self.lineEdit_col_find.text()
        if content.isdigit():
            self.comboBox_col_condition.clear()
            self.comboBox_col_condition.addItems(['模糊匹配', 'in', 'not in', '=', '>', '>=', '<', '<='])
        else:
            self.comboBox_col_condition.clear()
            self.comboBox_col_condition.addItems(['模糊匹配', 'in', 'not in'])
    @exception_handler
    def filter_column(self):
        # 根据列筛选
        data = self.current_dataset.copy()
        col = self.comboBox_columns.currentText()
        content = self.lineEdit_col_find.text()
        if self.comboBox_columns.currentText() != "变量列表":
            if content.isdigit():  # 判断列的筛选条件是否为数值
                if self.comboBox_col_condition.currentText() == "=":
                    self.filter_dataset = data[data[col] == float(content)]
                elif self.comboBox_col_condition.currentText() == ">":
                    self.filter_dataset = data[data[col] > float(content)]
                elif self.comboBox_col_condition.currentText() == ">=":
                    self.filter_dataset = data[data[col] >= float(content)]
                elif self.comboBox_col_condition.currentText() == "<":
                    self.filter_dataset = data[data[col] < float(content)]
                elif self.comboBox_col_condition.currentText() == "<=":
                    self.filter_dataset = data[data[col] <= float(content)]
            else:
                content=content.lower()
                if self.comboBox_col_condition.currentText() == "模糊匹配":
                    self.filter_dataset = data[data[col].map(str.lower).str.contains(content)]
                elif self.comboBox_col_condition.currentText() == "in":
                    self.filter_dataset = data[data[col].isin(content.split(','))]
                elif self.comboBox_col_condition.currentText() == "not in":
                    self.filter_dataset = data[~data[col].isin(content.split(','))]
        self.data_preview(self.filter_dataset)

    def filter_dtype(self):
        data = self.current_dataset.copy()
        dtype = self.comboBox_dtype.currentText()  # 当前要筛选的数据类型
        if dtype =="全部":
            self.data_preview(data)
            return
        self.filter_dataset = data.select_dtypes(include=dtype)
        self.data_preview(self.filter_dataset)

    def filter_default(self):
        self.filter_dataset = self.current_dataset.copy()
        self.data_preview(self.filter_dataset)

    def exec_filter(self):
        if self.radioButton_simple.isChecked():
            self.filter_simple()
        elif self.radioButton_random.isChecked():
            self.filter_random()
        elif self.radioButton_column.isChecked():
            self.filter_column()
        elif self.radioButton_dtype.isChecked():
            self.filter_dtype()
        else:
            self.filter_default()

    def dataset_save(self):
        self.exec_filter()
        default_name = self.current_dataset_name.split('.')[0] + '_filter'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.filter_dataset) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(dataset_name,
                                             self.filter_dataset.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()

    def dataset_update(self):
        self.exec_filter()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("发射导入数据信号")
            if len(self.filter_dataset) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(self.current_dataset_name,
                                             self.filter_dataset.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()


class DataColumnDescForm(QDialog, Columns_desc_Ui_Form):
    """
    打开"数据-列"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()
        self.current_dataset_name = ''
        self.dataset_alter = pd.DataFrame()
        self.all_dataset = dict()

        self.listWidget_selected.itemChanged.connect(self.slot_var_change)

        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_selected_add_2.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_group_add_2.clicked.connect(self.var_group_add)
        self.pushButton_group_add.clicked.connect(self.var_group_add)
        self.pushButton_group_up.clicked.connect(self.var_group_up)
        self.pushButton_group_down.clicked.connect(self.var_group_down)
        self.pushButton_group_del.clicked.connect(self.var_group_del)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def slot_var_change(self):
        # 只允许查看一个变量的描述
        if self.listWidget_selected.count() > 0:
            QMessageBox.information(self, "注意", "只允许查看一个变量的描述", QMessageBox.Yes)

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
        current_item = self.listWidget_var.currentItem()
        selected_item = self.listWidget_selected.item(0)
        if current_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        elif current_item is not None and selected_item is not None:
            if self.listWidget_var.currentItem().text() == self.listWidget_selected.item(0).text():
                QMessageBox.information(self, "注意", "变量已存在", QMessageBox.Yes)
            else:
                selected_item.setText(self.listWidget_var.currentItem().text())
        elif current_item is not None and selected_item is None:
            self.listWidget_selected.addItem(current_item.text())
        else:
            self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(0))
            self.listWidget_selected.addItem(current_item.text())

    def var_group_del(self):
        current_row = self.listWidget_group.currentRow()
        self.listWidget_group.removeItemWidget(self.listWidget_group.takeItem(current_row))

    def var_group_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_group.count()
        for i in range(count):
            var_list.append(self.listWidget_group.item(i).text())
        row = self.listWidget_group.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_group.clear()
        # 重新添加新项
        self.listWidget_group.addItems(var_list)

    def var_group_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_group.count()
        for i in range(count):
            var_list.append(self.listWidget_group.item(i).text())
        row = self.listWidget_group.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_group.clear()
        # 重新添加新项
        self.listWidget_group.addItems(var_list)

    def var_group_add(self):
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_group.addItem(selected_item.text())

    def dataset_column_desc(self):
        var = self.listWidget_selected.item(0).text()

        group_list = []  # 保存已选变量
        count = self.listWidget_group.count()  # 获取listwidget中条目数
        for i in range(count):
            group_list.append(self.listWidget_group.item(i).text())

        self.dataset_alter = self.current_dataset.copy().groupby(group_list)[var].describe().reset_index()
        if isinstance(self.dataset_alter, pd.DataFrame):
            self.flush_preview(self.dataset_alter)  # 预览列的基本描述
        else:
            self.dataset_alter = self.dataset_alter.to_frame()
            self.flush_preview(self.dataset_alter)

    def dataset_update(self):
        self.dataset_column_desc()
        self.tabWidget.setCurrentIndex(1)

    def dataset_save(self):
        self.dataset_column_desc()
        default_name = self.current_dataset_name.split('.')[0] + '_col'
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

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)


class DataDeleteRowForm(QWidget, DataDeleteRow_Ui_Form):
    """
    打开"数据-删除行"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataDeleteColumnForm(QWidget, DataDeleteColumn_Ui_Form):
    """
    打开"数据-删除列"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataMergeVerticalForm(QDialog, DataMergeVertical_Ui_Form):
    """
    打开"数据-纵向合并"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset_name = ""
        self.all_dataset = {}  # 定义“全部数据集”为一个字典
        self.all_dataset_name = ()
        self.dataset_alter = pd.DataFrame()  # 修改后的数据

        self.listWidget_dataset.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为按住ctrl可以多选
        self.listWidget_start.setAcceptDrops(True)
        self.listWidget_append.setAcceptDrops(True)

        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_cancel.clicked.connect(self.close)
        self.listWidget_start.itemChanged.connect(self.slot_listWidget_start_change)
        self.pushButton_insert_start.clicked.connect(self.dataset_insert_start)
        self.pushButton_insert_append.clicked.connect(self.dataset_insert_append)

        self.pushButton_start_add.clicked.connect(self.dataset_insert_start)
        self.pushButton_append_add.clicked.connect(self.dataset_insert_append)

        self.pushButton_start_del.clicked.connect(self.dataset_start_del)
        self.pushButton_append_del.clicked.connect(self.dataset_append_del)

        self.pushButton_start_up.clicked.connect(self.dataset_start_up)
        self.pushButton_append_up.clicked.connect(self.dataset_append_up)

        self.pushButton_start_down.clicked.connect(self.dataset_start_down)
        self.pushButton_append_down.clicked.connect(self.dataset_append_down)

    #  ================================事件处理函数=========================
    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def slot_listWidget_start_change(self):
        self.current_dataset_name = self.listWidget_start.item(0).text()

    #  ================================自定义功能函数=========================
    def dataset_start_del(self):
        current_row = self.listWidget_start.currentRow()
        self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(current_row))

    def dataset_append_del(self):
        current_row = self.listWidget_append.currentRow()
        self.listWidget_append.removeItemWidget(self.listWidget_append.takeItem(current_row))

    def dataset_append_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_append_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_start_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_start_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_insert_start(self):
        selected_item = self.listWidget_dataset.currentItem()
        start_item = self.listWidget_start.item(0)
        if selected_item is None:
            QMessageBox.information(self, "注意", "请先选择起始数据集", QMessageBox.Yes)
        elif start_item is not None:
            if selected_item.text() == self.listWidget_start.item(0).text():
                QMessageBox.information(self, "注意", "起始数据集已存在", QMessageBox.Yes)
            else:
                self.listWidget_start.item(0).setText(selected_item.text())
        elif start_item is None:
            self.listWidget_start.addItem(selected_item.text())
        else:
            self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(0))
            self.listWidget_start.addItem(selected_item.text())

    def dataset_insert_append(self):
        selected_item = self.listWidget_dataset.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes)
        elif selected_item.text() != self.listWidget_start.item(0).text():
            current_item = self.listWidget_dataset.currentItem()
            self.listWidget_append.addItem(current_item.text())
        elif selected_item.text() == self.listWidget_start.item(0).text():
            QMessageBox.information(self, "注意", "合并数据集不能与起始数据集同名", QMessageBox.Yes)
        else:
            selected = self.listWidget_dataset.selectedItems()
            dataset_start_text = self.listWidget_dataset.currentItem().text()
            for item in selected:
                if item.text() != dataset_start_text:
                    self.listWidget_append.addItem(item.text())

    def dataset_merge_vertical(self):
        dataset_name = self.listWidget_start.item(0).text()
        dataset_start = self.all_dataset.get(dataset_name)
        dataset_merge_list_name = []
        dataset_merge_list = [dataset_start, ]
        for i in range(self.listWidget_append.count()):
            dataset_merge_list_name.append(self.listWidget_append.item(i).text())
            dataset_merge_list.append(self.all_dataset.get(self.listWidget_append.item(i).text()))

        if self.listWidget_start.count() < 1:
            QMessageBox.information(self, "注意", "请选择起始数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif self.listWidget_append.count() < 1:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            self.dataset_alter = pd.concat(dataset_merge_list, ignore_index=True)  # 合并数据

    def dataset_update(self):
        self.dataset_merge_vertical()
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
        self.dataset_merge_vertical()
        default_name = self.current_dataset_name.split('.')[0] + '_v'
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


class DataMergeHorizontalForm(QDialog, DataMergeHorizontal_Ui_Form):
    """
    打开"数据-横向合并"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset_name = ""
        self.all_dataset = {}  # 定义“全部数据集”为一个字典
        self.dataset_alter = pd.DataFrame()

        self.listWidget_dataset.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为按住ctrl可以多选
        self.listWidget_start.setAcceptDrops(True)
        self.listWidget_append.setAcceptDrops(True)
        self.listWidget_start.itemChanged.connect(self.slot_listWidget_start_change)

        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_start_add.clicked.connect(self.dataset_start_add)
        self.pushButton_start_up.clicked.connect(self.dataset_start_up)
        self.pushButton_start_down.clicked.connect(self.dataset_start_down)
        self.pushButton_start_del.clicked.connect(self.dataset_start_del)
        self.pushButton_append_add.clicked.connect(self.dataset_append_add)
        self.pushButton_append_up.clicked.connect(self.dataset_append_up)
        self.pushButton_append_down.clicked.connect(self.dataset_append_down)
        self.pushButton_append_del.clicked.connect(self.dataset_append_del)

    #  ================================事件处理函数=========================
    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def slot_listWidget_start_change(self):
        self.current_dataset_name = self.listWidget_start.item(0).text()

    #  ================================自定义功能函数=========================
    def dataset_start_del(self):
        current_row = self.listWidget_start.currentRow()
        self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(current_row))

    def dataset_append_add(self):
        selected_item = self.listWidget_dataset.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes)
        elif selected_item.text() != self.listWidget_start.item(0).text():
            current_item = self.listWidget_dataset.currentItem()
            self.listWidget_append.addItem(current_item.text())
        elif selected_item.text() == self.listWidget_start.item(0).text():
            QMessageBox.information(self, "注意", "合并数据集不能与起始数据集同名", QMessageBox.Yes)
        else:
            selected = self.listWidget_dataset.selectedItems()
            dataset_start_text = self.listWidget_dataset.currentItem().text()
            for item in selected:
                if item.text() != dataset_start_text:
                    self.listWidget_append.addItem(item.text())

    def dataset_append_del(self):
        current_row = self.listWidget_append.currentRow()
        self.listWidget_append.removeItemWidget(self.listWidget_append.takeItem(current_row))

    def dataset_append_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_append_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_start_add(self):
        selected_item = self.listWidget_dataset.currentItem()
        start_item = self.listWidget_start.item(0)
        if selected_item is None:
            QMessageBox.information(self, "注意", "请先选择起始数据集", QMessageBox.Yes)
        elif start_item is not None:
            if selected_item.text() == self.listWidget_start.item(0).text():
                QMessageBox.information(self, "注意", "起始数据集已存在", QMessageBox.Yes)
            else:
                self.listWidget_start.item(0).setText(selected_item.text())
        elif start_item is None:
            self.listWidget_start.addItem(selected_item.text())
        else:
            self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(0))
            self.listWidget_start.addItem(selected_item.text())

    def dataset_start_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_start_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_merge_horizontal(self):
        dataset_name = self.listWidget_start.item(0).text()  # dataset_name
        dataset_start = self.all_dataset.get(dataset_name)  # dataset_start
        dataset_merge_list_name = []  # 要合并的数据集名称
        dataset_merge_list = []  # 要合并的数据
        for i in range(self.listWidget_append.count()):  # 遍历列表n-1次
            if i < self.listWidget_append.count():
                dataset_name = self.listWidget_append.item(i).text()
                dataset_merge_list_name.append(dataset_name)
                dataset = self.all_dataset.get(self.listWidget_append.item(i).text()).copy()  # 避免修改原始数据
                dataset.columns = [x + "_" + dataset_name.split('.')[0] for x in dataset.columns]  # 为列名添加数据集后缀
                dataset_merge_list.append(dataset)

        if self.listWidget_start.count() < 1:
            QMessageBox.information(self, "注意", "请选择起始数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif self.listWidget_append.count() < 1:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            data_element = [dataset_start]
            for item in dataset_merge_list:
                data_element.append(item)
            self.dataset_alter = pd.concat(data_element, ignore_index=False, axis=1)  # 横向合并

    def dataset_update(self):
        self.dataset_merge_horizontal()
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
        self.dataset_merge_horizontal()
        default_name = self.current_dataset_name.split('.')[0] + '_h'
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


class DataPartitionForm(QDialog, DataPartition_Ui_Form):
    """
    打开"数据-数据分区"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()


        self.current_dataset = pd.DataFrame()
        self.current_dataset_name = ''


        self.widget_part_2.hide()
        self.widget_part_3.hide()
        self.widget_part_4.hide()
        self.widget_part_other.setVisible(False)



    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")








class DataNewColumnForm(QWidget, DataNewColumn_Ui_Form):
    """
    打开"从sas导入"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataMissingValueForm(QDialog, DataMissingValue_Ui_Form):
    """
    打开"数据-缺失值"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.current_dataset_name = ""
        self.all_dataset = dict()
        self.missing_dataset = pd.DataFrame()  # 处理后的缺失值数据
        self.missing_stat_dataset = pd.DataFrame()  # 缺失值统计数据

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.dataset_missing)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)

        self.pushButton_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_delete.clicked.connect(self.var_selected_del)

        self.listWidget_selected.itemChanged.connect(self.dataset_filter_column)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

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

    def dataset_missing_stat(self):
        data = self.current_dataset.copy()
        col_name = list()
        dtype = list()
        total_cnt = list()
        missing = list()  # 缺失值数量
        missing_ratio = list()  # 缺失值占比
        unmissing = list()
        unmissing_ratio = list()  # 非缺失值占比
        for col in data.columns:
            col_name.append(col)
            dtype.append(str(data[col].dtypes))
            total_cnt.append(len(data))
            missing.append(data[col].isnull().sum())
            missing_ratio.append('{0:.2%}'.format(data[col].isnull().sum() / len(data)))
            unmissing.append(len(data) - data[col].isnull().sum())
            unmissing_ratio.append('{0:.2%}'.format((len(data) - data[col].isnull().sum()) / len(data)))

        self.missing_stat_dataset = pd.DataFrame({"名称": col_name, "类型": dtype, "总数": total_cnt,
                                                  "缺失值数量": missing,
                                                  "缺失值占比": missing_ratio,
                                                  "非缺失值数量": unmissing,
                                                  "非缺失值占比": unmissing_ratio})
        self.flush_preview(self.missing_stat_dataset)

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)

    def dataset_missing(self):
        from pandas.api.types import is_numeric_dtype
        from pandas.api.types import is_float_dtype
        from pandas.api.types import is_string_dtype

        from sklearn.impute import SimpleImputer
        data = self.current_dataset.copy()
        columns = []
        for i in range(self.listWidget_selected.count()):
            columns.append(self.listWidget_selected.item(i).text())

        if self.radioButton_mean.isChecked():  # 均值填充缺失值
            for col in columns:
                if is_numeric_dtype(data[col]):
                    data.fillna(data[col].mean(), inplace=True)
                    print(data)
                else:
                    print("不能用平均值填充非数值列")
        elif self.radioButton_median.isChecked():  # 中位数填充缺失值
            for col in columns:
                if is_numeric_dtype(data[col]):
                    data.fillna(data[col].median(), inplace=True)
                    print(data)
                else:
                    print("不能用中位数值填充非数值列")
        elif self.radioButton_mode.isChecked():  # 众数填充缺失值
            for col in columns:
                data.fillna(list(data[col].mode())[0], inplace=True)
                print(data)
        elif self.radioButton_drop.isChecked():  # 删除有缺失值的行
            data.dropna(axis=0, subset=columns, inplace=True)
            print(data)
        elif self.radioButton_drop_col.isChecked():  # 删除全部为缺失值的列
            data.dropna(axis=1, how="all", inplace=True)
            print(data)
        elif self.radioButton_replace.isChecked():  # 替换缺失值
            data.fillna(self.lineEdit_missing_replace.text().strip(), inplace=True)
            print(data)
        elif self.radioButton_drop_ratio.isChecked():  # 替换缺失值
            ratio = self.doubleSpinBox_missing_ratio.value()
            missing_ratio = data.isnull().sum() / len(data) >= ratio
            missing_column = list(missing_ratio[missing_ratio.values == True].index)
            for col in missing_column:
                del data[col]
            print(data)
        self.missing_dataset = data  # 保存数据
        self.dataset_update()  # 更新数据

    def dataset_filter_column(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        self.current_dataset = self.current_dataset.loc[:, var_list]  # 筛选列

    def dataset_update(self):
        logging.info("发射导入数据信号")
        if len(self.missing_dataset) > 0:
            create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.all_dataset.get(self.current_dataset_name + '.path')
            file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
            remarks = ''
            self.signal_data_change.emit(self.current_dataset_name, self.missing_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def dataset_save(self):
        print(self.current_dataset_name)
        default_name = self.current_dataset_name.split('.')[0] + '_missing'
        print(default_name)
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.missing_dataset) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(dataset_name, self.missing_dataset.to_dict(), path,
                                             create_time, update_time, remarks, file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()


class DataSortForm(QWidget, DataSort_Ui_Form):
    """
    打开"从sas导入"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataTransposeForm(QDialog, DataTranspose_Ui_Form):
    """
    打开"数据-转置"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改当前数据

    def __init__(self, parent=None):
        super().__init__(parent)
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

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    #  ================================自定义功能函数=========================
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


class DataStandardForm(QWidget, DataStandard_Ui_Form):
    """
    打开"从sas导入"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataSampleForm(QDialog, DataSample_Ui_Form):
    """
    打开"数据抽样"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self, parent=None):
        super().__init__(parent)
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

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

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


class DataColumnNameForm(QDialog, DataColumnName_Ui_Form):
    """
    打开"数据-列名处理"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据
    signal_flush_console = pyqtSignal(str, str, str)  # 自定义信号，用于修改日志

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.dataset_edit = pd.DataFrame()
        self.dataset_alter = pd.DataFrame()  # 处理后数据
        self.current_dataset_name = ""
        self.all_dataset = dict()

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_delete.clicked.connect(self.var_selected_del)
        self.pushButton_preview.clicked.connect(self.dataset_columns_preview)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

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
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_selected.addItem(selected_item.text())
            # 修改当前数据集
            var_list = []
            for i in range(self.listWidget_selected.count()):
                var_list.append(self.listWidget_selected.item(i).text())
            self.dataset_edit = self.current_dataset[var_list]

    def dataset_init(self):
        self.filter_dataset = self.current_dataset.head(10)
        self.tableWidget_dataset.setColumnCount(len(self.filter_dataset.columns))
        self.tableWidget_dataset.setRowCount(len(self.filter_dataset.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(self.filter_dataset.columns.values.tolist())

        for i in range(len(self.filter_dataset.index)):
            for j in range(len(self.filter_dataset.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(self.filter_dataset.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def dataset_columns_preview(self):
        data = self.dataset_edit.copy()
        col = self.comboBox_columns.currentText()
        replace = self.lineEdit_replace.text().strip()
        prefix_add = self.lineEdit_prefix_add.text().strip()
        prefix_del = self.lineEdit_prefix_del.text().strip()
        suffix_add = self.lineEdit_suffix_add.text().strip()
        suffix_del = self.lineEdit_suffix_del.text().strip()

        def check_prefix(x, y):
            if x[:len(y)] == y:
                return x[len(y):]
            else:
                return x

        def check_suffix(x, y):
            if x[-len(y):] == y:
                return x[:-len(y)]
            else:
                return x

        if len(replace) > 0:
            if col == "变量列表":
                QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
                return
            else:
                data.rename(columns={col: replace}, inplace=True)

        if self.checkBox_prefix_add.isChecked() and len(prefix_add) > 0:
            data.columns = [prefix_add + col for col in data.columns]
        if self.checkBox_prefix_del.isChecked() and len(prefix_del) > 0:
            data.columns = [check_prefix(col, prefix_del) for col in data.columns]
        if self.checkBox_suffix_add.isChecked() and len(suffix_add) > 0:
            data.columns = [col + suffix_add for col in data.columns]
        if self.checkBox_suffix_del.isChecked() and len(suffix_del) > 0:
            data.columns = [check_suffix(col, suffix_del) for col in data.columns]
        self.flush_preview(data)  # 刷新预览

    def dataset_columns(self):
        col = self.comboBox_columns.currentText()
        replace = self.lineEdit_replace.text().strip()
        prefix_add = self.lineEdit_prefix_add.text().strip()
        prefix_del = self.lineEdit_prefix_del.text().strip()
        suffix_add = self.lineEdit_suffix_add.text().strip()
        suffix_del = self.lineEdit_suffix_del.text().strip()

        def check_prefix(x, y):
            if x[:len(y)] == y:
                return x[len(y):]
            else:
                return x

        def check_suffix(x, y):
            if x[-len(y):] == y:
                return x[:-len(y)]
            else:
                return x

        if len(replace) > 0:
            if col == "变量列表":
                QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
                return
            else:
                self.current_dataset.rename(columns={col: replace}, inplace=True)

        if self.checkBox_prefix_add.isChecked() and len(prefix_add) > 0:
            self.dataset_edit.columns = [prefix_add + col for col in self.dataset_edit.columns]
        if self.checkBox_prefix_del.isChecked() and len(prefix_del) > 0:
            self.dataset_edit.columns = [check_prefix(col, prefix_del) for col in self.dataset_edit.columns]
        if self.checkBox_suffix_add.isChecked() and len(suffix_add) > 0:
            self.dataset_edit.columns = [col + suffix_add for col in self.dataset_edit.columns]
        if self.checkBox_suffix_del.isChecked() and len(suffix_del) > 0:
            self.dataset_edit.columns = [check_suffix(col, suffix_del) for col in self.dataset_edit.columns]
        self.dataset_alter = self.dataset_edit.copy()
        self.flush_preview(self.dataset_edit)  # 刷新预览

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)

    def dataset_update(self):
        self.dataset_columns()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
                self.signal_flush_console.emit('info', '数据处理', '列名处理完成')
            else:
                logging.info("导入数据信号发射失败")
                self.signal_flush_console.emit('error', '数据处理', '列名处理失败')
                self.close()

    def dataset_save(self):
        self.dataset_columns()
        default_name = self.current_dataset_name.split('.')[0] + '_col'
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


class DataColumnEncodeForm(QWidget, DataColumnEncode_Ui_Form):
    """
    打开"数据编码"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class DataReplaceForm(QDialog, DataReplace_Ui_Form):
    """
    打开"数据-内容替换"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据
    signal_flush_console = pyqtSignal(str, str, str)  # 自定义信号，用于修改日志

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.result_row = []
        self.result_col = []
        self.result_value = []
        self.current_dataset_name = ""
        self.all_dataset = dict()
        self.result_dataset = pd.DataFrame()
        self.dataset_alter = pd.DataFrame()  # 修改后的数据集
        self.tableWidget_dataset.setVisible(False)

        self.pushButton_cancel.clicked.connect(self.close)
        self.tabWidget.currentChanged.connect(self.ui_init)
        self.pushButton_find.clicked.connect(self.data_find)
        self.pushButton_replace.clicked.connect(self.dataset_update)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def ui_init(self):

        text = self.tabWidget.tabText(self.tabWidget.currentIndex())
        if text == "查找":
            self.pushButton_replace.setVisible(False)
        else:
            self.pushButton_replace.setVisible(True)

    def data_find(self):

        if self.tableWidget_dataset.isHidden():
            self.tableWidget_dataset.setVisible(True)

        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "查找":
            find_txt = self.lineEdit_find.text()
            if len(find_txt) == 0:
                QMessageBox.warning(self, '注意', '查找内容无效', QMessageBox.Yes)
                return

            self.result_dataset = ''
            self.result_col = []
            self.result_row = []
            self.result_value = []
            self.tableWidget_dataset.clearContents()

            data = self.current_dataset
            if self.comboBox_find_columns.currentText() == "全部列":
                for col in data.columns:
                    if is_string_dtype(data[col]):
                        if self.checkBox_find_cell.isChecked():
                            if self.checkBox_find_case.isChecked():  # 匹配单元格 且 匹配大小写
                                row = data[data[col].map(str) == find_txt].index.tolist()
                            else:  # 匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                        else:
                            if self.checkBox_find_case.isChecked():  # 不匹配单元格 且 匹配大小写
                                row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                            else:  # 不匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()

                    elif is_numeric_dtype(data[col]):
                        if self.checkBox_find_cell.isChecked():  # 匹配单元格
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 不匹配单元格
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                    # 写入结果预览表
                    if len(row) > 0:
                        for i in row:
                            print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                            self.result_row.append(col)
                            self.result_col.append(i)
                            self.result_value.append(data[col].iat[i])
            else:
                col = self.comboBox_find_columns.currentText()
                if is_string_dtype(data[col]):
                    if self.checkBox_find_cell.isChecked():
                        if self.checkBox_find_case.isChecked():  # 匹配单元格 且 匹配大小写
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                    else:
                        if self.checkBox_find_case.isChecked():  # 不匹配单元格 且 匹配大小写
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                        else:  # 不匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                elif is_numeric_dtype(data[col]):
                    if self.checkBox_find_cell.isChecked():  # 匹配单元格
                        row = data[data[col].map(str) == find_txt].index.tolist()
                    else:  # 不匹配单元格
                        row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                if len(row) > 0:
                    for i in row:
                        print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                        self.result_row.append(col)
                        self.result_col.append(i)
                        self.result_value.append(data[col].iat[i])

            self.result_dataset = pd.DataFrame({'列': self.result_row, '行': self.result_col, '值': self.result_value})
            self.flush_preview(self.result_dataset)
        else:
            find_txt = self.lineEdit_replace_find.text()
            if len(find_txt) == 0:
                QMessageBox.warning(self, '注意', '查找内容无效', QMessageBox.Yes)
                return

            self.result_dataset = ''
            self.result_col = []
            self.result_row = []
            self.result_value = []
            self.tableWidget_dataset.clearContents()

            data = self.current_dataset
            if self.comboBox_replace_columns.currentText() == "全部列":
                for col in data.columns:
                    if is_string_dtype(data[col]):
                        if self.checkBox_replace_cell.isChecked():
                            if self.checkBox_replace_case.isChecked():  # 匹配单元格 且 匹配大小写
                                row = data[data[col].map(str) == find_txt].index.tolist()
                            else:  # 匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                        else:
                            if self.checkBox_replace_case.isChecked():  # 不匹配单元格 且 匹配大小写
                                row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                            else:  # 不匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                    elif is_numeric_dtype(data[col]):
                        if self.checkBox_replace_cell.isChecked():  # 匹配单元格
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 不匹配单元格
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                    # 写入结果预览表
                    if len(row) > 0:
                        for i in row:
                            print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                            self.result_row.append(col)
                            self.result_col.append(i)
                            self.result_value.append(data[col].iat[i])
            else:
                col = self.comboBox_replace_columns.currentText()
                if is_string_dtype(data[col]):
                    if self.checkBox_replace_cell.isChecked():
                        if self.checkBox_replace_case.isChecked():  # 匹配单元格 且 匹配大小写
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                    else:
                        if self.checkBox_replace_case.isChecked():  # 不匹配单元格 且 匹配大小写
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                        else:  # 不匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                elif is_numeric_dtype(data[col]):
                    if self.checkBox_replace_cell.isChecked():  # 匹配单元格
                        row = data[data[col].map(str) == find_txt].index.tolist()
                    else:  # 不匹配单元格
                        row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                if len(row) > 0:
                    for i in row:
                        print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                        self.result_row.append(col)
                        self.result_col.append(i)
                        self.result_value.append(data[col].iat[i])

            self.result_dataset = pd.DataFrame({'列': self.result_row, '行': self.result_col, '值': self.result_value})
            self.flush_preview(self.result_dataset)

    def data_replace(self):
        if self.tableWidget_dataset.isHidden():
            self.tableWidget_dataset.setVisible(True)

        replace_txt = self.lineEdit_replace.text()
        self.dataset_alter = self.current_dataset.copy()
        if len(self.result_dataset) > 0:
            for col in self.result_dataset['列']:
                for row in self.result_dataset['行']:
                    content = self.dataset_alter[col].iat[row]
                    print('content:', content)
                    self.dataset_alter[col].iat[row] = replace_txt

        print('替换完成')

    def dataset_update(self):
        self.data_replace()
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
        else:
            self.dataset_save()

    def dataset_save(self):
        default_name = self.current_dataset_name.split('.')[0] + '_replace'
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

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)


# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = DataInfoForm()
    form.show()
    sys.exit(app.exec_())
