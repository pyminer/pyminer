import os

from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, Union

from PyQt5.QtCore import QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget

if TYPE_CHECKING:
    from pmgwidgets import PMGToolBar
    # from pyminer2.extensions.packages.ipython_console.main import ConsoleWidget


def wrapper():
    from pyminer2.extensions.extensions_manager.manager import extensions_manager
    from pyminer2.workspace.datamanager.datamanager import data_manager
    from pyminer2.workspace.datamanager.converter import ConvertError
    from pyminer2.workspace.datamanager.exceptions import ConflictError, NotFoundError
    from pyminer2.workspace.datamanager.metadataset import WouldBlockError
    from pyminer2.pmutil import get_root_dir, get_main_window, get_application
    from pyminer2.ui import pmwidgets
    from pyminer2.extensions.extensionlib import baseext
    from pyminer2.ui.common.locale import pmlocale
    from pyminer2.features.io.settings import Settings

    class ExtensionLib:
        pm_widgets = pmwidgets
        BaseInterface = baseext.BaseInterface
        BaseExtension = baseext.BaseExtension

        def get_interface(self, name):
            return extensions_manager.get_extension(name).public_interface

        def insert_widget(self, widget, insert_mode, config=None):
            return extensions_manager.ui_inserters[insert_mode](
                widget, config)

        def get_main_program_dir(self):
            return get_root_dir()

        class UI():
            @staticmethod
            def get_toolbar(toolbar_name: str) -> 'PMGToolBar':
                tb = get_main_window().toolbars.get(toolbar_name)

                return tb

            @staticmethod
            def get_toolbar_widget(toolbar_name: str, widget_name: str) -> 'QWidget':
                toolbar = ExtensionLib.UI.get_toolbar(toolbar_name)
                if toolbar is not None:
                    widget = toolbar.get_control_widget(widget_name)
                    return widget
                return None

            @staticmethod
            def _(text):
                return pmlocale.translate(text)

            @staticmethod
            def add_translation_file(file_name: str) -> None:
                get_application().trans.load(file_name)

            @staticmethod
            def get_main_window_geometry() -> 'QRect':
                return get_main_window().geometry()

            @staticmethod
            def raise_dock_into_view(dock_widget_name: str):
                return get_main_window().raise_dock_into_view(dock_widget_name)

            @staticmethod
            def get_default_font():
                app = get_main_window()
                return os.path.join(app.font_dir, app.default_font)

            @staticmethod
            def switch_toolbar(toolbar_name: str, switch_only: bool = True):
                app = get_main_window()
                app.switch_toolbar(toolbar_name, switch_only)

        class Signal():
            @staticmethod
            def get_close_signal():
                return get_main_window().close_signal

            @staticmethod
            def get_window_geometry_changed_signal():
                return get_main_window().window_geometry_changed_signal

            @staticmethod
            def get_layouts_ready_signal():
                return get_main_window().layouts_ready_signal

            @staticmethod
            def get_widgets_ready_signal():
                return get_main_window().widgets_ready_signal

            @staticmethod
            def get_events_ready_signal():
                return get_main_window().events_ready_signal

            @staticmethod
            def get_settings_changed_signal() -> 'pyqtSignal':
                return get_main_window().settings_changed_signal

        class Program():
            @staticmethod
            def add_settings_panel(text: str, panel_content: List[Tuple[str, str]]):
                """
                添加设置面板
                :param text:
                :param panel_content:
                :return:
                """
                return get_main_window().main_option_form.add_settings_panel(text, panel_content)

            @staticmethod
            def show_log(level: str, module: str, content: str):
                """
                在日志窗口显示log。
                :param level: 类型，比如‘info’
                :param module: 模块。比如'Jupyter'
                :param content: 内容。自定义的字符串
                :return:
                效果：
                调用——PluginInterface.show_log('info','CodeEditor','新建文件')
                输出——2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
                """
                get_main_window().slot_flush_console(level, module, content)

            def get_main_program_dir(self):
                """
                获取主程序路径
                :return:
                """
                return get_root_dir()

            @staticmethod
            def add_translation(locale: str, text: dict):
                return pmlocale.add_locale(locale, text)

            @staticmethod
            def _(text):
                return pmlocale.translate(text)

            @staticmethod
            def get_settings() -> Dict[str, str]:
                return Settings.get_instance()

            @staticmethod
            def set_work_dir(work_dir: str) -> None:
                """
                设置当前工作路径
                """
                Settings.get_instance()['work_dir'] = work_dir

            @staticmethod
            def get_work_dir() -> str:
                """
                获取当前工作路径
                """
                return Settings.get_instance()['work_dir']

            @staticmethod
            def run_python_file(file_path: str):
                from pyminer2.features.util.platformutil import run_python_file_in_terminal
                run_python_file_in_terminal(file_path)

        class Data():
            @staticmethod
            def delete_variable(var_name: str, provider: str = 'unknown'):
                data_manager.delete_data(var_name, provider)

            @staticmethod
            def get_all_variable_names() -> List[str]:
                return list(data_manager.varset.keys())

            @staticmethod
            def get_all_public_variable_names() -> List[str]:
                return list(data_manager.get_all_public_var().keys())

            @staticmethod
            def get_all_variables() -> Dict[str, object]:
                return data_manager.get_all_var()

            @staticmethod
            def get_all_public_variables() -> Dict[str, object]:
                """
                获取所有的外部可访问变量。
                :return:
                """
                return data_manager.get_all_public_var()

            @staticmethod
            def add_data_changed_callback(callable: Callable) -> None:
                """
                添加数据改变时触发的回调函数
                :param callable:
                :return:
                """
                data_manager.on_modification(callable)

            @staticmethod
            def get_all_vars_of_type(types: Union[object, Tuple]):
                """
                按照类型过滤变量。
                :param types:
                :return:
                """
                return data_manager.get_vars_of_types(types)

        ########################
        # 以下属性与数据管理类相关。
        def get_all_var(self) -> dict:
            return data_manager.get_all_var()

        def get_var(self, varname: str) -> object:
            return data_manager.get_var(varname)

        def get_data_info(self, varname: str) -> dict:
            return data_manager.get_data_info(varname)

        def set_var_dict(self, variables: dict, provider='unknown', info_dict: dict = {}):
            data_manager.set_var_dict(variables, provider, info_dict)

        def set_var(self, varname: str, variable, provider='unknown', **info):
            data_manager.set_var(varname, variable, provider)

        def update_data_info(self, varname: str, **info):
            data_manager.update_data_info(varname, **info)

        def delete_data(self, varname: str):
            data_manager.delete_data(varname)

        def clear(self):
            data_manager.clear()

        def get_recyclebin(self) -> list:
            return data_manager.get_recyclebin()

        def restore(self, index: int):
            data_manager.restore(index)

        def cancel(self, varname: str):
            data_manager.cancel(varname)

        def redo(self, varname: str):
            data_manager.redo(varname)

        def read_data(self, varname: str) -> dict:
            return data_manager.read_data(varname)

        def write_data(self, varname: str, data: dict, provider='server'):
            data_manager.write_data(varname, data, provider)

        def lock_data(self, varname: str):
            data_manager.lock_data(varname)

        def on_modification(self, modification_callback: Callable):
            data_manager.on_modification(modification_callback)

        def on_deletion(self, deletion_callback):
            data_manager.on_deletion(deletion_callback)

        def get_converter_error(self) -> type:
            return ConvertError

        def get_conflict_error(self) -> type:
            return ConflictError

        def get_not_found_error(self) -> type:
            return NotFoundError

        def get_would_block_error(self) -> type:
            return WouldBlockError

    return ExtensionLib()


extension_lib = wrapper()
