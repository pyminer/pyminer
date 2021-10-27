from PySide2.QtWidgets import QLineEdit, QLabel, QHBoxLayout
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGLineCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.on_check_callback = None

        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)
        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)

    def param_changed(self, event):
        pass

    def ontext(self, event):
        self.para_changed()

    def set_value(self, text: str):
        self.ctrl.clear()
        self.ctrl.setText(text)

    def get_value(self) -> str:
        return self.ctrl.text()
