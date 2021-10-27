"""
工具汇总。

作者：廖俊易

修改日期：20201215
修改作者：开始说故事
"""
import os
import typing

if typing.TYPE_CHECKING:
    import packages.dataio.sample as sample
else:
    import sample


class importutils(object):
    def doExcelImport(self, path=''):
        self.import_excel_form = sample.ImportExcelForm()
        if os.path.exists(path):
            self.import_excel_form.open_file(path)
        self.import_excel_form.exec_()

    def doCsvImport(self, path=''):
        self.import_csv_form = sample.ImportCsvForm()
        if os.path.exists(path):
            self.import_csv_form.open_file(path)
        self.import_csv_form.exec_()

    def doTextImport(self, path=''):
        self.import_form = sample.ImportTextForm()
        if os.path.exists(path):
            self.import_form.open_file(path)
        self.import_form.exec_()

    def doSPSSImport(self, path=''):
        self.import_spss_form = sample.ImportSpssForm()
        if os.path.exists(path):
            self.import_spss_form.open_file(path)
        self.import_spss_form.exec_()

    def doSASImport(self, path=''):
        self.import_sas_form = sample.ImportSasForm()
        if os.path.exists(path):
            self.import_sas_form.open_file(path)
        self.import_sas_form.exec_()

    def doMATLABImport(self, path=''):
        self.import_matlab_form = sample.ImportMatlabForm()
        if os.path.exists(path):
            self.import_matlab_form.open_file(path)
        self.import_matlab_form.exec_()

    def doSTATAImport(self, path=''):
        self.import_stata_form = sample.ImportStataForm()
        if os.path.exists(path):
            self.import_stata_form.open_file(path)
        self.import_stata_form.exec_()

    def doImportEngine(self, path=''):
        '''
        导入策略列表，后续需要新增导入策略，只需要在前端增加入口，以及导入的策略即可
        :return:
        '''
        ImportEngine = {
            "excel": importutils.doExcelImport,
            "text": importutils.doTextImport,
            "csv": importutils.doCsvImport,
            "spss": importutils.doSPSSImport,
            "sas": importutils.doSASImport,
            "matlab": importutils.doMATLABImport,
            "stata": importutils.doSTATAImport
        }
        return (ImportEngine)
