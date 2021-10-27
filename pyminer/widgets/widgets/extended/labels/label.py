from PySide2.QtWidgets import QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from ..base import BaseExtendedWidget


class PMGLabelShow(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir=layout_dir)
        self.on_check_callback = None
        layout = QVBoxLayout()
        self.prefix = QLabel(text=title)
        self.ctrl = QLabel()

        self.ctrl.setStyleSheet('QLabel{font-size:20px;}')
        self.central_layout.addLayout(layout)
        # layout.addWidget(QLabel(' '))
        layout.addWidget(self.prefix)
        layout.addWidget(self.ctrl)
        # layout.addItem(QSpacerItem(20, 20, QSizePolicy.Ignored, QSizePolicy.Expanding))

        self.set_value(initial_value)

    def set_value(self, value: str):
        self.ctrl.setText(value)
