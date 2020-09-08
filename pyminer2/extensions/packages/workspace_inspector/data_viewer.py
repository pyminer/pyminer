import pprint
from typing import Dict, TYPE_CHECKING
from PyQt5.QtWidgets import QTabWidget, QTextBrowser, QWidget, QTableWidget
from pyminer2.ui.generalwidgets import PMDockObject
from pmgwidgets import PMTableView, PMGTableWidget

if TYPE_CHECKING:
    from pyminer2.ui.generalwidgets import PMDockWidget
    from pyminer2.extensions import extensionlib
    from pyminer2.extensions.extensionlib.extension_lib import extension_lib


class AbstractViewer(object):
    @staticmethod
    def is_valid(data) -> bool:
        return True

    def set_data(self, data: object, metadata: dict):
        pass


class PDDataViewer(PMTableView, AbstractViewer):
    def __init__(self, parent=None):
        PMTableView.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data):
        import numpy as np
        return isinstance(data, np.ndarray)

    def set_data(self, data: object, metadata: dict = None):
        super().set_data(data)


class NPDataViewer(PMTableView, AbstractViewer):
    def __init__(self, parent=None):
        PMTableView.__init__(parent)
        AbstractViewer.__init__(parent)

    @staticmethod
    def is_valid(data):
        import numpy
        return isinstance(data, numpy.ndarray)

    def set_data(self, data: object, metadata: dict = None):
        super(NPDataViewer, self).set_data(data)


class GeneralIterableViewer(PMGTableWidget, AbstractViewer):
    def __init__(self, parent=None):
        PMGTableWidget.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data: object):
        import numpy,pandas
        if isinstance(data,numpy.ndarray) or isinstance(data,pandas.DataFrame):
            return False
        return PMGTableWidget.check_data_can_be_displayed_by_table(data=data)

    def set_data(self, data: 'np.ndarray', metadata: dict = None):
        super().set_data_2d(data)


class GeneralObjectViewer(QTextBrowser, AbstractViewer):
    def __init__(self, parent=None):
        QTextBrowser.__init__(self, parent)
        AbstractViewer.__init__(self)

    @staticmethod
    def is_valid(data: object):
        import numpy,pandas
        if isinstance(data,numpy.ndarray) or isinstance(data,pandas.DataFrame):
            return False
        elif GeneralIterableViewer.is_valid(data):
            return False
        return True

    def set_data(self, data: object, metadata: dict = None):
        self.setText('value:\n\n   ' + pprint.pformat(data)
                     + '\n\n\nmeta data:\n\n' + pprint.pformat(metadata))


viewer_classes = [PDDataViewer, NPDataViewer, GeneralIterableViewer, GeneralObjectViewer]


def build_viewer(data: object, metadata: object) -> 'QWidget':
    for viewer_class in viewer_classes:
        if viewer_class.is_valid(data):
            viewer = viewer_class()
            viewer.set_data(data, metadata)

            return viewer


class PMVariableViewerWidget(QTabWidget, PMDockObject):
    '''
    在这里采用了多继承的方式。注意，一定要把PMDockObject写在右边。
    '''
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
        self.lib = lib

        def on_modification(varname: str, variable):
            if varname in self.var_view_tables:
                self.show_data(varname, raise_window=False)

        def on_deletion(varname: str):
            if varname in self.var_view_tables:
                self.removeTab(varname)
                self.var_view_tables.pop(varname)

        self.lib.on_modification(on_modification)
        self.lib.on_deletion(on_deletion)

    def show_data(self, dataname: str, raise_window=True):
        '''
        显示数据，显示数据之后，使得上层控件将其提升到上层可见。特别适用于几个dockwidget叠在一起的情况。
        :param dataname:
        :return:
        '''

        try:
            dataview: 'QWidget' = self.var_view_tables.get(dataname)
            data = self.lib.get_var(dataname)
            metadata = self.lib.get_data_info(dataname)
        except:
            return
        last_index = self.count()
        if dataview is not None:
            if dataview.is_valid(data):
                dataview.set_data(data, metadata)
            else:
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

        self.setCurrentWidget(dataview)
        if raise_window:
            self.lib.UI.raise_dock_into_view('data_view_table')

    def on_tab_close_request(self, close_index: int):
        self.var_view_tables.pop(self.tabText(close_index))

        tab_to_close: 'QTextBrowser' = self.widget(close_index)
        tab_to_close.deleteLater()

        self.removeTab(close_index)
