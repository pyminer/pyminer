from PySide2.QtWidgets import QWidget, QDialog, QVBoxLayout, QTextBrowser, QLabel, QPushButton


class ReportWidget(QDialog):
    def __init__(self, parent: QWidget = None):
        super(ReportWidget, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.label_brief = QLabel()
        self.label_brief.setWordWrap(True)
        self.layout().addWidget(self.label_brief)
        self.detailed_info_show = QTextBrowser()
        self.layout().addWidget(self.detailed_info_show)
        self.ok_button = QPushButton()
        self.ok_button.setText(self.tr('Ok'))
        self.layout().addWidget(self.ok_button)

        self.ok_button.clicked.connect(self.close)
        self.setMinimumWidth(400)

    def show_info(self, brief: str, detailed: str, title=''):
        if title == '':
            title = self.tr('Info')
        self.label_brief.setText(brief)
        self.detailed_info_show.setText(detailed)
        self.setWindowTitle(title)


def show_error(parent: QWidget, brief: str, detailed: str, title: str = ''):
    rw = ReportWidget(parent)
    rw.show_info(brief, detailed, title)
    rw.exec_()
