from PyQt5.QtGui import QCloseEvent
from pmgwidgets import PMGDockWidget


class PMDockWidget(PMGDockWidget):

    def closeEvent(self, event: 'QCloseEvent'):
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
