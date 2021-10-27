import sys
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable
from widgets import PMGFlowContent, PMGPanelDialog

if TYPE_CHECKING:
    import pandas as pd


class DropDuplicated(PMGFlowContent):

    def __init__(self):
        super(DropDuplicated, self).__init__()
        self.input_args_labels = ['in']
        self.output_ports_labels = ['out']
        self.class_name = 'DropDuplicated'
        self.text = '去除重复值'
        self.icon_path = ''
        self.agg = None
        self.info = {'regulations': []}

    def process(self, *args) -> List:
        """
        删除缺失值的方法
        Args:
            *args:

        Returns:

        """
        import pandas as pd
        assert isinstance(args[0], pd.DataFrame)
        df: pd.DataFrame = args[0]
        # if df.duplicated():
        return [df.drop_duplicates()]

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
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
