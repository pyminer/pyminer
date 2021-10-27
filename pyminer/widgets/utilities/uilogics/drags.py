import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QDropEvent
from PySide2.QtWidgets import QApplication, QTextBrowser


class Demo(QTextBrowser):  # 1
    def __init__(self):
        super(Demo, self).__init__()
        self.setAcceptDrops(True)  # 2

    def dragEnterEvent(self, QDragEnterEvent):  # 3
        print('Drag Enter')
        if QDragEnterEvent.mimeData().hasText():
            QDragEnterEvent.acceptProposedAction()
            print()

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        # print('Drag Move')
        pass

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        # print('Drag Leave')
        pass

    def dropEvent(self, drop_event: QDropEvent):  # 6
        print('Drag Drop')
        url: QUrl = None
        urls = drop_event.mimeData().urls()
        for url in urls:
            print(url.toLocalFile())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
