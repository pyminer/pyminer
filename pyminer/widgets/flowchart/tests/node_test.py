import sys
from typing import List, Union

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit
# from widgets.flowchart.nodes.random import Random
# from widgets.flowchart.nodes.plots import HistPlot
from widgets.flowchart.nodes.dfoperation import DataReplace
import numpy as np

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # r.load_info({'gen_array': False, 'size': (1, 2, 3), 'type': 'normal'})
    # r.process()
    info = {
        'regulations': [
            {'input_col_name': 'aa', 'output_col_name': 'aa', 'str_to_replace': 'aa', 'replace_with': 'dddd',
             'match_words': True, 'regex': False, 'case_sensitive': False}]}
    r = DataReplace()
    r.load_info(info)
    r.on_settings_requested(None)
    sys.exit(app.exec_())
