# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 20:47
# @Author  :
# @FileName: main.py
import logging
import os
import subprocess
import sys

from PySide2.QtCore import Signal, QSize, QLocale, QTranslator, QCoreApplication
from PySide2.QtGui import QMouseEvent, QContextMenuEvent
from PySide2.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QHeaderView, QMenu, QAction
from lib.comm.base import DataDesc

from widgets import create_icon, QDialog
import socket
from contextlib import closing

logger = logging.getLogger(__name__)
from lib.extensions.extensionlib import BaseExtension, BaseInterface
from .ipython_data_show import IPythonDataShow

file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name()))
app = QApplication.instance()
trans_editor = QTranslator()
trans_editor.load(file_name)
app.installTranslator(trans_editor)


def find_free_port() -> int:
    """
    获取空闲端口
    :return:
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class NBInstanceShowTable(QTableWidget):
    signal_request_open_work_dir = Signal(str)  # str:工作路径的地址
    signal_request_open_url = Signal(str)  # str:url

    def __init__(self):
        super(NBInstanceShowTable, self).__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.tr('Address'), self.tr('Work Dir')])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.menu = QMenu()
        self.menu.addAction(self.tr('Open Work Dir')).triggered.connect(self.open_work_dir)
        self.menu.addAction(self.tr('Open Notebook')).triggered.connect(self.open_notebook)
        self.menu.addAction(self.tr('Scan Notebooks')).triggered.connect(self.list_instances)

    def contextMenuEvent(self, arg__1: 'QContextMenuEvent') -> None:
        self.menu.exec_(arg__1.globalPos())

    def sizeHint(self) -> 'QSize':
        return QSize(800, 600)

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        """
        双击打开事件
        :param e:
        :return:
        """
        super(NBInstanceShowTable, self).mouseDoubleClickEvent(e)

    def open_work_dir(self):
        self.signal_request_open_work_dir.emit(self.currentItem().text())

    def open_notebook(self):
        self.signal_request_open_url.emit(self.currentItem().text())

    def list_instances(self):
        cmd = sys.executable + ' -m notebook list'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        out_lines = out.decode('utf-8', errors='replace').splitlines()[1:]
        self.setRowCount(len(out_lines))
        for i, line in enumerate(out_lines):
            self.add_instance(i, line.split('::'))

    def add_instance(self, i, instance_property: list):
        for j, text in enumerate(instance_property):
            self.setItem(i, j, QTableWidgetItem(text.strip()))


class Extension(BaseExtension):

    def on_load(self):
        self.data_viewer = None
        self.extension_lib.Signal.get_events_ready_signal().connect(self.on_started)
        self.extension_lib.Data.add_data_changed_callback(self.on_data_changed)
        self.interface.ext = self

    def on_started(self):
        self.menu_jupyter: QMenu = self.extension_lib.UI.get_toolbar('toolbar_home').append_qmenu(
            'button_open', 'Jupyter Notebook', create_icon(':/resources/icons/Jupyter.svg')
        )
        self.action_open_notebook = QAction(
            create_icon(':/resources/icons/Jupyter.svg'),
            QCoreApplication.translate('JupyterSupportExtension', 'Open Notebook')
        )
        self.menu_jupyter.addAction(self.action_open_notebook)
        self.action_open_notebook.triggered.connect(self.open_notebook)

        self.action_manage_notebooks = QAction(
            text=QCoreApplication.translate('JupyterSupportExtension', 'Manage Notebooks')
        )
        self.menu_jupyter.addAction(self.action_manage_notebooks)
        self.action_manage_notebooks.triggered.connect(self.manage_notebooks)

        self.action_insert_data_viewer = QAction(
            text=QCoreApplication.translate('JupyterSupportExtension', 'IPython Variable Inspector')
        )
        self.menu_jupyter.addAction(self.action_insert_data_viewer)
        self.action_insert_data_viewer.triggered.connect(self.insert_data_viewer)

    def open_notebook(self):
        """
        打开Notebook
        :return:
        """
        script_path = os.path.join(os.path.expanduser("~"), '.ipython', 'profile_default', 'startup')

        port = find_free_port()
        import shutil
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), 'scripts', 'pyminer_ipython_node.py'),
            os.path.join(script_path, 'pyminer_ipython_node.py'))
        os.environ['IPYTHON_AS_PYMINER_NODE'] = str(port)
        self.extension_lib.get_interface('applications_toolbar').create_process(
            'Notebook', [
                sys.executable, '-m', 'notebook', '--port',
                str(port), '--no-browser', '--ip=\'*\'', '--NotebookApp.token=\'\'',
                '--notebook-dir=%s' % self.extension_lib.Program.get_work_dir()
            ]
        )
        self.extension_lib.get_interface('embedded_browser'
                                         ).open_url('http://127.0.0.1:{port}'.format(port=port),
                                                    side='top',
                                                    text=QCoreApplication.translate('JupyterSupportExtension',
                                                                                    "Jupyter"))
        self.insert_data_viewer()

    def manage_notebooks(self):
        """
        管理notebooks
        :return:
        """
        dlg = QDialog()
        dlg.setLayout(QVBoxLayout())
        te = NBInstanceShowTable()
        te.list_instances()
        te.signal_request_open_work_dir.connect(lambda dir: self.extension_lib.Program.set_work_dir(dir))
        te.signal_request_open_url.connect(
            lambda url: self.extension_lib.get_interface('embedded_browser').open_url(url)
        )
        dlg.layout().addWidget(te)
        dlg.exec_()

    def on_data_changed(self, dataname: str, var: DataDesc, provider):
        if self.data_viewer is not None:
            if dataname.startswith('IPy_') and issubclass(var.cls, dict):
                self.data_viewer.on_data_changed(dataname)

    def insert_data_viewer(self):
        if self.data_viewer is None:
            app = QApplication.instance()
            self.data_viewer_cls = IPythonDataShow
            self.data_viewer: 'IPythonDataShow' = \
                self.extension_lib.insert_widget(self.data_viewer_cls,
                                                 'new_dock_window',
                                                 {
                                                     "name": "ipython_kernel_data_inspector",
                                                     "side": "right",
                                                     "text": app.tr("Variable Viewer")})

            self.data_viewer.on_dock_widget_deleted = self.on_data_viewer_deleted
        self.extension_lib.UI.raise_dock_into_view('ipython_kernel_data_inspector')

    def on_data_viewer_deleted(self):
        self.data_viewer = None


class Interface(BaseInterface):
    ext: "Extension" = None

    def run(self):
        self.ext.open_notebook()


if __name__ == '__main__':
    app = QApplication([])
    table = NBInstanceShowTable()
    table.show()
    table.list_instances()
    app.exec_()
