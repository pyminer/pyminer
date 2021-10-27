"""
有无办法通过迭代器方式递归实现流程图的迭代仿真？
"""
import os
import sys
import time
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable
from widgets import PMGFlowContent, PMGPanelDialog, ErrorReporter, PANEL_VIEW_CLASS

if TYPE_CHECKING:
    import pandas as pd


def import_pandas(file: str, **kwargs):
    if not isinstance(file, str):
        raise ErrorReporter.create_type_error('File path', file, str)
    if not os.path.exists(file):
        raise ErrorReporter.create_file_not_found_error(file)

    import pandas as pd

    ext = os.path.splitext(file)[1]
    kw = {'skiprows': kwargs['skiprows']}
    if kwargs['limit_nrows'] == True:
        kw['nrows'] = kwargs['nrows']
    if kwargs['find_header_in_table'] == True:
        kw['header'] = kwargs['header']
    else:
        kw['header'] = None
    print(kw)
    if ext == '.csv':
        return [pd.read_csv(file, sep=kwargs['csv_sep'], **kw)]
    elif ext == '.xls' or ext == '.xlsx':
        return [pd.read_excel(file, **kw)]
    else:
        raise ValueError('Cannot Read file of this extension: \'%s\'' % ext)


class BaseTableImport(PMGFlowContent):
    def __init__(self):
        super().__init__()
        self.info = {
            'sampling_rate': 0.2, 'file_path': '',
            'csv_sep': ',',
            'find_header_in_table': True,
            'skiprows': 0,
            'limit_nrows': False,
            'nrows': -1,
            'header': 0
        }

    def format_settings(self, views: PANEL_VIEW_CLASS) -> PANEL_VIEW_CLASS:
        info = self.info
        views += [
            [('combo_ctrl', 'csv_sep', 'CSV分隔符', info['csv_sep'], ['\t', ','], ['制表符（Tab,\\t）', '逗号（’,‘）'])],
            ('numberspin_ctrl', 'skiprows', '跳过行数', info['skiprows'], '', (0, 100)),
            [
                ('check_ctrl', 'find_header_in_table', '从表中获取列名', info['find_header_in_table']),
                ('numberspin_ctrl', 'header', '表头行数', info['header'], '', (0, 100)),
            ], [
                ('check_ctrl', 'limit_nrows', '限制最大行数', info['limit_nrows']),
                ('numberspin_ctrl', 'nrows', '读取最大行数', info['nrows'], '', (0, 100000)),
            ]
        ]
        return views

    def process(self) -> List:
        """
        基础迭代器
        Args:
            *args:

        Returns:

        """
        return import_pandas(self.info['file_path'], **self.info)
        # csv_sep=self.info['csv_sep'], skip_rows=self.info['skiprows'],
        #                      first_row_as_header=self.info['find_header_in_table'], nrows=self.info['nrows'],limit_nrows = self.info['limit_nrows'] )


class PandasFileImport(BaseTableImport):
    def __init__(self):
        super(PandasFileImport, self).__init__()
        self.input_args_labels = []
        self.output_ports_labels = ['数据集']  # , '检验']
        self.class_name = 'PandasImport'
        self.text = '读取Pandas数据集'
        self.icon_path = ''

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
        views = [
            ('file_ctrl', 'file_path', '导入文件的路径', self.info['file_path']),
        ]
        views = self.format_settings(views)
        dlg = PMGPanelDialog(parent=parent, views=views)
        dlg.setMinimumSize(600, 480)
        dlg.exec_()
        self.info = dlg.panel.get_value()

    def process(self) -> List:
        """
        基础迭代器
        Args:
            *args:

        Returns:

        """
        return import_pandas(self.info['file_path'], **self.info)


class PandasImport(BaseTableImport):

    def __init__(self):
        super(PandasImport, self).__init__()
        self.input_args_labels = ['路径']
        self.output_ports_labels = ['数据集']  # , '检验']
        self.class_name = 'PandasImport'
        self.text = '从上游路径\n输入Pandas数据集'
        self.icon_path = ''

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
        views = self.format_settings([])

        dlg = PMGPanelDialog(parent=parent, views=views)
        dlg.setMinimumSize(600, 480)
        dlg.exec_()
        self.info = dlg.panel.get_value()

    def process(self,path) -> List:
        """
        被调用时执行的代码
        Args:
            *args:

        Returns:

        """
        return import_pandas(path, **self.info)


if __name__ == '__main__':
    import sys

    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    info = {'sampling_rate': 0.2}
    pj = lambda *s: os.path.normcase(os.path.join(*s))
    folder = pj(os.path.dirname(__file__), 'test_files')
    r = PandasFileImport()
    r.load_info({
        'sampling_rate': 0.2,
        'file_path': pj(folder, 'test.xlsx'),
        'csv_sep': '\t',
        'find_header_in_table': True,
        'skiprows': 0,
        'limit_nrows': True,
        'nrows': 3,
        'header': 0
    })
    print(r.process()[0])

    r.load_info({
        'sampling_rate': 0.2,
        'file_path': pj(folder, 'test.csv'),
        'csv_sep': '\t',
        'find_header_in_table': False,
        'skiprows': 3,
        'limit_nrows': False,
        'nrows': -1,
        'header': 0
    })

    print(r.process()[0])

    sys.exit(app.exec_())
