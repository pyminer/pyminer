import pprint
import threading
from typing import Dict, TYPE_CHECKING
from PySide2.QtWidgets import QTabWidget, QTextBrowser, QWidget

from lib.comm import get_var, set_var
from widgets import PMTableView, PMGTableWidget, PMDockObject, PMGTableViewer, PMGJsonTree

if TYPE_CHECKING:
    from lib.extensions.extensionlib.extension_lib import extension_lib


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
        # self.action_split_by_columns:QAction = self.table_view.menu.addAction('提取当前列')
        # self.action_split_by_columns.triggered.connect(self.split_by_columns)

    def split_by_columns(self):
        # row =
        # self.table_view.data
        print('splitted!')

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


class JsonViewer(PMGJsonTree, AbstractViewer):
    """
    树状图，专门显示dict型数据。
    """

    def __init__(self, parent=None):
        PMGJsonTree.__init__(self, parent)
        # AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data) -> bool:
        return isinstance(data, dict)

    def set_data(self, data: Dict[str, object], metadata: dict = None) -> None:
        self.set_data_dic({self.tr('Data:'): data})
        self.expandToDepth(1)


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


def get_viewer_class(data):
    for viewer_class in viewer_classes:
        if viewer_class.is_valid(data):
            return viewer_class


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

        self.variable_view_factory = None

    def is_temporary(self) -> bool:
        return True

    def get_widget_text(self) -> str:
        return self.tr('Variable Viewer')

    def set_lib(self, lib):
        '''
        设置回调函数。注意，只有主线程中才能刷新界面，否则将引起崩溃。
        :param varname:
        :param variable:
        :return:
        '''
        self.lib = lib

        def on_changed(varname: str, variable, source: str):
            if threading.current_thread() is threading.main_thread():
                if varname in self.var_view_tables:
                    self.show_data(varname, raise_window=False)

        def on_deletion(varname: str, provider: str):
            if threading.current_thread() is threading.main_thread():
                if varname in self.var_view_tables:
                    tab = self.var_view_tables.pop(varname)
                    index = self.indexOf(tab)
                    self.removeTab(index)

        self.lib.Data.add_data_changed_callback(on_changed)
        self.lib.Data.add_data_deleted_callback(on_deletion)

    def show_data(self, dataname: str, raise_window=True):
        """
        显示数据，显示数据之后，使得上层控件将其提升到上层可见。特别适用于几个dockwidget叠在一起的情况。
        如果与已有的数据不是同一种类型，就移除原先的，重建新的。
        :param dataname:
        :return:
        """
        from lib.comm.base import DataDesc
        desc: DataDesc = self.lib.Data.get_data_desc(dataname)
        if desc.big:
            data = get_var(dataname, preview=True)
        else:
            data = get_var(dataname)

        try:
            dataview: 'QWidget' = self.var_view_tables.get(dataname)
            metadata = self.lib.Data.get_metadata(dataname)
        except BaseException:
            import traceback
            traceback.print_exc()
            return
        last_index = self.count()
        if dataview is not None:
            if not isinstance(dataview, get_viewer_class(data)):
                index = self.indexOf(dataview)
                self.removeTab(index)
                last_index = index
                self.var_view_tables.pop(dataname)
                dataview = None

        if dataview is None:
            dataview = build_viewer(data, metadata)
            self.insertTab(last_index, dataview, dataname)
            self.addTab(dataview, dataname)
            self.var_view_tables[dataname] = dataview
        dataview.set_data(data, metadata)

        if hasattr(dataview, 'data_modified_signal'):
            def set_var_data_modified():
                set_var(dataname, dataview.get_data())

            dataview.data_modified_signal.connect(set_var_data_modified)

        dataview.setWindowTitle(dataname)
        dataview.windowTitleChanged.connect(self.on_tab_window_title_changed)

        self.setCurrentWidget(dataview)
        if raise_window:
            self.lib.UI.raise_dock_into_view('data_view_table')

    def on_tab_window_title_changed(self, title: str):
        widget = self.sender()
        self.setTabText(self.indexOf(widget), title)

    def on_tab_close_request(self, close_index: int):
        self.var_view_tables.pop(self.tabText(close_index))

        tab_to_close: 'QTextBrowser' = self.widget(close_index)
        tab_to_close.deleteLater()

        self.removeTab(close_index)
