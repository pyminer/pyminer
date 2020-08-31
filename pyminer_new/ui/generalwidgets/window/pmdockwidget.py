from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDockWidget, QMainWindow





class PMDockWidget(QDockWidget):
    def __init__(self, text='', parent: QMainWindow = None):
        super().__init__(text, parent)
        self.parent = parent
        print(self.titleBarWidget())

    def closeEvent(self, event: QCloseEvent):
        from pyminer_new.pmutil import get_main_window
        print('close')
        self.hide()
        event.accept()

        # dock_widgets = get_main_window().dock_widgets
        # for k in dock_widgets.keys():
        #     print(k, dock_widgets[k].isVisible())
        get_main_window().refresh_view_configs()
