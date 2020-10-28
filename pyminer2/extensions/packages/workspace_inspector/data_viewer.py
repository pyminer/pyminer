import pprint
import sys
import threading
from typing import Dict, TYPE_CHECKING
from PyQt5.QtWidgets import QTabWidget, QTextBrowser, QWidget, QMessageBox

from pmgwidgets import PMTableView, PMGTableWidget, PMDockObject, PMGTableViewer, PMJsonTreeViewer

if TYPE_CHECKING:
    from pyminer2.extensions.extensionlib.extension_lib import extension_lib


class AbstractViewer(object):
    """
    抽象视图
    """

    @staticmethod
    def is_valid(data) -> bool:
        """
        判断data是否为合法的变量类型
        """
        return True

    def set_data(self, data: object, metadata: dict):
        """
        设置其显示数据的值为data，显示的元数据为meadata。
        """
        pass


class PDDataViewer(PMGTableViewer, AbstractViewer):
    """
    显示Pandas数据的视图
    """

    def __init__(self, parent=None):
        PMGTableViewer.__init__(self, parent, table_view=PMTableView())
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data):
        import pandas as pd
        return isinstance(data, pd.DataFrame)

    def set_data(self, data: object, metadata: dict = None):
        super().set_data(data)


class NPDataViewer(PMGTableViewer, AbstractViewer):
    """
    显示numpy.ndarray的视图
    """

    def __init__(self, parent=None):
        PMGTableViewer.__init__(self, parent, table_view=PMTableView())
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data):
        import numpy
        return isinstance(data, numpy.ndarray)

    def set_data(self, data: object, metadata: dict = None):
        super(NPDataViewer, self).set_data(data)


class JsonViewer(PMJsonTreeViewer, AbstractViewer):
    """
    树状图，专门显示dict型数据。
    """

    def __init__(self, parent=None):
        PMJsonTreeViewer.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data) -> bool:
        return isinstance(data, dict)

    def set_data(self, data: Dict[str, object], metadata: dict = None) -> None:
        PMJsonTreeViewer.set_data_dic(self, data)


class GeneralIterableViewer(PMGTableWidget, AbstractViewer):
    """
    显示可迭代对象的视图
    这个变量可以为列表、每行长度不等的二维嵌套列表等。
    解析方式为先从第一个可迭代维度上解析，取出元素，也就是data[0],data[1]。。。data[len(data)-1]，逐行显示。
    如果元素不可迭代，那么就填在对应行的第一列；如果元素可迭代的，那么就把元素依次填写在同一行各个列中。
    data[0][1],data[0][2]....
    """

    def __init__(self, parent=None):
        PMGTableWidget.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data: object):
        import numpy
        import pandas
        if isinstance(data, numpy.ndarray) or isinstance(
                data, pandas.DataFrame):
            return False
        return PMGTableWidget.check_data_can_be_displayed_by_table(data=data)

    def set_data(self, data: 'np.ndarray', metadata: dict = None):
        super().set_data_2d(data)


class GeneralObjectViewer(QTextBrowser, AbstractViewer):
    """
    一个文本显示控件
    专门显示metadata。
    """

    def __init__(self, parent=None):
        QTextBrowser.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data: object):
        import numpy
        import pandas
        if isinstance(data, numpy.ndarray) or isinstance(
                data, pandas.DataFrame):
            return False
        elif GeneralIterableViewer.is_valid(data):
            return False
        return True

    def set_data(self, data: object, metadata: dict = None):
        self.setText(self.tr('value:') + '\n\n   ' + pprint.pformat(data)
                     + '\n\n\n' + self.tr('meta data:') + '\n\n' + pprint.pformat(metadata))


viewer_classes = [
    PDDataViewer,
    NPDataViewer,
    GeneralIterableViewer,
    JsonViewer,
    GeneralObjectViewer]


def build_viewer(data: object, metadata: object) -> 'QWidget':
    """
    创建变量视图的工厂函数。
    """
    for viewer_class in viewer_classes:
        if viewer_class.is_valid(data):
            viewer = viewer_class()
            viewer.set_data(data, metadata)

            return viewer


def is_big_data(data):
    try:
        import numpy, pandas
        if sys.getsizeof(data) / 1024 / 1024 > 50:
            return True
        elif hasattr(data, '__len__'):
            if len(data) > 10000:
                return True
        elif isinstance(data, numpy.ndarray):
            if numpy.prod(data.shape) > 100 * 100:
                return True
        elif isinstance(data, pandas.DataFrame):
            arr = data.values
            if numpy.prod(arr) > 100 * 100:
                return True
    except:
        import traceback
        traceback.print_exc()
    return False


class PMVariableViewerWidget(QTabWidget, PMDockObject):
    """
    在这里采用了多继承的方式。注意，一定要把PMDockObject写在右边。
    """
    if TYPE_CHECKING:
        lib = extension_lib

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.var_view_tables: Dict[str, object] = {}
        self.tabCloseRequested.connect(self.on_tab_close_request)
        self.on_closed_action = 'delete'
        self.variable_view_factory = None

    def set_lib(self, lib):
        '''
        设置回调函数。注意，只有主线程中才能刷新界面，否则不可刷新。
        :param varname:
        :param variable:
        :return:
        '''
        self.lib = lib

        def on_modification(varname: str, variable, source: str):
            if threading.current_thread() is threading.main_thread():
                if varname in self.var_view_tables:
                    self.show_data(varname, raise_window=False)

        def on_deletion(varname: str):
            if threading.current_thread() is threading.main_thread():
                if varname in self.var_view_tables:
                    self.removeTab(varname)
                    self.var_view_tables.pop(varname)

        self.lib.on_modification(on_modification)
        self.lib.on_deletion(on_deletion)

    def show_data(self, dataname: str, raise_window=True):
        """
        显示数据，显示数据之后，使得上层控件将其提升到上层可见。特别适用于几个dockwidget叠在一起的情况。
        :param dataname:
        :return:
        """
        data = self.lib.get_var(dataname)
        # size = sys.getsizeof(data) / (1024 ** 2)
        # print(size)
        # if is_big_data(data):
        #     QMessageBox.warning(self, self.tr('Big Data'),
        #                         self.tr("Showing this data can be very time-consuming.\n Still show it?"))
        try:
            dataview: 'QWidget' = self.var_view_tables.get(dataname)

            metadata = self.lib.get_data_info(dataname)
        except BaseException:
            return
        last_index = self.count()
        if dataview is not None:
            index = self.indexOf(dataview)
            self.removeTab(index)
            last_index = index
            self.var_view_tables.pop(dataname)
            dataview = None
        if dataview is None:
            dataview = build_viewer(data, metadata)
            self.insertTab(last_index, dataview, dataname)
            dataview.set_data(data, metadata)

            self.addTab(dataview, dataname)
            self.var_view_tables[dataname] = dataview
        if hasattr(dataview, 'data_modified_signal'):
            dataview.data_modified_signal.connect(lambda: self.lib.set_var(dataname, dataview.get_data()))
        self.setCurrentWidget(dataview)
        if raise_window:
            self.lib.UI.raise_dock_into_view('data_view_table')

    def on_tab_close_request(self, close_index: int):
        self.var_view_tables.pop(self.tabText(close_index))

        tab_to_close: 'QTextBrowser' = self.widget(close_index)
        tab_to_close.deleteLater()

        self.removeTab(close_index)
