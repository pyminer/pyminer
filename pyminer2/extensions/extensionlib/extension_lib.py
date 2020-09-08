from typing import TYPE_CHECKING, Callable, Dict

from PyQt5.QtCore import QRect, pyqtSignal

if TYPE_CHECKING:
    from pyminer2.extensions.packages.ipython_console.main import ConsoleWidget, ConsoleInterface
    from pyminer2.workspace.datamanager.datamanager import DataManager
    # from pyminer2.extensions.packages.ipython_console.main import ConsoleWidget


def wrapper():
    from pyminer2.extensions.extensions_manager.manager import extensions_manager
    from pyminer2.workspace.datamanager.datamanager import data_manager
    from pyminer2.pmutil import get_root_dir, get_main_window
    from pyminer2.ui import generalwidgets,pmwidgets
    from pyminer2.extensions.extensionlib import baseext
    class ExtensionLib:
        widgets = generalwidgets
        pm_widgets = pmwidgets
        BaseInterface = baseext.BaseInterface
        BaseExtension = baseext.BaseExtension

        def __init__(self):
            for item in dir(data_manager):
                member = data_manager.__getattribute__(item)
                if callable(member) and not item.startswith('_'):
                    self.__setattr__(item, member)

        def get_interface(self, name):
            return extensions_manager.get_ext_by_name(name).public_interface

        def insert_widget(self, widget, insert_mode, config=None):
            return extensions_manager.ui_inserters[insert_mode](
                widget, config)

        def get_main_program_dir(self):
            return get_root_dir()

        class UI():
            @staticmethod
            def get_main_window_geometry() -> 'QRect':
                return get_main_window().geometry()

            @staticmethod
            def raise_dock_into_view(dock_widget_name: str):
                return get_main_window().raise_dock_into_view(dock_widget_name)

        class Signal():
            @staticmethod
            def get_close_signal():
                return get_main_window().close_signal
            @staticmethod
            def get_resize_signal():
                return  get_main_window().resize_signal
            @staticmethod
            def get_layouts_ready_signal():
                return get_main_window().layouts_ready_signal
            @staticmethod
            def get_widgets_ready_signal():
                return get_main_window().widgets_ready_signal
            @staticmethod
            def get_events_ready_signal():
                return get_main_window().events_ready_signal

        class Program():
            @staticmethod
            def get_settings() -> Dict[str, str]:
                return get_main_window().settings

        ########################
        # 以下属性与数据管理类相关。这些方法是动态加载的，
        # 在这里定义只是为了方便各类IDE的自动补全和静态检查！
        def get_all_var(self) -> dict:
            pass

        def get_var(self, name: str) -> object:
            pass

        def get_data_info(self, varname: str) -> dict:
            pass

        def set_var_dict(self, variables: dict, provider='unknown', info_dict: dict = {}):
            pass

        def set_var(self, varname: str, variable, provider='unknown', **info):
            pass

        def update_data_info(self, varname: str, **info):
            pass

        def delete_data(self, varname: str):
            pass

        def get_recyclebin(self) -> list:
            pass

        def restore(self, index: int):
            pass

        def cancel(self, varname: str):
            pass

        def redo(self, varname: str):
            pass

        def read_data(self, varname: str) -> dict:
            pass

        def write_data(self, varname: str, data: dict, provider='server'):
            pass

        def lock_data(self, varname: str):
            pass

        def on_modification(self, modification_callback: Callable):
            pass

        def on_deletion(self, deletion_callback):
            pass

        def add_callbacks(self):
            pass

    return ExtensionLib()


extension_lib = wrapper()
