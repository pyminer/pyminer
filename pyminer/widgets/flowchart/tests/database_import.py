import sys
import time

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from widgets.flowchart.core.flowchart_widget import PMFlowWidget
import cgitb
cgitb.enable()
if __name__ == '__main__':

    times = {True: 0, False: 1}
    app = QApplication(sys.argv)
    graphics = PMFlowWidget(path='database_import.json')
    graphics.show()
    sys.exit(app.exec_())
