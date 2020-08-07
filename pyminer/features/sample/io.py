import os
import sys
import logging
import numpy as np
import pandas as pd
import datetime

# 导入PyQt5模块
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#导入功能组件
from pyminer.ui.data.data_import_text import Ui_Form as Import_Ui_Form
from pyminer.ui.data.data_import_excel import Ui_Form as ExcelImport_Ui_Form
from pyminer.ui.data.data_import_spss import Ui_Form as SPSSImport_Ui_Form
from pyminer.ui.data.data_import_sas import Ui_Form as SASImport_Ui_Form
from pyminer.ui.data.data_import_database import Ui_Form as ImportDatabase_Ui_Form

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)


class ImportForm(QDialog):
    """
    "导入"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于传递文件路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Import_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

        #QssTools.set_qss_to_obj(ui_dir + "/source/qss/patata.qss", self)

        self.file_path = ''
        self.__current_dataset_name = ""
        self.__path_openfile_name = ""
        self.__current_dataset = pd.DataFrame()

        # self.import_file_path_init()

        # 导入窗口的相关事件
        # 在"导入"窗口，打开选择文件
        self.__ui.pushButton_choosefile.clicked.connect(self.openFile)
        # 展示数据
        self.__ui.checkBox_ifColumns.stateChanged['int'].connect(self.import_dateset_reload)
        self.__ui.comboBox_separator.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.comboBox_encode.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_filePath.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_passHead.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_datasetName.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_limitRow.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_missValue.textChanged['QString'].connect(self.import_dateset_reload)

        # 更新数据
        self.__ui.pushButton_ok.clicked.connect(self.import_send_dataset)
        self.__ui.pushButton_cancel.clicked.connect(self.close)
        # 帮助
        # self.__ui.pushButton_help.clicked.connect(self.accept_signal)

    def file_path_init(self):
        print("开始更新数据")
        print("开始修改文件路径")
        self.__path_openfile_name = self.file_path
        if len(self.__path_openfile_name) != 0:
            self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

            self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
            self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
            logging.info(
                "加载成功file_path{}，datasetName：{}".format(self.__path_openfile_name, self.__current_dataset_name))

            if len(self.__path_openfile_name) > 0:
                if self.__ui.checkBox_ifColumns.isChecked():
                    header = 0
                else:
                    header = None
                # 仅预览前100条数据
                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows_preview = 100
                elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                    nrows_preview = int(self.__ui.lineEdit_limitRow.text())
                else:
                    nrows_preview = 100

                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows = 100000000
                else:
                    nrows = int(self.__ui.lineEdit_limitRow.text())

                encoding = self.__ui.comboBox_encode.currentText()
                skiprows = int(self.__ui.lineEdit_passHead.text())
                sep = self.__ui.comboBox_separator.currentText()

                if self.__ui.lineEdit_missValue.text() != "默认":
                    na_values = self.__ui.lineEdit_missValue.text()
                else:
                    na_values = None

                logging.info("path_openfile_name：{}，header：{}，skiprows：{}，nrows：{}，na_values:{}".format(
                    self.__path_openfile_name, header, skiprows, nrows_preview, na_values))

                self.__current_dataset = pd.read_csv(self.__path_openfile_name, engine="python", sep=sep,
                                                     encoding=encoding,
                                                     header=header,
                                                     skiprows=skiprows, nrows=nrows, na_values=na_values)

                if len(self.__current_dataset) == 0:
                    self.__ui.tableWidget_previewData.clear()
                    logging.info("当前有效数据为空")
                else:
                    self.import_dateset_preview()
                    logging.info("数据导入成功")
            else:
                logging.info("请选择数据集")

    def import_send_dataset(self):
        logging.info("发射导入数据信号")
        if len(self.__current_dataset) > 0:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.file_path
            print("path:", path)
            file_size=str(os.path.getsize(path))
            print("file_size:",file_size)
            remarks = ''
            self.signal_data_change.emit(self.__current_dataset_name, self.__current_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            logging.info("导入数据信号已发射")
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def openFile(self):
        """
        选择文件
        """
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', '文本文件(*.csv *.txt *.tsv)')
        self.__path_openfile_name = openfile_name[0]
        self.file_path = openfile_name[0]
        self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

        self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
        self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)

    def import_dateset_reload(self):
        """
        刷新导入的数据
        """
        header = 0
        nrows_preview = 100
        sep = ','
        skiprows = 0

        if len(self.__path_openfile_name) > 0:
            if self.__ui.checkBox_ifColumns.isChecked():
                header = 'infer'
            else:
                header = None
            # 仅预览前100条数据
            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows_preview = 100
            elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                nrows_preview = int(self.__ui.lineEdit_limitRow.text())
            else:
                nrows_preview = 100

            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows = 100000000
            else:
                nrows = int(self.__ui.lineEdit_limitRow.text())

            encoding = self.__ui.comboBox_encode.currentText()
            sep = self.__ui.comboBox_separator.currentText()
            skiprows = int(self.__ui.lineEdit_passHead.text())

            if self.__ui.lineEdit_limitRow.text() != "默认":
                na_values = self.__ui.lineEdit_missValue.text()

            self.__current_dataset = pd.read_csv(self.__path_openfile_name, engine="python", sep=sep, encoding=encoding,
                                                 header=header,
                                                 skiprows=skiprows, nrows=nrows, na_values=na_values)

            if len(self.__current_dataset) == 0:
                self.__ui.tableWidget_previewData.clear()
                logging.info("当前有效数据为空")
            else:
                self.import_dateset_preview()
                logging.info("数据导入成功")

    def import_dateset_preview(self):
        """
        刷新预览数据
        """
        if len(self.__current_dataset) > 0:
            input_table_rows = self.__current_dataset.head(100).shape[0]
            input_table_colunms = self.__current_dataset.shape[1]
            input_table_header = self.__current_dataset.columns.values.tolist()
            self.__ui.tableWidget_previewData.setColumnCount(input_table_colunms)
            self.__ui.tableWidget_previewData.setRowCount(input_table_rows)

            # 设置数据预览窗口的标题行
            table_header = []
            i = 1
            while i <= len(self.__current_dataset.columns):
                table_header.append("C" + str(i))
                i += 1

            if self.__ui.checkBox_ifColumns.isChecked():
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(input_table_header)
            else:
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(table_header)
                self.__current_dataset.columns = table_header
            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.__current_dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.__ui.tableWidget_previewData.setItem(i, j, newItem)

    def get_dateset_name(self):
        return self.__current_dataset_name

    def get_current_dataset(self):
        return self.__current_dataset

    def get_current_columns(self):
        return self.__current_dataset.columns


class ImportDatabase(QDialog):
    """
    "导入"窗口
    """
    signal_data_change = pyqtSignal(str, dict)  # 自定义信号，用于传递文件路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = ImportDatabase_Ui_Form()
        self.__ui.setupUi(self)
        self.center()
        #QssTools.set_qss_to_obj(ui_dir + "/source/qss/patata.qss", self)

        self.__ui.pushButton_cancel.clicked.connect(self.close)

    def closeEvent(self, event):
        """
        退出时弹出确认消息提示
        """
        reply = QMessageBox.question(self, '信息', '确认退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def import_send_dataset(self):
        logging.info("发射导入数据信号")
        if len(self.__current_dataset) > 0:
            self.signal_data_change.emit(self.__current_dataset_name, self.__current_dataset.to_dict())  # 发射信号
            logging.info("导入数据信号已发射")
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()


class ImportExcelForm(QDialog):
    """
    打开"从excel导入"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于传递文件路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = ExcelImport_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

        #QssTools.set_qss_to_obj(ui_dir + "/source/qss/patata.qss", self)

        self.file_path = ''
        self.__path_openfile_name = ""
        self.__current_dataset_name = ""
        self.__current_dataset = pd.DataFrame()

        # 导入窗口的相关事件
        # 在"导入"窗口，打开选择文件
        self.__ui.pushButton_choosefile.clicked.connect(self.openFile)
        # 展示数据
        self.__ui.checkBox_ifColumns.stateChanged['int'].connect(self.import_dateset_reload)
        self.__ui.comboBox_sheet.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.comboBox_encode.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_filePath.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_passHead.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_datasetName.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_limitRow.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_missValue.textChanged['QString'].connect(self.import_dateset_reload)

        # 更新数据
        self.__ui.pushButton_ok.clicked.connect(self.import_send_dataset)
        self.__ui.pushButton_cancel.clicked.connect(self.close)

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
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def import_send_dataset(self):
        logging.info("发射导入数据信号")
        if len(self.__current_dataset) > 0:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.file_path
            file_size = str(os.path.getsize(path))
            remarks = ''
            self.signal_data_change.emit(self.__current_dataset_name, self.__current_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def file_path_init(self, file_path):
        """
        #初始化excel文件路径、sheet名单,以便指定需要导入的sheet
        """
        self.__path_openfile_name = file_path
        if len(self.__path_openfile_name) != 0:
            self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

            import openpyxl
            wb = openpyxl.load_workbook(self.__path_openfile_name)

            # 获取excel 工作簿中所有的sheet
            sheets = wb.sheetnames
            self.__ui.comboBox_sheet.clear()
            for s in sheets:
                self.__ui.comboBox_sheet.addItem(s)

            self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
            self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
            logging.info(
                "加载成功file_path{}，datasetName：{}".format(self.__path_openfile_name, self.__current_dataset_name))

            if len(self.__path_openfile_name) > 0:
                if self.__ui.checkBox_ifColumns.isChecked():
                    header = 0
                else:
                    header = None
                # 仅预览前100条数据
                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows_preview = 100
                elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                    nrows_preview = int(self.__ui.lineEdit_limitRow.text())
                else:
                    nrows_preview = 100

                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows = 100000000
                else:
                    nrows = int(self.__ui.lineEdit_limitRow.text())

                encoding = self.__ui.comboBox_encode.currentText()
                skiprows = int(self.__ui.lineEdit_passHead.text())
                sheet = self.__ui.comboBox_sheet.currentText()

                if self.__ui.lineEdit_missValue.text() != "默认":
                    na_values = self.__ui.lineEdit_missValue.text()
                else:
                    na_values = None

                logging.info("path_openfile_name：{}，sheet_name：{}，header：{}，skiprows：{}，nrows：{}，na_values:{}".format(
                    self.__path_openfile_name, sheet, header, skiprows, nrows_preview, na_values))

                self.__current_dataset = pd.read_excel(self.__path_openfile_name, sheet_name=sheet,
                                                       header=header,
                                                       skiprows=skiprows, nrows=nrows, na_values=na_values)

                if len(self.__current_dataset) == 0:
                    self.__ui.tableWidget_previewData.clear()
                    logging.info("当前sheet页有效数据为空")
                else:
                    self.import_dateset_preview()
                    logging.info("数据导入成功")
            else:
                logging.info("请选择数据集")

    def openFile(self):
        """
        选择文件
        """
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'EXCEL文件(*.xls *.xlsx *.xlsm *.xltx *.xltm)')
        logging.info(openfile_name)

        self.__path_openfile_name = openfile_name[0]
        self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

        # 获取excel 工作簿中所有的sheet
        import openpyxl
        wb = openpyxl.load_workbook(self.__path_openfile_name)
        sheets = wb.sheetnames
        self.__ui.comboBox_sheet.clear()
        for s in sheets:
            self.__ui.comboBox_sheet.addItem(s)

        self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
        self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
        logging.info("加载成功file_path{}，datasetName：{}".format(openfile_name, self.__current_dataset_name))
        self.import_dateset_reload()

    def get_dateset_name(self):
        return self.__current_dataset_name

    def import_dateset_reload(self):
        """
        刷新导入的数据
        """
        header = 0
        nrows_preview = 100
        sep = ','
        skiprows = 0
        # datasetName 为当前已选文件对应的excel数据路径

        if len(self.__path_openfile_name) > 0:
            if self.__ui.checkBox_ifColumns.isChecked():
                header = 0
            else:
                header = None
            # 仅预览前100条数据
            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows_preview = 100
            elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                nrows_preview = int(self.__ui.lineEdit_limitRow.text())
            else:
                nrows_preview = 100

            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows = 100000000
            else:
                nrows = int(self.__ui.lineEdit_limitRow.text())

            encoding = self.__ui.comboBox_encode.currentText()
            skiprows = int(self.__ui.lineEdit_passHead.text())
            sheet = self.__ui.comboBox_sheet.currentText()

            if self.__ui.lineEdit_missValue.text() != "默认":
                na_values = self.__ui.lineEdit_missValue.text()
            else:
                na_values = None

            logging.info("path_openfile_name：{}，sheet_name：{}，header：{}，skiprows：{}，nrows：{}，na_values:{}".format(
                self.__path_openfile_name, sheet, header, skiprows, nrows_preview, na_values))
            self.__current_dataset = pd.read_excel(self.__path_openfile_name, sheet_name=sheet,
                                                   header=header,
                                                   skiprows=skiprows, nrows=nrows, na_values=na_values)

            if len(self.__current_dataset) == 0:
                self.__ui.tableWidget_previewData.clear()
                logging.info("当前sheet页有效数据为空")
            else:
                self.import_dateset_preview()
                logging.info("数据导入成功")

    def import_dateset_preview(self):
        """
        刷新预览数据
        """
        if len(self.__current_dataset) > 0:
            input_table_rows = self.__current_dataset.head(100).shape[0]  # 预览前100行
            input_table_colunms = self.__current_dataset.shape[1]
            input_table_header = self.__current_dataset.columns.values.tolist()
            self.__ui.tableWidget_previewData.setColumnCount(input_table_colunms)
            self.__ui.tableWidget_previewData.setRowCount(input_table_rows)

            # 设置数据预览窗口的标题行
            table_header = []
            i = 1
            while i <= len(self.__current_dataset.columns):
                table_header.append("C" + str(i))
                i += 1

            if self.__ui.checkBox_ifColumns.isChecked():
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(input_table_header)
            else:
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(table_header)
                self.__current_dataset.columns = table_header
            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.__current_dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.__ui.tableWidget_previewData.setItem(i, j, newItem)

    def get_current_dataset(self):
        return self.__current_dataset

    def get_current_columns(self):
        return self.__current_dataset.columns


class ImportSpssForm(QDialog):
    """
    打开"从spss导入"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于传递文件路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = SPSSImport_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

        #QssTools.set_qss_to_obj(ui_dir + "/source/qss/patata.qss", self)

        self.file_path = ''
        self.__path_openfile_name = ""
        self.__current_dataset_name = ""
        self.__current_dataset = pd.DataFrame()

        self.all_dataset = dict()

        # 导入窗口的相关事件
        # 在"导入"窗口，打开选择文件
        self.__ui.pushButton_choosefile.clicked.connect(self.openFile)
        # 展示数据
        self.__ui.checkBox_ifColumns.stateChanged['int'].connect(self.import_dateset_reload)
        self.__ui.comboBox_encode.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_filePath.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_passHead.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_datasetName.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_limitRow.textChanged['QString'].connect(self.import_dateset_reload)

        # 更新数据
        self.__ui.pushButton_ok.clicked.connect(self.import_send_dataset)
        self.__ui.pushButton_cancel.clicked.connect(self.close)

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
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def import_send_dataset(self):
        logging.info("发射导入数据信号")
        if len(self.__current_dataset) > 0:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.file_path
            file_size = self.all_dataset.get("")
            remarks = ''
            self.signal_data_change.emit(self.__current_dataset_name, self.__current_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def file_path_init(self, file_path):
        """
        #初始化spss文件路径
        """
        self.__path_openfile_name = file_path
        if len(self.__path_openfile_name) != 0:
            self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)
            self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
            self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
            logging.info(
                "加载成功file_path{}，datasetName：{}".format(self.__path_openfile_name, self.__current_dataset_name))

            if len(self.__path_openfile_name) > 0:
                if self.__ui.checkBox_ifColumns.isChecked():
                    header = 0
                else:
                    header = None
                # 仅预览前100条数据
                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows_preview = 100
                elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                    nrows_preview = int(self.__ui.lineEdit_limitRow.text())
                else:
                    nrows_preview = 100

                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows = 100000000
                else:
                    nrows = int(self.__ui.lineEdit_limitRow.text())

                encoding = self.__ui.comboBox_encode.currentText()
                skiprows = int(self.__ui.lineEdit_passHead.text())

                logging.info("path_openfile_name：{}，header：{}，skiprows：{}，nrows：{}".format(
                    self.__path_openfile_name, header, skiprows, nrows_preview))

                self.__current_dataset = pd.read_spss(self.__path_openfile_name)

                if len(self.__current_dataset) == 0:
                    self.__ui.tableWidget_previewData.clear()
                    logging.info("当前有效数据为空")
                else:
                    self.import_dateset_preview()
                    logging.info("数据导入成功")
            else:
                print("请选择数据集")

    def openFile(self):
        """
        选择文件
        """
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'SPSS文件(*.sav)')
        logging.info(openfile_name)

        self.__path_openfile_name = openfile_name[0]
        self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

        self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
        self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
        logging.info("加载成功file_path{}，datasetName：{}".format(openfile_name, self.__current_dataset_name))
        self.import_dateset_reload()

    def get_dateset_name(self):
        return self.__current_dataset_name

    def import_dateset_reload(self):
        """
        刷新导入的数据
        """
        header = 0
        nrows_preview = 100
        sep = ','
        skiprows = 0

        if len(self.__path_openfile_name) > 0:
            if self.__ui.checkBox_ifColumns.isChecked():
                header = 0
            else:
                header = None
            # 仅预览前100条数据
            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows_preview = 100
            elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                nrows_preview = int(self.__ui.lineEdit_limitRow.text())
            else:
                nrows_preview = 100

            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows = 100000000
            else:
                nrows = int(self.__ui.lineEdit_limitRow.text())

            encoding = self.__ui.comboBox_encode.currentText()
            skiprows = int(self.__ui.lineEdit_passHead.text())

            logging.info("path_openfile_name：{}，header：{}，skiprows：{}，nrows：{}".format(
                self.__path_openfile_name, header, skiprows, nrows_preview))

            self.__current_dataset = pd.read_spss(self.__path_openfile_name)

            if len(self.__current_dataset) == 0:
                self.__ui.tableWidget_previewData.clear()
                logging.info("当前有效数据为空")
            else:
                self.import_dateset_preview()
                logging.info("数据导入成功")

    def import_dateset_preview(self):
        """
        刷新预览数据
        """
        if len(self.__current_dataset) > 0:
            input_table_rows = self.__current_dataset.head(100).shape[0]
            input_table_colunms = self.__current_dataset.shape[1]
            input_table_header = self.__current_dataset.columns.values.tolist()
            self.__ui.tableWidget_previewData.setColumnCount(input_table_colunms)
            self.__ui.tableWidget_previewData.setRowCount(input_table_rows)

            # 设置数据预览窗口的标题行
            table_header = []
            i = 1
            while i <= len(self.__current_dataset.columns):
                table_header.append("C" + str(i))
                i += 1

            if self.__ui.checkBox_ifColumns.isChecked():
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(input_table_header)
            else:
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(table_header)
                self.__current_dataset.columns = table_header
            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.__current_dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.__ui.tableWidget_previewData.setItem(i, j, newItem)

    def get_current_dataset(self):
        return self.__current_dataset

    def get_current_columns(self):
        return self.__current_dataset.columns


class ImportSasForm(QDialog):
    """
    打开"从sas导入"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于传递文件路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = SASImport_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

        #QssTools.set_qss_to_obj(ui_dir + "/source/qss/patata.qss", self)

        self.file_path = ''
        self.__path_openfile_name = ""
        self.__current_dataset_name = ""
        self.__current_dataset = pd.DataFrame()

        # 导入窗口的相关事件
        # 在"导入"窗口，打开选择文件
        self.__ui.pushButton_choosefile.clicked.connect(self.openFile)
        # 展示数据
        self.__ui.checkBox_ifColumns.stateChanged['int'].connect(self.import_dateset_reload)

        self.__ui.comboBox_encode.currentTextChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_filePath.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_passHead.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_datasetName.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_limitRow.textChanged['QString'].connect(self.import_dateset_reload)
        self.__ui.lineEdit_missValue.textChanged['QString'].connect(self.import_dateset_reload)

        # 更新数据
        self.__ui.pushButton_ok.clicked.connect(self.import_send_dataset)
        self.__ui.pushButton_cancel.clicked.connect(self.close)

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
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def import_send_dataset(self):
        logging.info("发射导入数据信号")
        if len(self.__current_dataset) > 0:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.file_path
            file_size = str(os.path.getsize(path))
            remarks = ''
            self.signal_data_change.emit(self.__current_dataset_name, self.__current_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def file_path_init(self, file_path):
        """
        #初始化sas文件路径
        """
        self.__path_openfile_name = file_path
        if len(self.__path_openfile_name) != 0:
            self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

            self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
            self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
            logging.info(
                "加载成功file_path{}，datasetName：{}".format(self.__path_openfile_name, self.__current_dataset_name))

            if len(self.__path_openfile_name) > 0:
                if self.__ui.checkBox_ifColumns.isChecked():
                    header = 0
                else:
                    header = None
                # 仅预览前100条数据
                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows_preview = 100
                elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                    nrows_preview = int(self.__ui.lineEdit_limitRow.text())
                else:
                    nrows_preview = 100

                if self.__ui.lineEdit_limitRow.text() == "全部":
                    nrows = 100000000
                else:
                    nrows = int(self.__ui.lineEdit_limitRow.text())

                encoding = self.__ui.comboBox_encode.currentText()
                skiprows = int(self.__ui.lineEdit_passHead.text())

                logging.info("path_openfile_name：{}，header：{}，skiprows：{}，nrows：{}".format(
                    self.__path_openfile_name, header, skiprows, nrows_preview))

                self.__current_dataset = pd.read_sas(self.__path_openfile_name, format='sas7bdat', encoding=encoding)

                if len(self.__current_dataset) == 0:
                    self.__ui.tableWidget_previewData.clear()
                    logging.info("当前有效数据为空")
                else:
                    self.import_dateset_preview()
                    logging.info("数据导入成功")
            else:
                print("请选择数据集")

    def openFile(self):
        """
        选择文件
        """
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'SAS文件(*.sas7bdat)')
        logging.info(openfile_name)

        self.__path_openfile_name = openfile_name[0]
        self.__ui.lineEdit_filePath.setText(self.__path_openfile_name)

        self.__current_dataset_name = os.path.split(self.__ui.lineEdit_filePath.text())[1]
        self.__ui.lineEdit_datasetName.setText(self.__current_dataset_name)
        logging.info("加载成功file_path{}，datasetName：{}".format(openfile_name, self.__current_dataset_name))
        self.import_dateset_reload()

    def get_dateset_name(self):
        return self.__current_dataset_name

    def import_dateset_reload(self):
        """
        刷新导入的数据
        """
        header = 0
        nrows_preview = 100
        sep = ','
        skiprows = 0

        if len(self.__path_openfile_name) > 0:
            if self.__ui.checkBox_ifColumns.isChecked():
                header = 0
            else:
                header = None
            # 仅预览前100条数据
            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows_preview = 100
            elif int(self.__ui.lineEdit_limitRow.text()) <= 100:
                nrows_preview = int(self.__ui.lineEdit_limitRow.text())
            else:
                nrows_preview = 100

            if self.__ui.lineEdit_limitRow.text() == "全部":
                nrows = 100000000
            else:
                nrows = int(self.__ui.lineEdit_limitRow.text())

            encoding = self.__ui.comboBox_encode.currentText()
            skiprows = int(self.__ui.lineEdit_passHead.text())

            logging.info("path_openfile_name：{}，header：{}，skiprows：{}，nrows：{}".format(
                self.__path_openfile_name, header, skiprows, nrows_preview))

            self.__current_dataset = pd.read_sas(self.__path_openfile_name, format='sas7bdat', encoding=encoding)

            if len(self.__current_dataset) == 0:
                self.__ui.tableWidget_previewData.clear()
                logging.info("当前有效数据为空")
            else:
                self.import_dateset_preview()
                logging.info("数据导入成功")

    def import_dateset_preview(self):
        """
        刷新预览数据
        """
        if len(self.__current_dataset) > 0:
            input_table_rows = self.__current_dataset.head(100).shape[0]
            input_table_colunms = self.__current_dataset.shape[1]
            input_table_header = self.__current_dataset.columns.values.tolist()
            self.__ui.tableWidget_previewData.setColumnCount(input_table_colunms)
            self.__ui.tableWidget_previewData.setRowCount(input_table_rows)

            # 设置数据预览窗口的标题行
            table_header = []
            i = 1
            while i <= len(self.__current_dataset.columns):
                table_header.append("C" + str(i))
                i += 1

            if self.__ui.checkBox_ifColumns.isChecked():
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(input_table_header)
            else:
                self.__ui.tableWidget_previewData.setHorizontalHeaderLabels(table_header)
                self.__current_dataset.columns = table_header
            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.__current_dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.__ui.tableWidget_previewData.setItem(i, j, newItem)

    def get_current_dataset(self):
        return self.__current_dataset

    def get_current_columns(self):
        return self.__current_dataset.columns


# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ImportForm()
    form.show()
    sys.exit(app.exec_())
