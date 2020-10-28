from PyQt5.QtWidgets import QToolBox, QWidget
from typing import Dict, Callable


class PMGToolBox(QToolBox):
    group_widgets: Dict[str, QWidget] = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_num = 0
        pass

    def set_group_text(self, group_name: str, text: str):
        gw = self.group_widgets.get(group_name)
        if gw is not None:
            self.setItemText(self.indexOf(gw), text)

    def add_button(self, group_name: str, text: str, icon_path: str, action: Callable):
        from pmgwidgets import PMFlowArea
        if self.group_widgets.get(group_name) is None:
            fa = PMFlowArea()
            self.group_widgets[group_name] = fa
            self.addItem(fa, group_name)
            btn = fa.add_tool_button(name='button#%d' % self.button_num, text=text, icon_path=icon_path)
            btn.clicked.connect(action)
            self.button_num += 1
        else:
            fa: PMFlowArea = self.group_widgets[group_name]
            btn = fa.add_tool_button(name='button#%d' % self.button_num, text=text, icon_path=icon_path)
            btn.clicked.connect(action)
            self.button_num += 1
