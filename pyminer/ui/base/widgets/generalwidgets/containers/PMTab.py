from PyQt5.QtWidgets import QTabWidget, QWidget, QScrollArea


class PMTabWidget(QTabWidget):
    def setup_ui(self):
        for tab_id in range(self.count()):  # 遍历所有的tab
            w = self.widget(tab_id)
            if hasattr(w, 'setup_ui'):
                self.widget(tab_id).setup_ui()

    def addScrolledAreaTab(self, widget: QWidget, a1: str) -> int:
        '''
        添加使用QScrollArea包裹的Tab。
        :param widget:
        :param a1:
        :return:
        '''
        from pyminer.ui.base.widgets.generalwidgets.containers import PMScrollArea
        scroll = PMScrollArea()
        scroll.setWidget(widget)

        super().addTab(scroll, a1)
