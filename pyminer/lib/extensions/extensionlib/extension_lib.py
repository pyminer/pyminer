import inspect
import os
from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, Optional, Any

from PySide2.QtCore import QRect, Signal
from PySide2.QtWidgets import QWidget, QDialog

import utils
from lib.extensions.extensionlib import baseext
from lib.extensions.extensions_manager.manager import extensions_manager
from lib.io.exceptions import PMExceptions
from lib.ui import pmwidgets
from lib.workspace.data_adapter import UniversalAdapter
from lib.workspace.data_manager import data_manager
from lib.workspace_old.datamanager.datamanager import data_manager as  data_manager_old
from lib.comm.base import DataDesc
from utils import get_main_window

if TYPE_CHECKING:
    from widgets import PMGToolBar


class ExtensionLib:
    pm_widgets = pmwidgets
    BaseInterface = baseext.BaseInterface
    BaseExtension = baseext.BaseExtension

    @staticmethod
    def get_interface(name: str) -> BaseInterface:
        """获取名为 ``name`` 的插件的公共接口（由interface定义）

        Args:
            name: 插件名称
        """
        return extensions_manager.get_extension(name).public_interface

    @staticmethod
    def insert_widget(widget, insert_mode, config=None):
        """
        在主界面上插入一个控件。
        Args:
            widget:
            insert_mode:
            config:

        Returns:

        """
        return extensions_manager.ui_inserters[insert_mode](
            widget, config)

    @staticmethod
    def get_main_program_dir():
        """
        获取主程序的根目录
        Returns:

        """
        return utils.get_root_dir()

    class UI:
        @staticmethod
        def widget_exists(widget_name: str) -> bool:
            if widget_name in get_main_window().dock_widgets.keys():
                return True
            else:
                return False

        @staticmethod
        def get_toolbar(toolbar_name: str) -> 'PMGToolBar':
            """
            获取工具栏

            Args:
                toolbar_name:工具栏名称

            Returns:

            """
            tb = get_main_window().toolbars.get(toolbar_name)

            return tb

        @staticmethod
        def get_toolbar_widget(toolbar_name: str, widget_name: str) -> Optional['QWidget']:
            """
            获取工具栏上的控件（按钮等）

            Args:
                toolbar_name:工具栏名称
                widget_name:工具栏上的控件名称

            Returns:

            """
            toolbar = ExtensionLib.UI.get_toolbar(toolbar_name)
            if toolbar is not None:
                widget = toolbar.get_control_widget(widget_name)
                return widget
            return None

        @staticmethod
        def get_main_window_geometry() -> 'QRect':
            """
            获取主界面的尺寸

            Returns:

            """
            return get_main_window().geometry()

        @staticmethod
        def raise_dock_into_view(dock_widget_name: str) -> None:
            """
            将界面上的控件提升到可视的位置

            Args:
                dock_widget_name:

            Returns:

            """
            return get_main_window().raise_dock_into_view(dock_widget_name)

        @staticmethod
        def get_default_font() -> str:
            """
            获取默认字体文件

            Returns: Filepath of font.

            """
            app = get_main_window()
            return os.path.join(app.font_dir, app.default_font)

        @staticmethod
        def switch_toolbar(toolbar_name: str, switch_only: bool = True):
            """
            切换工具栏

            Args:
                toolbar_name:
                switch_only:

            Returns:

            """
            app = get_main_window()
            app.switch_toolbar(toolbar_name, switch_only)

        @staticmethod
        def exec_dialog(dlg: QDialog):
            assert isinstance(dlg, QDialog)
            win = get_main_window()
            dlg.setParent(win)
            dlg.exec_()

    class Signal:
        @staticmethod
        def get_close_signal() -> Signal:
            """
            获取关闭信号

            Returns:

            """
            return get_main_window().close_signal

        @staticmethod
        def get_window_geometry_changed_signal():
            """
            获取窗口位置和尺寸变化的事件

            Returns:

            """
            return get_main_window().window_geometry_changed_signal

        @staticmethod
        def get_layouts_ready_signal():
            """
            获取布局加载完毕的事件

            Returns:

            """
            return get_main_window().layouts_ready_signal

        @staticmethod
        def get_widgets_ready_signal():
            """
            获取控件加载完毕的事件

            Returns:

            """
            return get_main_window().widgets_ready_signal

        @staticmethod
        def get_events_ready_signal():
            """
            获取界面信号和事件绑定完毕的事件。

            Returns:

            """
            return get_main_window().events_ready_signal

        @staticmethod
        def get_settings_changed_signal() -> 'Signal':
            """
            获取设置发生变化时的事件。

            Returns:

            """
            return get_main_window().settings_changed_signal

    class Program:
        @staticmethod
        def add_settings_panel(text: str, panel_content: List[Tuple[str, str]]):
            """
            添加设置面板

            Args:
                text:
                panel_content:

            Returns:

            """

            return get_main_window().main_option_form.add_settings_panel(text, panel_content)

        @staticmethod
        def show_log(level: str, module: str, content: str) -> None:
            """
            调用——PluginInterface.show_log('info','CodeEditor','新建文件')
            输出——2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
            Args:
                level: 类型，比如‘info’
                module: 模块。比如'Jupyter'
                content: 内容。自定义的字符串

            Returns:
            """
            get_main_window().slot_flush_console(level, module, content)

        @staticmethod
        def get_main_program_dir():
            """
            获取主程序路径

            Returns:

            """
            return utils.get_root_dir()

        @staticmethod
        def get_settings_item_from_file(file: str, item: str, mode: str = "user"):
            """
            从设置文件中获取设置项
            Args:
                file:
                item:
                mode:

            Returns:

            """
            return utils.get_settings_item_from_file(file, item, mode)

        @staticmethod
        def write_settings_item_to_file(file: str, item: str, value: Any):
            """
            将配置项写入设置文件中
            Args:
                file:
                item:
                value:

            Returns:

            """
            utils.write_settings_item_to_file(file, item, value)
            get_main_window().settings_changed_signal.emit()

        @staticmethod
        def set_work_dir(work_dir: str) -> None:
            """
            设置当前工作路径

            Args:
                work_dir:

            Returns:

            """
            utils.write_settings_item_to_file("config.ini", "MAIN/PATH_WORKDIR", work_dir)
            get_main_window().settings_changed_signal.emit()

        @staticmethod
        def get_work_dir() -> str:
            """
            获取当前工作路径

            Returns:

            """

            dir = utils.get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR")
            if (not isinstance(dir, str)) or (not os.path.exists(dir)):
                dir = os.path.join(os.path.expanduser("~"), "Desktop")
                utils.write_settings_item_to_file("config.ini", "MAIN/PATH_WORKDIR", dir)
            return dir

        @staticmethod
        def get_theme() -> str:
            """
            获取主题
            Returns:

            """
            return utils.get_settings_item_from_file("config.ini", "MAIN/THEME")

        @staticmethod
        def run_python_file(file_path: str, interpreter_path: str):
            """
            运行Python文件命令
            TODO: Write a shell console into pyminer.

            Args:
                file_path:

            Returns:

            """
            raise DeprecationWarning

        @staticmethod
        def get_plugin_data_path(plugins_name: str) -> str:
            """
            获取插件的数据文件路径
            Args:
                plugins_name:

            Returns:str，文件夹路径。

            """
            ext = extensions_manager.get_extension(plugins_name)
            # assert ext is not None, 'Extension named %s isn\'t exist!' % plugins_name
            path = os.path.join(os.path.expanduser('~'), '.pyminer', 'packages')
            if not os.path.exists(path):
                os.mkdir(path)
            plugin_data_path = os.path.join(path, plugins_name)
            if not os.path.exists(plugin_data_path):
                os.mkdir(plugin_data_path)
            return plugin_data_path

        @staticmethod
        def show_exception_occured_panel(error: BaseException, solution: str, solution_command: str = ''):
            """

            :param error:
            :param solution:
            :param solution_command:
            :return:
            """
            PMExceptions.get_instance().emit_exception_occured_signal(error, solution, solution_command)

    class Data:
        @staticmethod
        def get_adapter(key: str) -> UniversalAdapter:
            return data_manager[key]

        @staticmethod
        def clear():
            data_manager_old.clear()

        @staticmethod
        def delete_variable(var_name: str, provider: str = 'unknown'):
            """
            删除变量
            Args:
                var_name:
                provider:

            Returns:

            """
            data_manager_old.delete_data(var_name, provider)

        @staticmethod
        def get_all_variable_names() -> List[str]:
            """
            获取所有的变量名

            Returns:

            """
            return list(data_manager.container.keys())

        @staticmethod
        def get_all_public_variable_names() -> List[str]:
            """
            获取所有非保留的变量的名称

            Returns:

            """
            return list(data_manager_old.get_all_public_var().keys())

        @staticmethod
        def get_all_variables() -> Dict[str, object]:
            """
            获取全部变量（包含保留类型，可能返回结果比较乱，需要审慎使用）

            Returns:
            """
            return data_manager_old.get_all_var()

        @staticmethod
        def get_all_public_variables() -> Dict[str, object]:
            """
            获取所有的外部可访问变量。

            Returns:
            """
            return data_manager_old.get_all_public_var()

        @staticmethod
        def add_data_changed_callback(callback: Callable[[str, Any, str], None]) -> None:
            """
            添加数据改变时触发的回调函数

            Args:
                callback:

            Returns:None
            """
            assert callable(callback)
            assert len(
                list(inspect.signature(callback).parameters.keys())) == 3, 'Function args should be 3'
            data_manager_old.on_modification(callback)

        @staticmethod
        def remove_data_changed_callback(callback: Callable):
            if callback in data_manager_old.modification_callback_actions:
                data_manager_old.modification_callback_actions.remove(callback)
                print('removed callback!')

        @staticmethod
        def add_data_deleted_callback(deletion_callback: Callable[[str, str], None]):
            """
            绑定的函数，要求其输入的函数参数为两个。

            Args:
                deletion_callback:

            Returns:

            """
            assert callable(deletion_callback)
            assert len(
                list(inspect.signature(deletion_callback).parameters.keys())) == 2, 'Function args should be 2'
            data_manager_old.on_deletion(deletion_callback)

        @staticmethod
        def var_exists(var_name: str):
            """
            判断var_name对应的变量是否存在
            Args:
                var_name:

            Returns:

            """
            return var_name in data_manager

        @staticmethod
        def set_var(varname: str, variable, provider='unknown', **info):
            """

            Args:
                varname:
                variable:
                provider:
                **info:

            Returns:

            """
            assert isinstance(variable, DataDesc), \
                'variable name %s ,%s is not type DataDesc' % (varname, variable)
            data_manager_old.set_var(varname, variable, provider)

        @staticmethod
        def get_var(var_name: str) -> object:
            """

            Args:
                var_name:

            Returns:

            """
            raise DeprecationWarning
            # return get_var(var_name)

        @staticmethod
        def get_data_desc(var_name) -> DataDesc:
            desc = data_manager_old.get_var(var_name)
            assert isinstance(desc, DataDesc), repr(desc)
            return desc

        @staticmethod
        def update_var_dic(var_dic: dict, provider: str, metadata_dic: dict = None):
            """

            Args:
                var_dic:
                provider:
                metadata_dic:

            Returns:

            """
            raise DeprecationWarning

        @staticmethod
        def get_metadata(varname: str) -> dict:
            """

            Args:
                varname:

            Returns:

            """
            return data_manager_old.get_data_info(varname)

        @staticmethod
        def get_all_metadata() -> dict:
            """

            Returns:

            """
            d = {k: v for k, v in data_manager_old.metadataset.items()}
            return d


extension_lib = ExtensionLib()
