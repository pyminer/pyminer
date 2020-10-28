from PyQt5.QtWidgets import QDockWidget, QMainWindow


class PMGDockWidget(QDockWidget):
    def __init__(self, name, text='', parent: QMainWindow = None):
        super().__init__(text, parent)
        self.parent = parent
        self.name = name

    def raise_into_view(self):
        """
        将控件提升到能直接看到的位置。特别适用于两个选项卡叠在一起的情况。
        :return:
        """
        self.setVisible(True)
        self.setFocus()
        self.raise_()
