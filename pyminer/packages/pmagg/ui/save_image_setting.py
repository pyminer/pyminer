# -*- coding: utf-8 -*-
"""
@Time ： 2020/12/25 9:35
@Author ： 慢慢来
@File ：save_image_setting.py
@IDE ：PyCharm
"""
from PySide2 import QtWidgets,QtGui
import os
import matplotlib

class Window(QtWidgets.QDialog):
    def __init__(self, canvas):
        super().__init__()
        self.setWindowTitle('Save Image Setting')
        self.canvas = canvas
        self.width_lineedit = QtWidgets.QLineEdit()
        self.height_lineedit = QtWidgets.QLineEdit()
        self.dpi_lineedit = QtWidgets.QLineEdit()
        self.path_lineedit = QtWidgets.QLineEdit()
        self.path_lineedit.setReadOnly(True)
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0)
        self.width_lineedit.setValidator(validator)
        self.height_lineedit.setValidator(validator)
        self.dpi_lineedit.setValidator(validator)
        self.width_lineedit.setText(str(self.canvas.figure.get_figwidth()))
        self.height_lineedit.setText(str(self.canvas.figure.get_figheight()))
        self.dpi_lineedit.setText(str(self.canvas.figure.get_dpi()))
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.choose_button = QtWidgets.QPushButton('选择路径')
        self.choose_button.clicked.connect(self.open_file_slot)
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('宽度/英寸', self.width_lineedit)
        self.layout.addRow('高度/英寸', self.height_lineedit)
        self.layout.addRow('DPI(像素/英寸)', self.dpi_lineedit)
        self.layout.addRow(self.choose_button, self.path_lineedit)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.exec_()
    def open_file_slot(self):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        if os.path.exists(matplotlib.rcParams['savefig.directory']):
            startpath = matplotlib.rcParams['savefig.directory']
        else:
            startpath = os.path.expanduser('~')
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)
        file_path, ok = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              'Save Image',
                                                              start,filter=filters,
                                                              initialFilter=selectedFilter)
        self.path_lineedit.setText(file_path)

    def confirm_slot(self):
        fname=self.path_lineedit.text()
        startpath = os.path.expanduser(
            matplotlib.rcParams['savefig.directory'])
        raw_width = self.canvas.figure.get_figwidth()
        raw_height = self.canvas.figure.get_figheight()
        width=float(self.width_lineedit.text())
        height=float(self.height_lineedit.text())
        dpi=float(self.dpi_lineedit.text())
        self.canvas.figure.set_figwidth(width)
        self.canvas.figure.set_figheight(height)
        if fname:
            if startpath != "":
                matplotlib.rcParams['savefig.directory'] = (
                    os.path.dirname(fname))
            try:
                self.canvas.figure.savefig(fname,dpi=dpi)
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "请确认路径正确，或输入了合理的尺寸和DPI值", str(e),
                    QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
        self.canvas.figure.set_figwidth(raw_width)
        self.canvas.figure.set_figheight(raw_height)
        self.canvas.draw_idle()
        self.close()

    def cancel_slot(self):
        self.close()
