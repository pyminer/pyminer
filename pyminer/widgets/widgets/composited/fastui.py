"""
这是定义基类的基础文件，里面是用代码生成方式来制作功能性面板的示例。比如
可以参阅同一目录下的其他文件。这些面板默认样式为悬浮在最上方，即使面板弹出，也可以操作主界面。

面板文件与PyMiner主程序完全解耦，启动PyMiner主程序后，可以直接运行此文件，或者fastui文件夹下的任何.py文件，
以此调试面板。此时，需要确保PyMiner的工作空间中有pandas.DataFrame类型的数据。

如datamerge.py(数据集合并)/ dropdata.py(去除缺失值)/ fillna(填充缺失值) 等。

最底层基类是BaseOperationDialog，是一个QDialog对话框基类，里面定义了一系列的基础方法，比如变量获取等。它是一个完全空白的对话框。
次底层基类是DFOperationDialog，是用于数据集操作的基类。它定义有一个变量选择下拉菜单self.combo_box、一个参数输入面板self.panel，以及一个带有
四个按钮（预览、保存、关闭和帮助）的按钮面板。

数据合并的面板继承于BaseOperationDialog，其余面板都继承于DFOperationDialog。这是因为数据合并面板需要多个选择数据的下拉框，用后者满足不了要求。

有关底层基类中的相关方法，请移步相应类定义的位置。

这些面板生成的函数，应当是一个有返回值的函数，参数为工作空间中的变量，或者是字符串、数字等。

比如，工作空间中有函数a、b。数据合并面板希望生成一个横向合并a和b的函数。那么，最终生成的代码应该为：
pd.concat([a,b],axis=0)

这段函数有两种执行方式。一种是预览（preview），由preview按钮触发，调用基类的preview方法，直接执行pd.concat([a,b],axis=0)；另一种是储存（store），
由“Save to var“按钮触发，调用基类store方法，要求用户输入一个新的变量名，然后执行代码f = pd.concat([a,b],axis=0)，(f为用户输入的变量名)。

pd.concat函数有返回值。在点击“preview”

@Time: 2021/2/8 12:54
@Author: Zhanyi Hou
@Email: 1295752786@qq.com
@File: pmgui.py
"""
from abc import abstractmethod
from typing import List

from PySide2.QtCore import Qt, QCoreApplication, Signal
from PySide2.QtWidgets import QDialog, QVBoxLayout, QApplication, QPushButton, QComboBox, QHBoxLayout, QLabel, \
    QTextBrowser

from lib.comm import get_var_names, run_command, call_interface
from utils import input_identifier, bind_combo_with_workspace


def kwargs_to_str(kwargs: dict) -> str:
    """
    将字典参数转化为字符串的简易方法
    Args:
        kwargs:

    Returns:

    """
    args_str = ''
    for k, v in kwargs.items():
        args_str += '{k}={v},'.format(k=k, v=repr(v))
    return args_str


class BaseOperationDialog(QDialog):
    """
    最底层的功能面板基类。
    定义了代码生成的有关方法。

    """
    signal_update_combo = Signal()

    def __init__(self):
        from widgets.utilities import PMGOneShotThreadRunner
        self.thrunner: PMGOneShotThreadRunner = None
        super(BaseOperationDialog, self).__init__()

    def store(self):
        """
        执行存储到变量的命令。

        Returns:

        """
        code = self.get_assignment_code()
        if code != '':
            run_command(command=code, hint_text=self.get_prompt_template() + code, hidden=False)

    def preview(self) -> None:
        """
        预览分析结果。
        Returns:

        """
        code = self.get_value_code()
        if code != '':
            run_command(command=code, hint_text=self.get_prompt_template() + code, hidden=False)

    def help(self) -> None:
        """
        弹出帮助面板
        Returns: None

        """
        dlg = QDialog()
        dlg.setLayout(QVBoxLayout())
        textBrowser = QTextBrowser(self)
        dlg.layout().addWidget(textBrowser)
        textBrowser.setMarkdown(self.get_help_content())
        dlg.exec_()

    def get_help_content(self) -> str:
        """
        生成帮助内容

        为markdown格式

        Notes:子类最好重写这个方法
        Returns:

        """
        return """# 帮助\n\n暂未定义帮助"""

    def get_prompt_template(self) -> str:
        """
        获取提示模板

        Notes:子类可以不重写这个方法
        Returns:
        """
        return ''

    def kwargs_to_str(self, kwargs: dict) -> str:
        """
        将字典参数转化为字符串的简易方法
        Args:
            kwargs:

        Returns:

        """
        args_str = ''
        for k, v in kwargs.items():
            args_str += '{k}={v},'.format(k=k, v=repr(v))
        return args_str

    @abstractmethod
    def get_value_code(self) -> str:
        """
        获取一段代码，这段代码应当有返回值，而不是赋值代码。
        例如， “a = pd.concat([c,d])”

        Notes:子类必须重写这个方法。

        Returns:
        """
        return ''

    def get_assignment_code(self) -> str:
        """
        获取赋值语句。实际上就是先让用户输入一个变量名，然后将这个变量名和赋值语句放在get_value_code方法
        生成的代码的左侧。

        倘若用户输入的变量名是“a”，get_value_code方法生成的代码为“pd.concat([c,d])”,那么这个方法生成的代码就是：
        “a = pd.concat([c,d])”

        子类中通常无需重写这个方法

        Returns: 合并好的代码
        """
        code = self.get_value_code()
        identifier = input_identifier(parent=self, default_name=self.combo_box.currentText(), allow_existing_name=True)
        if identifier != '':
            code = identifier + ' = ' + code
            return code
        return ''

    def get_selected_variables(self) -> List[str]:
        """
        获取当前界面上选中的变量。
        当界面为PyMiner调用时，此方法不能在主进程中调用，否则会阻塞消息循环。
        Returns: 当前界面上选中的变量，可能是一个列表。
        """
        return call_interface('workspace_inspector', 'get_selected_variables', {}, request_ret=True)

    def showEvent(self, arg__1: 'QShowEvent') -> None:
        from widgets.utilities import PMGOneShotThreadRunner
        if self.thrunner is None or not self.thrunner.is_running():
            self.thrunner = PMGOneShotThreadRunner(callback=self.get_selected_variables)
            self.thrunner.signal_finished.connect(self.on_update_combo)


class DFOperationDialog(BaseOperationDialog):
    signal_update_combo = Signal()

    def __init__(self):
        from widgets.widgets.composited import PMGPanel
        super(DFOperationDialog, self).__init__()
        self.setLayout(QVBoxLayout())
        self.combo_box = QComboBox()
        bind_combo_with_workspace(self.combo_box)
        self.panel = PMGPanel()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.button_layout = QHBoxLayout()

        self.button_preview = QPushButton(QCoreApplication.translate('BaseDFOperationDialog', "预览"))
        self.button_store = QPushButton(QCoreApplication.translate('BaseDFOperationDialog', "保存到变量"))
        self.button_close = QPushButton(QCoreApplication.translate('BaseDFOperationDialog', "关闭"))
        self.button_help = QPushButton(QCoreApplication.translate('BaseDFOperationDialog', "帮助"))

        # self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help)
        self.button_layout.addWidget(self.button_preview)
        self.button_layout.addWidget(self.button_store)
        self.button_layout.addWidget(self.button_help)
        self.button_layout.addWidget(self.button_close)

        self.button_preview.clicked.connect(self.preview)  # 预览
        self.button_store.clicked.connect(self.store)  # 储存
        self.button_close.clicked.connect(self.close)  # 关闭对话框
        self.button_help.clicked.connect(self.help)  # 显示帮助

        self.hint_label = QLabel(self.tr('选择变量'))
        self.layout().addWidget(self.hint_label)
        self.layout().addWidget(self.combo_box)
        self.layout().addWidget(self.panel)
        self.layout().addLayout(self.button_layout)

    def on_update_combo(self, vars: List[str]):
        self.combo_box.clear()
        self.combo_box.addItems(get_var_names())
        if len(vars) > 0:
            self.combo_box.setCurrentText(vars[0])


class FunctionGUIDialog(DFOperationDialog):
    def __init__(self, dic):
        super(FunctionGUIDialog, self).__init__()
        self.func_name = dic["func_name"]
        self.with_object = dic["with_object"]
        if not self.with_object:
            self.combo_box.hide()
        self.setWindowTitle(dic["title"])
        views = []
        optional_names = []
        for arg in dic["args"]:
            views.append("-" * 60)
            if arg["optional"]:
                optional_names.append(arg["name"])
                views.append(("check_ctrl", arg["name"] + "#enable", "", True))
            arg["ctrl"]["name"] = arg["name"]
            views.append(arg["ctrl"])

        self.panel.set_items(views)
        for op_name in optional_names:
            self.panel.set_as_controller(op_name + "#enable", [op_name], True, )

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        print(values,self.panel.widgets_dic)
        values = {k: v for k, v in values.items() if k.isidentifier()}
        varname = self.combo_box.currentText()
        args_str = ''
        for k, v in values.items():
            args_str += '{k}={v},'.format(k=k, v=repr(v))
        if not self.with_object:
            code = '{func_name}({args})'.format(func_name=self.func_name, args=args_str)
        else:
            code = '{var_name}.{method_name}({args})'.format(var_name=varname,
                                                             method_name=self.func_name,
                                                             args=args_str)
        print(code,values)
        return code


if __name__ == '__main__':
    app = QApplication([])
    md = DFOperationDialog()
    md.show()
    app.exec_()
