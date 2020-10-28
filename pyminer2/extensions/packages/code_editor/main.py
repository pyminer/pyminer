#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from typing import Dict, Union

from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.dirname(__file__))

from pyminer2.extensions.extensionlib import BaseInterface, BaseExtension
from .codeeditor.tabwidget import PMCodeEditTabWidget
from .toolbar import PMEditorToolbar
from pmgwidgets import SettingsPanel, create_file_if_not_exist, load_json, dump_json
import json


class Extension(BaseExtension):
    def __init__(self):
        super(Extension, self).__init__()
        self.settings: Dict[str, Union[int, str]] = {}
        self.editor_widget: 'PMCodeEditTabWidget' = None

    def on_loading(self):
        self.load_settings()
        self.extension_lib.Program.add_translation('zh_CN', {'Editor': '编辑器'})

    def on_load(self):
        self.widgets['EditorsWidget'].extension_lib = self.extension_lib
        self.editor_widget = self.widgets['EditorsWidget']
        self.editor_widget.settings = self.settings
        self.extension_lib.Signal.get_settings_changed_signal().connect(self.change_theme)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.bind_event)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.change_theme)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.add_settings_panel)
        self.extension_lib.Signal.get_close_signal().connect(self.save_settings)

    def change_theme(self):
        theme = self.extension_lib.Program.get_settings()['theme']
        app = QApplication.instance()
        if theme.lower() in ('fusion', 'windows', 'windowsvista'):

            style_sheet = '\n' + """
               PMBaseEditor {
                   qproperty-theme: "tomorrow";
               }
               """
        else:
            style_sheet = '\n' + """
               PMBaseEditor {
                   qproperty-theme:  "tomorrow_night";
               }
               """
        app.setStyleSheet(app.styleSheet() + '\n' + style_sheet)

    def bind_event(self):

        self.extension_lib.get_interface('file_tree').add_open_file_callback('.py', self.new_script)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.c', self.new_script)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.cpp', self.new_script)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.h', self.new_script)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.pyx', self.new_script)

    def load_settings(self):
        settings = {'encoding_declaration_text': '# coding = utf-8',
                    'check_syntax_background': True,
                    'smart_autocomp_on': True,
                    'font_size': 12,
                    'wrap': True}
        config_path = os.path.join(os.path.dirname(__file__), 'customized', 'settings.json')
        create_file_if_not_exist(config_path, json.dumps(settings).encode('utf-8'))
        custom_settings = load_json(config_path)
        settings.update(custom_settings)
        self.settings = settings

    def add_settings_panel(self):
        settings = self.settings

        new_settings = [
            ('line_edit', 'encoding_declaration_text', 'Encoding Declaration', settings['encoding_declaration_text']),
            ('spin_box', 'font_size', 'Font Size', settings['font_size'], '', (5, 25), 1),
            ('bool', 'check_syntax_background', 'Check Syntax Background',
             settings['check_syntax_background']),
            ('bool', 'smart_autocomp_on', 'Smart Autocompletion', settings['smart_autocomp_on']),
            ('bool', 'wrap', 'Wrap', settings['wrap']),
        ]
        self.update_settings(settings)
        panel: 'SettingsPanel' = self.extension_lib.Program.add_settings_panel('Editor', new_settings)
        panel.signal_settings_changed.connect(self.update_settings)
        panel.get_ctrl('font_size').setEnabled(False)

    def update_settings(self, settings: dict):
        self.settings = settings
        self.editor_widget.update_settings(settings)
        # self.editor_widget.set_background_syntax_checking(settings['check_syntax_background'])
        # self.editor_widget.set_smart_autocomp_stat(settings['smart_autocomp_on'])

    def save_settings(self):
        config_path = os.path.join(os.path.dirname(__file__), 'customized', 'settings.json')
        dump_json(self.settings, config_path)

    def new_script(self, abs_path: str):
        self.editor_widget.slot_new_script(abs_path)

    def on_install(self):
        pass

    def on_uninstall(self):
        pass


class Interface(BaseInterface):
    pass


class EditorToolBar(PMEditorToolbar):
    pass


class EditorsWidget(PMCodeEditTabWidget):
    pass
