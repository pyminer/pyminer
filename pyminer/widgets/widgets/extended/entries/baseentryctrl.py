from PySide2.QtWidgets import QLineEdit
from ..base import BaseExtendedWidget


class PMGBaseEntryCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str):
        super().__init__(layout_dir)
        self.ctrl: 'QLineEdit' = None

    def set_ctrl_warning(self, warning: bool):
        if warning == True:
            self.ctrl.setStyleSheet("background-color:#ff0000;")
        else:
            self.ctrl.setStyleSheet("")
