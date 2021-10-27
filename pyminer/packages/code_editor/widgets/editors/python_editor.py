#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/9/7
@author:Irony，侯展意
@email:
@file: pythoneditor
@description: Code Editor

输入 ### 开头的行，可以触发运行一个模块的功能。
输入if __name__=='__main__':可以触发运行全部代码的功能。
按照PyMiner控件协议，输入# mkval后面接widgets控件表达式，可以触发控件编辑按钮。
"""
# -*- coding:utf-8 -*-
#
# 代码高亮部分来源：
# https://blog.csdn.net/xiaoyangyang20/article/details/68923133
#
# 窗口交互逻辑为本人原创，转载请注明出处！
#
# 自动补全借用了Jedi库，能够达到不错的体验。
# 文本编辑器采用了一个QThread作为后台线程，避免补全过程发生卡顿。后台线程会延迟结果返回，
# 返回时如果光标位置未发生变化，则可以显示补全菜单，否则认为文本已经改变，就应当进行下一次补全操作。

# @Time: 2021/1/18 8:03
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: editor.py

import ast
import json
import logging
import os
import re
from functools import cached_property
from pathlib import Path
from typing import List, Tuple, Optional, TYPE_CHECKING, Callable

from PySide2.QtCore import SignalInstance, Signal, QDir
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMessageBox

from widgets import in_unit_test, PMGOneShotThreadRunner, run_python_file_in_terminal, parse_simplified_pmgjson, \
    PMGPanelDialog
from .base_editor import PMBaseEditor
from ..text_edit.python_text_edit import PMPythonCodeEdit
from ...utils.highlighter.python_highlighter import PythonHighlighter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PMPythonEditor(PMBaseEditor):
    """
    自定义编辑器控件
    """
    signal_goto_definition: SignalInstance = Signal(str, int, int)

    SHOW_AS_ERROR = {'E999'}
    SHOW_AS_WARNING = set()
    SHOW_AS_INFO = {'F841', 'F401', 'F403', 'F405', 'E303'}  # 分别是变量导入未使用、定义未使用、使用*导入以及无法推断可能由*导入的类型。
    help_runner: 'PMGOneShotThreadRunner'

    text_edit_class = PMPythonCodeEdit
    if TYPE_CHECKING:
        tr: Callable[[str], str]

    def __init__(self, parent=None):
        super(PMPythonEditor, self).__init__(parent)  # , comment_string='# ')
        self.browser_id = None
        self._parent = parent
        self.last_hint = ''

    def stop_auto_complete_thread(self):
        logger.info('autocomp stopped')
        self.text_edit.auto_complete_thread.on_exit()

    @cached_property
    def flake8_translations(self):
        """Flake8的翻译内容"""
        with open(Path(__file__).parent.parent.parent.absolute() / 'assets' / 'flake8_trans.json', 'rb') as f:
            result = json.load(f)
        return result

    def set_indicators(self, msgs: List[Tuple[int, int, str, str]], clear=True):
        """
        设置 error warning info 指示器

        :param msgs: 消息数组
        :param clear: 是否清空之前的标记
        :type msgs: Options[list, str]
        :type clear: bool
        :return:
        """
        logger.info(msgs)
        if in_unit_test():
            var_names_in_workspace = set()
        else:
            var_names_in_workspace = set(self.extension_lib.Data.get_all_public_variable_names())
        logger.debug(str(msgs))
        # 清除所有效果
        if clear:
            self.text_edit.clear_highlight()
        if not isinstance(msgs, (tuple, list)):
            return
        for msg in msgs:
            from_line, to_col, n_type, desc = msg
            marker_type = self.get_number_and_f_color(n_type)
            # 把检测详情封装
            # e_msg = ''.join(s_msg[3:])
            e_msg = self.get_message(n_type, desc, var_names_in_workspace=var_names_in_workspace)
            if e_msg == '':
                continue
            self.text_edit.register_highlight(from_line - 1, to_col - 1, -1, marker_type, e_msg)

        self.text_edit.rehighlight()

    def get_message(self, msgid: str, msg: str, var_names_in_workspace: set) -> str:
        """获取报错信息

        Args:
            msgid: error type such as 'F821'
            msg: message content such as 'xxxxxx'
            var_name_in_workspace:set such as {'a','b','c'}

        Returns:信息。也可能返回空字符串''。

        """
        try:
            matches = re.findall('\'.*?\'', msg)
            if msgid == 'F821' and len(matches) == 1 and matches[0].strip(
                    '\'') in var_names_in_workspace:  # 排除工作空间中已经定义的变量！
                return ''
            message = self.flake8_translations.get(msgid)
            if message is not None:
                try:
                    if len(matches) == 1:
                        try:
                            return message % matches[0]
                        except TypeError:
                            return f'{message}({matches[0]})'
                    else:
                        return message % matches
                except:
                    import traceback
                    traceback.print_exc()
                    return f'{message}({matches})'
            else:
                return msg
        except:
            import traceback
            traceback.print_exc()
            return msg

    def get_number_and_f_color(self, n_type: str) -> int:
        """
        返回警示类型。
        F开头的警告：
            F4xx是定义未引用、引用未定义等；
            F5xx是和字符串相关的问题；
            F6xx是和字典、参数解包、运算符相关的问题；
            F70x代表死循环、yield误用等，F72x代表doctest等等的问题。
            F8xx代表引用未定义、重复定义、函数参数重复。
            F9xx只有F901，代表NotImplementedError调用错误。
            具体链接可见：https://flake8.pycqa.org/en/latest/user/error-codes.html
        C开头的警告只有C901，代表圈复杂度太高。(目前似乎没调通。)
        E开头的警告除了E999之外都是和格式有关的警告。参考见这里：https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
            E1:缩进；
            E2:空格；
            E3:空行；
            E4：引用格式（单行多引用、多行单引用）
            E5:行长度
            E7：这个就是列的长度。
            E9:语法错误或者输入输出错误。
        除了E999之外其余E警告，都不是太重要，不妨忽略之。
        W开头的警告通常比较严重。
        :param n_type:
        :return:
        """
        if n_type in self.SHOW_AS_ERROR:
            return PythonHighlighter.ERROR
        elif n_type in self.SHOW_AS_INFO:
            return PythonHighlighter.HINT
        elif n_type in self.SHOW_AS_WARNING:
            return PythonHighlighter.WARNING

        if n_type.startswith('E'):
            return PythonHighlighter.HINT
        elif n_type.startswith('W'):
            return PythonHighlighter.WARNING
        elif n_type.startswith('F'):
            return PythonHighlighter.ERROR
        else:
            return PythonHighlighter.HINT

    def get_editor_cell(self, line: int) -> Tuple[str, int]:
        """
        获取当前单元格的文字。
        :param line:
        :return:
        """
        text = self.text().strip()
        l = text.split('\n')
        cell_text = ''
        cell_lines = 0
        for i, line_str in enumerate(l[line:]):
            if i != 0:  # 跳过第一行，因其可能含有很多注释。
                if line_str.startswith('###'):
                    break
                else:
                    cell_text += line_str + '\n'
                    cell_lines += 1
        if in_unit_test():
            logger.info('cell text:\n' + cell_text)
        return cell_text, cell_lines

    def get_help_in_console(self):
        """在console中获取帮助"""

        def show_help(help_namelist):
            if len(help_namelist) > 0:
                full_name: str = help_namelist[0].full_name
                self.interfaces.ipython_console.run_command(f'help(\'{full_name}\')', hidden=False)
            else:
                return

        if self.help_runner is None or self.help_runner.is_running() == False:
            self.help_runner = PMGOneShotThreadRunner(callback=show_help)

    def get_help_namelist(self) -> List:
        """
        获取函数的帮助
        :return:
        """

        text = self.text()
        path = self._path.replace(os.sep, '/')
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            path = ''
        else:
            path = self._path
        try:
            import jedi
            script = jedi.Script(text, path=path)
            jedi_name_list = script.infer(self.text_edit.textCursor().blockNumber() + 1,
                                          self.text_edit.textCursor().positionInBlock())
        except Exception:
            import traceback
            traceback.print_exc()
            jedi_name_list = []
        if len(jedi_name_list) == 0:
            QMessageBox.warning(self.text_edit, self.tr('Help'),
                                self.tr('Cannot get name.\n' +
                                        'Maybe There is:\n' +
                                        '1、Syntax error in your code.\n' +
                                        '2、No word under text cursor.'), QMessageBox.Ok)
        return jedi_name_list

    def get_help(self):
        """
        获取函数的帮助
        :return:
        """

        def on_namelist_received(jedi_name_list):
            if len(jedi_name_list) > 0:
                full_name: str = jedi_name_list[0].full_name
                name: str = jedi_name_list[0].name
                if not in_unit_test():
                    path = 'https://cn.bing.com/search?q=%s' % full_name
                    if self.browser_id is None:
                        self.browser_id = self.interfaces.embedded_browser.open_url(url=path, side='right')
                    else:
                        self.browser_id = self.interfaces.embedded_browser.open_url(
                            url=path, browser_id=self.browser_id, side='right')
            else:

                return

        if self.help_runner is None or self.help_runner.is_running() == False:
            self.help_runner = PMGOneShotThreadRunner(self.get_help_namelist)
            self.help_runner.signal_finished.connect(on_namelist_received)

    def slot_goto_definition(self):
        """转到函数的定义"""
        jedi_name_list = self.get_help_namelist()
        if len(jedi_name_list) > 0:
            # full_name: str = jedi_name_list[0].full_name
            # name: str = jedi_name_list[0].name
            # jedi_name_list[0].get_definition_end_position(), full_name, jedi_name_list[0].goto_assignments()
            # jedi_name_list[0], jedi_name_list[0].line, 'definitoins!!!!!'
            if jedi_name_list[0].line is not None and jedi_name_list[0].line is not None:
                line, column = jedi_name_list[0].line, 0
                path = jedi_name_list[0].module_path
                self.signal_goto_definition.emit(path, line, column)
                logger.debug(f'{jedi_name_list},{path},{line},{column}')

    def slot_run_in_terminal(self):
        """在终端中运行代码

        调用程序的进程管理接口。
        """
        text = self.text().strip()
        if not text:
            return
        path = self._path

        run_python_file_in_terminal(path)

    def slot_run_cell(self, start_line: int):
        text, lines = self.get_editor_cell(start_line)
        if not text:
            return

        self._parent.slot_run_script(text, self.tr(
            f'Running Current Script Cell (Line {start_line + 1} to {start_line + lines + 1}).'))

    def slot_edit_widget_show(self, line):
        """处理显示设置控件的事件。"""

        def get_indent(line: str):
            for i, s in enumerate(line):
                if s != ' ':
                    return i

        code = self.text().split('\n')[line]
        if len(re.findall(r'.*=.*#[ \t]*(?:mkval|mkvar)[ \t]*\[.*\]', code)) > 0:
            splitted = code.split('#')
            if len(splitted) == 2:
                assign_expr, mkvar_expr = splitted
                indentation = get_indent(assign_expr)
                try:
                    val = self.check_mkval_expr(code)
                    if val is not None:
                        identifier, data, params = val
                        l = parse_simplified_pmgjson(identifier, data, params)
                        if l is None:
                            return
                        dlg = PMGPanelDialog(parent=self, views=[l], with_spacer=False)
                        dlg.exec_()
                        vals = dlg.panel.get_value()
                        for k, v in vals.items():
                            line_text = ' ' * indentation + '%s = %s #%s' % (k, repr(v), mkvar_expr)
                            break
                        line_text_list = self.text().split('\n')
                        line_text_list[line] = line_text
                        first_visible_line = self.text_edit.first_visible_line_number
                        cursor_pos = self.text_edit.get_cursor_position()
                        text = '\n'.join(line_text_list)
                        self.set_text(text)
                        self.set_marker_for_run()
                        self.text_edit.setCursorPosition(line, cursor_pos[1])
                        self.text_edit.setFirstVisibleLine(first_visible_line)
                    else:
                        QMessageBox.warning(self, '警告', '控件创建命令\n\"%s\"\n格式错误。' % mkvar_expr)
                        return
                except:
                    import traceback
                    traceback.print_exc()
                    pass

    def check_mkval_expr(self, code: str) -> Optional[Tuple[str, object, List[object]]]:
        """
        判断一行是否满足mkval的需求。
        :param code:
        :return:
        """
        if len(re.findall(r'.*=.*#[ \t]*(?:mkval|mkvar)[ \t]*\[.*\]', code)) > 0:
            splitted = code.split('#')
            if len(splitted) == 2:
                assign_expr, mkvar_expr = splitted
                if len(assign_expr.split('=')) == 2:
                    assign_expr_splitted = assign_expr.split('=')
                    if assign_expr_splitted[0].strip().isidentifier():
                        identifier: str = assign_expr_splitted[0].strip()
                        value_str = assign_expr_splitted[1].strip()
                        if identifier != '' and value_str != '':
                            params_str = re.findall('\[.*\]', mkvar_expr)
                            try:
                                params = ast.literal_eval(params_str[0].strip())
                                data = ast.literal_eval(value_str)
                                return identifier, data, params
                            except:
                                import traceback
                                traceback.print_exc()
        return None

    # def update_api(self, hint: str, pos: tuple):
    #     if (len(self.last_hint) > len(hint) or hint == '') and not self.ends_with_dot():
    #         self.last_hint = hint
    #         return
    #     self.last_hint = hint
    #
    #     path = self._path.replace(os.sep, '/')
    #     if path.startswith(QDir.tempPath().replace(os.sep, '/')):
    #         path = ''
    #     else:
    #         path = self._path
    #     self.completer.worker.set_scan_task(code=self.text_edit.text(), line=pos[0], col=pos[1], path=path)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop_auto_complete_thread()

    def instant_boot(self):
        self.interfaces.application_toolbar.create_instant_boot_python_file_process(self.path())
