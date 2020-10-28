import os
import string
import sys
import time
from typing import List, Dict, Tuple, Union, Callable

from PyQt5.QtCore import pyqtSignal, Qt, QDate, QCalendar
from PyQt5.QtGui import QCloseEvent, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QApplication, \
    QColorDialog, QRadioButton, QCheckBox, QComboBox, QSpacerItem, QSizePolicy, QSpinBox, QDoubleSpinBox, QListWidget, \
    QDateEdit, QFileDialog, QDialog, QMessageBox
from PyQt5.Qsci import QsciScintilla, QsciLexerPython


class BaseParamWidget(QWidget):
    """
    基础参数控件的类型。所有的参数控件都在其上派生而来。
    """
    signal_param_changed = pyqtSignal()

    def __init__(self, layout_dir='v'):
        super(BaseParamWidget, self).__init__()
        if layout_dir == 'v':
            self.central_layout = QVBoxLayout()
        else:
            self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.on_para_change = None
        self.__app = None  # SciApp。初始化控件的时候指定，并且在调用set_app的时候传入。

    def para_changed(self):
        if (self.on_para_change is not None) and (self.__app is not None):
            self.on_para_change(self.__app)

    def set_app(self, app):
        self.__app = app

    def is_key(self, event, type=''):
        """
        'dir':判断方向键
        'alpha':判断是否为26个字母
        'hex':判断是否为十六进制数字或者字母
        'digit':判断是否为数字0~9
        'valid':包含数字、字母或者退格键。
        """

        type = type.lower()
        if type == '':
            return True
        elif type.startswith('dir'):
            return event.keysym.lower() in ('left', 'right', 'up', 'down')
        elif type.startswith('alpha'):
            return event.keysym in string.ascii_lowercase
        elif type.startswith('hex'):
            return event.keysym in string.hexdigits
        elif type.startswith(('digit')):
            return event.keysym in string.digits

    def set_value(self, value: object):
        pass

    def get_value(self):
        pass

    def set_params(self, *args, **kwargs):
        pass


class NumCtrl(BaseParamWidget):
    """NumCtrl: derived from tk.Entry
    用于输入数值。
    """

    def __init__(self, layout_dir: str, title: str, initial_value: int, unit: str, rang: tuple):
        super().__init__(layout_dir=layout_dir)
        self.on_check_callback = None

        self.prefix = QLabel(text=title)
        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)

        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)
        self.ctrl.textChanged.connect(self.signal_param_changed)

        self.postfix = QLabel(text=unit)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.postfix)

        self.min, self.max = rang
        self.accury = initial_value
        self.set_value(initial_value)

    def Bind(self, z, f):
        self.f = f

    def ontext(self, event):
        self.f(self)
        if self.get_value() is None:
            self.ctrl.setStyleSheet("background-color:#ff0000;")
        else:

            self.ctrl.setStyleSheet("background-color:#ffffff;")
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, n):
        self.ctrl.clear()
        self.ctrl.setText(str(n))

    def get_value(self):
        sval = self.ctrl.text()
        try:
            num = float(sval)
        except ValueError:
            import traceback
            traceback.print_exc()
            return None
        if num < self.min or num > self.max:
            return None
        return num

    def f(self, e):
        pass

    def Refresh(self):
        pass


class SpinCtrl(BaseParamWidget):
    """
    利用spinbox的控制面板，当最大值、最小值、初始值和步长均为整数的时候，类型为整数；、反之只要有任意一个是float，
    类型就是浮点数了。
    """

    def __init__(self, layout_dir: str, title: str, initial_value: Union[int, float], unit: str,
                 val_range: Tuple[Union[float, int], Union[float, int]],
                 step: int = 1):
        super().__init__(layout_dir)
        self.on_check_callback = None

        self.prefix = QLabel(text=title)
        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)
        self.min, self.max = val_range
        self.step = step
        if isinstance(self.min, int) and isinstance(self.max, int) and isinstance(self.step, int) \
                and isinstance(initial_value, int):
            self.ctrl = QSpinBox()
        else:
            self.ctrl = QDoubleSpinBox()
        # self.ctrl.valueChanged.connect(self.signal_param_changed.emit)
        # self.ctrl.valueChanged.connect(lambda :print('123123123'))
        self.postfix = QLabel(text=unit)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.postfix)

        self.ctrl.setMinimum(self.min)
        self.ctrl.setMaximum(self.max)
        self.ctrl.setSingleStep(step)
        self.accury = initial_value
        self.set_value(initial_value)

    def set_value(self, value: Union[float, int]) -> None:
        self.ctrl.setValue(value)

    def get_value(self) -> Union[int, float]:
        return self.ctrl.value()


class TextCtrl(BaseParamWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.on_check_callback = None

        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)
        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)
        # self.ctrl.textChanged.connect(self.signal_param_changed.emit)
        # self.postfix = lab_unit = QLabel(text=unit)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)
        # entryLayout.addWidget(self.postfix)

    def param_changed(self, event):
        pass

    # ! TODO: what is this?
    def Bind(self, z, f):
        self.f = f

    def ontext(self, event):
        self.para_changed()

    def set_value(self, text: str):
        self.ctrl.clear()
        self.ctrl.setText(text)

    def get_value(self) -> str:
        return self.ctrl.text()


class ColorCtrl(BaseParamWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.on_check_callback = None
        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.oncolor)

        # self.postfix = lab_unit = QLabel(text=unit)
        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.color_button)
        # entryLayout.addWidget(self.postfix)
        self.set_value(initial_value)

    def Bind(self, z, f):
        self.f = f

    def ontext(self, event):
        if self.get_value() is None:
            self.color_button.setStyleSheet("background-color:#ff0000;")
            self.ctrl.setStyleSheet("background-color:#ff0000;")
        else:
            self.ctrl.setStyleSheet('background-color:#ffffff;')
            self.color_button.setStyleSheet("background-color:%s;" % self.colorTup2Str(self.get_value()))
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def oncolor(self, event):
        color = QColorDialog.getColor(initial=QColor(*self.get_value()))
        self.set_value(self.colorStr2Tup(color.name()))
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, color: Tuple = None):
        if color is None:
            color = (255, 255, 255)
        strcolor = self.colorTup2Str(color)
        self.color_button.setStyleSheet('background-color:%s;' % strcolor)
        self.ctrl.clear()
        self.ctrl.setText(strcolor)

    def get_value(self):
        rgb = self.ctrl.text().strip()
        if len(rgb) != 7 or rgb[0] != '#':
            return None
        try:
            int(rgb[1:], 16)
        except:
            import traceback
            traceback.print_exc()
            return None
        return self.colorStr2Tup(rgb)

    def colorStr2Tup(self, value: str) -> tuple:  # pos或者wh的输入都是tuple
        def convert(c):
            v = ord(c)
            if (48 <= v <= 57):
                return v - 48
            else:
                return v - 87  # 返回a的值。

        value = value.lower()
        c0 = convert(value[1])
        c1 = convert(value[2])
        c2 = convert(value[3])
        c3 = convert(value[4])
        c4 = convert(value[5])
        c5 = convert(value[6])
        a1 = c0 * 16 + c1
        a2 = c2 * 16 + c3
        a3 = c4 * 16 + c5
        return (a1, a2, a3)

    def colorTup2Str(self, value: tuple) -> str:
        if value is None:
            return None
        strcolor = '#'
        for i in value:
            strcolor += hex(int(i))[-2:].replace('x', '0')
        return strcolor


class FilePathCtrl(BaseParamWidget):
    def __init__(self, layout_dir: str, title, initial_value: str = '', filt=None):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QLineEdit()
        print(initial_value)
        self.ctrl.setText(initial_value)
        path_layout.addWidget(self.ctrl)
        self.file_choose_button = QPushButton('..')
        self.file_choose_button.clicked.connect(self.select_file)
        path_layout.addWidget(self.file_choose_button)
        self.central_layout.addLayout(path_layout)

    def select_file(self):
        name, ext = QFileDialog.getOpenFileName(self, self.tr("Select File"),
                                                os.path.dirname(self.get_value()),  # 起始路径
                                                "All Files (*);;Text Files (*.txt)")
        if name != '':
            self.ctrl.setText(name)

    def ontext(self, event):
        self.para_changed()

    def set_value(self, value: str):
        self.ctrl.setText(value)

    def get_value(self) -> str:
        return self.ctrl.text()


class DateCtrl(BaseParamWidget):
    def __init__(self, layout_dir: str, title, initial_date):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QDateEdit()
        path_layout.addWidget(self.ctrl)

        calendar_widget = QCalendar()
        self.ctrl.setCalendar(calendar_widget)

        self.central_layout.addLayout(path_layout)
        self.set_value(initial_date)

    def set_value(self, value: Union[Tuple[int, int, int], float, int]):
        if isinstance(value, tuple):
            assert len(value) == 3
            date = QDate(*value)
        elif isinstance(value, (float, int)):
            loc_time = time.localtime(value)
            print(loc_time)
            date = QDate(loc_time.tm_year, loc_time.tm_mon, loc_time.tm_mday)
        else:
            raise ValueError("value is not allowed", value)
        self.ctrl.setDate(date)

    def get_value(self) -> float:
        """
        计算值
        :return:
        """
        return time.mktime(self.ctrl.date().toPyDate().timetuple())


class Choice(BaseParamWidget):
    def __init__(self, layout_dir: str, choices, tp, title, unit):
        super().__init__(layout_dir)
        self.tp, self.choices = tp, choices
        self.on_check_callback = None

        self.prefix = QLabel(self, text=title)
        self.central_layout.addWidget(self.prefix)
        self.radio_buttons: List['QRadioButton'] = []
        for i, choice in enumerate(self.choices):
            b = QRadioButton(text=str(choice))
            b.toggled.connect(self.on_radio_button_toggled)
            self.radio_buttons.append(b)
            self.central_layout.addWidget(b)

        self.postfix = QLabel(text=unit)
        self.central_layout.addWidget(self.postfix)

    def on_radio_button_toggled(self):
        sender: QRadioButton = self.sender()
        if sender.isChecked():
            # index = self.radio_buttons.index(sender)
            pass

    def on_choice(self, event=None):
        # attention : button command will not transfer any event as args .
        # 注意：按钮本身并不会传递event作为参数，与键鼠的event不同。
        self.f(self)
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, x):
        for i, choice in enumerate(self.choices):
            if x == choice:
                self.radio_buttons[i].setChecked(True)
            else:
                self.radio_buttons[i].setChecked(False)

    def get_value(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return self.choices[i]


class Check(BaseParamWidget):
    """
    bool, 'sport', 'do you like sport',True
    """

    def __init__(self, layout_dir: str, title: str, initial_value: bool):
        super().__init__(layout_dir)
        QLabel(text=title)
        layout = QHBoxLayout()
        self.on_check_callback = None
        check = QCheckBox(text=title)
        check.clicked.connect(self.on_check)
        layout.addWidget(check)
        self.check = check
        self.central_layout.addLayout(layout)
        self.set_value(initial_value)

    def get_value(self):
        return self.check.isChecked()

    def set_value(self, value: bool):
        self.check.setChecked(value)

    def on_check(self):
        pass


class TextEdit(BaseParamWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str = '', lexer=''):
        super().__init__(layout_dir)
        self.on_check_callback = None

        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)
        self.ctrl = QsciScintilla()
        if lexer == 'python':
            self.ctrl.setLexer(QsciLexerPython())
        self.ctrl.setText(initial_value)
        # self.ctrl.textChanged.connect(self.ontext)

        # self.postfix = lab_unit = QLabel(text=unit)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)
        # entryLayout.addWidget(self.postfix)

    def get_value(self):
        return self.ctrl.text()

    def set_value(self, value: str):
        self.ctrl.setText(value)


class ListEntry(BaseParamWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: List[List[str]], new_id_func: Callable):
        super().__init__(layout_dir)
        self.choices = []
        self.text_list = []
        lab_title = QLabel(text=title)
        layout = QHBoxLayout()
        self.central_layout.addWidget(lab_title)
        self.on_check_callback = None
        self.list_widget = QListWidget()
        self.set_value(initial_value)
        layout_tools = QVBoxLayout()
        self.button_add_item = QPushButton('+')
        self.button_delete_item = QPushButton('-')
        self.button_delete_item.clicked.connect(self.delete_row)
        self.button_add_item.clicked.connect(self.add_row)
        self.button_add_item.setMaximumWidth(20)
        self.button_delete_item.setMaximumWidth(20)
        layout_tools.addWidget(self.button_add_item)
        layout_tools.addWidget(self.button_delete_item)
        layout.addLayout(layout_tools)
        layout.addWidget(self.list_widget)
        self.central_layout.addLayout(layout)
        self.data = initial_value
        self.new_id_func = new_id_func

    def new_id(self):
        if callable(self.new_id_func):
            return self.new_id_func()
        else:
            return None

    def add_row(self):
        self.data[0].append(self.new_id())
        self.data[1].append('Unnamed')
        self.set_value(self.data)

    def delete_row(self):
        # item = self.list_widget.currentItem()
        index = self.list_widget.currentIndex().row()
        self.data[0].pop(index)
        self.data[1].pop(index)
        self.set_value(self.data)

    def on_listwidget_double_cicked(self):
        print('edit')
        item = self.list_widget.currentItem()
        self.list_widget.editItem(item)

    def get_value(self):
        text = []
        for i in range(self.list_widget.count()):
            text.append(self.list_widget.item(i).text())
        self.data[1] = text
        return self.data

    def set_value(self, data: List[List[str]]):
        self.list_widget.clear()
        self.list_widget.addItems(data[1])
        self.data = data
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEditable)


class ChoiceBoxCtrl(BaseParamWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: object, choices: list, texts=None):

        super().__init__(layout_dir)
        self.choices = []
        self.text_list = []

        lab_title = QLabel(text=title)
        # layout_v = QVBoxLayout()
        layout = QHBoxLayout()
        self.central_layout.addWidget(lab_title)
        # layout_v.addLayout(layout)
        self.on_check_callback = None
        check = QComboBox()

        check.currentIndexChanged.connect(self.on_value_changed)

        layout.addWidget(check)
        self.central_layout.addLayout(layout)
        self.check = check
        # self.central_layout.addLayout(layout_v)
        self.set_choices(choices, texts)
        self.set_value(initial_value)

    def set_choices(self, choices: list, texts: list = None):
        self.check.clear()
        self.choices = choices
        self.text_list = []
        if texts is None:
            for choice in choices:
                self.text_list.append(str(choice))
        else:
            if len(texts) != len(choices):
                raise Exception('Length of argument \'choices\'(len=%d) and \'texts\'(len=%d) are not same!' %
                                (len(choices), len(texts)))
            else:
                self.text_list = texts
        self.check.addItems(self.text_list)

    def on_value_changed(self):
        pass

    def set_value(self, value: object):
        index = self.choices.index(value)
        self.check.setCurrentIndex(index)

    def get_value(self):
        return self.choices[self.check.currentIndex()]


class EvalInput(BaseParamWidget):
    """
    type:
    safe--can only input ',[](){}:1234567890.'
    """

    def __init__(self, layout_dir: str, title: str, initial_value: str,type='normal'):
        super().__init__(layout_dir)
        self.allowed_chars = set(',[](){}:1234567890.+-*/')
        self.on_check_callback = None
        self.prefix = QLabel(text=title)
        self.type = type
        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()
        # self.ctrl.textChanged.connect(self.ontext)

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.on_eval_test)

        # self.postfix = lab_unit = QLabel(text=unit)
        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.color_button)
        # entryLayout.addWidget(self.postfix)
        self.set_value(initial_value)

    def get_code(self) -> str:
        text = self.ctrl.text()
        if self.type=='safe':
            for char in text:
                if char not in self.allowed_chars:
                    return None
        return text

    def set_value(self, obj:object):
        try:
            # eval(code)
            self.ctrl.setText(repr(obj))
        except:
            import traceback
            traceback.print_exc()

    def get_value(self) -> object:
        if self.get_code() is not None:
            try:
                return eval(self.ctrl.text())
            except:
                import traceback
                traceback.print_exc()
                return None
        else:
            return None

    def on_eval_test(self):
        val = self.get_value()
        print(val)
        dlg = QMessageBox.information(self,self.tr('Result'),repr(val),QMessageBox.Ok)


views_dic = {str: TextCtrl, int: NumCtrl, float: NumCtrl, bool: Check, list: Choice}
views_dic.update({'choose_box': ChoiceBoxCtrl, 'color': ColorCtrl, 'number': NumCtrl
                     , 'line_edit': TextCtrl, 'bool': Check, 'spin_box': SpinCtrl, 'entry_list': ListEntry,
                  'text_edit': TextEdit, 'datetime': DateCtrl, 'file': FilePathCtrl,'eval':EvalInput})


class SettingsPanel(QWidget):
    widgets_dic: Dict[str, BaseParamWidget] = {}
    signal_settings_changed = pyqtSignal(dict)

    # signal_settings_modified = pyqtSignal(dict)
    def __init__(self, parent=None, views: List[Tuple] = None, layout_dir: str = 'v'):
        super(SettingsPanel, self).__init__(parent)
        self.layout_dir = layout_dir
        if layout_dir == 'v':
            self.setLayout(QVBoxLayout())
        else:
            self.setLayout(QHBoxLayout())

        self.set_items(views)

    def on_settings_changed(self):
        self.signal_settings_changed.emit(self.get_value())

    def _set_items(self, views: List[Tuple[str]] = None):
        if views is None:
            return
        self.widgets_dic: Dict[str, QWidget] = {}
        self.layout().setContentsMargins(0, 0, 0, 0)
        for v in views:
            if isinstance(v, tuple):
                name = v[1]
                widget = views_dic[v[0]](self.layout_dir, *v[2:])
                if self.widgets_dic.get(name) is None:
                    self.widgets_dic[name] = widget
                self.layout().addWidget(widget)
                widget.signal_param_changed.connect(self.on_settings_changed)

            elif isinstance(v, list):
                sub_layout = None
                if self.layout_dir == 'v':
                    sub_layout = QHBoxLayout()
                    self.layout().addLayout(sub_layout)
                else:
                    sub_layout = QVBoxLayout()
                    self.layout().addLayout(sub_layout)
                for subv in v:
                    name = subv[1]
                    widget = views_dic[subv[0]](self.layout_dir, *subv[2:])
                    if self.widgets_dic.get(name) is None:
                        self.widgets_dic[name] = widget
                    sub_layout.addWidget(widget)
                    # if self.force_spacing == True:
                    #     self.layout().addWidget(QLabel(' '))
                if self.layout_dir == 'h':
                    sub_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
                else:
                    sub_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout().addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def set_items(self, items: List[Tuple] = None):
        self.widgets_dic = {}
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i).widget()
            if item is not None:
                item.deleteLater()
        self._set_items(items)

    def get_ctrl(self, ctrl_name: str) -> 'BaseParamWidget':
        return self.widgets_dic.get(ctrl_name)

    def get_value(self):
        result = {}
        for k in self.widgets_dic:
            result[k] = self.widgets_dic[k].get_value()
        return result

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.deleteLater()
        self.signal_settings_changed.emit(self.get_value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 类型；名称；显示的提示文字;初始值；//单位；范围
    views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),

             ('file', 'file_dir', 'File Name', '/home/hzy/Desktop/123.txt'),
             ('text_edit', 'code', 'Input Python Code', 'print(123)', 'python'),
             ('number', 'age', 'How old are you?', 88, 'years old', (0, 150)),
             ('number', 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
             ('bool', 'sport', 'do you like sport', True),
             ('spin_box', 'eyesight', '视力', 4.0, '度', (3.0, 5.5), 0.1),
             ('spin_box', 'apple_num', '苹果数量', 4, '个', (0, 10), 1),
             # ('choose_box', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
             #  ['f22战斗机', 'f18战斗轰炸机', 'j20战斗机', 'su57战斗机']),
             # ('color', 'color', 'Which color do u like?', (0, 200, 0)),
             # ('entry_list', 'inputs', 'Set Inputs', [['1', '2', '3'], ['#1', '#2', '#3']], lambda: str(123)),
             # ('entry_list', 'inputs_2', 'Set Inputs', [[None, None, None], ['##1', '##2', '##3'], ], lambda: None),
             # ('datetime', 'time', '设置时间', (1972, 1, 2)),
             ('eval', 'code_eval', 'Evaluate this code', 123+456,'normal'),
             ('eval', 'code_eval', 'Evaluate this code', (1,2,3),'safe'),
             ]
    sp = SettingsPanel(views=views, layout_dir='v')
    # sp.widgets_dic['plane_type'].set_choices(['aaa', 'vvvvv', 'xxxxxx'])
    sp.set_items(views)
    sp.show()
    # sp2 = SettingsPanel(views=views, layout_dir='h')
    # sp2.show()
    # sp2.setMaximumHeight(30)
    val = sp.get_value()  # 返回一个字典。初始值为表格的第二列：第四列。
    print(val)
    sp.signal_settings_changed.connect(lambda x: print(x))
    # root.mainloop()
    sys.exit(app.exec_())
