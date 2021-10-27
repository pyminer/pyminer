import time
from typing import Union, Tuple

from PySide2.QtCore import QCalendar, QDate
from PySide2.QtWidgets import QLabel, QHBoxLayout, QDateEdit
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGDateCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title, initial_date):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QDateEdit()
        path_layout.addWidget(self.ctrl)

        calendar_widget = QCalendar()
        self.ctrl.setCalendar(calendar_widget)

        self.central_layout.addLayout(path_layout)
        self.set_value(initial_date)

    def set_value(self, value: Union[Tuple[int, int, int], float, int]):
        if isinstance(value, tuple):
            assert len(value) == 3
            date = QDate(*value)
        elif isinstance(value, (float, int)):
            loc_time = time.localtime(value)
            print(loc_time)
            date = QDate(loc_time.tm_year, loc_time.tm_mon, loc_time.tm_mday)
        else:
            raise ValueError("value is not allowed", value)
        self.ctrl.setDate(date)

    def get_value(self) -> float:
        """
        计算值
        :return:
        """
        return time.mktime(self.ctrl.date().toPyDate().timetuple())


class PMGDateTimeCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title, initial_date):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QDateEdit()
        path_layout.addWidget(self.ctrl)

        calendar_widget = QCalendar()
        self.ctrl.setCalendar(calendar_widget)

        self.central_layout.addLayout(path_layout)
        self.set_value(initial_date)

    def set_value(self, value: Union[Tuple[int, int, int], float, int]):
        if isinstance(value, tuple):
            assert len(value) == 3
            date = QDate(*value)
        elif isinstance(value, (float, int)):
            loc_time = time.localtime(value)
            print(loc_time)
            date = QDate(loc_time.tm_year, loc_time.tm_mon, loc_time.tm_mday)
        else:
            raise ValueError("value is not allowed", value)
        self.ctrl.setDate(date)

    def get_value(self) -> float:
        """
        计算值
        :return:
        """
        return time.mktime(self.ctrl.date().toPyDate().timetuple())


class PMGTimeCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title, initial_date):
        super().__init__(layout_dir)
        self.prefix = lab_title = QLabel(text=title)
        path_layout = QHBoxLayout()
        path_layout.addWidget(lab_title)

        self.ctrl = QDateEdit()
        path_layout.addWidget(self.ctrl)

        calendar_widget = QCalendar()
        self.ctrl.setCalendar(calendar_widget)

        self.central_layout.addLayout(path_layout)
        self.set_value(initial_date)

    def set_value(self, value: Union[Tuple[int, int, int], float, int]):
        if isinstance(value, tuple):
            assert len(value) == 3
            date = QDate(*value)
        elif isinstance(value, (float, int)):
            loc_time = time.localtime(value)
            print(loc_time)
            date = QDate(loc_time.tm_year, loc_time.tm_mon, loc_time.tm_mday)
        else:
            raise ValueError("value is not allowed", value)
        self.ctrl.setDate(date)

    def get_value(self) -> float:
        """
        计算值
        :return:
        """
        return time.mktime(self.ctrl.date().toPyDate().timetuple())
