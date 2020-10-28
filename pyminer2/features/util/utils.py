"""
工具汇总：
作者：廖俊易

"""
import logging
import os

from PyQt5.QtWidgets import QFileDialog, QWidget

from pyminer2.features.io import sample



class importutils(object):
    def doSPSSImport(self):
            self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                            '选择文件', '',
                                                                            "All Files (*);;SPSS文件 (*.sav *.zsav)")  # 设置文件扩展名过滤,用双分号间隔

            if len(self.__file_path_choose) == 0:
                logging.info("\n取消选择")
                return
            else:

                if os.path.split(self.__file_path_choose)[1].endswith(('sav', 'zsav')):
                    if len(self.__file_path_choose) > 0:
                        self.import_spss_form = sample.ImportSpssForm()
                        # self.import_spss_form.file_path_init(self.__file_path_choose)
                        # self.import_spss_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                        self.import_spss_form.exec_()
                    else:
                        logging.info("信号发射失败")


    def doSASImport(self):
            self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                            '选择文件', '',
                                                                            "All Files (*);;SAS文件 (*.sas7bdat)")  # 设置文件扩展名过滤,用双分号间隔

            if len(self.__file_path_choose) == 0:
                logging.info("\n取消选择")
                return
            else:

                if os.path.split(self.__file_path_choose)[1].endswith(('sas7bdat')):
                    if len(self.__file_path_choose) > 0:
                        self.import_sas_form = sample.ImportSasForm()
                        # self.import_sas_form.file_path_init(self.__file_path_choose)
                        # self.import_sas_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                        self.import_sas_form.exec_()
                    else:
                        logging.info("信号发射失败")


    def doExcelImport(self):
            self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                            '选择文件', '',
                                                                            "All Files (*);;EXCEL文件 (*.xls *.xlsx *.xlsm *.xltx *.xltm)")  # 设置文件扩展名过滤,用双分号间隔

            if len(self.__file_path_choose) == 0:
                logging.info("\n取消选择")
                return
            else:
                if os.path.split(self.__file_path_choose)[1].endswith(('xlsx', 'xlsm', 'xltx', 'xltm')):
                    if len(self.__file_path_choose) > 0:
                        self.import_excel_form = sample.ImportExcelForm()
                        # self.import_excel_form.file_path_init(self.__file_path_choose)
                        # self.import_excel_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                        self.import_excel_form.exec_()
                    else:
                        logging.info("信号发射失败--导入文件已选择")


    def doTextImport(self):
            self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                            '选择文件', '',
                                                                            "All Files (*);;文本文件 (*.txt *.csv *.tsv *.tab *.dat)")
            if len(self.__file_path_choose) == 0:
                logging.info("\n取消选择")
                return
            else:
                self.import_form = sample.ImportForm()
                # self.import_form.file_path_init()
                # self.import_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_form.exec_()