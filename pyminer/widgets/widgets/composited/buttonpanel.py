from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class PMGButtonPanel(QWidget):
    def __init__(self, parent=None, layout_dir: str = 'v'):
        super().__init__(parent=parent)
        if layout_dir == 'v':
            self.setLayout(QVBoxLayout())
        else:
            self.setLayout(QHBoxLayout())

    def add_button(self, text: str, callback: str = None, icon: str = None) -> QPushButton:
        b = QPushButton()
        b.setText(text)
        self.layout().addWidget(b)
        if callback is not None:
            b.clicked.connect(callback)
        return b