from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QWidget
from PyQt5.QtCore import QSize


class PMTextEditConsole(QWidget):
    def __init__(self):
        super().__init__()
        # self.setObjectName("tab_3")
        self.verticalLayout_4 = QVBoxLayout(self)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.textEdit_console = QTextEdit(self)
        self.textEdit_console.setMaximumSize(QSize(16777215, 16777215))
        self.textEdit_console.setReadOnly(True)
        # self.textEdit_console.setObjectName("textEdit_console")
        self.verticalLayout_4.addWidget(self.textEdit_console)
