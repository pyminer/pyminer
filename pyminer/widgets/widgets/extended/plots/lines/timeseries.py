from typing import List, Dict, Tuple

import pyqtgraph as pg
from PySide2.QtWidgets import QHBoxLayout
from widgets.widgets.extended.base import BaseExtendedWidget
from widgets import iter_isinstance, TYPE_RANGE


class PMGTimeSeriesShow(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: Dict[str, List[float]],
                 y_range: Tuple[int, int] = None, threshold_range: TYPE_RANGE = None,
                 xlabel: str = '', ylabel: str = '',
                 face_color: str = '#ffffff', legend_face_color: str = '#dddddd', x_range: Tuple[int, int] = None,
                 text_color: str = 'k'):
        super().__init__(layout_dir=layout_dir)
        from widgets import PMGTimeSeriesPlot
        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)

        self.ctrl = PMGTimeSeriesPlot(parent=None, threshold_range=threshold_range, face_color=face_color,
                                      text_color=text_color)
        self.ctrl.time_series.xlabel = xlabel
        self.ctrl.time_series.ylabel = ylabel
        self.ctrl.time_series.title = title
        self.ctrl.time_series.x_range = x_range
        self.ctrl.time_series.y_range = y_range
        self.ctrl.time_series.threshold_range = threshold_range
        self.ctrl.time_series.face_color = face_color
        pg.setConfigOption('background', face_color)
        self.ctrl.time_series.legend_face_color = legend_face_color
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)

        self.accury = initial_value
        if initial_value is not None:
            self.set_value(initial_value)

    def set_value(self, values: Dict[str, List[float]]):
        """
        {'timestamps':[...],
         'info1':{name:'unnamed','data':[...]}
         }
        :param values:
        :return:
        """
        timestamps = values['timestamps']
        values_list = []
        tags_list = []
        length = len(timestamps)
        for k in values:
            if k != 'timestamps':
                assert len(values[k]['data']) == length, 'timestamps and datas may not be of same length!'
                assert values[k].get('data') is not None
                assert values[k].get('tag') is not None
                values_list.append(values[k]['data'])
                tags_list.append(values[k]['tag'])
        self.ctrl.set_data(timestamps, values=values_list, tags=tags_list)

    def alert(self, alert_level: int):
        self.ctrl.alert(alert_level)

    def set_threshold_y(self, threshold: Tuple[int, int]):
        self.ctrl.time_series.y_range = threshold
        self.ctrl.time_series.threshold_range = threshold
