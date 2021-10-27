from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea


from PySide2.QtCore import Qt


class PMScrollableLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.label = QLabel()
        layout_label = QVBoxLayout()
        layout_label.addWidget(self.label)
        self.scroll_area.setLayout(layout_label)

        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

        self.setText = self.label.setText
        self.setWordWrap = self.label.setWordWrap


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    w = PMScrollableLabel()
    w.setWordWrap(True)
    w.setText('aaaaaaaaa ' * 10000)
    w.show()
    sys.exit(app.exec_())
