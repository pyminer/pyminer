"""
集成了流式布局、按钮排布的窗口。
"""
from PyQt5.QtWidgets import QScrollArea, QWidget, QToolButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtGui import QResizeEvent
    from pmgwidgets import PMFlowLayout


class PMFlowAreaWidget(QWidget):
    def __init__(self):
        super().__init__()
        from pmgwidgets import PMFlowLayout

        self.outer_layout = QVBoxLayout()

        self.flow_layout = PMFlowLayout()
        self.setMinimumWidth(100)
        self.outer_layout.addLayout(self.flow_layout)
        spacer_v = QSpacerItem(20, 20, QSizePolicy.Minimum,
                               QSizePolicy.Expanding)

        self.outer_layout.addItem(spacer_v)
        self.setLayout(self.outer_layout)

    def add_widget(self, w: 'QWidget'):
        self.flow_layout.add_widget(w)

    def setup_ui(self):
        if hasattr(self.widget(), 'setup_ui'):
            self.widget().setup_ui()

    def resizeEvent(self, a0: 'QResizeEvent') -> None:
        super().resizeEvent(a0)
        layout: 'PMFlowLayout' = self.flow_layout
        layout.on_resize()


class PMFlowArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.flow_widget = PMFlowAreaWidget()
        self.widgets_list = self.flow_widget.flow_layout.widgets_list
        self.setWidget(self.flow_widget)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def set_layout_content_margins(
            self, left: int, right: int, up: int, down: int):
        self.flow_widget.flow_layout.setContentsMargins(left, right, up, down)

    def add_tool_button(self, name: str, text: str, icon_path: str = ''):
        from pmgwidgets import create_icon
        b = QToolButton()
        b.setText(text)
        icon = create_icon(icon_path)
        b.setIcon(icon)
        b.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        b.setIconSize(QSize(40, 40))
        b.setMaximumWidth(80)
        b.setMinimumWidth(80)
        b.setMinimumHeight(60)
        b.setMaximumHeight(60)
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
        w.setMinimumWidth(100)
        w.setMaximumWidth(100)
    sa.show()
    sys.exit(app.exec())
