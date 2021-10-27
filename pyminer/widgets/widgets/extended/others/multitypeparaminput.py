from typing import List, Any, Dict

from PySide2.QtWidgets import QApplication, QRadioButton, QLayout
from PySide2.QtWidgets import QLabel

from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGMultiTypeCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: Any=None, types: List[Dict]=None):
        super().__init__(layout_dir)
        from widgets.widgets.composited.generalpanel import PMGPanel
        self.on_check_callback = None

        self.prefix = QLabel(text=title)

        self.central_layout.addWidget(self.prefix)

        self.radio_buttons: List[QRadioButton] = []
        self.ctrls = types
        radiobtn_texts = [self.ctrls[i]["type_title"] for i in range(len(self.ctrls))]
        for i, ctrl in enumerate(self.ctrls):
            radio_button = QRadioButton(radiobtn_texts[i])
            radio_button.toggled.connect(self.on_type_changed)
            self.radio_buttons.append(radio_button)
            self.central_layout.addWidget(radio_button)

        self.sub_panel = PMGPanel()
        self.central_layout.addWidget(self.sub_panel)

        self.set_value(initial_value)

    def on_type_changed(self, event):

        index = self.get_type_index()
        self.sub_panel.set_items([self.ctrls[index]["ctrls"]])

        # print(self.get_value())
        # self.setFixedSize(0)

    def on_param_changed(self, event):
        print(self.get_value())

    def ontext(self, event):
        self.para_changed()

    def set_type_index(self, index: int):
        self.radio_buttons[index].setChecked(True)

    def get_type_index(self) -> int:
        for i, btn in enumerate(self.radio_buttons):
            if btn.isChecked():
                return i

    def set_value(self, value: Any):
        for i, ctrl in enumerate(self.ctrls):
            try:
                self.set_type_index(i)
                keys = list(self.sub_panel.widgets_dic.keys())
                assert len(keys) == 1
                print(i, ctrl, {keys[0]: value})
                self.sub_panel.set_value({keys[0]: value})
                break
            except:
                import traceback
                traceback.print_exc()

    def get_value(self) -> Any:
        values = self.sub_panel.get_value()
        fcn = self.ctrls[self.get_type_index()].get("on_ok")
        if fcn is None:
            if len(list(values.keys())) == 1:
                return values[list(values.keys())[0]]
            else:
                return values
        else:
            return fcn(values)


if __name__ == '__main__':
    app = QApplication()
    types = [{
        "type_title": "字符串列表",
        "ctrls": [
            ("list_ctrl", "list_ctrl", 'input list of strings',),
        ],
        "on_ok": lambda values: values["list_ctrl"][1]
    },
        {
            "type_title": "字符串",
            "ctrls": [
                ("line_ctrl", "aaaa", 'input a string', "Please input a string"),
            ],
            "on_ok": None
        }
    ]

    e = PMGMultiTypeCtrl("v", "aaaaaa", [[None, None, None], ["aaaaaa", "aaaaaa", "aaaaaa"]], types)

    # e.set_value([[None, None, None], ["aaaaaa", "aaaaaa", "aaaaaa"]])
    e.show()

    app.exec_()
