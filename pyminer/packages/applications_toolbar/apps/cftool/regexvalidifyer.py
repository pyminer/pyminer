import re

from PySide2.QtWidgets import QDialog, QApplication, QListWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton

from widgets import PMGPanel


class RegexDialog(QDialog):
    def __init__(self, parent=None):
        
        self.matches = [{'text': '网址（URL）', 'regex': '[a-zA-z]+://[^\\s]*'},
                        # {'text': 'IP地址(IP Address)',
                        #  'regex': '((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)'},
                        # {'text': '电子邮件(Email)',
                        #  'regex': '\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*'},
                        {'text': 'QQ号码', 'regex': '[1-9]\\d{4,}'},
                        {'text': 'HTML标记(包含内容或自闭合)', 'regex': '<([a-zA-Z]*)>\w*</\\1>'},
                        {'text': '密码(由数字/大写字母/小写字母/标点符号组成，四种都必有，8位以上)',
                         'regex': '(?=^.{8,}$)(?=.*\\d)(?=.*\\W+)(?=.*[A-Z])(?=.*[a-z])(?!.*'},
                        {'text': '日期(年-月-日)',
                         'regex': '(\\d{4}|\\d{2})-((1[0-2])|(0?[1-9]))-(([12][0-9])|(3[01])|(0?[1-9]))'},
                        {'text': '日期(月/日/年)',
                         'regex': '((1[0-2])|(0?[1-9]))/(([12][0-9])|(3[01])|(0?[1-9]))/(\\d{4}|\\d{2})'},
                        {'text': '时间(小时:分钟, 24小时制)', 'regex': '((1|0?)[0-9]|2[0-3]):([0-5][0-9])'},
                        {'text': '汉字(字符)', 'regex': '[一-龥]'},
                        {'text': '中文及全角标点符号(字符)', 'regex': '[\u3000-〞︐-︙︰-﹄﹐-﹫！-￮]'},
                        {'text': '中国大陆固定电话号码', 'regex': '(\\d{4}-|\\d{3}-)?(\\d{8}|\\d{7})'},
                        {'text': '中国大陆手机号码', 'regex': '1\\d{10}'},
                        {'text': '中国大陆邮政编码', 'regex': '[1-9]\\d{5}'},
                        {'text': '中国大陆身份证号(15位或18位)', 'regex': '\\d{15}(\\d\\d[0-9xX])?'},
                        {'text': '非负整数(正整数或零)', 'regex': '\\d+'},
                        {'text': '正整数', 'regex': '[0-9]*[1-9][0-9]*'},
                        {'text': '负整数', 'regex': '-[0-9]*[1-9][0-9]*'},
                        {'text': '整数', 'regex': '-?\\d+'},
                        {'text': '小数', 'regex': '(-?\\d+)(\\.\\d+)?'},
                        {'text': '不包含abc的单词', 'regex': '\x08((?!abc)\\w)+\x08'}]

        super(RegexDialog, self).__init__(parent)
        self.setLayout(QHBoxLayout())
        self.regex_list = QListWidget()

        # for d in self.matches:
        self.regex_list.addItems([d['text'] for d in self.matches])
        self.regex_list.setMaximumWidth(300)

        self.layout().addWidget(self.regex_list)
        self.main_layout = QVBoxLayout()

        self.layout().addLayout(self.main_layout)
        views = [
            ('line_ctrl', 'target', '目标', 'aewfafwer ewrwerewr1234565'),
            ('line_ctrl', 'regex', '输入正则表达式', ''),
            ('line_ctrl', 'result', '展示结果', ''),
            ('combo_ctrl', 'mode', '匹配模式', 'findall', ['search', 'findall'])
        ]
        self.settings_panel = PMGPanel(views=views)
        self.main_layout.addWidget(self.settings_panel)
        button_calc = QPushButton('计算！')
        button_calc.clicked.connect(self.calc)
        self.main_layout.addWidget(button_calc)
        self.regex_list.doubleClicked.connect(self.load_regex)

        # self.functions = {'findall':re.findall,'search':re.search}

    def load_regex(self, e):
        row = self.regex_list.currentIndex().row()
        self.settings_panel.set_value({'regex': self.matches[row]['regex']})

    def func_findall(self, regex, target):
        import re
        print(regex, target)
        return re.findall(regex, target)

    def calc(self):
        values = self.settings_panel.get_value()
        regex = values['regex']
        target = values['target']
        mode = values['mode']
        if mode == 'findall':
            res = self.func_findall(regex, target)
        elif mode == 'search':
            res = re.search(regex, target)
        self.settings_panel.set_value({'result': repr(res)})


if __name__ == '__main__':
    app = QApplication([])
    dlg = RegexDialog()
    dlg.show()
    dlg.setMinimumWidth(800)
    app.exec_()
