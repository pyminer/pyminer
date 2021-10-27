import logging
import os
from typing import Dict, Union, TYPE_CHECKING

from .utils.base_object import CodeEditorBaseObject

if TYPE_CHECKING:
    pass

from lib.extensions.extensionlib import BaseInterface, BaseExtension
from .widgets.tab_widget import PMCodeEditTabWidget
from .widgets.debugger import PMDebugConsoleTabWidget
from .widgets.toolbar import PMEditorToolbar
from widgets import PMGPanel, load_json, dump_json

__prevent_from_ide_optimization = PMEditorToolbar  # 这一行的目的是防止导入被编辑器自动优化。
logger = logging.getLogger('code_editor')


class Extension(CodeEditorBaseObject, BaseExtension):
    editor_widget: 'PMCodeEditTabWidget'
    debuggers_widget: 'PMDebugConsoleTabWidget'

    def __init__(self):
        super(Extension, self).__init__()
        self.settings: Dict[str, Union[int, str]] = {}

    def on_loading(self):
        self.load_settings()

    def on_load(self):
        self.widgets["PMCodeEditTabWidget"].set_extension_lib(self.extension_lib)
        self.editor_widget = self.widgets["PMCodeEditTabWidget"]
        self.interface.editor_tab_widget = self.editor_widget
        self.editor_widget.settings = self.settings
        self.debuggers_widget = self.widgets['PMDebugConsoleTabWidget']
        self.debuggers_widget.signal_goto_file.connect(self.on_gotoline_requested)
        self.debuggers_widget.extension_lib = self.extension_lib
        self.editor_widget.set_debug_widget(self.debuggers_widget)
        self.on_settings_changed()

        self.extension_lib.Signal.get_settings_changed_signal().connect(self.on_settings_changed)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.bind_event)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.on_settings_changed)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.add_settings_panel)
        self.extension_lib.Signal.get_close_signal().connect(self.save_settings)

    def on_gotoline_requested(self, file_path: str, line_no: int):
        """
        前往某个点。
        :param file_path:
        :param line_no:
        :return:
        """
        self.editor_widget.slot_new_script(file_path)
        for index in range(self.editor_widget.count()):
            self.editor_widget.widget(index).remove_debug_indicator()
        current_widget = self.editor_widget.currentWidget()
        current_widget.goto_line(line_no)
        current_widget.add_debug_indicator(line_no - 1)

    def on_settings_changed(self):
        """
        处理设置项改变时候的事件
        Deal with events that settings changed.
        :return:
        """
        theme = self.extension_lib.Program.get_theme()
        work_dir = self.extension_lib.Program.get_work_dir()
        if theme != self.editor_widget._color_scheme:
            if theme.lower() in ('fusion', 'windows', 'windowsvista'):
                self.editor_widget.set_color_scheme('light')
            else:
                self.editor_widget.set_color_scheme('dark')
        logger.debug(f'Working directory: {work_dir}')
        self.editor_widget.on_work_dir_changed(work_dir)

    def bind_event(self):
        extensions = ('.py', '.c', '.cpp', '.h', '.pyx', '.md')
        [self.interfaces.file_tree.add_open_file_callback(ext, self.new_script) for ext in extensions]

    def load_settings(self):
        settings = {
            'encoding_declaration_text': '# coding = utf-8',
            'check_syntax_background': True,
            'smart_autocomp_on': True,
            'font_size': 12,
            'wrap': True,
            'key_comment': 'Ctrl+/',
            'key_format': 'Ctrl+Alt+L'
        }
        config_folder = self.extension_lib.Program.get_plugin_data_path('code_editor')
        config_path = os.path.join(config_folder, 'settings.json')
        try:
            custom_settings = load_json(config_path)
            settings.update(custom_settings)
        except FileNotFoundError:
            pass
        self.settings = settings

    def add_settings_panel(self):
        """向主界面的设置面板插入一个设置页面，并且按照设置数据来更新设置。"""
        settings = self.settings

        new_settings = [
            ('line_ctrl', 'encoding_declaration_text', '编码声明', settings['encoding_declaration_text']),
            ('numberspin_ctrl', 'font_size', '字体大小', settings['font_size'], '', (5, 25), 1),
            ('check_ctrl', 'check_syntax_background', '后台语法检查',  # Check Syntax Background',
             settings['check_syntax_background']),
            ('check_ctrl', 'smart_autocomp_on', '智能自动补全（jedi）', settings['smart_autocomp_on']),
            ('check_ctrl', 'wrap', '自动换行', settings['wrap']),
            ('keymap_ctrl', 'key_comment', '注释/取消注释快捷键', settings['key_comment']),
        ]
        self.update_settings(settings)
        panel: 'PMGPanel' = self.extension_lib.Program.add_settings_panel('编辑器', new_settings)
        panel.signal_settings_changed.connect(self.update_settings)
        panel.get_ctrl('font_size').setEnabled(False)

    def update_settings(self, settings: dict):
        self.settings = settings
        self.editor_widget.update_settings(settings)
        # self.editor_widget.set_background_syntax_checking(settings['check_syntax_background'])
        # self.editor_widget.set_smart_autocomp_stat(settings['smart_autocomp_on'])

    def save_settings(self):
        config_folder = self.extension_lib.Program.get_plugin_data_path('code_editor')
        config_path = os.path.join(config_folder, 'settings.json')
        dump_json(self.settings, config_path)

    def new_script(self, abs_path: str):
        self.editor_widget.slot_new_script(abs_path)

    def on_install(self):
        pass

    def on_uninstall(self):
        pass


class Interface(BaseInterface):
    editor_tab_widget: 'PMCodeEditTabWidget'

    def open_script(self, path: str):
        self.editor_tab_widget.slot_new_script(path)

    def goto_file(self, path: str, row: int):
        self.editor_tab_widget.slot_goto_file(path, row, 0)
