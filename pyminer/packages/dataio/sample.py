# -*- encoding: utf-8 -*-
import logging
import os
import time

import numpy as np
import openpyxl
import pandas as pd
import xlrd
# 导入PyQt5模块
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from dataImportModel import Ui_Form as dataImportFormEngine
from widgets import kwargs_to_str
from lib.comm import set_var, run_command

# 导入matlab加载模块

# 定义日志输出格式
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ImportDialog(QDialog):
    signal_data_change = Signal(str, dict, str, str, str, str, str)  # 自定义信号，用于传递文件路径
    extension_lib = None

    def __init__(self, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.current_dataset: pd.DataFrame = None
        self.import_message = {"isError": False, "warningMessage": []}
        self.separator_char = [",", ";", "\\s", "\\t"]
        self.encode_type = ["utf8", "gb2312", "gbk", "ascii"]

    def importDatasetPreview(self):
        pass

    def getImportParam(self):
        pass

    def importDatasetReload(self):
        pass

    def updateTableView(self):
        pass

    def open_file(self, path: str):
        assert os.path.exists(path)
        self.lineEdit_filePath.setText(path)
        self.previewButton()

    def openfile(self):
        """
            选择文件，需要支持三种场景：
            （1）点击 “浏览” 按钮
            （2）点击 “预览” 按钮
        """
        path = self.lineEdit_filePath.text()
        self.import_param.update(choosefile=False)
        if not path:
            # 先判断传入的 path 是否有内容，
            path, openfile_type = QFileDialog.getOpenFileName(self, '选择文件', self.get_work_dir(),
                                                              "文件类型({})".format(self.file_types))
            self.lineEdit_filePath.setText(path)
        if path:
            # 如果没有选择文件就关闭窗口，这时候path还是没有路径，datasetName 则清空
            temp_name = (os.path.split(self.lineEdit_filePath.text())[1]).split(".")[0:-1]
            # 获取文件名称，并将文件名称作为导入的变量名称，如果文件名称为空，则使用 temp 作为变量名称
            dataset_name = "temp" if temp_name == [""] else ".".join(temp_name)
            self.lineEdit_datasetName.setText(dataset_name)
        else:
            self.lineEdit_filePath.setText(self.import_param["filepath"])

    def chooseFileButton(self):
        """选择文件按钮"""
        self.lineEdit_filePath.setText("")
        self.previewButton()

    def previewButton(self):
        """预览按钮"""
        self.import_param.update(ispreview=True)
        self.openfile()
        self.getImportParam()
        if self.import_message["isError"]:
            self.showWarningMessage()
        else:
            if self.lineEdit_filePath.text():
                self.importDatasetLoad()
        self.updateTableView()

    def importDatasetButton(self):
        """对发送钱的数据验证"""
        self.import_param.update(ispreview=False)
        self.getImportParam()
        if self.import_message["isError"]:
            self.showWarningMessage()
            return

        # if self.import_param["filepath"] == "" or len(self.current_dataset) == 0:
        if len(self.current_dataset) == 0:
            self.showWarningMessage(info="导入失败！\n提示：请提供正确数据集")
            return

        var_name_check = self.updateDatasetVarname()
        if var_name_check:
            import sys
            t0 = time.time()
            self.importDatasetLoad()
            self.sendDataset()
            t1 = time.time()
            logger.info("导入数据集所用时间: {t} s 大小 {m} MB".format(
                t=round(t1 - t0, 2), m=round(sys.getsizeof(self.current_dataset) / 1024, 2)
            ))
            self.current_dataset = None

    def importDatasetLoad(self):
        """获取数据并做检验"""
        error = ""
        self.import_param.update(status=False)
        try:
            self.importDatasetReload()
            self.import_param.update(status=True)

        except UnicodeDecodeError as e:
            encodetype = self.import_param["param"]["encoding"]
            self.updateWarningMessage(info="指定的编码方式“{}”无法解码要打开的文件,请尝试其他编码方式".format(encodetype))
            error = str(e)

        except MemoryError as e:
            self.updateWarningMessage(info="文件过大，超过内存上限，导入失败！")
            error = str(e)

        except Exception as e:
            self.updateWarningMessage(info="导入失败，错误详情：\n{}".format(str(e)))
            error = str(e)

        if self.import_message["isError"]:
            self.showWarningMessage()
        return (error)

    def getDatasetInfo(self, varname=""):
        """
            获取变量的名称、数据结构等信息
            目前暂不支持保留用户重新配置的字段数据类型方案
            varname = 变量统一命名
        """
        self.import_param.update(varname={}, dtypes={})
        for k in self.current_dataset:
            self.import_param["varname"][k] = varname if varname else k
            if type(self.current_dataset[k]) == pd.DataFrame:
                self.import_param["dtypes"][k] = self.current_dataset[k].dtypes
            else:
                self.import_param["dtypes"][k] = type(self.current_dataset[k])

    def updateDatasetVarname(self):
        """
            更新导入数据集时候的名称
            TODO: 重置数据集名称
            考虑到未来导入数据集时候需要重命名数据集的名称，可能会存在这几类场景：
            （1）导入后的变量名称更新
                【1】一个文件一个单变量（页面）导入
                【2】一个文件多变量（页面）导入，导入后可能以一个字典导入，或是多个变量名称，如果数据结构都一致情况下，
                    可能还有合并成一个变量导入
            （2）导入时候使用什么类型数据结构导入，数据框，字典，字符，列表等
            （3）导入时候的数据结构的调整
            （4）导入时候变量是否有存在，如果有存在，则需要提醒用户修改冲突的变量名称
            因此考虑将这部分独立出来进行处理。
        """
        # 使用当前“数据集名” / “页面” 的名称
        self.newdatasetname = {"varname": {}}
        e = self.import_param["datasetname"]
        while True:
            var_name, ok = QInputDialog.getText(self, "变量名", "输入新的变量名称:", QLineEdit.Normal, e)
            if ok:
                if len(var_name) == 0:
                    QMessageBox.warning(self, "提示", "请输入变量名称！")
                    continue
                elif self.extension_lib.Data.var_exists(var_name):
                    # 在变量名称冲突情况下，允许用户判断是否覆盖变量名称
                    isCover = QMessageBox().question(None, "提示", "变量 {} 已经存在，是否覆盖？".format(var_name),
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if isCover == QMessageBox.Yes:
                        break
                    else:
                        continue
                elif not var_name.isidentifier():
                    QMessageBox.warning(self, '提示', '变量名无效\n提示：\n1、不要以数字开头;\n2、不要包含除下划线外的所有符号。')
                else:
                    break
            else:
                ok = False
                self.import_param.update(ispreview=True, status=True)
                break
        if ok:
            self.newdatasetname["varname"][e] = var_name
            # if self.import_param["ismerge"]:
            #    self.newdatasetname["datasetname"] = var_name
            # self.import_param["datasetname"] = var_name
            # else:
            #    self.newdatasetname["varname"][e] = var_name
            # self.import_param["varname"][e] = var_name
        return (ok)

    def sendDataset(self):
        """
        这个方法与具体导入sas，spss还是excel数据都是无关的。
        其实意思就是把pandas数据加入到工作空间中。
        """
        if self.import_param["status"]:
            # if self.import_param["ismerge"]:
            #    set_var(self.newdatasetname["datasetname"], self.current_dataset)
            # else:
            for name_i, var_i in self.newdatasetname["varname"].items():
                set_var(var_i, self.current_dataset[name_i])  # 将数据导入工作空间
            QMessageBox.information(self, "{}导入结果".format(""), "数据导入完成！", QMessageBox.Yes)
            self.close()

    def clearImportParam(self):
        """重置数据集"""
        self.current_dataset = {}
        self.import_message = {"isError": False, "warningMessage": []}
        self.import_param = {
            "datasetname": "",  # 数据集名称
            "varname": {},  # 导入的变量名称，dict，用于后续存放更改变量名称后的结果
            "filepath": "",  # 文件路径
            "hasheader": True,  # 首行是否为列名称
            "dtypes": {},  # 字段数据类型，dict，用于后续存放更改数据类型后的结果
            "status": False,  # 导入结果状态：True = 导入成功，False = 导入失败
            "param": {},  # 导入面板上的参数，dict
            "ispreview": True,  # 是否预览
            "ismerge": False  # 多变量数据集是否合并成字典导入
        }

    def get_work_dir(self) -> str:
        """获取工作路径"""
        return self.extension_lib.Program.get_work_dir()

    def center(self):
        """将窗口置于中心"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        """按键盘Escape退出当前窗口"""
        if e.key() == Qt.Key_Escape:
            button = QMessageBox.question(self, "Question", "是否退出当前窗口？",
                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

            if button == QMessageBox.Ok:
                self.close()

    def showWarningMessage(self, info=""):
        """显示异常信息"""
        info = info if info else self.import_message["warningMessage"][0]
        if info:
            QMessageBox.warning(self, '警告：', info)
            logging.info("获取数据警告：\n" + info)

    def updateWarningMessage(self, info="", new=True):
        """更新导入状态"""
        if new:
            self.import_message["isError"] = True
            self.import_message["warningMessage"].append(info)
        else:
            self.import_message["isError"] = False
            self.import_message["warningMessage"] = []

    def checkFilePath(self, path):
        '''检查输入的文件路径是否合法'''
        if path:
            if not os.path.exists(path):
                self.updateWarningMessage(info="数据集路径不存在，\n请重新输入数据集路径！")

            if os.path.split(path)[-1].split(".")[-1].lower() not in self.file_types:
                self.updateWarningMessage(
                    info="数据文件格式有错：\n仅支持({})类型文件，\n请重新输入数据集路径！".format(self.file_types)
                )
        return (path)

    def checkRowsNumber(self, rows, types):
        '''检查行数是否为正整数或“全部”'''
        typesDict = {
            "limitRows": "“限定行数”必须是大于等于0的整数或“全部”",
            "skipRows": "“跳过行数”必须是大于等于0的整数"
        }
        if rows == "全部":
            row_number = None
        elif rows.isdigit():
            row_number = int(rows)
        else:
            row_number = 0
            self.updateWarningMessage(info="{}\n请重新输入！".format(typesDict[types]))
        if self.import_param["ispreview"] and types == "limitRows":
            # 判断是否为预览，或是限制行数
            row_number = min([100, row_number if row_number else 101])
        return (row_number)

    def headerAsColumns(self, data):
        """首行为列名"""
        colnames = pd.DataFrame([data.columns], index=[0], columns=data.columns.tolist())
        data.index += 1
        data = data.append(colnames, ignore_index=False)
        data.sort_index(inplace=True)
        data.columns = ["C" + str(i + 1) for i in range(data.shape[1])]
        return (data)

    def datasetUpdate(self, data, skiprow, limitrow):
        """对数据集的规模进行处理"""
        data = data[data.index >= skiprow]  # 跳过行数
        if limitrow:
            limitrows = min(data.shape[0], limitrow)
            data = data.head(limitrows)
        return (data)

    def showDatasetPreview(self, data, header=True):
        """导入的数据集可视化"""
        if not header:
            # 首行不为列名情况下的处理
            data = self.headerAsColumns(data)

        table_rows, table_colunms = data.head(100).shape
        table_header = [str(col_i) for col_i in data.columns.tolist()]

        self.tableWidget_previewData.setColumnCount(table_colunms)
        self.tableWidget_previewData.setRowCount(table_rows)
        self.tableWidget_previewData.setHorizontalHeaderLabels(table_header)

        # 数据预览窗口
        for i in range(table_rows):
            row_values = data.iloc[i].tolist()
            for j, element in enumerate(row_values):
                newItem = QTableWidgetItem(str(element))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_previewData.setItem(i, j, newItem)

    def updateDatasetNameLine(self, tag):
        """更新数据集显示标签"""
        new_datasetname = self.import_param["datasetname"] if tag == "（全部导入）" else tag
        self.lineEdit_datasetName.setText(new_datasetname)

    def clearPreviewDataTableWidget(self):
        """清理表格组件内容"""
        self.tableWidget_previewData.clear()
        self.showDatasetPreview(data=pd.DataFrame([]))

    def showHelp(self):
        from packages.pm_helpLinkEngine import helpLinkEngine as h
        h.helpLink.openHelp("dataio_sample_showhelp")

    # 数据库相关的方法

    def checkTextNotNull(self, dicts):
        """检验输入内容是否为空"""
        db_dict = {"host": "IP地址", "user": "用户名称", "passwd": "密码", "db": "数据库名称", "password": "密码",
                   "port": "IP端口", "charset": "数据类型", "table": "表格名称", "schema": "数据模式", "database": "数据库名称",
                   "server_name": "服务名称"}
        for k, v in dicts.items():
            if not v:
                self.updateWarningMessage(info="‘{tag}’不能为空，请重新输入！".format(tag=db_dict[k]))

    def updateDatabaseConnectStatusLabel(self, e=""):
        tag = {"label": "连接成功", "color": "color: blue;"}
        if e:
            tag.update(label='连接失败:' + e, color="color: rgb(255, 0, 0);")
        self.label_test.setHidden(False)
        self.label_test.setText(tag["label"])
        self.label_test.setStyleSheet(tag["color"])

    def dbConnectTestButton(self):
        """检查数据库连接是否有效"""
        self.import_param.update(ispreview=True)
        self.getImportParam()
        if self.import_message["isError"]:
            self.showWarningMessage()
            return

        error = self.importDatasetLoad()
        self.updateDatabaseConnectStatusLabel(error)

    def dbDatasetImportButton(self):
        """导入数据按钮"""
        self.import_param.update(ispreview=False)
        self.getImportParam()
        if self.import_message["isError"]:
            self.showWarningMessage()
            return
        var_name_check = self.updateDatasetVarname()
        if var_name_check:
            import sys
            t0 = time.time()
            error = self.importDatasetLoad()
            self.updateDatabaseConnectStatusLabel(error)
            self.sendDataset()
            t1 = time.time()
            logger.info("导入数据集所用时间: {t} s 大小 {m} MB".format(
                t=round(t1 - t0, 2), m=round(sys.getsizeof(self.current_dataset) / 1024, 2)
            ))
            self.current_dataset = None

    def getCurFetchData(self, cur):
        """获取数据库返回的分页数据"""
        temp = pd.DataFrame([])
        try:
            cur.execute(self.import_param["sql"])
            if cur.description:
                temp = pd.DataFrame(data=list(cur.fetchall()),
                                    columns=list(map(lambda x: x[0], cur.description)))
        except Exception as e:
            self.updateWarningMessage("导入失败，错误详情：\n{}" + str(e))
        return (temp)

    def updateChooseTagName(self, comboBox, tagname=[]):
        """ 加载导入文件变量名称 """
        comboBox.clear()
        if not self.import_param["status"]:
            return
        if not tagname:
            tagname = list(self.current_dataset)
        tagname = ["（全部导入）"] + tagname if len(tagname) > 1 else tagname
        for v in tagname:
            # 更新Excel导入界面中"数据位置"列表
            comboBox.addItem(v)


# 优化完成
class ImportTextForm(ImportDialog, dataImportFormEngine):
    """
    "导入Text"窗口，包含方法：
    （1）getImportParam：获取面板中的配置信息
    （2）importDatasetReload：重新加载文件数据内容
    （3）updateTableView：更新视图呈现数据
    """

    def __init__(self, parent=None):
        self.file_types = "*.csv *.txt *.tsv"
        self.IconPath = ":/resources/icons/txt.svg"
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_ifColumns.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.checkBox_asString.stateChanged.connect(self.previewButton)  # 是否以文本形式导入
        self.comboBox_encode.currentTextChanged.connect(self.previewButton)  # 选择编码方式
        self.comboBox_separator.currentTextChanged.connect(self.previewButton)  # 选择分割符号

    def updateUIForm(self):
        """ImportTextForm配置参数部分"""
        separator_char = ["\\n"] + self.separator_char
        self.comboBox_encode = self.updateForm_ComboBox(self.comboBox_encode, self.encode_type)
        self.comboBox_separator = self.updateForm_ComboBox(self.comboBox_separator, separator_char)

        self.horizontalLayoutAddUI(self.checkBox_asString)
        self.horizontalLayoutAddUI(self.checkBox_ifColumns)

        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.verticalLayoutAddUI(self.lineEdit_limitRow, "left")
        self.verticalLayoutAddUI(self.lineEdit_skipRow, "left")
        self.verticalLayoutAddUI(self.comboBox_separator, "right")
        self.verticalLayoutAddUI(self.comboBox_encode, "right")
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=self.checkBox_ifColumns.isChecked(),
            status=False, varname={}, dtypes={},
            asString=self.checkBox_asString.isChecked(),
            param={
                "filepath_or_buffer": self.checkFilePath(self.lineEdit_filePath.text()),
                "engine": "python",
                "header": 'infer' if self.checkBox_ifColumns.isChecked() else None,
                "sep": self.comboBox_separator.currentText(),
                "encoding": self.comboBox_encode.currentText(),
                "nrows": self.checkRowsNumber(self.lineEdit_limitRow.text(), "limitRows"),
                "skiprows": self.checkRowsNumber(self.lineEdit_skipRow.text(), "skipRows")
            }
        )

    def importDatasetReload(self):
        """
            刷新导入的数据
            file_path: 导入路径
        """
        param = self.import_param["param"]
        self.current_dataset = {}
        varname = self.import_param["datasetname"]

        if self.import_param["asString"]:
            with open(file=param["filepath_or_buffer"], encoding=param["encoding"]) as f:
                size = param["nrows"] if param["nrows"] else -1
                temp = f.read(size)
            f.close()
        else:
            temp = pd.read_table(**param)
        # 文本一次只导入一个文件，因此默认变名称即为数据集名称
        self.current_dataset[varname] = temp
        self.getDatasetInfo()
        self.import_param.update(status=True)

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()

        if not self.import_param["status"]:
            return

        dataset = self.current_dataset[self.import_param["datasetname"]]
        if self.checkBox_asString.isChecked():
            preview_data = pd.DataFrame({"文本": [dataset[:100]]})
            header = True
        else:
            preview_data = dataset.head(100)
            header = self.checkBox_ifColumns.isChecked()

        self.showDatasetPreview(data=preview_data, header=header)


# 优化完成
class ImportCsvForm(ImportDialog, dataImportFormEngine):
    """导入CSV窗口"""

    def __init__(self, parent=None):
        self.IconPath = ":/resources/icons/csv.svg"
        self.file_types = "*.csv"
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_ifColumns.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.checkBox_ifColIndex.stateChanged.connect(self.previewButton)  # 首列是否为列名
        self.comboBox_encode.currentTextChanged.connect(self.previewButton)  # 选择编码方式
        self.comboBox_separator.currentTextChanged.connect(self.previewButton)  # 选择分割符号

    def updateUIForm(self):
        """ImportTextForm配置参数部分"""
        self.comboBox_separator = self.updateForm_ComboBox(self.comboBox_separator, self.separator_char)
        self.comboBox_encode = self.updateForm_ComboBox(self.comboBox_encode, self.encode_type)

        self.horizontalLayoutAddUI(self.checkBox_ifColumns)
        self.horizontalLayoutAddUI(self.checkBox_ifColIndex)

        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.verticalLayoutAddUI(self.lineEdit_limitRow, "left")
        self.verticalLayoutAddUI(self.lineEdit_skipRow, "left")
        self.verticalLayoutAddUI(self.comboBox_separator, "right")
        self.verticalLayoutAddUI(self.comboBox_encode, "right")
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=self.checkBox_ifColumns.isChecked(),
            status=False, varname={}, dtypes={},
            param={
                "filepath_or_buffer": self.checkFilePath(self.lineEdit_filePath.text()),
                "engine": "c",
                "header": 'infer' if self.checkBox_ifColumns.isChecked() else None,
                "sep": self.comboBox_separator.currentText(),
                "index_col": 0 if self.checkBox_ifColIndex.isChecked() else None,
                "encoding": self.comboBox_encode.currentText(),
                "nrows": self.checkRowsNumber(self.lineEdit_limitRow.text(), "limitRows"),
                "skiprows": self.checkRowsNumber(self.lineEdit_skipRow.text(), "skipRows")
            }
        )

    def importDatasetReload(self):
        """
            刷新导入的数据
            file_path: 导入路径
        """
        param = self.import_param["param"]
        self.current_dataset = {}
        varname = self.import_param["datasetname"]
        # CSV一次只导入一个文件，因此默认变名称即为数据集名称
        self.current_dataset[varname] = pd.read_csv(**param)
        run_command("", "pd.read_csv(%s)" % kwargs_to_str(param))
        self.getDatasetInfo()
        self.import_param.update(status=True)

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()

        if not self.import_param["status"]:
            return

        dataset = self.current_dataset[self.import_param["datasetname"]]
        if self.comboBox_separator.currentText() == "(无)":
            preview_data = pd.DataFrame({"文本": [dataset[:100]]})
            header = True
        else:
            preview_data = dataset.head(100)
            header = self.checkBox_ifColumns.isChecked()

        self.showDatasetPreview(data=preview_data, header=header)


# 后续还需要进一步优化方案
class ImportExcelForm(ImportDialog, dataImportFormEngine):
    """打开excel导入窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.IconPath = ":/resources/icons/excel.svg"
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.new_import_filepath = ""
        self.file_types = "*.xls *.xlsx"
        self.sheetsname = []
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_ifColumns.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.checkBox_ifColIndex.stateChanged.connect(self.previewButton)  # 首列是否为列名
        self.comboBox_sheetname.currentTextChanged.connect(self.updateTableView)  # 切换页面

    def updateUIForm(self):
        """ImportTextForm配置参数部分"""
        self.horizontalLayoutAddUI(self.checkBox_ifColumns)  # 首行为列名
        self.horizontalLayoutAddUI(self.checkBox_ifColIndex)  # 首列为行名

        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")  # 数据集名称
        self.verticalLayoutAddUI(self.comboBox_sheetname, "right")  # 页面名称
        self.verticalLayoutAddUI(self.lineEdit_limitRow, "left")  # 限制行数
        self.verticalLayoutAddUI(self.lineEdit_skipRow, "right")  # 跳过行数
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取Excel里头的页面信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        # Excel 部分，默认都是全部数据导入后在内存中做处理, 因此 ispreview 都是 False
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=self.checkBox_ifColumns.isChecked(),
            status=False, varname={}, dtypes={}, loaddataset=False, ismerge=True,
            limitrows=self.checkRowsNumber(self.lineEdit_limitRow.text(), "limitRows"),
            skiprows=self.checkRowsNumber(self.lineEdit_skipRow.text(), "skipRows"),
            param={
                "io": self.checkFilePath(self.lineEdit_filePath.text()),
                "engine": "python",
                "sheet_name": "",
                "header": 'infer' if self.checkBox_ifColumns.isChecked() else None,
                "nrows": None,  # 默认全部加载，在内存中做处理
                "index_col": 0 if self.checkBox_ifColIndex.isChecked() else None,
                "skiprows": 0
            }
        )

        if self.import_message["isError"]:
            return

        if self.new_import_filepath != self.import_param["filepath"]:
            # 当前仅当文件路径发生变化时候进行重载，否则以内存中数据呈现对应变化
            self.import_param.update(loaddataset=True)
            self.LoadSheetname()

    def LoadSheetname(self):
        """预先加载 sheetname 信息"""
        ftype = os.path.split(self.import_param["filepath"])[1].endswith("xls")
        # 获取excel 工作簿中所有的sheet,设置 sheet 名
        if ftype:
            # 针对 xls 格式
            wb = xlrd.open_workbook(self.import_param["filepath"])
            self.sheetsname = wb.sheet_names()
        else:
            # 针对 xlsx 格式
            wb = openpyxl.load_workbook(self.import_param["filepath"], read_only=True)
            self.sheetsname = wb.sheetnames

        # 选择导入引擎
        self.import_param["param"].update(engine='xlrd' if ftype else 'openpyxl')

        # 如果存在多个页面时，需要考虑到将Excel文件中所有页面都导入，因此通过（全部导入）作为标识
        # self.updateChooseTagName(self.comboBox_sheetname, tagname = self.sheetsname)
        self.comboBox_sheetname.clear()
        tagname = ["（全部导入）"] + self.sheetsname if len(self.sheetsname) > 1 else self.sheetsname
        for v in tagname:
            # 更新Excel导入界面中"数据位置"列表
            self.comboBox_sheetname.addItem(v)

    def importDatasetReload(self):
        """
            刷新导入的数据
        """
        if self.import_param["loaddataset"]:
            param = self.import_param["param"]
            self.current_dataset = {}
            for sheet_i in self.sheetsname:
                # 默认都是全部加载后在处理
                param.update(sheet_name=sheet_i)
                self.current_dataset[sheet_i] = pd.read_excel(**param)
                run_command("", "pd.read_excel(%s)" % kwargs_to_str(param))

        if not self.import_param["ispreview"]:
            sheet_ind = self.comboBox_sheetname.currentText()
            if sheet_ind != "（全部导入）":
                self.import_param.update(ismerge=False)
                self.current_dataset = {sheet_ind: self.current_dataset[sheet_ind]}

            for name_i, temp in self.current_dataset.items():
                if not self.import_param["hasheader"]:
                    temp = self.headerAsColumns(temp)
                self.current_dataset[name_i] = self.datasetUpdate(
                    data=temp, limitrow=self.import_param["limitrows"], skiprow=self.import_param["skiprows"]
                )

        self.new_import_filepath = self.import_param["filepath"]
        self.getDatasetInfo()
        self.import_param.update(status=True, loaddataset=False)

    def updateTableView(self):
        """
            刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()

        self.updateDatasetNameLine(tag=self.comboBox_sheetname.currentText())

        if not self.import_param["status"]:
            self.showDatasetPreview(data=pd.DataFrame([]))
            return

        # 首行是否为列名
        header = self.checkBox_ifColumns.isChecked()
        # 获取当前选择的表格信息
        load_sheet = self.comboBox_sheetname.currentText()
        l = self.import_param["limitrows"]
        s = self.import_param["skiprows"]

        if load_sheet == "（全部导入）":
            temp = []
            for name_i, data_i in self.current_dataset.items():
                if not header:
                    data_i = self.headerAsColumns(data_i)
                data_i = self.datasetUpdate(data_i, limitrow=l, skiprow=s)
                row_i, col_i = data_i.shape
                temp.append([name_i, row_i, col_i, data_i.columns.tolist()])
            header = True  # 避免呈现矩阵时候效果出现问题
            preview_data = pd.DataFrame(temp, columns=["表名称", "行数", "列数", "列名称"])
        else:
            preview_data = self.datasetUpdate(self.current_dataset[load_sheet], limitrow=l, skiprow=s)
        self.showDatasetPreview(data=preview_data, header=header)


# 优化完成
class ImportSpssForm(ImportDialog, dataImportFormEngine):
    """
    打开"从spss导入"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_types = "*.sav"
        self.IconPath = ":/resources/icons/spss.svg"
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_ifColumns.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.comboBox_encode.currentIndexChanged.connect(self.previewButton)  # 选择编码方式

    def updateUIForm(self):
        """ImportTextForm配置参数部分"""
        self.encode_type = ["gbk", "utf8", "gb2312", "ascii"]
        self.comboBox_encode = self.updateForm_ComboBox(self.comboBox_encode, self.encode_type)

        self.horizontalLayoutAddUI(self.checkBox_ifColumns)
        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.verticalLayoutAddUI(self.comboBox_encode, "right")
        self.verticalLayoutAddUI(self.lineEdit_limitRow, "left")
        self.verticalLayoutAddUI(self.lineEdit_skipRow, "right")
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=self.checkBox_ifColumns.isChecked(),
            status=False, varname={}, dtypes={},
            limitrows=self.checkRowsNumber(self.lineEdit_limitRow.text(), "limitRows"),
            skiprows=self.checkRowsNumber(self.lineEdit_skipRow.text(), "skipRows"),
            param={
                "filename_path": self.checkFilePath(self.lineEdit_filePath.text()),
                "encoding": self.comboBox_encode.currentText()
            }
        )

    def importDatasetReload(self):
        """
            刷新导入的数据
        """
        import pyreadstat
        param = self.import_param["param"]
        self.current_dataset = {}
        varname = self.import_param["datasetname"]
        self.current_dataset[varname], meta = pyreadstat.read_sav(**param)
        # SPSS一次只导入一个文件，因此默认变名称即为数据集名称
        self.getDatasetInfo()
        self.import_param.update(status=True)

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()
        if not self.import_param["status"]:
            return

        name = self.import_param["datasetname"]
        self.showDatasetPreview(data=self.current_dataset[name], header=True)


# 优化完成
class ImportSasForm(ImportDialog, dataImportFormEngine):
    """打开从sas导入窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_types = "*.sas7bdat"
        self.IconPath = ":/resources/icons/sas.ico"
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        # 导入窗口的相关事件
        # 在"导入"窗口，打开选择文件
        self.pushButton_choosefile.clicked.connect(self.chooseFileButton)

        # 帮助
        self.pushButton_help.clicked.connect(self.showHelp)

        # 配置更新数据
        self.checkBox_ifColumns.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.comboBox_encode.currentIndexChanged.connect(self.previewButton)  # 选择编码方式

        # 按键更新数据
        self.pushButton_preview.clicked.connect(self.previewButton)  # 预览
        self.pushButton_ok.clicked.connect(self.importDatasetButton)  # 导入
        self.pushButton_cancel.clicked.connect(self.close)  # 取消

    def updateUIForm(self):
        """ImportTextForm配置参数部分"""
        self.comboBox_encode = self.updateForm_ComboBox(self.comboBox_encode, self.encode_type)

        self.horizontalLayoutAddUI(self.checkBox_ifColumns)
        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.verticalLayoutAddUI(self.comboBox_encode, "right")
        self.verticalLayoutAddUI(self.lineEdit_limitRow, "left")
        self.verticalLayoutAddUI(self.lineEdit_skipRow, "right")
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=self.checkBox_ifColumns.isChecked(),
            status=False, varname={}, dtypes={},
            param={
                "filepath_or_buffer": self.checkFilePath(self.lineEdit_filePath.text()),
                "format": "sas7bdat",
                "encoding": self.comboBox_encode.currentText()
            }
        )

    def importDatasetReload(self):
        """
            刷新导入的数据
        """
        param = self.import_param["param"]
        self.current_dataset = {}
        varname = self.import_param["datasetname"]
        self.current_dataset[varname] = pd.read_sas(**param)
        # SPSS一次只导入一个文件，因此默认变名称即为数据集名称
        self.getDatasetInfo()
        self.import_param.update(status=True)

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()
        if not self.import_param["status"]:
            return

        name = self.import_param["datasetname"]
        self.showDatasetPreview(data=self.current_dataset[name], header=True)


# 优化完成
class ImportMatlabForm(ImportDialog, dataImportFormEngine):
    """打开matlab导入窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.new_import_filepath = ""
        self.file_types = "*.mat"
        self.IconPath = ":/resources/icons/matlab.svg"
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_asDataFrame.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名
        self.comboBox_varname.currentTextChanged.connect(self.updateTableView)

    def updateUIForm(self):
        """ImportMatlabForm配置参数部分"""
        self.horizontalLayoutAddUI(self.checkBox_asDataFrame)
        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.verticalLayoutAddUI(self.comboBox_varname, "right")
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(), loaddataset=False,
            status=False, varname={}, dtypes={}, ismerge=True,
            asdataframe=self.checkBox_asDataFrame.isChecked(),
            param={
                "file_name": self.checkFilePath(self.lineEdit_filePath.text())
            }
        )

        if self.import_message["isError"]:
            return

        if self.new_import_filepath != self.import_param["filepath"]:
            # 当前仅当文件路径发生变化时候进行重载，否则以内存中数据呈现对应变化
            self.import_param.update(loaddataset=True)

    def importDatasetReload(self):
        """
            刷新导入的数据
        """
        if self.import_param["loaddataset"]:
            import scipy.io as sio
            param = self.import_param["param"]
            self.current_dataset = {}
            mat_dataset = sio.loadmat(**param)
            self.new_import_filepath = self.import_param["filepath"]
            for name_i, var_i in mat_dataset.items():
                if type(var_i) == np.ndarray and name_i[:2] != "__":
                    # 只保留数组类型的数据
                    # 由于部分非矩阵类型数据也是使用 ndarray 类型存储，因此只能使用 type 获取到的类型和 np.ndarray来比较
                    # 这样才能定位到需要的数组类型数据
                    # 注意：目前 scipy.io.loadmat 方法无法解析 matlab 的 table 类型数据！
                    # 预留一种场景：导入时候以 DataFrame 还是 ndarray 形式
                    self.current_dataset[name_i] = var_i
            self.import_param.update(status=True, loaddataset=False)
            self.updateChooseTagName(self.comboBox_varname)

        if not self.import_param["ispreview"]:
            for name_i, var_i in self.current_dataset.items():
                self.current_dataset[name_i] = pd.DataFrame(var_i) if self.import_param["asdataframe"] and len(
                    var_i.shape) <= 2 else var_i
            varname = self.comboBox_varname.currentText()
            if varname != "（全部导入）":
                self.import_param.update(ismerge=False)
                self.current_dataset = {varname: self.current_dataset[varname]}
        self.getDatasetInfo()  # 更新当前数据集的信息

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容

        varname = self.comboBox_varname.currentText()
        self.clearPreviewDataTableWidget()
        self.updateDatasetNameLine(tag=varname)
        if not self.import_param["status"]:
            self.showDatasetPreview(data=pd.DataFrame([]))
            return

        if varname == "（全部导入）":
            temp = []
            for name_i, data_i in self.current_dataset.items():
                temp.append([name_i, data_i.shape, type(data_i)])
            preview_data = pd.DataFrame(temp, columns=["表名称", "大小", "数据格式"])
        elif not varname:
            return
        else:
            temp = self.current_dataset[varname]
            if len(self.current_dataset[varname].shape) > 2:
                temp = pd.DataFrame([{
                    "变量": varname, "数据类型": type(temp), "数据格式": temp.dtype,
                    "大小": self.current_dataset[varname].shape
                }])
            else:
                temp = pd.DataFrame(self.current_dataset[varname][0:100])
                temp.columns = ["C" + str(i + 1) for i in range(temp.shape[1])]
            preview_data = temp
        self.showDatasetPreview(data=preview_data, header=True)


# 优化完成
class ImportStataForm(ImportDialog, dataImportFormEngine):
    """打开stata导入窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_types = "*.dta"
        self.IconPath = ":/resources/icons/stata.svg"
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.updateUIForm()

    def AddUIFormActivity(self):
        """增加界面中的操作操作响应"""
        self.checkBox_ifColIndex.stateChanged.connect(self.updateTableView)  # 选择首行是否为列名

    def updateUIForm(self):
        """ImportMatlabForm配置参数部分"""
        self.horizontalLayoutAddUI(self.checkBox_ifColIndex)
        self.verticalLayoutAddUI(self.lineEdit_datasetName, "left")
        self.publicUIFormActivity()
        self.AddUIFormActivity()

    def getImportParam(self):
        """
            获取界面中的配置信息
            （1）首行列名（2）数据集名称（3）跳过行数（4）限定行数（5）文件编码（6）分割符号
        """
        self.updateWarningMessage(new=False)
        self.import_param.update(
            datasetname=self.lineEdit_datasetName.text(),
            filepath=self.lineEdit_filePath.text(),
            hasheader=True,
            status=False, varname={}, dtypes={},
            param={
                "filepath_or_buffer": self.checkFilePath(self.lineEdit_filePath.text()),
                "index_col": 0 if self.checkBox_ifColIndex.isChecked() else None
            }
        )

    def importDatasetReload(self):
        """
            刷新导入的数据
        """
        param = self.import_param["param"]
        self.current_dataset = {}
        varname = self.import_param["datasetname"]
        self.current_dataset[varname] = pd.read_stata(**param)
        # Stata一次只导入一个文件，因此默认变名称即为数据集名称
        self.getDatasetInfo()
        self.import_param.update(status=True)

    def updateTableView(self):
        """
        刷新预览数据
        """
        # 处理需要呈现的内容
        self.clearPreviewDataTableWidget()
        if not self.import_param["status"]:
            return

        name = self.import_param["datasetname"]
        self.showDatasetPreview(data=self.current_dataset[name], header=True)
