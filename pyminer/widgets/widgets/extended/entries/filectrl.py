import os
from PySide2.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QFileDialog
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGFileCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title, initial_value: str = '', filt="All Files (*);;Text Files (*.txt)",
                 initial_dir: str = '', mode: str = 'open'):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        self.layout().addWidget(lab_title)
        self.filter = filt

        self.ctrl = QLineEdit()
        self.mode = mode
        self.current_dir = initial_dir
        if os.path.exists(initial_value):
            self.ctrl.setText(initial_value)
            self.current_dir = os.path.dirname(self.current_dir)
        else:
            self.current_dir = initial_dir
        path_layout.addWidget(self.ctrl)
        self.file_choose_button = QPushButton('..')
        self.file_choose_button.clicked.connect(self.select_file)
        self.file_choose_button.setMaximumWidth(30)
        path_layout.addWidget(self.file_choose_button)
        self.central_layout.addLayout(path_layout)
        self.ctrl.textChanged.connect(self.on_text_changed)

    def select_file(self):
        if self.mode == 'open':
            name, ext = QFileDialog.getOpenFileName(self, self.tr("Select File"),
                                                    self.current_dir,  # 起始路径
                                                    self.filter)
        elif self.mode == 'save':
            name, ext = QFileDialog.getSaveFileName(self, self.tr("Save File"), self.current_dir,
                                                    self.filter)
        else:
            raise ValueError
        if name != '':
            self.ctrl.setText(name)
            self.current_dir = os.path.dirname(name)

    def on_text_changed(self, event):
        """

        Args:
            event:

        Returns:

        """
        # self.para_changed()
        path = self.ctrl.text().strip()
        if self.mode == 'open' and os.path.isfile(path):
            self.signal_param_changed.emit(self.name)
        elif self.mode == 'save':
            self.signal_param_changed.emit(self.name)

    def set_value(self, value: str):
        self.ctrl.setText(value)

    def get_value(self) -> str:
        return self.ctrl.text()
