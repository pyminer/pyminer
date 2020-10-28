from typing import List, Dict, Tuple

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QApplication, \
    QColorDialog, QRadioButton, QCheckBox, QComboBox
import warnings
import time
import string
import sys


class BaseParamWidget(QWidget):
    """
    基础参数控件的类型。所有的参数控件都在其上派生而来。
    """

    def __init__(self):
        super().__init__()
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)
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

    def set_value(self):
        pass

    def get_value(self):
        pass


class NumCtrl(BaseParamWidget):
    """NumCtrl: derived from tk.Entry
    用于输入数值。
    """

    # (int, 'age', 'How old are you?', 88, 'years old', (0, 150)),
    def __init__(self, title: str, initial_value: int, unit: str, rang: tuple):
        super().__init__()
        self.on_check_callback = None

        self.prefix = lab_title = QLabel(text=title)
        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)

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
        if self.get_value() == None:
            self.ctrl.setStyleSheet("background-color:#ff0000;")
        else:

            self.ctrl.setStyleSheet("background-color:#ffffff;")
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, n):
        self.ctrl.clear()
        self.ctrl.setText(str(round(n, self.accury) if self.accury > 0 else int(n)))

    def get_value(self):
        sval = self.ctrl.text()
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            import traceback
            traceback.print_exc()
            return None
        if num < self.min or num > self.max:
            return None
        if abs(round(num, self.accury) - num) > 10 ** -(self.accury + 5):  # 这么写才比较严谨吧
            return None
        return num

    def f(self, e):
        pass

    def Refresh(self):
        pass


class TextCtrl(BaseParamWidget):
    def __init__(self, title: str, initial_value: str):
        super().__init__()
        self.on_check_callback = None

        self.prefix = lab_title = QLabel(text=title)

        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)

        # self.postfix = lab_unit = QLabel(text=unit)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)
        # entryLayout.addWidget(self.postfix)

    def param_changed(self, event):
        pass

    # ! TODO: what is this?
    def Bind(self, z, f): self.f = f

    def ontext(self, event):
        self.para_changed()

    def set_value(self, text: str):
        self.ctrl.clear()
        self.ctrl.setText(text)

    def get_value(self) -> str:
        return self.ctrl.text()


class ColorCtrl(BaseParamWidget):
    def __init__(self, title: str, initial_value: str):
        super().__init__()
        self.on_check_callback = None
        self.prefix = lab_title = QLabel(text=title)

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
        if self.get_value() == None:
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
        rst = None
        val = self.get_value()
        color = self.colorTup2Str(self.get_value())
        if color is None:
            color = '#ffffff'
        color = QColorDialog.getColor()  # colorchooser.askcolor(color)  # wx.ColourDialog(self)
        self.set_value(self.colorStr2Tup(color.name()))
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, color):
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


class PathCtrl(BaseParamWidget):
    def __init__(self, parent, title, filt):
        super().__init__(parent)
        self.prefix = lab_title = QLabel(text=title)
        # self.prefix.pack(fill=tk.X, expand=1)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        # entryFrame = ttk.Frame(self)
        self.ctrl = QLineEdit()  # tk.Entry(entryFrame)
        # self.ctrl.bind('<KeyRelease>', self.ontext)
        # self.ctrl.bind('<ButtonPress-1>', self.onselect)
        path_layout.addWidget(self.ctrl)
        # self.ctrl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # entryFrame.pack(expand=1, fill=tk.X)
        self.file_choose_button = QPushButton('..')
        path_layout.addWidget(self.file_choose_button)
        self.central_layout.addLayout(path_layout)

    def ontext(self, event):
        self.para_changed()

    def onselect(self, event):
        # [TODO]:对应的这个函数是啥意思？一定要注意一下！
        pass

    def set_value(self, value: str):
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, value)

    def get_value(self) -> str:
        return self.ctrl.get()


class Choice(BaseParamWidget):
    def __init__(self, choices, tp, title, unit):
        super().__init__()
        self.tp, self.choices = tp, choices
        self.on_check_callback = None

        self.prefix = lab_title = QLabel(self, text=title)
        self.central_layout.addWidget(self.prefix)
        self.radio_buttons: List['QRadioButton'] = []
        for i, choice in enumerate(self.choices):
            b = QRadioButton(text=str(choice))
            b.toggled.connect(self.on_radio_button_toggled)
            self.radio_buttons.append(b)
            self.central_layout.addWidget(b)

        self.postfix = lab_unit = QLabel(text=unit)
        self.central_layout.addWidget(self.postfix)

    def on_radio_button_toggled(self):
        sender: QRadioButton = self.sender()
        if sender.isChecked():
            index = self.radio_buttons.index(sender)

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


class AnyType(BaseParamWidget):
    def __init__(self, parent, title, types=['Int', 'Float', 'Str']):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.TAB_TRAVERSAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prefix = lab_title = wx.StaticText(self, wx.ID_ANY, title,
                                                wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap(-1)
        sizer.Add(lab_title, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.txt_value = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.txt_value, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        com_typeChoices = types
        self.postfix = self.com_type = wx.ComboBox(self, wx.ID_ANY, 'Float', wx.DefaultPosition, wx.DefaultSize,
                                                   com_typeChoices, 0)
        sizer.Add(self.com_type, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        # Connect Events
        self.txt_value.Bind(wx.EVT_KEY_UP, self.on_text)
        self.com_type.Bind(wx.EVT_COMBOBOX, self.on_type)

    def Bind(self, z, f):
        self.f = f

    def set_value(self, v):
        self.txt_value.set_value(str(v))
        if isinstance(v, int):
            self.com_type.Select(0)
        if isinstance(v, float):
            self.com_type.Select(1)
        else:
            self.com_type.Select(2)

    def get_value(self):
        tp = self.com_type.get_value()
        sval = wx.TextCtrl.get_value(self.txt_value)
        if tp == 'Float':
            try:
                num = float(sval)
            except ValueError:
                return None
        if tp == 'Int':
            try:
                num = int(sval)
            except ValueError:
                return None
        if tp == 'Str':
            try:
                num = str(sval)
            except ValueError:
                return None
        return num

    # Virtual event handlers, overide them in your derived class
    def on_text(self, event):
        self.f(self)
        if self.get_value() == None:
            self.txt_value.SetBackgroundColour((255, 255, 0))
        else:
            self.txt_value.SetBackgroundColour((255, 255, 255))
        self.Refresh()

    def on_type(self, event):
        if self.get_value() == None:
            self.txt_value.SetBackgroundColour((255, 255, 0))
        else:
            self.txt_value.SetBackgroundColour((255, 255, 255))
        self.Refresh()


class Choices(BaseParamWidget):
    def __init__(self, parent, choices, title):
        self.choices = list(choices)
        super().__init__(parent)

        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(anchor=tk.W)

        self.boolVarList = [tk.BooleanVar() for i in range(len(self.choices))]
        # print(self.boolVarList)
        self.on_check_callback = None
        for i, choice in enumerate(self.choices):
            b = ttk.Checkbutton(self, text=str(choice),
                                variable=self.boolVarList[i], command=self.on_check)
            b.pack(anchor=tk.W)

    def Bind(self, z, f):
        self.f = f

    def on_check(self):
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def get_value(self):
        l = []
        for i, bv in enumerate(self.boolVarList):
            if bv.get() == True:
                l.append(self.choices[i])
        return l

    def set_value(self, value: list):
        for bv in self.boolVarList: bv.set(False)
        for i, v in enumerate(value):
            n = self.choices.index(v) if v in self.choices else -1  # -1 stands for input error
            if n != -1:
                self.boolVarList[n].set(True)
            else:
                warnings.warn('Index item \'%s\' is not in choices list : %s' %
                              (v, repr(self.choices)))


class FloatSlider(BaseParamWidget):
    def __init__(self, parent, rang, accury, title, unit=''):
        super().__init__(parent)
        self.accury = accury
        self.on_check_callback = None

        self.lab_title = ttk.Label(self, text=title)
        self.lab_title.pack(anchor=tk.W)

        self.slider = ttk.Scale(self, from_=rang[0], to=rang[1], orient=tk.HORIZONTAL, command=self.on_scroll)
        self.slider.pack(expand=1, fill=tk.X)
        self.spinboxFrame = ttk.Frame(self)

        self.lab_min = ttk.Label(self.spinboxFrame)
        self.lab_min.pack(side=tk.LEFT)

        self.spinvar = tk.StringVar()
        self.spin = tk.Spinbox(self.spinboxFrame, from_=rang[0], to=rang[1], increment=10 ** -accury, format='%10.4f',
                               command=self.on_spin, textvariable=self.spinvar)
        self.spin.bind('<KeyRelease>', self.on_text)

        self.spin.pack(side=tk.LEFT)
        self.spinboxFrame.pack(expand=1, fill=tk.BOTH, pady=(3, 0))

        self.lab_max = ttk.Label(self.spinboxFrame)
        self.lab_max.pack(side=tk.LEFT)

        self.lab_unit = ttk.Label(self.spinboxFrame, text=unit)
        self.lab_unit.pack(side=tk.LEFT)

        self.set_para(rang, accury)

    def Bind(self, z, f):
        self.f = f

    def set_para(self, rang, accury):
        self.min = round(rang[0], accury)
        self.max = round(rang[1], accury)
        self.lab_min.config(text=str(round(rang[0], accury)))
        self.lab_max.config(text=str(round(rang[1], accury)))
        self.accury = accury

    def on_scroll(self, event):
        """
        只有这个方法会调用回调函数。原因：当用户通过拖动滚动条进行操作的时候，输入的值一定是合理的，无需进行判断；
        当用户通过按spinbox或者是对spinbox输入文本的时候，只有文本符合规定的时候会对slider设置值，此时会调用这个方法。
        这样总能调用到这个回调函数。
        """
        value = self.slider.get()
        self.spinvar.set(round(value, self.accury))
        self.spin.config(bg='#ffffff')
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def on_spin(self):

        self.slider.set(self.spin.get())
        if callable(self.on_check_callback):
            self.on_check_callback()

    def on_text(self, event):
        if self.is_key(event, 'dir'):
            return
        if self.get_value() == None:
            self.spin.config(bg="#ffff00")
        else:
            self.spin.config(bg="#ffffff")
            self.set_value(self.get_value())

    def set_value(self, n):
        self.slider.set(n)
        self.spinvar.set(round(n, self.accury))

    def get_value(self):
        sval = self.spinvar.get()
        try:
            val = float(sval) if self.accury > 0 else int(float(sval))
            if self.min <= val <= self.max:
                return val
            else:
                return None
        except Exception as e:
            import traceback
            traceback.print_exc()


class Label(BaseParamWidget):
    def __init__(self, parent, title):
        super().__init__(parent)
        lab_title = ttk.Label(self, text=title)
        lab_title.pack(anchor=tk.W)

    def Bind(self, z, f): pass

    def set_value(self, v): pass

    def get_value(self, v): pass


class Check(BaseParamWidget):
    """
    bool, 'sport', 'do you like sport',True
    """

    def __init__(self, title: str, initial_value: bool):
        super().__init__()
        lab_title = QLabel(text=title)
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


class ChoiceBoxCtrl(BaseParamWidget):
    def __init__(self, title: str, initial_value: object, choices: list,texts = None):

        super().__init__()
        self.text_list = []
        self.choices = choices
        if texts is None:
            for choice in choices:
                self.text_list.append(str(choice))
        else:
            if len(texts)!=len(choices):
                raise Exception('Length of argument \'choices\'(len=%d) and \'texts\'(len=%d) are not same!'%
                                (len(choices),len(texts)))
            else:
                self.text_list = texts
        lab_title = QLabel(text=title)
        layout_v = QVBoxLayout()
        layout = QHBoxLayout()
        layout_v.addWidget(lab_title)
        layout_v.addLayout(layout)
        self.on_check_callback = None
        check = QComboBox()

        check.addItems(self.text_list)
        check.currentIndexChanged.connect(self.on_value_changed)
        layout.addWidget(check)
        self.check = check
        self.central_layout.addLayout(layout_v)
        self.set_value(initial_value)
    def on_value_changed(self):
        pass

    def set_value(self, value: object):
        index = self.choices.index(value)
        self.check.setCurrentIndex(index)

    def get_value(self):
        return self.choices[self.check.currentIndex()]


views_dic = {'lab': Label, str: TextCtrl, int: NumCtrl, float: NumCtrl, 'slide': FloatSlider
    , bool: Check, list: Choice, 'choose_box': ChoiceBoxCtrl, 'chos': Choices, 'color': ColorCtrl}


class SettingsPanel(QWidget):
    widgets_dic: Dict[str, QWidget] = {}

    def __init__(self, views: List[Tuple[str]] = None, parent=None):
        super(SettingsPanel, self).__init__(parent)

        self.widgets_dic: Dict[str, QWidget] = {}
        self.setLayout(QVBoxLayout())
        for v in views:
            name = v[1]
            widget = views_dic[v[0]](*v[2:])
            if self.widgets_dic.get(name) is None:
                self.widgets_dic[name] = widget
            self.layout().addWidget(widget)

    def get_value(self):
        result = {}
        for k in self.widgets_dic:
            result[k] = self.widgets_dic[k].get_value()
        return result

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        print(self.get_value())
        self.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 类型；名称；显示的提示文字;初始值；//单位；范围
    views = [(str, 'name', 'What\'s your name?', 'hzy'),
             (int, 'age', 'How old are you?', 88, 'years old', (0, 150)),
             (float, 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
             (bool, 'sport', 'do you like sport', True),
             ('choose_box', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
              ['f22战斗机','f18战斗轰炸机','j20战斗机','su57战斗机']),
             ('color', 'color', 'Which color do u like?', (0, 200, 0))]
    sp = SettingsPanel(views=views)
    sp.show()
    val = sp.get_value()  # 返回一个字典。初始值为表格的第二列：第四列。
    print(val)
    # root.mainloop()
    sys.exit(app.exec_())
