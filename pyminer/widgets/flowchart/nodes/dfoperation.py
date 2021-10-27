import sys
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable
from widgets import PMGFlowContent, PMGPanelDialog

if TYPE_CHECKING:
    import pandas as pd


class DataReplace(PMGFlowContent):

    def __init__(self):
        super(DataReplace, self).__init__()
        self.input_args_labels = ['in']
        self.output_ports_labels = ['out']
        self.class_name = 'DataReplace'
        self.text = '数据替换'
        self.icon_path = ''
        self.agg = None
        self.info = {'regulations': []}

    def get_rule(self, match_words) -> Tuple[Callable, Callable]:
        """
        抽象为：
        待替换的字符（origin）,match,replacement,
        Args:
            match_words:

        Returns:

        """
        if match_words:
            return self.equals, lambda origin, match, replacement: replacement
        else:
            return self.contains, lambda origin, match, replacement: origin.replace(match, replacement)

    def equals(self, origin: str, match: str) -> bool:
        return origin == match

    def contains(self, origin: str, match: str) -> bool:
        if isinstance(origin, str):
            return origin.find(match) != -1
        return False

    def process(self, *args) -> List:
        """

        Args:
            *args:

        Returns:

        """
        import pandas as pd
        assert isinstance(args[0], pd.DataFrame)
        df: pd.DataFrame = args[0]
        regulations = self.info['regulations']

        for regulation in regulations:
            column_name = regulation['input_col_name']
            match = regulation['str_to_replace']
            replace_with = regulation['replace_with']
            match_words = regulation['match_words']
            match_rule, replace_rule = self.get_rule(match_words=match_words)
            if column_name == '$ALL' or column_name == '':
                for row in range(df.shape[0]):
                    for col in range(df.shape[1]):
                        if match_rule(df.iloc[row, col], match):
                            df.iloc[row, col] = replace_rule(df.iloc[row, col], match, replace_with)
            else:
                column = df[column_name]
                # print(column,match)
                for row in range(df.shape[0]):
                    print('row', row, column_name)
                    if match_rule(column[row], match):
                        df.loc[row, column_name] = replace_rule(column[row], match, replace_with)

        return [df]

    def check_data(self, data):
        pass

    def load_info(self, info: dict):
        print('load info!!!!!!!!!!')
        self.info = info
        print(self.info)

    def on_settings_requested(self, parent):
        '''
                headers = ['输入流字段', '输出流字段', '待替换数据', '替换为', '使用正则表达式', '全字匹配', '大小写敏感']
        self.table_keys = ['input_col_name', 'output_col_name', 'str_to_replace', 'replace_with', 'match_words',
                           'regex',
                           'case_sensitive']
        Args:
            parent:

        Returns:

        '''
        views = [['rules_ctrl', 'rules', '规则编辑',
                  [
                      {'name': 'input_col_name', 'text': '输入流字段', 'init': '$ALL'},
                      {'name': 'output_col_name', 'text': '输出流字段', 'init': ''},
                      {'name': 'str_to_replace', 'text': '待替换数据', 'init': ''},
                      {'name': 'replace_with', 'text': '替换为', 'init': ''},
                      {'name': 'regex', 'text': '使用正则表达式', 'init': False},
                      {'name': 'match_words', 'text': '全字匹配', 'init': True},
                      {'name': 'case_sensitive', 'text': '大小写敏感', 'init': False}
                  ],
                  ]
                 ]
        dlg = PMGPanelDialog(parent=parent, views=views)

        dlg.setMinimumSize(600, 480)

        dlg.panel.set_value({'rules': self.info['regulations']})
        dlg.exec_()

        self.info['regulations'] = dlg.panel.get_value()['rules']
