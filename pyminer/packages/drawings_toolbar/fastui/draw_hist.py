"""
"""
import os
from collections import OrderedDict

from PySide2.QtWidgets import QApplication

from lib.comm import get_var_names
from utils import bind_panel_combo_ctrl_with_workspace

if not __name__ == '__main__':
    from .base import DFOperationDialog
else:
    from base import DFOperationDialog

hist_code_plt = """
plt.hist({variable},{args_str})
plt.gcf()
"""
hist_code_ax = """
{ax}.hist({variable},{args_str})
plt.gcf()
"""


class DrawHistDialog(DFOperationDialog):
    def __init__(self, ):
        super(DrawHistDialog, self).__init__()
        self.setWindowTitle("绘制直方图")
        self.combo_box.hide()
        self.hint_label.hide()
        names = get_var_names()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "numerical_integration.md")

        if len(names) == 0:
            names = [self.no_var_in_workspace_hint()]
            name = self.no_var_in_workspace_hint()
        else:
            name = names[0]

        views = [
            ('combo_ctrl', 'op_global_axes', '操作的坐标轴', True, [True, False], ["全局空间(plt)", "用户指定（Axes变量）"]),
            ('combo_ctrl', 'ax', '坐标轴（Axes）', name, names),
            ('combo_ctrl', 'variable', '要分析的变量', name, names),
            ('numberspin_ctrl', 'bins', '柱子个数', 20, '', (0, 100000)),
            ('numberspin_ctrl', 'size', '变量个数', 1, '', (0, 2 ** 30)),
            ('check_ctrl', 'enable_range', '限制范围（无穷请输入-inf或+inf）', False),
            ('number_ctrl', 'start', '最小值', 0, ''),
            ('number_ctrl', 'end', '最大值', 1, ''),
            ('combo_ctrl', 'density', '绘制类型', False, [False, True], ['累计数量图', "概率密度图"]),
        ]

        self.panel.set_items(views)
        self.panel.set_as_controller("enable_range", ["start", "end"], True, "enable")
        self.panel.set_as_controller("op_global_axes", ["ax"], False, "enable")

        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("variable"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("ax"),
                                             type_filter=lambda s: s.lower().find("axessubplot") != -1)

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        variable = values.pop("variable")
        op_global_axes = values.pop("op_global_axes")
        ax = values.pop("ax") if values.get("ax") is not None else None
        args_str = ""

        ordered_dict = OrderedDict()
        ordered_dict["bins"] = values["bins"]
        if values.pop("enable_range"):
            start = values.pop("start")
            end = values.pop("end")
            range = (start, end)
            ordered_dict["range"] = range
        ordered_dict["density"] = values["density"]
        args_str += self.kwargs_to_str(ordered_dict)
        if op_global_axes:
            cmd = hist_code_plt.format(variable=variable, args_str=args_str)
        else:
            cmd = hist_code_ax.format(ax=ax, variable=variable, args_str=args_str)
        return cmd

if __name__ == '__main__':
    app = QApplication([])
    md = DrawHistDialog()
    md.show()
    app.exec_()
