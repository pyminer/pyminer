import sys
from typing import List

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit
from widgets import PMFlowWidget, PMGFlowContent


class ContentDialog(QDialog):
    def __init__(self, parent=None, initial_value: float = 0):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.line_edit = QLineEdit()
        self.layout().addWidget(self.line_edit)
        self.line_edit.setText(str(initial_value))


class Constant(PMGFlowContent):
    def __init__(self):
        super(Constant, self).__init__()
        self.input_args_labels = []
        self.output_ports_labels = ['output1']
        self.class_name = 'Constant'
        self.text = '常数'
        self.icon_path = ''
        self._value = 0

    def process(self, *args) -> List[object]:
        return [self._value]

    def on_settings_requested(self, parent):
        dlg = ContentDialog(parent)

        dlg.exec_()
        self._value = float(dlg.line_edit.text())
        print(self._value)

    def format_param(self) -> str:
        return '值:' + str(self._value)


class Add(PMGFlowContent):
    def __init__(self):
        super(Add, self).__init__()
        self.input_args_labels = ['in1', 'in2']
        self.output_ports_labels = ['out']
        self.class_name = 'Add'
        self.text = '求和'
        self.icon_path = ''
        self.ports_changable = [True, False]

    def process(self, *args) -> List[object]:
        if len(args) > 1:
            sum = args[0]
            for a in args[1:]:
                sum += a
        else:
            raise ValueError
        print(args[0], args[1])
        return [sum]


class Mul(PMGFlowContent):
    def __init__(self):
        super().__init__()
        self.input_args_labels = ['in1', 'in2']
        self.output_ports_labels = ['out']
        self.class_name = 'Mul'
        self.text = '乘积'
        self.icon_path = ''

    def process(self, *args) -> List[object]:
        if len(args) > 1:
            mul = args[0]
            for a in args[1:]:
                mul *= a
        else:
            raise ValueError
        return [mul]
