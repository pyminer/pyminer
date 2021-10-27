from typing import List, Any

from PySide2.QtWidgets import QLabel, QHBoxLayout, QComboBox
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGComboCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: Any, choices: list, texts=None):
        """
        ComboBox control to select values
        Args:
            layout_dir:
            title:
            initial_value:
            choices:
            texts:
        """
        super().__init__(layout_dir)
        self.choices = []
        self.text_list = []

        lab_title = QLabel(text=title)
        layout = QHBoxLayout()
        self.central_layout.addWidget(lab_title)
        self.on_check_callback = None
        check = QComboBox()

        check.currentIndexChanged.connect(self.on_value_changed)

        layout.addWidget(check)
        self.central_layout.addLayout(layout)
        self.check = check
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
        self.signal_param_changed.emit(self.name)

    def set_value(self, value: Any):
        index = self.choices.index(value)
        self.check.setCurrentIndex(index)

    def get_value(self) -> Any:
        try:
            return self.choices[self.check.currentIndex()]
        except:
            return None
