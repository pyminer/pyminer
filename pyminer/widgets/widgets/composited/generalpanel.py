"""
命名规范：

PMG+控件类型+功能类型
控件类型可以是一词或者两个词。

相关设计思想来自ImagePy团队的SciWx中的normal控件，对接口做出相关调整，增加了json解码解包的部分。

作者：侯展意
qq:1295752786@qq.com
"""

import logging
from typing import Any, List, Tuple, Dict, Callable, Union, Optional

from PySide2.QtCore import Signal
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QSpacerItem, QSizePolicy, QDialog, QFrame, QVBoxLayout, QHBoxLayout, QDialogButtonBox, \
    QApplication, QLabel

from widgets.widgets.extended import (BaseExtendedWidget, PMGCheckCtrl, PMGColorCtrl, PMGEvalCtrl, PMGComboCtrl,
                                         PMGFileCtrl, PMGMultiTypeCtrl, PMGVariablesComboCtrl,
                                         PMGKeyMapCtrl, PMGFolderCtrl, PMGLineCtrl, PMGNumberCtrl, PMGPasswordCtrl,
                                         PMGListCtrl, PMGDateCtrl, PMGTimeCtrl, PMGDateTimeCtrl, PMGNumberSpinCtrl,
                                         PMGTableShow, PMGLabelShow, PMGRuleCtrl)

try:
    from widgets.widgets.extended import PMGTimeSeriesShow
except ImportError:
    PMGTimeSeriesShow = None

from widgets.utilities.uilogics.codechecking import iter_isinstance, ErrorReporter

logger = logging.getLogger(__name__)
views_dic = {}
views_dic.update({'color_ctrl': PMGColorCtrl,
                  'eval_ctrl': PMGEvalCtrl,
                  'file_ctrl': PMGFileCtrl,
                  'keymap_ctrl': PMGKeyMapCtrl,
                  'folder_ctrl': PMGFolderCtrl,
                  'line_ctrl': PMGLineCtrl,
                  'number_ctrl': PMGNumberCtrl,
                  'password_ctrl': PMGPasswordCtrl,
                  'multitype_ctrl': PMGMultiTypeCtrl,
                  "vars_combo_ctrl": PMGVariablesComboCtrl})

views_dic.update({'editor_ctrl': globals().get('PMGEditorCtrl'),
                  'check_ctrl': PMGCheckCtrl,
                  'combo_ctrl': PMGComboCtrl,
                  'list_ctrl': PMGListCtrl,
                  'time_ctrl': PMGTimeCtrl,
                  'date_ctrl': PMGDateCtrl,
                  'datetime_ctrl': PMGDateTimeCtrl,
                  'numberspin_ctrl': PMGNumberSpinCtrl
                  })

views_dic.update({'timeseries_show': PMGTimeSeriesShow,
                  'label_show': PMGLabelShow,
                  'table_show': PMGTableShow,
                  'rules_ctrl': PMGRuleCtrl
                  })

PANEL_VIEW_CLASS = List[Union[
    Tuple[Any],
    List[Any],
    Dict[str, Any]
]]


class PMGPanel(QFrame):
    widgets_dic: Dict[str, BaseExtendedWidget] = {}
    signal_settings_changed = Signal(dict)

    def __init__(self, parent=None, views: PANEL_VIEW_CLASS = None, layout_dir: str = 'v', with_spacer: bool = True,
                 with_aux_spacer=False,
                 spacing: int = 0,
                 margins: Union[int, Tuple[int, int, int, int]] = 0):
        super(PMGPanel, self).__init__(parent)
        self._initial_style_sheet = self.styleSheet()
        self.layout_dir = layout_dir
        self.with_spacer = with_spacer
        self.with_aux_spacer = with_aux_spacer

        if layout_dir == 'v':
            self.setLayout(QVBoxLayout())
        else:
            self.setLayout(QHBoxLayout())

        self.layout().setSpacing(spacing)
        if isinstance(margins, tuple):
            assert iter_isinstance(margins, int), \
                ErrorReporter.create_invalid_parameter_type_message('margins', type(margins), int)
            self.layout().setContentsMargins(*margins)
        elif isinstance(margins, int):
            margins = [margins] * 4
            self.layout().setContentsMargins(*margins)
        else:
            raise TypeError(ErrorReporter.create_invalid_parameter_type_message('margins', type(margins),
                                                                                'int or Tuple[int,int,int,int]'))
        self.layout()
        self.set_items(views)

        self._param_changd_callbacks: Dict[str, List[Callable]] = {}

    def set_param_changed_callback(self, param: str, callback: Callable):
        """

        Args:
            param:
            callback:

        Returns:

        """
        # assert param not in self._param_changd_callbacks.keys(), \
        #     repr(param) + ' is already in callback dict\'s keys: %s ' % (repr(self._param_changd_callbacks.keys()))
        assert param in self.widgets_dic.keys(), 'widget with param \'%s\' is not found in this PMGPanel' % param
        if param not in self._param_changd_callbacks.keys():
            self._param_changd_callbacks[param] = [callback]
        else:
            self._param_changd_callbacks[param].append(callback)

    def on_param_changed(self, param):
        if param in self._param_changd_callbacks.keys():
            for callback in self._param_changd_callbacks[param]:
                callback(self.get_value())

    def set_debug_mode(self, debug: bool):
        """
        :param debug:将debug设置为True，即可进入debug模式。该模式下，PMGPanel会用醒目（但是很丑）的颜色显示出其上的不同控件，方便布局调整。
        :return:
        """
        if debug:
            self._initial_style_sheet = self.styleSheet()
            red = 100 + random.randint(0, 155)
            self.setStyleSheet(
                'PMGPanel{background-color:#%s0000;}QLabel{background-color:yellow;}BaseExtendedWidget{background-color:green;}' % hex(
                    red)[2:])
        else:
            self.setStyleSheet(self._initial_style_sheet)

    def emit_settings_changed_signal(self):
        """
        发出设置已改变的信号
        :return:
        """
        self.signal_settings_changed.emit(self.get_value())

    def on_settings_changed(self, name):
        self.signal_settings_changed.emit(self.get_value())
        self.on_param_changed(name)

    def add_widget(self, argument: Union[List, Tuple, Dict], layout: Union[QHBoxLayout, QVBoxLayout]) -> None:
        """
        创建控件，并且将其添加到控件字典中。
        :param argument:
        :return:
        """
        if isinstance(argument, str):
            layout.addWidget(QLabel(argument))
        elif isinstance(argument, (tuple, list)):
            name = argument[1]
            try:
                widget = views_dic[argument[0]](self.layout_dir, *argument[2:])
            except:
                import traceback
                traceback.print_exc()
                raise ValueError(repr(argument) + 'is invalid!')
            if self.widgets_dic.get(name) is None:
                self.widgets_dic[name] = widget
            widget.signal_param_changed.connect(self.on_settings_changed)
            widget.name = name
            layout.addWidget(widget)
        elif isinstance(argument, dict):
            widget_type = views_dic.get(argument['type'])
            assert widget_type is not None, repr(argument) + 'is of invalid widget type!!'
            name = argument['name']
            title = argument.get('title') if 'title' in argument.keys() else ''
            initial_value = argument.get('init')
            preserved_params = ['type', 'name', 'title', 'init']
            kwargs = {k: v for k, v in argument.items() if k not in preserved_params}
            widget = widget_type(self.layout_dir, title, initial_value, **kwargs)
            if self.widgets_dic.get(name) is None:
                self.widgets_dic[name] = widget
            widget.name = name
            widget.signal_param_changed.connect(self.on_settings_changed)
            layout.addWidget(widget)
            pass
        else:
            raise TypeError('Argument %s should be ')

    def _set_items(self, views: PANEL_VIEW_CLASS = None):
        """
        Clear all items on the panel and then add items from argument 'views'.
        Args:
            views:

        Returns:

        """
        if views is None:
            return
        self.widgets_dic: Dict[str, QWidget] = {}
        self.layout().setContentsMargins(0, 0, 0, 0)
        for v in views:
            if isinstance(v, dict):
                self.add_widget(v, self.layout())
            elif isinstance(v[0], str):
                self.add_widget(v, self.layout())

            elif isinstance(v[0], (list, tuple, dict)):
                sub_layout = None
                if self.layout_dir == 'v':
                    sub_layout = QHBoxLayout()
                    self.layout().addLayout(sub_layout)
                else:
                    sub_layout = QVBoxLayout()
                    self.layout().addLayout(sub_layout)
                for subv in v:
                    self.add_widget(subv, sub_layout)
                if self.with_aux_spacer:
                    if self.layout_dir == 'h':
                        sub_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
                    else:
                        sub_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        if self.with_spacer:
            if self.layout_dir == 'v':
                self.layout().addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            else:
                self.layout().addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    def set_items(self, items: PANEL_VIEW_CLASS = None):
        self.widgets_dic = {}
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            layout = self.layout().itemAt(i).layout()
            if widget is not None:
                widget.deleteLater()
            if layout is not None:
                for j in range(layout.count()):
                    widget = layout.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                layout.deleteLater()
        self._set_items(items)

    def get_ctrl(self, ctrl_name: str) -> 'BaseExtendedWidget':
        return self.widgets_dic.get(ctrl_name)

    def get_value(self):
        result = {}
        for k in self.widgets_dic:
            result[k] = self.widgets_dic[k].get_value()
        return result

    def get_value_with_filter(self, filter: str = 'enabled_and_visible'):
        assert filter in {'enabled', 'visible', 'enabled_and_visible'}
        result = {}
        for k in self.widgets_dic:
            widget = self.widgets_dic[k]
            if filter == 'enabled_and_visible' and widget.isEnabled() and widget.isVisible():
                result[k] = widget.get_value()
            elif (widget.isVisible() and filter == 'visible') or (widget.isEnabled() and filter == 'enabled'):
                result[k] = widget.get_value()
        return result

    def set_as_controller(self, controller_param: str, target_params: List[str],
                          trigger_value: [Any, Callable[[Any], bool]],
                          action='enable'):
        assert action in ['enable', 'disable', 'show', 'hide']
        assert isinstance(target_params, list)
        trigger_condition_func: Callable[[Any], bool] = None
        if not callable(trigger_value):
            trigger_condition_func = lambda obj: obj == trigger_value
        else:
            trigger_condition_func = trigger_value
        _condition_func = lambda params: trigger_condition_func(params[controller_param])
        for target_param in target_params:
            assert target_param in self.widgets_dic.keys(), 'Widget %s does not exist!, all widgets: %s' % (
                target_param, self.widgets_dic)

        if action == 'enable' or action == 'show':
            condition_func = lambda params: _condition_func(params)
        else:
            condition_func = lambda params: not _condition_func(params)

        def callback(params):
            for target_param in target_params:
                if action == 'enable' or action == 'disable':
                    self.get_ctrl(target_param).setEnabled(condition_func(params))
                else:
                    self.get_ctrl(target_param).setVisible(condition_func(params))

        self.set_param_changed_callback(controller_param, callback)
        callback(self.get_value())  # 设置时会被调用一次，以自动刷新界面。

    def set_value(self, values: Dict[str, Union[int, str, List, float, Tuple]]):
        """
        设置值。如果values中键对应的控件不存在，那么也不会报错，而是会忽略这一项。
        :param values:字典。如果values中键对应的控件不存在，那么也不会报错，而是会忽略这一项。
        :return:
        """
        for k in values.keys():
            w = self.widgets_dic.get(k)
            if w is not None:
                w.set_value(values[k])

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.deleteLater()
        self.signal_settings_changed.emit(self.get_value())


class PMGPanelDialog(QDialog):
    """
    一个对话框，直接弹出PMGPanel。
    TODO:要求如果有不合法的数值，就不可关闭。
    """

    def __init__(self, parent, views, with_spacer=False):
        super().__init__(parent)
        self.panel = PMGPanel(parent=self, views=views, with_spacer=with_spacer)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.panel)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)
        self.changes_accepted = False

    def get_value(self) -> Dict[str, Any]:
        return self.panel.get_value()

    def set_value(self, values: Dict[str, Any]) -> None:
        self.panel.set_value(values)

    def accept(self):
        if self.verify(self.get_value()):
            self.changes_accepted = True
            super().accept()

    def verify(self, values) -> bool:
        return True


def is_standard_widget_name(widget_name: str) -> bool:
    """
    返回字符串是否对应一个标准化的PMGPanel控件。
    :return:
    """
    return views_dic.get(widget_name) is not None


def parse_simplified_pmgjson(identifier, data, params) -> Optional[List[Union[int, str]]]:
    """
    解析简化版的json数据！
    :param identifier:
    :param data:
    :param params:
    :return:
    """
    if len(params) > 0:
        if is_standard_widget_name(params[0]):
            return [params[0], identifier, 'Input Value', data] + params[1:]

    if isinstance(data, bool):
        return ['check_ctrl', identifier, 'Input Bool', data]

    elif isinstance(data, (int, float)):

        return ['numberspin_ctrl', identifier, 'Input Value', data] + params

    elif isinstance(data, str):
        return ['line_ctrl', identifier, 'Input String', data]


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # 类型；名称；显示的提示文字;初始值；//单位；范围
    views1 = [('line_ctrl', 'name', 'What\'s your name?', 'hzy'),
              {'type': 'line_ctrl', 'name': 'your_name', 'title': 'what is your name?', 'init': 'hzy'},
              ('password_ctrl', 'password', 'What\'s your password?', '123456'),
              ('file_ctrl', 'file_dir', 'File Name', '/home/hzy/Desktop/123.txt'),
              # ('editor_ctrl', 'code', 'Input Python Code', 'print(123)', 'sql'),
              ('number_ctrl', 'age', 'How old are you?', 88, 'years old', (0, 150)),
              ('number_ctrl', 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
              ('check_ctrl', 'sport', 'do you like sport', True),
              ('numberspin_ctrl', 'eyesight', '视力', 4.0, '度', (3.0, 5.5), 0.1),
              ('numberspin_ctrl', 'apple_num', '苹果数量', 4, '个', (0, 10), 1), ]
    views2 = [('combo_ctrl', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
               ['f22战斗机', 'f18战斗轰炸机', 'j20战斗机', 'su57战斗机']),
              ('color_ctrl', 'color', 'Which color do u like?', (0, 200, 0)),
              ('list_ctrl', 'inputs', 'Set Inputs', [['1', '2', '3'], ['#1', '#2', '#3']], lambda: str(123)),
              ('list_ctrl', 'inputs_2', 'Set Inputs', [[None, None, None], ['##1', '##2', '##3'], ], lambda: None),
              ('date_ctrl', 'date', '设置时间', (1970, 7, 21)),
              [
                  ('eval_ctrl', 'code_eval', 'Evaluate this code', 123 + 456, 'normal'),
                  ('eval_ctrl', 'code_eval2', 'Evaluate this code', (1, 2, 3), 'safe')
              ],
              # ('keymap_ctrl', 'key_map2', 'Key For Find', 'Ctrl+F'),
              ]
    sp = PMGPanel(views=views1, layout_dir='v')
    sp.set_items(views1)
    sp.signal_settings_changed.connect(lambda settings: print('views1-settings', settings))
    # sp.show()

    sp2 = PMGPanel(views=views2, layout_dir='v')
    sp2.signal_settings_changed.connect(lambda settings: print('views2-settings', settings))
    sp2.set_items(views2)
    # sp2.show()

    import random

    views3 = \
        [
            # {'type': 'timeseries_show',
            #  'name': 'cpu_occupation',
            #  'title': 'CPU占用',
            #  'init': {'timestamps': [i + 1 for i in range(10)],
            #           'line1': {'tag': 'CPU利用率1',
            #                     'data': [random.randint(0, 100) for i in
            #                              range(10)]},
            #           'line2': {'tag': 'CPU利用率2',
            #                     'data': [random.randint(0, 100) for i in
            #                              range(10)]}
            #           },
            #  'y_range': (0, 100),
            #  'xlabel': '时间',
            #  'ylabel': '占用率',
            #  'threshold_range': (0, 78),
            #  'legend_face_color': "#00ff00"
            #  },
            ("vars_combo_ctrl", "variables", "选择变量", ""),
            ("multitype_ctrl", "multiple_types", "多种类型", [[None, None, None], ['诶诶诶', '嗷嗷喊', 'qq']], [{
                "type_title": "字符串列表",
                "ctrls": [
                    ("list_ctrl", "list_ctrl", 'input list of strings', [[None, None, None], ['##1', '##2', '##3']],
                     lambda: None),
                ],
                "on_ok": lambda values: values["list_ctrl"][1]},
                {
                    "type_title": "字符串",
                    "ctrls": [
                        ("line_ctrl", "aaaa", 'input a string', "Please input a string"),
                    ],
                    "on_ok": None
                }
            ])
        ]
    sp3 = PMGPanel(views=views3, layout_dir='v')
    sp3.signal_settings_changed.connect(lambda settings: print('views2-settings', settings))
    sp3.set_items(views3)
    sp3.show()

    sys.exit(app.exec_())
