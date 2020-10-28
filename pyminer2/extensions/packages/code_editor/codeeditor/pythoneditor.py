#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/9/7
@author:
@email:
@file: pythoneditor
@description: Code Editor
"""

__version__ = '0.1'

import logging
import os
import re
from typing import List

# TODO to remove (use extensionlib)
import jedi
import numpy
from PyQt5.Qsci import QsciLexerPython, QsciLexer
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QMessageBox, QMenu, QAction, QShortcut
from yapf.yapflib import py3compat, yapf_api

from .baseeditor import PMBaseEditor, PMAPI

# jedi.preload_module(numpy)

logger = logging.getLogger(__name__)


class PMPythonEditor(PMBaseEditor):
    """
    自定义编辑器控件
    """

    def __init__(self, parent=None):
        super(PMPythonEditor, self).__init__(parent, comment_string='#')
        self._extension_names.append('.py')
        self._init_editor()
        self._init_lexer(QsciLexerPython(self.textEdit))
        self._init_apis()
        self._init_actions()
        self._init_signals()
        # 编辑器主题
        self.slot_set_theme(self._theme)

        self.last_hint = ''

    def set_indicators(self, msgs, clear=True):
        """
        设置 error warning info 指示器

        :param msgs: 消息数组
        :param clear: 是否清空之前的标记
        :type msgs: Options[list, str]
        :type clear: bool
        :return:
        """
        logger.debug(str(msgs))
        # 清除所有效果
        if clear:
            # self.textEdit.clearAnnotations()
            self._indicator_dict.clear()
            lines = self.textEdit.lines()
            columns = self.textEdit.lineLength(lines - 1)
            self.textEdit.clearIndicatorRange(0, 0, lines, columns, self._indicator_error)
            self.textEdit.clearIndicatorRange(0, 0, lines, columns, self._indicator_warn)
            self.textEdit.clearIndicatorRange(0, 0, lines, columns, self._indicator_info)
        if not isinstance(msgs, (tuple, list)):
            return
        for msg in msgs:
            s_msg = msg.split(':')
            if len(s_msg) < 4:
                continue
            from_line, from_col, n_type = s_msg[:3]
            from_line, from_col = int(from_line) - 1, int(from_col) - 1
            # msg = ''.join(s_msg[3:])
            # try:
            #     matched = re.match(r'\s+["\'](.*?)["\']\s+', msg)  # 匹配可能出现的文字
            #     to_col = from_col + matched.end() - matched.start()
            # except Exception as e:
            #     logger.debug(str(e))
            to_col = self.textEdit.lineLength(from_line)
            to_col = to_col - 1 if to_col > 0 else 0
            number, f_color = (self._indicator_error, self.fc_red.name()) if n_type.startswith('E') else (
                self._indicator_warn, self.fc_purple.name()) if n_type.startswith('W') else (
                self._indicator_info,
                self.fc_black.name() if self.textEdit.lexer().paper(0).lightness() > 192 else '#ffffff')
            # 把检测详情封装
            e_msg = ''.join(s_msg[3:])
            if from_line not in self._indicator_dict:
                self._indicator_dict[from_line] = '<p><span style="color:{0};">{1}</span></p>'.format(f_color, e_msg)
            else:
                tmp = self._indicator_dict[from_line]
                tmp += '<p><span style="color:{0};">{1}</span></p>'.format(f_color, e_msg)
                self._indicator_dict[from_line] = tmp

            self.textEdit.fillIndicatorRange(from_line, 0, from_line, to_col, number)

    def _init_actions(self) -> None:
        super()._init_actions()
        self._action_help = QAction(self.tr('Function Help'), self.textEdit)
        self._action_help_in_console = QAction(self.tr('Help In Console'), self.textEdit)

        self._shortcut_help = QShortcut(Qt.Key_F1, self.textEdit)
        self._shortcut_help_in_console = QShortcut(Qt.Key_F2, self.textEdit)
        self._action_help.setShortcut(Qt.Key_F1)
        self._action_help_in_console.setShortcut(Qt.Key_F2)

    def _init_lexer(self, lexer: QsciLexer) -> None:
        """
        初始化语法解析器

        :return: None
        """
        super(PMPythonEditor, self)._init_lexer(lexer)

    def create_context_menu(self) -> 'QMenu':
        menu = super().create_context_menu()
        menu.addAction(self._action_help)
        menu.addAction(self._action_help_in_console)
        return menu

    def _init_signals(self) -> None:
        """
        初始化信号绑定

        :return: None
        """
        super(PMPythonEditor, self)._init_signals()
        self._shortcut_help.activated.connect(self.get_help)
        self._action_help.triggered.connect(self.get_help)
        self._shortcut_help_in_console.activated.connect(self.get_help_in_console)
        self._action_help_in_console.triggered.connect(self.get_help_in_console)

    def get_help_in_console(self):
        """
        在console中获取帮助
        :return:
        """
        jedi_name_list = self.get_help_namelist()
        if len(jedi_name_list) > 0:
            full_name: str = jedi_name_list[0].full_name
            self.extension_lib.get_interface('ipython_console').run_command('help(\'%s\')' % full_name, hidden=False)
        else:
            return

    def get_hint(self):
        pos = self.textEdit.getCursorPosition()
        text = self.textEdit.text(pos[0])
        try:
            line = text[:pos[1] + 1]
        except Exception as e:
            logger.debug(e)
            line = ''
        hint: str = re.split(r'[;,:\./ \\!&\|\*\+\s\(\)\{\}\[\]]', line)[-1].strip()
        return hint

    def ends_with_dot(self):
        """
        判断光标左侧的代码是否以‘.’符号结束
        :return:
        """
        pos = self.textEdit.getCursorPosition()
        text = self.textEdit.text(pos[0])

        if text.strip() != '':
            return text.strip()[-1] == '.'
        return False

    def get_help_namelist(self) -> List:
        """
        获取函数的帮助
        :return:
        """
        text = self.textEdit.text()
        path = self._path.replace(os.sep, '/')
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            path = ''
        else:
            path = self._path
        script = jedi.Script(text, path=path)
        cursor_position = self.textEdit.getCursorPosition()
        try:
            jedi_name_list = script.infer(cursor_position[0] + 1, cursor_position[1])
        except Exception:
            import traceback
            traceback.print_exc()
            jedi_name_list = []
        if len(jedi_name_list) == 0:
            QMessageBox.warning(self.textEdit, self.tr('Help'),
                                self.tr('Cannot find documentation.\n' +
                                        'Maybe There is:\n' +
                                        '1、Syntax error in your code.\n' +
                                        '2、No word under text cursor.'), QMessageBox.Ok)
        return jedi_name_list

    def get_help(self):
        """
        获取函数的帮助
        :return:
        """
        jedi_name_list = self.get_help_namelist()
        if len(jedi_name_list) > 0:
            full_name: str = jedi_name_list[0].full_name
            name: str = jedi_name_list[0].name
            print(full_name)
            if full_name.find('pyminer_algorithms')!=-1:
                # jedi_name_list
                # jedi_name_list[0].get_definition_start_position()
                # jedi_name_list[0].module_path
                print('name')
                self.extension_lib.get_interface('document_server').open_by_function_name(name)
                return
            else:
                self.extension_lib.get_interface('document_server').open_external_search_result(full_name)
        else:

            return

    def update_api(self, hint: str, pos: tuple):
        if (len(self.last_hint) > len(hint) or hint == '') and not self.ends_with_dot():
            self.last_hint = hint
            return
        self.last_hint = hint

        path = self._path.replace(os.sep, '/')
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            path = ''
        else:
            path = self._path
        script = jedi.Script(code=self.textEdit.text(), path=path)
        try:
            completions = script.complete(pos[0] + 1, pos[1] + 1, fuzzy=True)
        except ValueError:
            return
        l = [c.name for c in completions]
        self.set_api(l)

    def set_api(self, api_list):
        self._apis = PMAPI(self._lexer)  # QsciAPIs(self._lexer)
        for s in api_list:
            self._apis.add(s)
        self._apis.prepare()

    def slot_text_changed(self) -> None:
        """
        内容变化槽函数

        :return: None
        """
        if self._smart_autocomp_on:
            pos = self.textEdit.getCursorPosition()
            hint = self.get_hint()
            if (not hint.startswith(self.last_hint)) or self.last_hint == '':
                if not hint == '':
                    if hint[-1] not in ('(', ')', '[', ']', '{', '}', '\'', '\:', ';', '/', '\\'):
                        self.update_api(hint, pos)
                    else:
                        pass
                else:
                    self.update_api(hint, pos)
            elif self.ends_with_dot():
                self.update_api(hint, pos)

        super(PMPythonEditor, self).slot_text_changed()

    def slot_about_close(self, save_all=False) -> QMessageBox.StandardButton:
        """
        是否需要关闭以及保存

        :param save_all: 当整个窗口关闭时增加是否全部关闭
        :return:QMessageBox.StandardButton
        """
        return super(PMPythonEditor, self).slot_about_close(save_all)

    def slot_code_format(self):
        """
        格式化代码
        注意，格式化之前需要保存光标的位置，格式化之后再将光标设置回当前的位置。
        :return:
        """
        text = self.text().strip()
        prev_pos = self.textEdit.getCursorPosition()
        if not text:
            return
        text = py3compat.removeBOM(text)
        try:
            reformatted_source, _ = yapf_api.FormatCode(
                text,
                filename=self.filename(),
                # print_diff=True,
                style_config=os.path.join(os.path.dirname(__file__), 'config', '.style.yapf')
            )
            self.set_text(reformatted_source)
            self.textEdit.setCursorPosition(*prev_pos)
        except Exception as e:
            logger.warning(str(e))
            lines = re.findall(r'line (\d+)\)', str(e))
            row = -1
            if lines:
                # 跳转到指定行
                row = int(lines[0])
                row = row - 1 if row else 0
                col = self.textEdit.lineLength(row)
                self.textEdit.setCursorPosition(row, col - 1)
                # 标记波浪线
                self.textEdit.fillIndicatorRange(row, 0, row, col, self._indicator_error2)
            QMessageBox.critical(self, self.tr('Error'), str(e))
            if row > -1:
                # 清除被标记波浪线
                self.textEdit.clearIndicatorRange(row, 0, row, col, self._indicator_error2)

    def slot_code_sel_run(self):
        """
        运行选中代码

        :return:
        """
        text = self.text(True).strip()
        if not text:
            text = self.current_line_text().strip()

        try:
            self._parent.slot_run_sel(text)
        except Exception as e:
            logger.warning(str(e))

    def slot_code_run(self):
        """
        运行代码

        :return:
        """
        logger.warning('run code' + repr(self._parent))
        text = self.text().strip()
        if not text:
            return
        try:
            self._parent.slot_run_script(text)
        except Exception as e:
            logger.warning(str(e))

    def slot_run_in_terminal(self):
        """
        在终端中运行代码
        调用程序的进程管理接口。
        :return:
        """
        text = self.text().strip()
        if not text:
            return
        path = self._path
        try:
            self._parent.run_python_file_in_terminal(path)
        except Exception as e:
            logger.warning(str(e))
