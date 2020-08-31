from PyQt5.QtWidgets import QMainWindow


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('结果')
        self.setGeometry(5, 30, 1355, 730)
