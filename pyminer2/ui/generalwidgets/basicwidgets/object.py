from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class PMDockObject(object):
    on_closed_action = 'hide'  # 或者'delete'。
    signal_raise_into_view = pyqtSignal()

    def raise_widget_to_visible(self, widget: 'QWidget'):
        pass

    def on_dock_widget_deleted(self):
        pass
