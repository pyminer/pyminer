from typing import Any, List, TYPE_CHECKING
from PySide2.QtWidgets import QApplication, QWidget, QDialog, QHBoxLayout, QVBoxLayout, QMessageBox, QDialogButtonBox
from widgets import PMTableView, PMGPanel, in_unit_test
from lib.comm import get_var
import json

if TYPE_CHECKING:
    import pandas as pd


class ExportDialog(QDialog):
    ext = 'All Files (*);;Text Files (*.txt)'
    extension_lib = None

    def __init__(self, initial_var_name: str = '', initial_path: str = ''):
        super(ExportDialog, self).__init__(parent=None)
        self.normal = False
        if initial_path == '' and not in_unit_test():
            initial_path = self.extension_lib.Program.get_work_dir()
        self.setLayout(QVBoxLayout())
        self.initial_var_name = initial_var_name
        self.initial_path = initial_path
        try:
            choose_views = self.create_choose_views()
            # self.table_view = PMTableView()
            self.choose_panel = PMGPanel(parent=self, views=choose_views)
            config_views = self.create_config_views()
            self.config_panel = PMGPanel(parent=self, views=config_views)
            self.layout().addWidget(self.choose_panel)
            # self.layout().addWidget(self.table_view)
            self.layout().addWidget(self.config_panel)
            bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            bb.rejected.connect(self.close)
            bb.accepted.connect(self.accept)
            self.layout().addWidget(bb)
            self.setMinimumWidth(600)
            self.normal = True
        except ValueError:
            self.normal = False
            return

    def export(self) -> bool:
        var_name = self.choose_panel.get_value()['var_name']
        path = self.choose_panel.get_value()['path']

        df = self.get_var(var_name)
        config = self.config_panel.get_value()
        try:
            self._export(df, path, config)
            return True
        except FileNotFoundError:
            QMessageBox.warning(self, '警告', '无法创建路径为\"%s\"的文件，请检查路径输入。' % path)
        except Exception:
            import traceback
            traceback.print_exc()
        return False

    def _export(self, df: 'pd.DataFrame', path, config):
        return

    def create_config_views(self) -> list:
        return [[
            ('check_ctrl', 'header', '含列名', True),
            ('check_ctrl', 'index', '含行索引', False),
        ],
            ('line_ctrl', 'na_rep', '替换空值为', '',),
            ('numberspin_ctrl', 'float_format', '保留小数位数', 6, '', (0, 30))
        ]

    def create_choose_views(self) -> list:
        var_names = self.get_all_var_names()
        if len(var_names) > 0:
            return [
                ('combo_ctrl', 'var_name', '名称', var_names[0], var_names),
                ('file_ctrl', 'path', '保存路径', '', self.ext, self.initial_path, 'save')
            ]
        else:
            QMessageBox.warning(self, 'Warning', '工作空间中尚不存在可供导出的变量', QMessageBox.Ok, QMessageBox.Ok)
            raise ValueError()

    def get_var(self, varname: str) -> 'pd.DataFrame':
        if not in_unit_test():
            return get_var(varname)
        else:
            import pandas
            return pandas.DataFrame([[1, 2, 3], [4, 5, 6]])

    def get_all_var_names(self) -> List[str]:
        if not in_unit_test():
            return self.extension_lib.Data.get_all_public_variable_names()
        else:
            return ['a', 'b', 'c']

    def accept(self):
        if self.export():
            QMessageBox.information(self, '状态', '导出成功！', QMessageBox.Ok)
            self.close()

    # def get_config(self)->dict:
    #     config = {'na_rep'}


class ExportCSVDialog(ExportDialog):
    ext = 'CSV Files (*.csv)'

    def create_config_views(self) -> list:
        cvs = super().create_config_views()
        cvs += [('combo_ctrl', 'sep', '分隔符', ',', [',', '\t'], [',', '\\t', ])]
        return cvs

    def _export(self, df: 'pd.DataFrame', path: str, config):
        df.to_csv(path_or_buf=path, **config)


class ExportExcelDialog(ExportDialog):
    ext = 'Excel(*.xls);;Modern Excel(*.xlsx)'

    def create_config_views(self) -> list:
        cvs = super().create_config_views()
        cvs += [('line_ctrl', 'sheet_name', '页名', 'Sheet1')]
        return cvs

    def _export(self, df: 'pd.DataFrame', path, config):
        df.to_excel(path, **config)


if __name__ == '__main__':
    app = QApplication([])
    # ed = ExportCSVDialog(initial_path=r'c:\users\12957\Desktop')
    # ed.show()
    ed = ExportExcelDialog(initial_path=r'c:\users\12957\Desktop')
    ed.show()
    app.exec_()
