'''
集成了流式布局、按钮排布的窗口。
'''
from PyQt5.QtWidgets import QScrollArea, QWidget, QToolButton
from PyQt5.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtGui import QResizeEvent
    from pyminer2.ui.generalwidgets import PMFlowLayout


class PMFlowAreaWidget(QWidget):
    def __init__(self):
        super().__init__()
        from pyminer2.ui.generalwidgets import PMFlowLayout

        layout = PMFlowLayout()
        self.setLayout(layout)

    def add_widget(self, w: 'QWidget'):
        self.layout().add_widget(w)

    def setup_ui(self):
        if hasattr(self.widget(), 'setup_ui'):
            self.widget().setup_ui()

    def resizeEvent(self, a0: 'QResizeEvent') -> None:
        super().resizeEvent(a0)
        layout: 'PMFlowLayout' = self.layout()
        layout.on_resize()


class PMFlowArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidget(PMFlowAreaWidget())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def set_layout_content_margins(self, left: int, right: int, up: int, down: int):
        self.widget().layout().setContentsMargins(left, right, up, down)

    def add_tool_button(self, name: str, text: str, icon_path: str = ''):
        b = QToolButton()
        b.setText(text)
        b.setMaximumWidth(60)
        b.setMinimumWidth(60)
        b.setMinimumHeight(40)
        b.setMaximumHeight(40)
        self.add_widget(b)
        return b

    def add_widget(self, w: 'QWidget'):
        self.widget().add_widget(w)
        return w

    def setup_ui(self):
        if hasattr(self.widget(), 'setup_ui'):
            self.widget().setup_ui()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QPushButton
    import sys

    app = QApplication(sys.argv)
    sa = PMFlowArea()
    for i in range(10):
        w = sa.add_widget(QPushButton('ad%d' % i))
        w.setMaximumHeight(60)
        w.setMinimumHeight(60)
    sa.show()
    sys.exit(app.exec())
