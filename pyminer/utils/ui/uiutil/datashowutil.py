from typing import TYPE_CHECKING
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtCore import Qt
if TYPE_CHECKING:
    import pandas as pd
    import numpy as np


def table_show_dataframe(dataframe: 'pd.DataFrame', table: QTableWidget):
    """
    让表格显示dataframe。适用于数据预览。
    :param dataframe:
    :param table:
    :return:
    """
    import numpy as np
    input_table_rows = dataframe.head(100).shape[0]
    input_table_colunms = dataframe.shape[1]
    input_table_header = [str(x) for x in dataframe.columns.values.tolist()]
    table.setColumnCount(input_table_colunms)
    table.setRowCount(input_table_rows)
    table.setHorizontalHeaderLabels(input_table_header)
    for i in range(input_table_rows):
        input_table_rows_values = dataframe.iloc[[i]]
        input_table_rows_values_array = np.array(input_table_rows_values)
        input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
        for j in range(input_table_colunms):
            input_table_item = input_table_rows_values_list[j]

            input_table_item = str(input_table_item)
            newItem = QTableWidgetItem(input_table_item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(i, j, newItem)
