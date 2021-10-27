from PySide2.QtGui import QCloseEvent
from widgets import PMGDockWidget


class PMDockWidget(PMGDockWidget):

    def closeEvent(self, event: 'QCloseEvent'):
        from utils import get_main_window
        main_window = get_main_window()
        w = self.widget()
        if hasattr(w, 'on_closed_action'):
            if w.on_closed_action == 'delete':
                main_window.delete_dock_widget(self.name)
                return
        self.hide()
        event.accept()
        main_window.refresh_view_configs()

    def bind_events(self):
        """绑定该控件的所有事件，会在主程序加载结束后自动执行，不需要在__init__里面手动执行"""
        pass
