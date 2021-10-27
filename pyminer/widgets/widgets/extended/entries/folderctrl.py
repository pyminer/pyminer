import os
from PySide2.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QFileDialog
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGFolderCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title, initial_value: str = '', filt=None):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QLineEdit()
        self.ctrl.setText(initial_value)
        path_layout.addWidget(self.ctrl)
        self.file_choose_button = QPushButton('..')
        self.file_choose_button.clicked.connect(self.select_file)
        path_layout.addWidget(self.file_choose_button)
        self.central_layout.addLayout(path_layout)

    def select_file(self):
        name = QFileDialog.getExistingDirectory(self, self.tr("Select File"),
                                                     os.path.dirname(self.get_value()),  # 起始路径
                                                     )
        if name != '':
            self.ctrl.setText(name)

    def ontext(self, event):
        self.para_changed()

    def set_value(self, value: str):
        self.ctrl.setText(value)

    def get_value(self) -> str:
        return self.ctrl.text()
