import sys

from PySide2.QtWidgets import QApplication

from pmgwidgets import PMGPanelDialog

app = QApplication(sys.argv)

views3 = \
    [

        ("multitype_ctrl", "index", "选择行", [[None, ], ['']], [{
            "type_title": "字符串列表",
            "ctrls": [
                ("list_ctrl", "list_ctrl", '输入字符串列表', [[None, ], ['']], lambda: None),
            ],
            "on_ok": lambda values: values["list_ctrl"][1]
        }, {
            "type_title": "字符串",
            "ctrls": [
                ("line_ctrl", "aaaa", '输入一个字符串', "Please input a string"),
            ], "on_ok": lambda values: repr(values["aaaa"])
        }, {
            "type_title": "选择变量",
            "ctrls": [
                ("vars_combo_ctrl", "variables", "选择变量", ""),
            ],
        }]),

        ("multitype_ctrl", "column", "选择列", [[None, ], ['']], [{
            "type_title": "字符串列表",
            "ctrls": [
                ("list_ctrl", "list_ctrl", '输入字符串列表', [[None, ], ['']], lambda: None),
            ],
            "on_ok": lambda values: values["list_ctrl"][1]
        }, {
            "type_title": "字符串",
            "ctrls": [
                ("line_ctrl", "aaaa", '输入一个字符串', "Please input a string"),
            ],
            "on_ok": lambda values: repr(values["aaaa"])
        }, {
            "type_title": "选择变量",
            "ctrls": [
                ("vars_combo_ctrl", "variables", "选择变量", ""),
            ],
        }]),

        ("multitype_ctrl", 'values', "值", [[None, ], ['']], [{
            "type_title": "字符串列表",
            "ctrls": [
                ("list_ctrl", "list_ctrl", '输入字符串列表', [[None, ], ['']], lambda: None),
            ],
            "on_ok": lambda values: values["list_ctrl"][1]
        }, {
            "type_title": "字符串",
            "ctrls": [
                ("line_ctrl", "aaaa", '输入一个字符串', "Please input a string"),
            ],
            "on_ok": lambda values: repr(values["aaaa"])
        }, {
            "type_title": "选择变量",
            "ctrls": [
                ("vars_combo_ctrl", "variables", "选择变量", ""),
            ],
        }])
    ]

optionals = ["index", "values"]  # 列出了所有的可选参数
sp3 = PMGPanelDialog(parent=None, views=views3)
sp3.panel.signal_settings_changed.connect(lambda settings: print('views2-settings', settings))
sp3.panel.set_items(views3)
sp3.show()
ok = sp3.exec_()

if ok:
    print(sp3.get_value())
