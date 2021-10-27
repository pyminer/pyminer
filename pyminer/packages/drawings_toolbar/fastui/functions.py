import os

from PySide2.QtWidgets import QApplication, QMessageBox, QWidget

from lib.comm import run_command, get_var_names
from utils import bind_panel_combo_ctrl_with_workspace

if not __name__ == '__main__':
    from .base import DFOperationDialog
else:
    from base import DFOperationDialog


def run_code_in_ipython(code, comment):
    run_command(command=code, hint_text=code + "  # " + comment, hidden=False)


def plt_show():
    run_code_in_ipython("plt.show()", "显示图像")


def plt_clf(parent: QWidget):
    ret = QMessageBox.warning(parent, "清空当前绘图", "当前绘图的全部更改将丢失，确认要清空当前绘图吗？",
                              QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
    if ret == QMessageBox.Ok:
        run_code_in_ipython("plt.clf()", "清空当前绘图")


class EditLabelDialog(DFOperationDialog):
    def __init__(self, ):
        super(EditLabelDialog, self).__init__()
        self.setWindowTitle("编辑标签")
        self.combo_box.hide()
        self.hint_label.hide()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "numerical_integration.md")
        names = get_var_names()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "numerical_integration.md")

        if len(names) == 0:
            names = [self.no_var_in_workspace_hint()]
            name_tick = self.no_var_in_workspace_hint()
        else:
            name_tick = names[0]

        views = [
            ('combo_ctrl', 'op_global_axes', '操作的坐标轴', False, [False, True], ["全局空间(plt)", "用户指定（Axes变量）"]),
            ('combo_ctrl', 'ax', '坐标轴（Axes）', name_tick, names),
            ('line_ctrl', 'title', '标题', ''),
            ('line_ctrl', 'xlabel', 'x轴标签', ''),
            ('line_ctrl', 'ylabel', 'y轴标签', ''),
        ]

        self.panel.set_items(views)
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("ax"),
                                             type_filter=lambda s: s.lower().find("axessubplot") != -1)
        self.panel.set_as_controller("op_global_axes", ["ax"], True)

        self.code_template_plt = """
plt.title({title})
plt.xlabel({xlabel})
plt.ylabel({ylabel})
plt.draw()
plt.gcf()
"""
        self.code_template_ax = """
{ax}.set_title({title})
{ax}.set_xlabel({xlabel})
{ax}.set_ylabel({ylabel})
plt.draw()
plt.gcf()        
"""

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        op_global_axes = values.pop("op_global_axes")
        code_template = self.code_template_plt if not op_global_axes else self.code_template_ax
        print(values)
        if op_global_axes:
            ax = values.pop("ax")
            values = {k: "\'" + v + "\'" for k, v in values.items()}
            values["ax"] = ax
        else:
            values = {k: "\'" + v + "\'" for k, v in values.items()}
        cmd = code_template.format(**values)
        print(cmd)
        return cmd


class EditTickDialog(DFOperationDialog):
    def __init__(self, ):
        super(EditTickDialog, self).__init__()
        self.setWindowTitle("编辑轴刻度及标签")
        self.combo_box.hide()
        self.hint_label.hide()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "numerical_integration.md")

        names = get_var_names()
        if len(names) == 0:
            names = [self.no_var_in_workspace_hint()]
            name_tick = self.no_var_in_workspace_hint()
            name_ticklabel = self.no_var_in_workspace_hint()
        else:
            name_tick = names[0]
            name_ticklabel = names[-1]
        views = [
            ('combo_ctrl', 'op_global_axes', '操作的坐标轴', True, [False, True], ["全局空间(plt)", "用户指定（Axes变量）"]),
            ('combo_ctrl', 'ax_name', '坐标轴（Axes）', name_tick, names),

            ('check_ctrl', 'enable_xtick', '使用x轴刻度', True),
            ('combo_ctrl', 'xticks', 'x轴刻度', name_tick, names),
            ('combo_ctrl', 'xticklabels', 'x轴刻度标签', name_ticklabel, names),
            ('check_ctrl', 'enable_ytick', '使用y轴标签', True),
            ('combo_ctrl', 'yticks', 'y轴刻度', name_tick, names),
            ('combo_ctrl', 'yticklabels', 'y轴刻度标签', name_ticklabel, names),
        ]

        self.panel.set_items(views)
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("xticks"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("xticklabels"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("yticks"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("yticklabels"))
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("ax_name"),
                                             type_filter=lambda s: s.lower().find("axessubplot") != -1)

        self.panel.set_as_controller("enable_xtick", ["xticks", "xticklabels"], True)
        self.panel.set_as_controller("enable_ytick", ["yticks", "yticklabels"], True)
        self.panel.set_as_controller("op_global_axes", ["ax_name"], True)

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        enable_xtick = values.pop("enable_xtick")
        enable_ytick = values.pop("enable_ytick")
        cmd = ""
        if not values["op_global_axes"]:
            if enable_xtick:
                cmd += "plt.xticks({xticks},{xticklabels})\n".format(xticks=values["xticks"],
                                                                     xticklabels=values["xticklabels"])
            if enable_ytick:
                cmd += "plt.yticks({yticks},{yticklabels})\n".format(yticks=values["yticks"],
                                                                     yticklabels=values["yticklabels"])
        else:
            ax_name = values["ax_name"]
            if enable_xtick:
                cmd += "{ax_name}.set_xticks({xticks})\n".format(ax_name=ax_name, xticks=values["xticks"])
                cmd += "{ax_name}.set_xticklabels({xticklabels})\n".format(ax_name=ax_name,
                                                                           xticklabels=values["xticklabels"])
            if enable_ytick:
                cmd += "{ax_name}.set_yticks({yticks})\n".format(ax_name=ax_name, yticks=values["yticks"])
                cmd += "{ax_name}.set_yticklabels({yticklabels})\n".format(ax_name=ax_name,
                                                                           yticklabels=values["yticklabels"])

        cmd += "plt.gcf()"
        return cmd


class CreateSubplotDialog(DFOperationDialog):
    """
    创建子图的对话框
    """

    def __init__(self, ):
        super(CreateSubplotDialog, self).__init__()
        self.setWindowTitle("编辑标签")
        self.combo_box.hide()
        self.hint_label.hide()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "plot.md")
        views = [
            ('numberspin_ctrl', 'nrows', '行数', 2, "", (1, 6)),
            ('numberspin_ctrl', 'ncols', '列数', 2, "", (1, 6)),
        ]

        self.panel.set_items(views)

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        nrows = values["nrows"]
        ncols = values["ncols"]
        code = ""
        ax_num = 1
        for row in range(1, nrows + 1):
            for col in range(1, ncols + 1):
                code += f"ax_{row}_{col} = plt.subplot({nrows}, {ncols}, {ax_num})\n"
                ax_num += 1
        print(code)

        code += "plt.draw()\nplt.gcf()"
        return code


class CreateGridDialog(DFOperationDialog):
    """
    创建子图的对话框
    """

    def __init__(self, ):
        super(CreateGridDialog, self).__init__()
        self.setWindowTitle("网格线")
        self.combo_box.hide()
        self.hint_label.hide()
        self.help_file_path = os.path.join(os.path.dirname(__file__), "helps", "plot.md")
        names = get_var_names()
        if len(names) == 0:
            names = [self.no_var_in_workspace_hint()]
            name_tick = self.no_var_in_workspace_hint()
        else:
            name_tick = names[0]
        views = [
            ('combo_ctrl', 'op_global_axes', '操作的坐标轴', True, [True, False], ["全局空间，当前坐标轴(plt)", "用户指定（Axes变量）"]),
            ('combo_ctrl', 'ax', '坐标轴（Axes）', name_tick, names),
            ('combo_ctrl', 'b', '绘制或清除', True, [True, False], ["绘制网格线", "清除网格线"]),
            ('combo_ctrl', 'axis', '显示网格的坐标轴', "both", ["both", "x", "y"], ["所有", "X（网格线从上到下）", "Y（网格线从左到右）"]),
        ]

        self.panel.set_items(views)
        self.panel.set_as_controller("b", ["axis"], True)
        self.panel.set_as_controller("op_global_axes", ["ax"], False)
        bind_panel_combo_ctrl_with_workspace(self.panel.get_ctrl("ax"),
                                             type_filter=lambda s: s.lower().find("axessubplot") != -1)

    def get_value_code(self) -> str:
        values = self.panel.get_value_with_filter()  # 只获取使能并且可见的控件的值
        op_global_axes = values.pop("op_global_axes")
        if op_global_axes:
            code = f"plt.grid({self.kwargs_to_str(values)})\nplt.gcf()"
        else:
            ax = values.pop("ax")
            code = f"{ax}.grid({self.kwargs_to_str(values)})\nplt.gcf()"
        return code


if __name__ == "__main__":
    app = QApplication([])
    # md = EditTickDialog()
    # md = EditLabelDialog()
    # md = CreateSubplotDialog()
    md = CreateGridDialog()
    md.show()
    app.exec_()
