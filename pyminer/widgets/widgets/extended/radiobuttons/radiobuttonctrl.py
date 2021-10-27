import sys
from typing import List

from PySide2.QtWidgets import *
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QLabel

from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGRadioCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str,
                 choices: list, texts=None):
        super().__init__(layout_dir)
        if texts is not None:
            assert len(choices) == len(texts)
        else:
            texts = [str(c) for c in choices]
        self.on_check_callback = None

        self.prefix = QLabel(text=title)

        # entryLayout = QHBoxLayout()
        # entryLayout.setContentsMargins(0, 0, 0, 0)
        # self.ctrl = QLineEdit()
        # self.ctrl.textChanged.connect(self.ontext)

        # self.central_layout.addWidget(self.prefix)
        # self.central_layout.addLayout(entryLayout)
        # entryLayout.addWidget(self.ctrl)
        self.radio_buttons: List[QRadioButton] = []
        self.choices = choices
        self.texts = texts
        for text in texts:
            radio_button = QRadioButton(text)
            radio_button.toggled.connect(self.on_param_changed)
            self.radio_buttons.append(radio_button)
            self.central_layout.addWidget(radio_button)

        self.set_value(initial_value)

    def on_param_changed(self, event):
        if event:
            self.para_changed()

    def set_value(self, value: str):
        for i, c in enumerate(self.choices):
            if c == value:
                self.radio_buttons[i].setChecked(True)

    def get_value(self) -> str:
        for i, btn in enumerate(self.radio_buttons):
            if btn.isChecked():
                return self.choices[i]
        raise ValueError(self.choices)


if __name__ == '__main__':
    app = QApplication()
    radioDemo = PMGRadioCtrl("v", "Radio Demo", "aaa", ["aaa", "bbb", "ccc"], ["啊啊啊", "波波波", "呲呲呲"])
    radioDemo.set_value("bbb")
    radioDemo.show()
    sys.exit(app.exec_())
