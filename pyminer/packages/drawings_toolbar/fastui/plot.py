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

plot_code = """
plt.plot({variables},{fmt_with_comma}{kwargs_str})
plt.gcf()
"""
ax_plot_code = """
{ax}.plot({variables},{fmt_with_comma}{kwargs_str})
plt.gcf()
"""

class PlotDialog(DFOperationDialog):
    def __init__(self, ):
        super(PlotDialog, self).__init__()
        self.setWindowTitle("绘制折线图")
        self.combo_box.hide()
        self.hint_label.hide()
        names = get_var_names()

        if len(names) == 0:
            names = [self.no_var_in_workspace_hint()]
            name = self.no_var_in_workspace_hint()
        else:
            name = names[0]

        views = [
            ('combo_ctrl', 'op_global_axes', '操作的坐标轴', True, [True, False], ["全局空间(plt)", "用户指定（Axes变量）"]),
            ('combo_ctrl', 'ax', '坐标轴（Axes）', name, names),
            ("check_ctrl", "enable_x", "启用x轴", False),
            ('combo_ctrl', 'x', 'x轴', name, names),
            ('combo_ctrl', 'y', 'y轴', name, names),
            # ('numberspin_ctrl', 'bins', '柱子个数', 20, '', (0, 100000)),
            # ('numberspin_ctrl', 'size', '变量个数', 1, '', (0, 2 ** 30)),
            # ('check_ctrl', 'enable_xrange', '限制x轴范围（无穷请输入-inf或+inf）', False),
            # [('number_ctrl', 'x_min', 'x最小值', 0, ''), ('number_ctrl', 'x_max', 'x最大值', 1, '')],
            # ('check_ctrl', 'enable_yrange', '限制y轴范围（无穷请输入-inf或+inf）', False),
            # [('number_ctrl', 'y_min', 'y最小值', 0, ''), ('number_ctrl', 'y_max', 'y最大值', 1, '')],
            ('combo_ctrl', "marker", "点标记", "",
             ["", 'o', 'v', '^', '<', '>', '8', 's',
              'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'],
             ["无标记", "● 实心圆点", "▼ 倒三角", "▲ 正三角", "◀ 左三角", "▶ 右三角", "八边形", "█ 方块",
              "五边形", "★ 五角星", "六边形(直立)", "六边形（平放）", "◆ 菱形（上下、左右等长）", "菱形（上下长于左右）", "✚ 实心+号", "✖ 叉号"]),
            ('combo_ctrl', 'linestyle', '线型', '-', ['-', '--', '-.', ':', ''], ['实线', "虚线", "点划线", "点虚线", "无"]),
            # ('combo_ctrl', 'density', '绘制类型', False, [False, True], ['累计数量图', "概率密度图"]),
        ]

        self.panel.set_items(views)
        self.panel.set_as_controller("enable_x", ["x"], True, "enable")
        self.panel.set_as_controller("op_global_axes", ["ax"], False, "enable")
        # self.panel.set_as_controller("enable_xrange", ["x_min", "x_max"], True, "enable")
        # self.panel.set_as_controller("enable_yrange", ["y_min", "y_max"], True, "enable")

        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("x"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("y"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("ax"),
                                             type_filter=lambda s: s.lower().find("axessubplot") != -1)

        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "plot.md")

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        op_global_axes = values.pop('op_global_axes')

        y = values.pop("y")
        vars_str = ""
        if values.pop("enable_x"):
            x = values.pop("x")
            vars_str = f"{x},{y}"
        else:
            vars_str = f"{y}"

        fmt = values.pop("marker") + values.pop("linestyle")
        if fmt != "":
            fmt = "\'" + fmt + "\',"

        args_str = ""

        ordered_dict = OrderedDict()
        # if values.pop("enable_xrange"):
        #     start = values.pop("x_min")
        #     end = values.pop("x_max")
        #     xrange = (start, end)
        # if values.pop("enable_yrange"):
        #     start = values.pop("y_min")
        #     end = values.pop("y_max")
        #     yrange = (start, end)

        args_str += self.kwargs_to_str(ordered_dict)
        if op_global_axes:
            cmd = plot_code.format(variables=vars_str, fmt_with_comma=fmt, kwargs_str=args_str)
        else:
            cmd = ax_plot_code.format(ax=values["ax"],variables=vars_str, fmt_with_comma=fmt, kwargs_str=args_str)
        return cmd


if __name__ == '__main__':
    app = QApplication([])
    md = PlotDialog()
    md.show()
    app.exec_()
