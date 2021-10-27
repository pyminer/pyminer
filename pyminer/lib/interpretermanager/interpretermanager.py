"""
settings['interpreters'] =
{'base':{'name':'base',
         'info':'pypy3 python 3.6 compatible',
         'path':'/home/.../python3.8'}
}
"""
import os
import sys
from typing import Dict, List

from PySide2.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QDialog, \
    QListWidget, QMessageBox, QSpacerItem, QSizePolicy

import utils
from widgets import PMGPanelDialog
from utils import get_settings_item_from_file


class Interpreter():
    def __init__(self, name: str, absolute_path: str, version: str):
        self.name = name
        self.path = absolute_path
        self.versioin = version


class InterpreterManager():
    interpreter_paths = []

    def __init__(self):
        pass


def get_interpreter_version(interpreter_path: str) -> str:
    version = os.popen('%s -c \"import sys;print(sys.version.split()[0])\"' % interpreter_path).read().strip()
    return version


def get_all_external_interpreters() -> List[Dict]:
    """
    获取所有的外部解释器
    Returns:

    """
    return utils.get_settings_item_from_file("config.ini", "RUN/EXTERNAL_INTERPRETERS")


def modify_interpreter_config(mode, info: Dict = None, index: int = -1):
    """

    Args:
        info: 一个存储解释器信息的字典
        mode: "add","delete","modify"

    Returns:

    """

    external_interpreters = utils.get_settings_item_from_file("config.ini", "RUN/EXTERNAL_INTERPRETERS")
    if mode == "add":
        external_interpreters.append(info)
    elif mode == "modify":
        external_interpreters[index] = info
    elif mode == "delete":
        external_interpreters.pop(index)
    else:
        raise NotImplementedError(mode)
    utils.write_settings_item_to_file("config.ini", "RUN/EXTERNAL_INTERPRETERS", external_interpreters)


class InterpreterManagerWidget(QWidget):
    def __init__(self, parent=None):
        super(InterpreterManagerWidget, self).__init__(parent)
        self.interpreters_list_show = QListWidget()
        self.button_add = QPushButton('+')
        self.button_delete = QPushButton('-')
        self.button_edit = QPushButton(self.tr('Edit'))
        self.button_manage_packages = QPushButton(self.tr('Packages'))
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.interpreters_list_show)
        self.button_layout = QVBoxLayout()
        self.layout().addLayout(self.button_layout)
        self.button_layout.addWidget(self.button_add)
        self.button_layout.addWidget(self.button_edit)
        self.button_layout.addWidget(self.button_manage_packages)
        self.button_layout.addWidget(self.button_delete)
        self.button_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.button_add.clicked.connect(self.add)
        self.button_edit.clicked.connect(self.edit)
        self.button_delete.clicked.connect(self.remove)
        self.button_manage_packages.clicked.connect(self.manage_packages)
        self.interpreters_list_show.currentItemChanged.connect(self.on_list_current_item_changed)
        self.show_interpreters()

    def gen_info_template(self):
        views = [
            ('line_ctrl', 'name', '名称', ''),
            ('file_ctrl', 'interpreter_path', '解释器路径', '')
        ]

    def add(self):
        views = [
            ('line_ctrl', 'name', self.tr('Name'), ''),
            ('file_ctrl', 'path', self.tr('Executable Path'), '', 'Executables(*.exe)')
        ]

        def set_interpreter_name(settings):
            interpreter_path = settings['path']
            dlg.panel.get_ctrl('name').set_value(os.path.basename(interpreter_path))

        dlg = PMGPanelDialog(parent=self, views=views)
        dlg.panel.set_param_changed_callback('path', set_interpreter_name)

        ret = dlg.exec_()
        if ret == QDialog.Accepted:
            res = dlg.get_value()
            d = {'name': res['name'], 'path': res['path'], 'version': get_interpreter_version(res['path'])}
            modify_interpreter_config("add", d)
            self.show_interpreters()

    def edit(self):
        current_index = self.interpreters_list_show.currentRow()
        list_index = current_index - 1  # 第一个是默认解释器，所以要减去1

        external_interpreters = get_all_external_interpreters()
        current_interpreter = external_interpreters[list_index]

        views = [
            ('line_ctrl', 'name', self.tr('Name'), current_interpreter['name']),
            ('file_ctrl', 'path', self.tr('Executable Path'), current_interpreter['path'])
        ]

        dlg = PMGPanelDialog(parent=self, views=views)
        dlg.verify = self.verify
        ret = dlg.exec_()

        if ret == QDialog.Accepted:
            res = dlg.get_value()
            d = {'name': res['name'], 'path': res['path'], 'version': get_interpreter_version(res['path'])}
            modify_interpreter_config("modify", d, list_index)
            self.show_interpreters()

    def manage_packages(self):
        from features.interpretermanager.packagemanager import MarketPlace
        current_interpreter = self.get_current_interpreter()
        if current_interpreter is not None:
            path = current_interpreter['path']
            mp = MarketPlace(path)
            mp.exec_()

    def verify(self, values) -> bool:
        LEN = 16
        if len(values['name']) > LEN:
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr(
                                    f'Name should be less than {repr(LEN)} characters,but your input was %d characters.' %
                                    len(values['name'])))
            return False
        else:
            return True

    def remove(self):
        modify_interpreter_config("delete", index=self.interpreters_list_show.currentRow() - 1)
        self.show_interpreters()

    def show_interpreters(self):
        self.interpreters_list_show.clear()
        self.interpreters_list_show.addItem(self.tr('BuiltIn (3.8.5)'))
        ext_interpreters = get_all_external_interpreters()
        for interpreter in ext_interpreters:
            name = interpreter['name']
            version = interpreter['version']
            text = name + ' (%s)' % version
            self.interpreters_list_show.addItem(text)

    def on_list_current_item_changed(self):
        """
        如果是默认解释器的时候，不支持修改。
        Returns:

        """
        self.button_delete.setEnabled(not self.interpreters_list_show.currentRow() == 0)
        self.button_edit.setEnabled(not self.interpreters_list_show.currentRow() == 0)

    def get_current_interpreter(self) -> Dict:

        current_index = self.interpreters_list_show.currentRow()
        if current_index == 0:
            return {'name': 'Builtin', 'path': sys.executable, 'version': sys.version.split()[0]}
        elif current_index < 0:
            return
        else:
            list_index = current_index - 1
            return get_all_external_interpreters()[list_index]


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication([])
    w = InterpreterManagerWidget()
    w.show()
    app.exec_()
