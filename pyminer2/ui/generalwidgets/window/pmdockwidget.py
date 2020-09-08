from PyQt5.QtGui import QCloseEvent, QResizeEvent
from PyQt5.QtWidgets import QDockWidget, QMainWindow


class PMGDockWidget(QDockWidget):
    def __init__(self, name, text='', parent: QMainWindow = None):
        super().__init__(text, parent)
        self.parent = parent
        self.name = name


class PMDockWidget(PMGDockWidget):

    def closeEvent(self, event: QCloseEvent):
        from pyminer2.pmutil import get_main_window
        main_window = get_main_window()
        w = self.widget()
        if hasattr(w, 'on_closed_action'):
            if w.on_closed_action == 'delete':
                main_window.delete_dock_widget(self.name)
                return
        self.hide()
        event.accept()
        main_window.refresh_view_configs()

    def raise_into_view(self):
        '''
        将控件提升到能直接看到的位置。特别适用于两个选项卡叠在一起的情况。
        :return:
        '''
        self.setVisible(True)
        self.setFocus()
        self.raise_()
