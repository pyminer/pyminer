from PySide2.QtWidgets import QLabel, QHBoxLayout, QCheckBox
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGCheckCtrl(BaseExtendedWidget):
    """
    bool, 'sport', 'do you like sport',True
    """

    def __init__(self, layout_dir: str, title: str, initial_value: bool):
        super().__init__(layout_dir)

        # layout = QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.on_check_callback = None
        check = QCheckBox(text=title)
        check.stateChanged.connect(self.on_check)
        # layout.addWidget(check)
        self.check = check
        self.central_layout.addWidget(check)
        self.set_value(initial_value)

    def get_value(self) -> bool:
        return self.check.isChecked()

    def set_value(self, value: bool):
        self.check.setChecked(value)

    def on_check(self):
        self.signal_param_changed.emit(self.name)
