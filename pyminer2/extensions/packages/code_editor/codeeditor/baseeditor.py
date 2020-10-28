#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编辑器
编辑器构造参数：
{'language':'Python',
'ext_name':'.py',
'lexer':PythonLexer,
'builtin_keywords':['int','float',...],
'dynamic_keywords':['func','method',...]
}
常用功能：
1、批量缩进、批量取消缩进（语言无关）
2、整理格式（语言相关，需要对应语言进行重写）
3、在终端执行代码（语言相关：需要已知编译器或者解释器的路径。）
4、更新补全选项（语言无关）
5、复制、粘贴、剪切（语言无关）
6、批量注释、批量取消注释（未实现。注意，这部分功能比较复杂，需要该语言的注释符号）
7、查找、替换等（语言无关）
8、保存、打开（需要已知扩展名）
Created on 2020/9/7
@author: Irony
@email: 892768447@qq.com
@file: editor
@description: Code Editor
"""

__version__ = '0.1'

import logging
import os
import re
from itertools import groupby
from typing import TYPE_CHECKING

from PyQt5.Qsci import QsciScintilla, QsciAPIs, QsciLexer
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QDir, QEvent, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QKeySequence, QKeyEvent, QCursor
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QAction, QShortcut, QDialog, QVBoxLayout, QPushButton, \
    QHBoxLayout, QMenu, QToolTip
from lxml import etree

if TYPE_CHECKING:
    from pyminer2.extensions.packages.code_editor.codeeditor.tools import Utilities
    from pyminer2.extensions.packages.code_editor.codeeditor.ui.ui_formeditor import Ui_FormEditor
    from pyminer2.extensions.packages.code_editor.codeeditor.ui.ui_gotoline import Ui_DialogGoto
else:
    from codeeditor.tools import Utilities
    from codeeditor.ui.ui_formeditor import Ui_FormEditor
    from codeeditor.ui.ui_gotoline import Ui_DialogGoto
# TODO to remove (use extensionlib)

from pmgwidgets import SettingsPanel
import jedi
import numpy
import typing
from .syntaxana import filter_words

# jedi.preload_module(numpy)

logger = logging.getLogger(__name__)


class Commenter():

    def __init__(self, sci: QsciScintilla, comment_string: str):
        self.sci = sci
        self.comment_string = comment_string
        self.line_ending = "\n"

        sci.SendScintilla(self.sci.SCI_SETMULTIPLESELECTION, 1)
        sci.SendScintilla(self.sci.SCI_SETADDITIONALSELECTIONTYPING, True)
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_7), self.sci, self.toggle_commenting)

    def toggle_commenting(self):
        sci = self.sci

        # Check if the selections are valid
        selections = self.get_selections()
        if selections == None:
            return
        # Merge overlapping selections
        while self.merge_test(selections) == True:
            selections = self.merge_selections(selections)
        # Start the undo action that can undo all commenting at once
        sci.beginUndoAction()
        # Loop over selections and comment them
        for i, sel in enumerate(selections):
            if sci.text(sel[0]).lstrip().startswith(self.comment_string):
                self.set_commenting(sel[0], sel[1], self._uncomment)
            else:
                self.set_commenting(sel[0], sel[1], self._comment)
        # Select back the previously selected regions
        sci.SendScintilla(sci.SCI_CLEARSELECTIONS)
        for i, sel in enumerate(selections):
            start_index = sci.positionFromLineIndex(sel[0], 0)
            # Check if ending line is the last line in the editor
            last_line = sel[1]
            if last_line == sci.lines() - 1:
                end_index = sci.positionFromLineIndex(
                    sel[1], len(sci.text(last_line)))
            else:
                end_index = sci.positionFromLineIndex(
                    sel[1], len(sci.text(last_line)) - 1)
            if i == 0:
                sci.SendScintilla(sci.SCI_SETSELECTION,
                                  start_index, end_index)
            else:
                sci.SendScintilla(sci.SCI_ADDSELECTION,
                                  start_index, end_index)
        # Set the end of the undo action
        sci.endUndoAction()

    def get_selections(self):
        sci = self.sci

        # Get the selection and store them in a list
        selections = []
        for i in range(sci.SendScintilla(sci.SCI_GETSELECTIONS)):
            selection = (
                sci.SendScintilla(sci.SCI_GETSELECTIONNSTART, i),
                sci.SendScintilla(sci.SCI_GETSELECTIONNEND, i)
            )
            # Add selection to list
            from_line, from_index = sci.lineIndexFromPosition(selection[0])
            to_line, to_index = sci.lineIndexFromPosition(selection[1])
            selections.append((from_line, to_line))
        selections.sort()
        # Return selection list
        return selections

    def merge_test(self, selections):
        """
        Test if merging of selections is needed
        """
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i - 1][0]
            previous_end_line = selections[i - 1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            if previous_end_line == current_start_line:
                return True
        # Merging is not needed
        return False

    def merge_selections(self, selections):
        """
        This function merges selections with overlapping lines
        """
        # Test if merging is required
        if len(selections) < 2:
            return selections
        merged_selections = []
        skip_flag = False
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i - 1][0]
            previous_end_line = selections[i - 1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            # Test for merge
            if previous_end_line == current_start_line and skip_flag == False:
                merged_selections.append(
                    (previous_start_line, current_end_line)
                )
                skip_flag = True
            else:
                if skip_flag == False:
                    merged_selections.append(
                        (previous_start_line, previous_end_line)
                    )
                skip_flag = False
                # Add the last selection only if it was not merged
                if i == (len(selections) - 1):
                    merged_selections.append(
                        (current_start_line, current_end_line)
                    )
        # Return the merged selections
        return merged_selections

    def set_commenting(self, arg_from_line, arg_to_line, func):
        sci = self.sci

        # Get the cursor information
        from_line = arg_from_line
        to_line = arg_to_line
        # Check if ending line is the last line in the editor
        last_line = to_line
        if last_line == sci.lines() - 1:
            to_index = len(sci.text(to_line))
        else:
            to_index = len(sci.text(to_line)) - 1
        # Set the selection from the beginning of the cursor line
        # to the end of the last selection line
        sci.setSelection(
            from_line, 0, to_line, to_index
        )
        # Get the selected text and split it into lines
        selected_text = sci.selectedText()
        selected_list = selected_text.split("\n")
        # Find the smallest indent level
        indent_levels = []
        for line in selected_list:
            indent_levels.append(len(line) - len(line.lstrip()))
        min_indent_level = min(indent_levels)
        # Add the commenting character to every line
        for i, line in enumerate(selected_list):
            selected_list[i] = func(line, min_indent_level)
        # Replace the whole selected text with the merged lines
        # containing the commenting characters
        replace_text = self.line_ending.join(selected_list)
        sci.replaceSelectedText(replace_text)

    def _comment(self, line, indent_level):
        if line.strip() != "":
            return line[:indent_level] + self.comment_string + line[indent_level:]
        else:
            return line

    def _uncomment(self, line, indent_level):
        if line.strip().startswith(self.comment_string):
            return line.replace(self.comment_string, "", 1)
        else:
            return line


class PMAPI(QsciAPIs):

    def __init__(self, *args):
        super(PMAPI, self).__init__(*args)
        self.keywords = []

    def add(self, entry: str) -> None:
        super(PMAPI, self).add(entry)
        self.keywords.append(entry)

    def updateAutoCompletionList(self, context: typing.Iterable[str], var_list: typing.Iterable[str]) \
            -> typing.List[str]:
        li = filter_words(self.keywords, context[0])
        li += super(PMAPI, self).updateAutoCompletionList(context, var_list)
        return list(set(li))


class FindDialog(QDialog):
    def __init__(self, parent=None, text_edit: 'PMCodeEditor' = None):
        super(FindDialog, self).__init__(parent)
        self.text_editor = text_edit
        self.qsci_text_edit: 'QsciScintilla' = text_edit.textEdit
        views = [(str, 'text_to_find', self.tr('Text to Find'), ''),
                 (str, 'text_to_replace', self.tr('Text to Replace'), ''),
                 (bool, 'wrap', self.tr('Wrap'), True),
                 (bool, 'regex', self.tr('Regex'), False),
                 (bool, 'case_sensitive', self.tr('Case Sensitive'), True),
                 (bool, 'whole_word', self.tr('Whole Word'), True),
                 ]
        self.settings_panel = SettingsPanel(parent=self, views=views)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.settings_panel)
        self.button_up = QPushButton('up')
        self.button_down = QPushButton('dn')
        self.button_replace = QPushButton('replace')
        self.button_replace_all = QPushButton('replace all')

        self.button_up.clicked.connect(self.search_up)
        self.button_down.clicked.connect(self.search_down)
        self.button_replace.clicked.connect(self.replace_current)
        self.button_replace_all.clicked.connect(self.replace_all)

        self.button_bar = QHBoxLayout()
        self.button_bar.addWidget(self.button_up)
        self.button_bar.addWidget(self.button_down)
        self.button_bar.addWidget(self.button_replace)
        self.button_bar.addWidget(self.button_replace_all)
        self.button_bar.setContentsMargins(0, 0, 0, 0)
        self.layout().addLayout(self.button_bar)

    def search_up(self):
        settings = self.settings_panel.get_value()
        self.text_editor.search_word(forward=True, **settings)
        pass

    def search_down(self):
        """
        反方向查找。注意，简单的设置qsci的forward=False是不够的，还需要对位置进行处理。
        这似乎是QSciScintilla的bug.
        """
        settings = self.settings_panel.get_value()
        line, index = self.text_editor.textEdit.getSelection()[:2]
        self.text_editor.search_word(forward=False, **settings, line=line, index=index)

        pass

    def replace_current(self):
        text: str = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        if self.qsci_text_edit.hasSelectedText():
            self.qsci_text_edit.replace(text)

    def replace_all(self):
        settings = self.settings_panel.get_value()
        text_to_replace = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        while (1):
            b = self.text_editor.search_word(forward=True, **settings)
            if b:
                self.qsci_text_edit.replace(text_to_replace)
            else:
                break


class GotoLineDialog(QDialog, Ui_DialogGoto):
    """跳转指定行"""

    def __init__(self, editor: 'PMCodeEditor', *args, **kwargs):
        super(GotoLineDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.editor = editor
        self.buttonBox.accepted.connect(self.slot_accepted)
        line, column = editor.getCursorPosition()
        self.lineEdit.setText('%s:%s' % (line + 1, column + 1))
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()

    def slot_accepted(self):
        """
        跳转到对应行列
        :return:
        """
        text = re.findall(r'^\d+$|^\d+:\d+$', self.lineEdit.text().strip())
        if not text:
            return
        text = text[0]
        if text.find(':') == -1:
            text += ':0'
        try:
            line, column = text.split(':')
            self.editor.setCursorPosition(max(0, int(line) - 1), max(0, int(column) - 1))
            self.accept()
        except Exception as e:
            logger.warning(str(e))


class PMBaseEditor(QWidget, Ui_FormEditor):
    def __init__(self, parent=None, comment_string: str = '//'):
        super(PMBaseEditor, self).__init__(parent=parent)
        self._parent = self.parent()
        self.setupUi(self)

        self._lexer = None
        self._apis = None
        self._path = ''
        self._extension_names: typing.List[str] = []
        self._encoding = 'utf-8'
        self._action_format = None  # 格式化
        self._action_run_sel_code = None  # 运行选中代码
        self._action_run_code = None  # 运行代码
        self._shortcut_format = None
        self._shortcut_run = None
        self._shortcut_run_sel = None
        self._shortcut_goto = None
        self._indicator_error = -1
        self._indicator_error2 = -1
        self._indicator_warn = -1
        self._indicator_info = -1
        self._indicator_dict = {}  # 指示器记录
        self._smart_autocomp_on = True
        # 自定义属性用于控制QSS设置
        self._theme = 'tomorrow'

        # 代码检测后详情提示颜色
        self.fc_red = QColor(255, 23, 23)
        self.bc_red = QColor(255, 240, 240)
        self.fc_yellow = QColor(191, 153, 36)
        self.bc_yellow = QColor(255, 255, 240)
        self.fc_black = QColor(0, 0, 0)
        self.bc_black = QColor(239, 239, 239)
        self.fc_purple = QColor(197, 67, 153)
        self.bc_purple = QColor(255, 240, 255)

        self.extension_lib = None
        self.find_dialog: 'FindDialog' = None

        self.commenter = Commenter(self.textEdit, comment_string=comment_string)

    def update_settings(self, settings: typing.Dict[str, object]):
        wrap = settings['wrap']
        if wrap:
            self.textEdit.setWrapMode(QsciScintilla.WrapWord)
        else:
            self.textEdit.setWrapMode(QsciScintilla.WrapNone)
        self.set_smart_autocomp_stat(settings['smart_autocomp_on'])

    def set_smart_autocomp_stat(self, autocomp_on: bool) -> None:
        self._smart_autocomp_on = autocomp_on
        # self.textEdit.setAutoCompletionThreshold(0)

    def search_word(self, text_to_find: str, wrap: bool, regex: bool, case_sensitive: bool, whole_word: bool,
                    forward: bool, index=-1, line=-1, **kwargs):

        return self.textEdit.findFirst(text_to_find, regex, case_sensitive, whole_word, wrap, forward, line, index)

    def slot_cursor_position_changed(self, line: int, column: int) -> None:
        """
        光标变化槽函数

        :param line: 行
        :param column: 列
        :type line: int
        :type column: int
        :return: None
        """
        self.label_status_ln_col.setText(
            self.tr('Ln:{0}  Col:{1}').format(format(line + 1, ','), format(column + 1, ',')))

    def on_textedit_focusin(self, e):
        QsciScintilla.focusInEvent(self.textEdit, e)
        self.extension_lib.UI.switch_toolbar('code_editor_toolbar', switch_only=True)

    def _init_apis(self) -> None:
        """
        加载自定义智能提示文件

        :return: None
        """
        self._apis = QsciAPIs(self._lexer)
        # for path in Path(os.path.join(os.path.dirname(__file__), 'api')).rglob('*.api'):
        #     logger.info('load %s' % str(path.absolute()))
        #     self._apis.load(str(path.absolute()))
        try:
            # 添加额外关键词
            for word in self._parent.keywords():
                self._apis.add(word)
        except Exception as e:
            logger.warning(str(e))
        self._apis.prepare()

    def _init_editor(self) -> None:
        """
        初始化编辑器设置

        :return: None
        """
        self.label_status_ln_col.setText(self.tr('Ln:1  Col:1'))
        self.label_status_length.setText(self.tr('Length:0  Lines:1'))
        self.label_status_sel.setText(self.tr('Sel:0 | 0'))
        self.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        # 设置字体
        self.textEdit.setFont(QFont('Source Code Pro', 12))  # Consolas
        self.textEdit.setMarginsFont(self.textEdit.font())
        # 自动换行
        self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行
        self.textEdit.setWrapMode(QsciScintilla.WrapWord)  # 自动换行
        self.textEdit.setWrapVisualFlags(QsciScintilla.WrapFlagNone)
        self.textEdit.setWrapIndentMode(QsciScintilla.WrapIndentFixed)
        # 编码
        self.textEdit.setUtf8(True)
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF8)
        # 自动提示
        self.textEdit.setAnnotationDisplay(QsciScintilla.AnnotationBoxed)  # 提示显示方式
        self.textEdit.setAutoCompletionSource(QsciScintilla.AcsAll)  # 自动补全。对于所有Ascii字符
        self.textEdit.setAutoCompletionReplaceWord(True)
        self.textEdit.setAutoCompletionCaseSensitivity(False)  # 忽略大小写

        # self.textEdit.setAutoCompletionFillupsEnabled(True)
        self.textEdit.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        # self.textEdit.setAutoCompletionUseSingle(QsciScintilla.AcusAlways)
        # self.textEdit.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        self.textEdit.setAutoCompletionThreshold(1)  # 输入多少个字符才弹出补全提示
        # QsciScintilla.setAutoCompletionUseSingle()
        self.textEdit.setCallTipsPosition(QsciScintilla.CallTipsBelowText)  # 设置提示位置
        self.textEdit.setCallTipsStyle(QsciScintilla.CallTipsNoContext)  # 设置提示样式
        # 设置折叠样式
        self.textEdit.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)  # 代码折叠
        # self.textEdit.setFoldMarginColors(QColor(233, 233, 233), Qt.white)
        # 折叠标签颜色
        # self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK, QsciScintilla.SC_MARKNUM_FOLDERSUB,
        #                             QColor('0xa0a0a0'))
        # self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK, QsciScintilla.SC_MARKNUM_FOLDERMIDTAIL,
        #                             QColor('0xa0a0a0'))
        # self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK, QsciScintilla.SC_MARKNUM_FOLDERTAIL,
        #                             QColor('0xa0a0a0'))
        # 设置当前行背景
        self.textEdit.setCaretLineVisible(True)
        # self.textEdit.setCaretLineBackgroundColor(QColor(232, 232, 255))

        # 设置选中文本颜色
        # self.textEdit.setSelectionForegroundColor(QColor(192, 192, 192))
        # self.textEdit.setSelectionBackgroundColor(QColor(192, 192, 192))

        # 括号匹配
        self.textEdit.setBraceMatching(QsciScintilla.StrictBraceMatch)  # 大括号严格匹配
        # self.textEdit.setMatchedBraceBackgroundColor(Qt.blue)
        # self.textEdit.setMatchedBraceForegroundColor(Qt.white)
        # self.textEdit.setUnmatchedBraceBackgroundColor(Qt.red)
        # self.textEdit.setUnmatchedBraceForegroundColor(Qt.white)

        # 启用活动热点区域的下划线
        self.textEdit.setHotspotUnderline(True)
        self.textEdit.setHotspotWrap(True)

        # 缩进
        self.textEdit.setAutoIndent(True)  # 换行后自动缩进
        self.textEdit.setTabWidth(4)
        self.textEdit.setIndentationWidth(4)
        self.textEdit.setTabIndents(True)

        # 缩进指南
        self.textEdit.setIndentationGuides(True)
        self.textEdit.setIndentationsUseTabs(False)  # 不使用Tab
        self.textEdit.setBackspaceUnindents(True)  # 当一行没有其它字符时删除前面的缩进
        # self.textEdit.setIndentationGuidesForegroundColor(QColor(192, 192, 192))
        # self.textEdit.setIndentationGuidesBackgroundColor(Qt.white)

        # 显示行号
        self.textEdit.setMarginLineNumbers(0, True)
        self.textEdit.setMarginWidth(0, 50)
        self.textEdit.setMarginWidth(1, 0)  # 行号
        #  self.textEdit.setMarginWidth(2, 0)  # 折叠
        self.textEdit.setMarginWidth(3, 0)
        self.textEdit.setMarginWidth(4, 0)
        #  # 折叠区域
        #  self.textEdit.setMarginType(3, QsciScintilla.SymbolMargin)
        #  self.textEdit.setMarginLineNumbers(3, False)
        #  self.textEdit.setMarginWidth(3, 15)
        #  self.textEdit.setMarginSensitivity(3, True)

        # 设置空白字符显示
        self.textEdit.setWhitespaceSize(1)  # 可见的空白点的尺寸
        self.textEdit.setWhitespaceVisibility(QsciScintilla.WsVisible)  # 空白的可见性。默认的是空格是无形的
        # self.textEdit.setWhitespaceForegroundColor(QColor(255, 181, 106))

        # 设置右边边界线
        self.textEdit.setEdgeColumn(120)
        self.textEdit.setEdgeMode(QsciScintilla.EdgeLine)

        # 设置代码检测后波浪线
        self._indicator_error = self.textEdit.indicatorDefine(QsciScintilla.SquigglePixmapIndicator)
        self._indicator_error2 = self.textEdit.indicatorDefine(QsciScintilla.SquigglePixmapIndicator)
        self._indicator_warn = self.textEdit.indicatorDefine(QsciScintilla.SquigglePixmapIndicator)
        self._indicator_info = self.textEdit.indicatorDefine(QsciScintilla.SquigglePixmapIndicator)
        self.textEdit.setIndicatorForegroundColor(QColor(Qt.red), self._indicator_error)
        self.textEdit.setIndicatorForegroundColor(QColor(Qt.red), self._indicator_error2)
        self.textEdit.setIndicatorForegroundColor(QColor(244, 152, 16), self._indicator_warn)
        self.textEdit.setIndicatorForegroundColor(QColor(Qt.green), self._indicator_info)

        # 鼠标跟踪
        # self.textEdit.viewport().setMouseTracking(True)
        # # 安装键盘过滤器
        # self.textEdit.installEventFilter(self)
        # 安装鼠标移动过滤器
        self.textEdit.viewport().installEventFilter(self)

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if event.type() == QEvent.ToolTip:
            # 如果有错误则显示详情
            line = self.textEdit.lineAt(event.pos())
            if line >= 0 and line in self._indicator_dict:
                text = self._indicator_dict.get(line, '')
                if text:
                    color = self.textEdit.lexer().paper(0)
                    QToolTip.showText(QCursor.pos(),
                                      '<html><head/><body><div style="background:{0};">{1}</div></body></html>'.format(
                                          color.name(), text), self)
        return False

    def indent(self):

        sel = self.textEdit.getSelection()
        if sel[0] == sel[3]:
            row = self.textEdit.getCursorPosition()[0]
            self.textEdit.indent(row)
        else:
            ke = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
            self.textEdit.keyPressEvent(ke)

    def unindent(self):
        """
        取消缩进。
        方式就是注入一个tab快捷键。
        :return:
        """
        sel = self.textEdit.getSelection()
        if sel[0] == sel[3]:
            row = self.textEdit.getCursorPosition()[0]
            self.textEdit.unindent(row)
        else:
            ke = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)
            self.textEdit.keyPressEvent(ke)

    def _init_lexer(self, lexer: 'QsciLexer') -> None:
        """
        初始化语法解析器

        :return: None
        """
        self._lexer = lexer
        self._lexer.setFont(self.textEdit.font())
        self.textEdit.setLexer(self._lexer)

    def _init_signals(self) -> None:
        """
        初始化信号绑定

        :return: None
        """

        # 绑定获得焦点信号
        self.textEdit.focusInEvent = self.on_textedit_focusin
        # 绑定光标变化信号
        self.textEdit.cursorPositionChanged.connect(self.slot_cursor_position_changed)
        # 绑定内容改变信号
        self.textEdit.textChanged.connect(self.slot_text_changed)
        # 绑定选中变化信号
        self.textEdit.selectionChanged.connect(self.slot_selection_changed)
        # 绑定是否被修改信号
        self.textEdit.modificationChanged.connect(self.slot_modification_changed)
        # 绑定右键菜单信号
        self.textEdit.customContextMenuRequested.connect(self.slot_custom_context_menu_requested)
        # 绑定快捷键信号
        self._action_format.triggered.connect(self.slot_code_format)
        self._shortcut_format.activated.connect(self.slot_code_format)
        self._action_run_code.triggered.connect(self.slot_code_run)
        self._shortcut_run.activated.connect(self.slot_code_run)
        self._action_run_sel_code.triggered.connect(self.slot_code_sel_run)
        self._shortcut_run_sel.activated.connect(self.slot_code_sel_run)

        self._shortcut_save.activated.connect(self.slot_save)
        self._action_save.triggered.connect(self.slot_save)

        self._action_find_replace.triggered.connect(self.slot_find_or_replace)
        self._shortcut_find_replace.activated.connect(self.slot_find_or_replace)

        self._action_autocomp.triggered.connect(self.autocomp)
        self._shortcut_autocomp.activated.connect(self.autocomp)

        self._shortcut_goto.activated.connect(self.slot_goto_line)

    def autocomp(self):
        logger.warning('Manual Autocompletion Triggered!')

    def get_word_under_cursor(self):
        pos = self.textEdit.getCursorPosition()
        text = self.textEdit.text(pos[0])
        try:
            line = text[:pos[1] + 1]
        except Exception as e:
            logger.debug(e)
            line = ''
        word: str = re.split(r'[;,:/ .\\!&\|\*\+-=\s\(\)\{\}\[\]]', line)[-1].strip()
        col = pos[1]
        while (1):
            col += 1
            if col > len(text) - 1:
                break
            char = text[col]
            if char in ' \n()[]{}\'\";:\t!+-*/\\=.':
                break
            word += char
        return word

    def current_line_text(self):
        current_row = self.textEdit.getCursorPosition()[0]
        current_len = self.textEdit.lineLength(current_row)
        self.textEdit.setSelection(current_row, 0, current_row, current_len)
        return self.text(True)

    def text(self, selected: bool = False) -> str:
        """
        返回编辑器选中或者全部内容

        :rtype: str
        :return: 返回编辑器选中或者全部内容
        """
        if selected:
            return self.textEdit.selectedText()
        return self.textEdit.text()

    def set_text(self, text: str) -> None:
        """
        设置编辑器内容

        :type text: str
        :param text: 文本内容
        :return: None
        """
        # self.textEdit.setText(text)  # 该方法会重置撤销历史
        try:
            text = text.encode(self._encoding)
        except Exception as e:
            logger.warning(str(e))
            text = text.encode('utf-8', errors='ignore')
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETTEXT, text)

    def filename(self) -> str:
        """
        返回当前文件名

        :rtype: str
        :return: 返回当前文件名
        """
        return os.path.basename(self._path)

    def path(self) -> str:
        """
        返回当前文件路径

        :rtype: str
        :return: 返回当前文件路径
        """
        return self._path

    def set_path(self, path: str) -> None:
        """
        设置文件路径

        :param path: 设置文件路径
        :type path: str
        :return: None
        """
        self._path = path

    def modified(self) -> bool:
        """
        返回内容是否被修改

        :rtype: bool
        :return: 返回内容是否被修改
        """
        return self.textEdit.isModified()

    def set_modified(self, modified: bool) -> None:
        """
        设置内容是否被修改

        :param modified: 是否被修改 True or False
        :type: bool
        :return: None
        """
        self.textEdit.setModified(modified)

    def load_file(self, path: str) -> None:
        """
        加载文件

        :param path: 文件路径
        :type path: str
        :return: None
        """
        self._path = ''
        try:
            # 读取文件内容并加载
            with open(path, 'rb') as fp:
                text = fp.read()
                text, coding = Utilities.decode(text)
                self.set_encoding(coding)
                self.set_text(text)
                self.set_modified(False)
                self.set_eol_status()
        except Exception as e:
            logger.warning(str(e))
            self.extension_lib.show_log('error', 'CodeEditor', str(e))
        self._path = path
        self.setWindowTitle(self.filename())

    def set_encoding(self, encoding: str):
        """
        设置文本编码，仅支持 ASCII 和 UTF-8

        :param encoding: ascii or gbk or utf-8
        :type: str
        :return:
        """
        encoding = encoding.lower()
        self._encoding = encoding
        self.label_status_encoding.setText(encoding.upper())
        if encoding.startswith('utf'):
            self.textEdit.setUtf8(True)
            self.textEdit.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF8)
        else:
            self.textEdit.setUtf8(False)
            self.textEdit.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, 936)

    def slot_find_or_replace(self):
        if self.find_dialog is None:
            self.find_dialog = FindDialog(parent=self, text_edit=self)
        self.find_dialog.show()
        return
        # match_regex = False
        # case_sensitive = False
        # match_whole_word = False
        # wrap_find = False
        #
        # first = self.textEdit.findFirst('def', False, False, False, False)
        # self.textEdit.replace('ggg')

    def slot_about_close(self, save_all=False) -> QMessageBox.StandardButton:
        """
        是否需要关闭以及保存

        :param save_all: 当整个窗口关闭时增加是否全部关闭
        :return:QMessageBox.StandardButton
        """
        if not self.modified():
            return QMessageBox.Discard
        buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        if save_all:
            buttons |= QMessageBox.SaveAll  # 保存全部
            buttons |= QMessageBox.NoToAll  # 放弃所有
        ret = QMessageBox.question(self, self.tr('Save'), self.tr('Save file "{0}"?').format(self.filename()), buttons,
                                   QMessageBox.Save)
        if ret == QMessageBox.Save or ret == QMessageBox.SaveAll:
            if not self.slot_save():
                return QMessageBox.Cancel
        return ret

    def slot_modification_changed(self, modified: bool) -> None:
        """
        内容被修改槽函数

        :param modified: 是否被修改
        :type modified: bool
        :return:
        """
        title = self.windowTitle()
        if modified:
            if not title.startswith('*'):
                self.setWindowTitle('*' + title)
        else:
            if title.startswith('*'):
                self.setWindowTitle(title[1:])

    def create_context_menu(self) -> 'QMenu':
        menu = self.textEdit.createStandardContextMenu()

        # 遍历本身已有的菜单项做翻译处理
        # 前提是要加载了Qt自带的翻译文件
        for action in menu.actions():
            action.setText(QCoreApplication.translate('QTextControl', action.text()))
        # 添加额外菜单
        menu.addSeparator()
        menu.addAction(self._action_format)
        menu.addAction(self._action_run_code)
        menu.addAction(self._action_run_sel_code)
        menu.addAction(self._action_save)
        menu.addAction(self._action_find_replace)
        # menu.addAction(self)
        return menu

    def slot_custom_context_menu_requested(self, pos: QPoint) -> None:
        """
        右键菜单修改

        :param pos:
        :type pos: QPoint
        :return: None
        """
        menu = self.create_context_menu()
        # 根据条件决定菜单是否可用
        enabled = len(self.text().strip()) > 0
        self._action_format.setEnabled(enabled)
        self._action_run_code.setEnabled(enabled)
        # self._action_run_sel_code.setEnabled(self.textEdit.hasSelectedText())
        self._action_run_sel_code.setEnabled(enabled)
        menu.exec_(self.textEdit.mapToGlobal(pos))
        del menu

    def slot_save(self) -> bool:
        """
        保存时触发的事件。
        :return:
        """
        return self.save()

    def slot_text_changed(self) -> None:
        self.label_status_length.setText(self.tr('Length:{0}  Lines:{1}').format(format(self.textEdit.length(), ','),
                                                                                 format(self.textEdit.lines(), ',')))

        self.slot_modification_changed(True)
        self.set_modified(True)

    def save(self):
        """
        保存文件时调用的方法
        :param ext_name:
        :return:
        """
        path = self._path.replace(os.sep, '/')
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            # 弹出对话框要求选择真实路径保存
            path, ext = QFileDialog.getSaveFileName(self, self.tr('Save file'),
                                                    self.extension_lib.Program.get_work_dir(),
                                                    filter='*.py')

            if not path:
                return False
            if not path.endswith('.py'):
                path += '.py'
            self._path = path
        try:
            with open(self._path, 'wb') as fp:
                fp.write(self.text().encode('utf-8', errors='ignore'))

            self.setWindowTitle(os.path.basename(path))
            self.slot_modification_changed(False)
            self.set_modified(False)
            return True
        except Exception as e:
            # 保存失败
            logger.warning(str(e))
        return False

    def set_eol_status(self):
        """
        根据文件内容中的换行符设置底部状态

        :return:
        """
        eols = re.findall(r'\r\n|\r|\n', self.text())
        if not eols:
            self.label_status_eol.setText('Unix(LF)')
            self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行
            return
        grouped = [(len(list(group)), key) for key, group in groupby(sorted(eols))]
        eol = sorted(grouped, reverse=True)[0][1]
        if eol == '\r\n':
            self.label_status_eol.setText('Windows(CR LF)')
            self.textEdit.setEolMode(QsciScintilla.EolWindows)  # \r\n换行
            return QsciScintilla.EolWindows
        if eol == '\r':
            self.label_status_eol.setText('Mac(CR)')
            self.textEdit.setEolMode(QsciScintilla.EolMac)  # \r换行
            return
        self.label_status_eol.setText('Unix(LF)')
        self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行

    def _init_actions(self) -> None:
        """
        初始化额外菜单项

        :return:
        """
        self._action_format = QAction(self.tr('Format Code'), self.textEdit)
        self._action_run_code = QAction(self.tr('Run Code'), self.textEdit)
        self._action_run_sel_code = QAction(self.tr('Run Selected Code'), self.textEdit)
        self._action_save = QAction(self.tr('Save'), self.textEdit)
        self._action_find_replace = QAction(self.tr('Find/Replace'), self.textEdit)
        self._action_autocomp = QAction(self.tr('AutoComp'), self.textEdit)

        # 设置快捷键
        self._shortcut_format = QShortcut(QKeySequence('Ctrl+Alt+F'), self.textEdit)
        self._action_format.setShortcut(QKeySequence('Ctrl+Alt+F'))

        self._shortcut_autocomp = QShortcut(QKeySequence('Ctrl+P'), self.textEdit)
        self._action_autocomp.setShortcut(QKeySequence("Ctrl+P"))

        self._shortcut_run = QShortcut(QKeySequence('Ctrl+R'), self.textEdit)
        self._action_run_code.setShortcut(QKeySequence('Ctrl+R'))

        self._shortcut_run_sel = QShortcut(Qt.Key_F9, self.textEdit)
        self._action_run_sel_code.setShortcut(Qt.Key_F9)

        self._action_save.setShortcut(QKeySequence('Ctrl+S'))
        self._shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self.textEdit)

        self._action_find_replace.setShortcut(QKeySequence('Ctrl+F'))
        self._shortcut_find_replace = QShortcut(QKeySequence('Ctrl+F'), self.textEdit)

        self._shortcut_goto = QShortcut(QKeySequence('Ctrl+G'), self.textEdit)

    def slot_selection_changed(self) -> None:
        """
        选中内容变化槽函数

        :return: None
        """
        line_from, index_from, line_to, index_to = self.textEdit.getSelection()
        lines = 0 if line_from == line_to == -1 else line_to - line_from + 1
        self.label_status_sel.setText(
            self.tr('Sel:{0} | {1}').format(format(len(self.textEdit.selectedText()), ','), format(lines, ',')))

    def slot_run_in_terminal(self):
        logger.warning('不支持在终端运行！')
        pass

    def slot_code_sel_run(self):
        """
        运行选中代码

        :return:
        """
        logger.warning('不支持在ipython运行！')

    def slot_code_run(self):
        """
        运行代码

        :return:
        """
        logger.warning('不支持在ipython运行！')

    def slot_code_format(self):
        pass

    def slot_goto_line(self):
        """
        跳转到指定行列
        :return:
        """
        GotoLineDialog(self.textEdit, self).exec_()
        self.textEdit.setFocus()

    def slot_set_theme(self, name: str, language=None):
        """设置编辑器主题

        :param name:
        :param language:
        :return:
        """
        if not name.endswith('.xml'):
            name += '.xml'
        path = os.path.join(os.path.dirname(__file__), 'themes', name)
        if not os.path.exists(path):
            return

        # 默认样式
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETSELBACK, 1, QColor(128, 128, 128))
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor(Qt.black))
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETEDGECOLOUR, QColor(192, 192, 192))
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETFOLDMARGINCOLOUR, True, QColor(128, 128, 128))
        self.textEdit.SendScintilla(QsciScintilla.SCI_SETFOLDMARGINHICOLOUR, True, QColor(Qt.white))
        # self.textEdit.SendScintilla(QsciScintilla.SCI_INDICSETHOVERFORE, 8, QColor(128, 128, 128))

        background = QColor('#FFFFFF')
        try:
            style = etree.parse(path)
            # 全局样式
            for c in style.xpath('/NotepadPlus/GlobalStyles/WidgetStyle'):
                name, styleID, fgColor, bgColor = c.get('name'), int(c.get('styleID', 0)), '#' + str(
                    c.get('fgColor', '')), '#' + str(c.get('bgColor', ''))
                logger.debug('name:%s, styleID:%s, fgColor:%s, bgColor:%s', name, styleID, fgColor, bgColor)
                if name == 'Default Style':
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETFORE,
                                                    QsciScintilla.STYLE_DEFAULT, QColor(fgColor))
                        logger.debug('SCI_STYLESETFORE STYLE_DEFAULT %s', fgColor)
                    if bgColor != '#':
                        background = QColor(bgColor)
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETBACK,
                                                    QsciScintilla.STYLE_DEFAULT, QColor(bgColor))
                        logger.debug('SCI_STYLESETBACK STYLE_DEFAULT %s', bgColor)
                elif name == 'Current line background colour':
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETCARETLINEBACK, QColor(bgColor))
                        logger.debug('SCI_SETCARETLINEBACK %s', bgColor)
                elif name == 'Selected text colour':
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETSELBACK, 1, QColor(bgColor))
                        logger.debug('SCI_SETSELBACK %s', bgColor)
                elif styleID == QsciScintilla.SCI_SETCARETFORE:
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor(fgColor))
                        logger.debug('SCI_SETCARETFORE %s', fgColor)
                elif name == 'Edge colour':
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETEDGECOLOUR, QColor(fgColor))
                        logger.debug('SCI_SETEDGECOLOUR %s', fgColor)
                elif name == 'Fold margin':
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETFOLDMARGINHICOLOUR, True, QColor(fgColor))
                        logger.debug('SCI_SETFOLDMARGINHICOLOUR %s', fgColor)
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETFOLDMARGINCOLOUR, True, QColor(bgColor))
                        logger.debug('SCI_SETFOLDMARGINCOLOUR %s', bgColor)
                # elif name == 'URL hovered':
                #     if fgColor != '#':
                #         self.textEdit.SendScintilla(QsciScintilla.SCI_INDICSETHOVERFORE, 8, QColor(fgColor))
                #         logger.debug('SCI_INDICSETHOVERFORE %s', fgColor)
                elif name == 'White space symbol':
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_SETWHITESPACEFORE, True, QColor(fgColor))
                        logger.debug('SCI_SETWHITESPACEFORE %s', fgColor)
                elif styleID == QsciScintilla.STYLE_INDENTGUIDE:
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_INDENTGUIDE,
                                                    QColor(fgColor))
                        logger.debug('SCI_STYLESETFORE STYLE_INDENTGUIDE %s', fgColor)
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_INDENTGUIDE,
                                                    QColor(bgColor))
                        logger.debug('SCI_STYLESETBACK STYLE_INDENTGUIDE %s', bgColor)
                elif styleID == QsciScintilla.STYLE_BRACELIGHT:
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_BRACELIGHT,
                                                    QColor(fgColor))
                        logger.debug('SCI_STYLESETFORE STYLE_BRACELIGHT %s', fgColor)
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_BRACELIGHT,
                                                    QColor(bgColor))
                        logger.debug('SCI_STYLESETBACK STYLE_BRACELIGHT %s', bgColor)
                elif styleID == QsciScintilla.STYLE_BRACEBAD:
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_BRACEBAD,
                                                    QColor(fgColor))
                        logger.debug('SCI_STYLESETFORE STYLE_BRACEBAD %s', fgColor)
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_BRACEBAD,
                                                    QColor(bgColor))
                        logger.debug('SCI_STYLESETBACK STYLE_BRACEBAD %s', bgColor)
                elif styleID == QsciScintilla.STYLE_LINENUMBER:
                    if fgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_LINENUMBER,
                                                    QColor(fgColor))
                        logger.debug('SCI_STYLESETFORE STYLE_LINENUMBER %s', fgColor)
                    if bgColor != '#':
                        self.textEdit.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_LINENUMBER,
                                                    QColor(bgColor))
                        logger.debug('SCI_STYLESETBACK STYLE_LINENUMBER %s', bgColor)

            if not self._lexer:
                return
            self._lexer.setPaper(background)
            # 关键词高亮
            logger.debug('lexer language: %s', self._lexer.language())
            # print(self._lexer.lexer())
            for w in style.xpath('/NotepadPlus/LexerStyles/LexerType[@name="{0}"]/WordsStyle'.format(
                    language if language else self._lexer.lexer().lower())):
                name, styleID, fgColor, bgColor = w.get('name'), int(w.get('styleID', 0)), '#' + str(
                    w.get('fgColor', '')), '#' + str(w.get('bgColor', ''))
                logger.debug('name:%s, styleID:%s, fgColor:%s, bgColor:%s', name, styleID, fgColor, bgColor)
                self._lexer.setColor(QColor(fgColor), styleID)
        except Exception as e:
            logger.warning(str(e), exc_info=1)

    @pyqtProperty(str)
    def theme(self) -> str:
        """返回编辑器主题

        :return:
        """
        return self._theme

    @theme.setter
    def theme(self, name):
        """设置编辑器主题

        :param name:
        :return:
        """
        if name == self._theme:
            return
        self._theme = name
        self.slot_set_theme(name)
