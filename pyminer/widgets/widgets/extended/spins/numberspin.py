from typing import Union, Tuple

from PySide2.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QDoubleSpinBox
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGNumberSpinCtrl(BaseExtendedWidget):
    """
    利用spinbox的控制面板，当最大值、最小值、初始值和步长均为整数的时候，类型为整数；、反之只要有任意一个是float，
    类型就是浮点数了。
    """

    def __init__(self, layout_dir: str, title: str, initial_value: Union[int, float], unit: str = '',
                 val_range: Tuple[Union[float, int], Union[float, int]] = (None, None),
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
        self.ctrl.valueChanged.connect(self.on_value_changed)
        self.postfix = QLabel(text=unit)

        # self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.prefix)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.postfix)
        if self.min is not None:
            self.ctrl.setMinimum(self.min)
        if self.max is not None:
            self.ctrl.setMaximum(self.max)
        self.ctrl.setSingleStep(step)
        self.accury = initial_value
        self.set_value(initial_value)

    def set_value(self, value: Union[float, int]) -> None:
        self.ctrl.setValue(value)

    def get_value(self) -> Union[int, float]:
        return self.ctrl.value()

    def on_value_changed(self):
        self.signal_param_changed.emit(self.name)
