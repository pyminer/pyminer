from PySide2.QtWidgets import QScrollArea
from PySide2.QtCore import Qt


class PMScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def setup_ui(self):
        if hasattr(self.widget(), 'setup_ui'):
            self.widget().setup_ui()
