#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
from typing import Dict, Union

from PySide2.QtCore import QLocale
from PySide2.QtWidgets import QApplication

sys.path.append(os.path.dirname(__file__))

from lib.extensions.extensionlib import BaseInterface, BaseExtension

from widgets import PMGPanel, create_file_if_not_exist, load_json, dump_json, create_icon, assert_in
import json
from .importutils import importutils
from .dbimport import dbimportutils
from .exportutils import exportutils
import sample
import export
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Extension(BaseExtension):
    def __init__(self):
        super(Extension, self).__init__()

    def on_loading(self):

        return

    def on_load(self):
        """
        为主菜单按钮添加子菜单
        """
        self.interface.extension = self
        sample.ImportDialog.extension_lib = self.extension_lib
        export.ExportDialog.extension_lib = self.extension_lib
        exportutils.extension_lib = self.extension_lib
        toolbar = self.extension_lib.UI.get_toolbar('toolbar_home')

        textImportIcon = create_icon(':/resources/icons/txt.svg')
        toolbar.append_menu('button_import_data', 'Text Data', lambda: self.process_file('text', ''),
                            textImportIcon)
        csvImportIcon = create_icon(':/resources/icons/csv.svg')
        toolbar.append_menu('button_import_data', 'CSV', lambda: self.process_file('csv', ''),
                            csvImportIcon)
        excelImportIcon = create_icon(':/resources/icons/excel.svg')
        toolbar.append_menu('button_import_data', 'Excel', lambda: self.process_file('excel', ''),
                            excelImportIcon)
        sasImportIcon = create_icon(':/resources/icons/sas.ico')
        toolbar.append_menu('button_import_data', 'SAS', lambda: self.process_file('sas', ''),
                            sasImportIcon)
        spssImportIcon = create_icon(':/resources/icons/spss.svg')
        toolbar.append_menu('button_import_data', 'SPSS', lambda: self.process_file('spss', ''),
                            spssImportIcon)
        matlabImportIcon = create_icon(':/resources/icons/matlab.svg')
        toolbar.append_menu('button_import_data', 'MATLAB', lambda: self.process_file('matlab', ''),
                            matlabImportIcon)
        stataImportIcon = create_icon(':/resources/icons/stata.svg')
        toolbar.append_menu('button_import_data', 'STATA', lambda: self.process_file('stata', ''),
                            stataImportIcon)

        toolbar.add_menu_separator('button_import_data')

        toolbar.append_menu('button_import_data', 'Encoding transform',
                            lambda: self.show_encoding_converter())

        mysqlIcon = create_icon(':/resources/icons/MySQL.svg')
        toolbar.append_menu('button_import_database', 'MySQL', lambda: self.import_db('mysql'),
                            mysqlIcon)
        oracleIcon = create_icon(':/resources/icons/oracle.svg')
        toolbar.append_menu('button_import_database', 'Oracle', lambda: self.import_db('oracle'),
                            oracleIcon)
        postgresqlIcon = create_icon(':/resources/icons/postgresql.svg')
        toolbar.append_menu('button_import_database', 'PostgreSQL',
                            lambda: self.import_db('postgresql'),
                            postgresqlIcon)

        toolbar.append_menu('button_save_workspace', 'Save workspace',
                            lambda: self.extension_lib.get_interface('workspace_inspector').save_workspace())
        toolbar.append_menu('button_save_workspace', 'Save current variable',
                            lambda: self.extension_lib.get_interface('workspace_inspector').save_current_variable())
        file_export_menu = toolbar.append_qmenu('button_save_workspace','Output as a file')  
        file_export_menu.addAction(excelImportIcon, 'Excel', lambda: self.export_file('excel'))
        file_export_menu.addAction(csvImportIcon, 'CSV', lambda: self.export_file('csv'))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.csv',
                                                                             lambda path: self.process_file('csv',
                                                                                                            path))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.xls',
                                                                             lambda path: self.process_file('excel',
                                                                                                            path))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.xlsx',
                                                                             lambda path: self.process_file('excel',
                                                                                                            path))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.sav',
                                                                             lambda path: self.process_file('spss',
                                                                                                            path))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.sas7bdat',
                                                                             lambda path: self.process_file('sas',
                                                                                                            path))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.mat',
                                                                             lambda path: self.process_file('matlab',
                                                                                                            path))

    def on_install(self):
        pass

    def on_uninstall(self):
        pass

    def process_file(self, type: str, path: str = ''):
        '''
            对这部分代码进行了优化，替换了原来多个if-else的代码
        '''

        if type is not None:
            ImportEngine = importutils.doImportEngine(self)
            if type in ImportEngine:
                if path == '':
                    ImportEngine[type](self)
                else:
                    ImportEngine[type](self, path)
            else:
                logger.info("type is not supported yet")
        else:
            logger.info('type is null')

    def import_db(self, type: str):
        DBImportEngine = dbimportutils().doImportEngine()
        if type in DBImportEngine:
            DBImportEngine[type]()
        else:
            logger.info("type is not supported yet")

    def export_file(self, type: str, var: str = '', path: str = ''):
        exportEngine = exportutils().doExportEngine()
        if type in exportEngine.keys():
            exportEngine[type](var, path)

    def show_db_account_editor(self):
        """
        显示账户编辑面板
        Returns:

        """
        from features.io.database import DatabaseConfigPanel
        sp2 = DatabaseConfigPanel()
        sp2.exec_()

    def show_encoding_converter(self):
        """
        槽函数：弹出转换编码方式的面板
        Returns:

        """
        from features.io.encoding import EncodingConversionWidget
        encoding_convert_form = EncodingConversionWidget()
        encoding_convert_form.exec_()


class Interface(BaseInterface):
    """
        数据导入模块的对外接口
    """
    extension: 'Extension' = None

    def __init__(self):
        self.file_types = {'csv', 'matlab', 'sas', 'spss', 'excel', 'stata'}
        self.db_types = {'mysql', 'oracle', 'postgresql'}

    def show_import_file_dialog(self, type: str, path: str):
        """
        Args:
            type: should be in {'csv', 'matlab', 'sas', 'text', 'spss', 'excel', 'stata'}
            path: valid path

        Returns:
        """
        assert_in(type, self.file_types)
        self.extension.process_file(type, path)

    def show_import_database_dialog(self, type: str):
        """

        Args:
            type: should be in {'mysql','oracle','postgresql'}

        Returns:

        """
        assert_in(type, self.file_types)
        self.extension.import_db(type)
