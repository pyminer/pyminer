from collections import OrderedDict
from typing import Union, Callable

from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QComboBox, QInputDialog, QWidget, QLineEdit, QMessageBox




def input_identifier(parent: QWidget, default_name: str = '', allow_existing_name: bool = False) -> str:
    """
    要求用户输入一个变量名
    :param default_name: 
    :return: 
    """
    from lib.comm import get_var_names
    assert default_name.isidentifier()
    var_names = get_var_names()
    if var_names is None:
        var_names = []
    while 1:
        name, ok = QInputDialog.getText(parent, "变量命名", "输入新的变量名称:", QLineEdit.Normal, default_name)
        if ok and (len(name) != 0):

            if name in var_names:
                if not allow_existing_name:
                    QMessageBox.warning(parent, "提示", "变量名已存在")
                else:
                    ret = QMessageBox.warning(parent, '提示', "变量名已存在，是否要覆盖？",
                                              QMessageBox.Ok | QMessageBox.Cancel,
                                              QMessageBox.Cancel)
                    if ret == QMessageBox.Ok:
                        return name
                    else:
                        continue
            elif not name.isidentifier():
                QMessageBox.warning(parent, '提示', '变量名无效\n提示：\n1、不要以数字开头;\n2、不要包含除下划线外的所有符号。')
                continue
            else:
                return name
        else:
            return ''


def bind_combo_with_workspace(combo: QComboBox, type_filter: str = ''):
    """
    将combobox与工作空间的变量变更绑定起来。自动获取相应的变量名。

    :param combo:
    :param type_filter:          变量类型的字符表示
        目前支持四种：string,table,array和numeric。使用table可以过滤出所有的二维array\pd.DataFrame
        默认值为‘’也就是空字符串，此时将返回所有的变量名。
    :return:
    """
    from lib.comm import get_var_names

    def on_combo_var_name_mouse_pressed(event):
        """
        combo box在点击（菜单未弹出）的时候，从PyMiner主程序获取全部符合要求的变量名。
        同时需要调用QComboBox的mousePressEvent事件，保证选单正常弹出。
        :return:
        """
        var_names = get_var_names(filter=type_filter)

        last_item_text = combo.currentText()

        combo.clear()
        combo.addItems(var_names)
        if last_item_text in var_names:
            combo.setCurrentIndex(var_names.index(last_item_text))
        QComboBox.mousePressEvent(combo, event)

    combo.mousePressEvent = on_combo_var_name_mouse_pressed


def bind_panel_combo_ctrl_with_workspace(combo_ctrl: "PMGComboCtrl", type_filter: Union[str, Callable[[str], bool]] = '',
                                         shape_filter: Callable[[Union[int, tuple]], bool] = None):
    """
    将pmgpanel 中的 下拉列表框PMGComboCtrl与工作空间的变量变更绑定起来。自动获取相应的变量名。

    :param combo:
    :param type_filter:          变量类型的字符表示，也可以是一个函数。当为字符串时，将判断字符串是不是在变量内部。
        可以直接指定type字符串中含有什么内容。
    :return:
    """
    from lib.comm import get_data_descs
    from widgets import PMGComboCtrl
    assert isinstance(combo_ctrl, PMGComboCtrl), combo_ctrl
    combo = combo_ctrl.check
    if type_filter == "":
        type_filter = lambda s: True
    else:
        type_filter = (lambda s: (s.find(type_filter) != -1)) if isinstance(type_filter, str) else type_filter
    shape_filter = lambda s: True if shape_filter is None else shape_filter

    def on_combo_var_name_mouse_pressed(event: QMouseEvent):
        """
        combo box在点击（菜单未弹出）的时候，从PyMiner主程序获取全部符合要求的变量名。
        同时需要调用QComboBox的mousePressEvent事件，保证选单正常弹出。
        Args
        Returns
        """
        var_descs = get_data_descs()
        var_name_dic = OrderedDict()
        for name, desc in var_descs.items():
            if type_filter(desc.type):
                var_name_dic[name] = ""
        var_name_dic.update(var_descs)
        var_names = list(var_name_dic.keys())
        last_item_text = combo.currentText()

        combo.clear()
        combo_ctrl.set_choices(var_names)
        if last_item_text in var_names:
            combo.setCurrentIndex(var_names.index(last_item_text))
        if event is not None:
            QComboBox.mousePressEvent(combo, event)
        else:
            if len(var_names) > 0:
                combo.setCurrentIndex(0)

    combo.mousePressEvent = on_combo_var_name_mouse_pressed

    on_combo_var_name_mouse_pressed(None)


def IS_ONE_DIM_ARRAY(shape: Union[tuple, int]):
    if isinstance(shape, int) and shape > 1:
        return True
