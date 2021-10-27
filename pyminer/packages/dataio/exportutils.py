import typing
from PySide2.QtWidgets import QMessageBox

if typing.TYPE_CHECKING:
    import packages.dataio.export as export
else:
    import export


def has_var_to_export(func):
    def inner(self, var, path):
        if len(exportutils.extension_lib.Data.get_all_public_variable_names()) > 0:
            func(self, var, path)
        else:
            QMessageBox.warning(None, 'Warning', '工作空间中尚不存在可供导出的变量', QMessageBox.Ok, QMessageBox.Ok)

    return inner


class exportutils():
    extension_lib = None

    def __init__(self):
        self.csv_export_dialog: export.ExportCSVDialog = None
        self.excel_export_dialog: export.ExportExcelDialog = None

    def get_all_var_names(self) -> typing.List:
        return self.extension_lib.Data.get_all_public_variable_names()

    @has_var_to_export
    def doCSVExport(self, var='', path=''):
        if self.csv_export_dialog is None:
            self.csv_export_dialog = export.ExportCSVDialog(var, path)
        self.csv_export_dialog.exec_()

    @has_var_to_export
    def doExcelExport(self, var='', path=''):
        if self.excel_export_dialog is None:
            self.excel_export_dialog = export.ExportExcelDialog(var, path)
        self.excel_export_dialog.exec_()

    def doExportEngine(self):
        return {'excel': self.doExcelExport,
                'csv': self.doCSVExport
                }
