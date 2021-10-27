import sys
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable
from widgets import PMGFlowContent, PMGPanelDialog

if TYPE_CHECKING:
    import pandas as pd


class RandomRowSample(PMGFlowContent):

    def __init__(self):
        super(RandomRowSample, self).__init__()
        self.input_args_labels = ['输入']
        self.output_ports_labels = ['取样']  # , '检验']
        self.class_name = 'RandomRowSample'
        self.text = '随机抽样'
        self.icon_path = ''
        self.info = {'sampling_rate': 0.2}

    def process(self, *args) -> List:
        """
        随机取样的方法
        Args:
            *args:

        Returns:

        """
        import pandas as pd
        assert isinstance(args[0], pd.DataFrame)
        df: pd.DataFrame = args[0]
        # if df.duplicated():
        length = df.shape[0]
        return [df.sample(n=int(self.info['sampling_rate'] * length))]

    def on_settings_requested(self, parent):
        """

        Args:
            parent:

        Returns:

        """
        views = [('numberspin_ctrl', 'sampling_rate', '抽样比率', self.info['sampling_rate'], '', (0, 1), 0.0001)]
        dlg = PMGPanelDialog(parent=parent, views=views)

        dlg.setMinimumSize(600, 480)
        dlg.exec_()

        self.info['sampling_rate'] = dlg.panel.get_value()['sampling_rate']


if __name__ == '__main__':
    import sys

    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # r.load_info({'gen_array': False, 'size': (1, 2, 3), 'type': 'normal'})
    # r.process()
    info = {'sampling_rate': 0.2}
    r = RandomRowSample()
    r.load_info(info)
    r.on_settings_requested(None)
    print(r.info)
    sys.exit(app.exec_())
