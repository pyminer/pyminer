import os
from typing import List, Union, Tuple, Any
from widgets import PMGFlowContent, PMGPanelDialog


def convert_path_to_identifier(path: str):
    basename = os.path.basename(path)
    basename = basename.replace('.', '_')
    basename = basename.replace('-', '_')
    basename = basename.replace('&', '_')
    basename = basename.replace('$', '_')
    basename = basename.replace('(', '_')
    basename = basename.replace(')', '_')
    basename = basename.replace('[', '_')
    basename = basename.replace(']', '_')
    basename = basename.replace('{', '_')
    basename = basename.replace('}', '_')
    basename = 'var_' + basename
    basename = basename.replace(' ', '')
    print(basename, basename.isidentifier())
    assert basename.isidentifier(), 'basename invalid :\'%s\'' % basename
    return basename


class VariableSetter(PMGFlowContent):
    """
    根据输入的数据，绘制一条直线。
    允许输入的数据类型：多个端口的直线。

    """

    def __init__(self):
        super(VariableSetter, self).__init__()
        self.input_args_labels = ['value', 'name']
        self.output_ports_labels = []
        self.class_name = 'SetVariable'
        self.text = '变量上传工作空间'
        self.icon_path = ''
        self.info = {'var_name': 'Unnamed'}

    def process(self, value: Any, name: str = '') -> List:
        """

        Args:
            value:
            name:

        Returns:

        """
        from lib.comm import set_var
        # print(args)
        # assert len(value) == 1, repr(args)
        if name.isidentifier():
            self.info['var_name'] = name
        else:
            if os.path.exists(name):
                name = convert_path_to_identifier(name)
                self.info['var_name'] = name
            else:
                raise ValueError('Variable name \'%s\' is not an identifier!' % name)

        return [set_var(self.info['var_name'], value)]

    def on_settings_requested(self, parent):
        if not self.info['var_name'].isidentifier():
            self.info['var_name'] = 'Unnamed'
        views = [
            ['line_ctrl', 'var_name', 'Variable Name', self.info['var_name']]
        ]
        dlg = PMGPanelDialog(parent=parent, views=views)
        dlg.exec_()
        self.info['var_name'] = dlg.panel.get_value()['var_name']

    def load_info(self, info: dict):
        self.info['var_name'] = info['var_name'] if 'var_name' in info else 'Unnamed'

    def format_param(self) -> str:
        return self.info['var_name']


class VariableGetter(PMGFlowContent):
    """
    根据输入的数据，绘制一条直线。
    允许输入的数据类型：多个端口的直线。

    """

    def __init__(self):
        super(VariableGetter, self).__init__()
        self.input_args_labels = []
        self.output_ports_labels = ['out']
        self.class_name = 'GetVariable'
        self.text = '选择工作空间变量'
        self.icon_path = ''
        self.info = {'var_name': 'Unnamed'}

    def process(self, *args) -> List:
        """

        Args:
            *args:

        Returns:

        """
        from lib.comm import get_var, get_var_names
        assert self.info['var_name'] in get_var_names(), 'Variable is not Chosen!'

        return [get_var(self.info['var_name'])]

    def on_settings_requested(self, parent):
        from lib.comm import get_var_names
        vars = get_var_names()
        if not self.info['var_name'] in vars:
            if len(vars) != 0:
                self.info['var_name'] = vars[0]
            else:
                self.info['var_name'] = ''
        views = [
            ['combo_ctrl', 'var_name', 'Variable Name', self.info['var_name'], vars]
        ]
        dlg = PMGPanelDialog(parent=parent, views=views)
        dlg.exec_()
        self.info['var_name'] = dlg.panel.get_value()['var_name']

    def format_param(self) -> str:
        return self.info['var_name']

    def load_info(self, info: dict):
        self.info['var_name'] = info['var_name'] if 'var_name' in info else 'Unnamed'
