from typing import List, Union, TYPE_CHECKING, ClassVar
from PySide2.QtWidgets import QWidget, QSplitter, QApplication, QVBoxLayout, QComboBox
from utils.ui.uiutil.workspaceutil import bind_combo_with_workspace
from lib.comm import get_var

if TYPE_CHECKING:
    import pandas as pd
    import numpy as np


class VariableSelect(QWidget):
    """

    """

    # signal_calc =
    def __init__(self, parent=None, title: str = '', type_filter: str = ''):
        super().__init__(parent=parent)
        self.type_filter = type_filter
        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())
        self.current_variable: 'Union[pd.DataFrame, np.array, List[float]]' = None
        self.combo_select_variable = QComboBox()
        self.combo_select_series = QComboBox()
        self.layout().addWidget(self.combo_select_variable)
        self.layout().addWidget(self.combo_select_series)
        self.combo_select_series.setEnabled(False)
        bind_combo_with_workspace(self.combo_select_variable, self.type_filter)
        self.combo_select_variable.currentIndexChanged.connect(self.slot_var_selected)
        # self.combo_select_series.currentIndexChanged.connect(self.slot_series_selected)

    def slot_var_selected(self, e):
        import pandas as pd
        import numpy as np
        if self.get_current_variable_name().isidentifier():
            variable: Union[pd.DataFrame, np.array, List[float]] = get_var(self.get_current_variable_name())
            if isinstance(variable, pd.DataFrame):
                series = variable.columns.tolist() + ['<全部>']
                self.combo_select_series.clear()
                for i, col in enumerate(series):
                    self.combo_select_series.addItem(str(col))
                    self.combo_select_series.setItemData(i, col)

                self.combo_select_series.setEnabled(True)
                self.combo_select_series.setCurrentIndex(len(series) - 1)
            else:
                self.combo_select_series.clear()
                self.combo_select_series.setEnabled(False)
            self.current_variable = variable
            print(self.combo_select_variable.currentText())

    def get_current_variable_name(self) -> str:
        return self.combo_select_variable.currentText()

    def get_variable(self) -> 'Union[pd.DataFrame, np.array, List[float]]':
        import pandas as pd
        if isinstance(self.current_variable, pd.DataFrame):
            series = self.combo_select_series.currentData()
            if series == '<全部>':
                return self.current_variable
            else:
                return self.current_variable[series]
        else:
            return self.current_variable

    def get_variable_to_array(self) -> 'np.ndarray':
        return


if __name__ == '__main__':
    app = QApplication([])
    a = VariableSelect()
    a.show()
    app.exec_()
