#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/9/7
@author: Irony
@email: 892768447@qq.com
@file: editor
@description: Code Editor
"""

__version__ = '0.1'

import os
from pathlib import Path

import chardet
from PyQt5.Qsci import QsciLexerPython, QsciScintilla, QsciAPIs
from PyQt5.QtCore import QCoreApplication, QLocale, Qt, QPoint
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QTabWidget, QFileDialog

try:
    from .ui_formeditor import Ui_FormEditor
except:
    from ui_formeditor import Ui_FormEditor
# TODO to remove (use extensionlib)
from pyminer2.extensions.extensionlib.pmext import PluginInterface


class PMCodeEditor(QWidget, Ui_FormEditor):

    def __init__(self, *args, **kwargs):
        super(PMCodeEditor, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._lexer = None
        self._apis = None
        self._init_editor()
        self._init_lexer()
        self._init_apis()
        self._init_signals()

    def _init_editor(self):
        """
        初始化编辑器设置
        Returns:
        """
        self.label_status_ln_col.setText(self.tr('行：1  列：1'))
        self.label_status_length.setText(self.tr('长度：0  行数：1'))
        self.label_status_sel.setText(self.tr('选中：0 | 0'))
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
        # self.textEdit.setAutoCompletionUseSingle(QsciScintilla.AcusAlways)
        self.textEdit.setAutoCompletionThreshold(1)  # 输入多少个字符才弹出补全提示
        self.textEdit.setCallTipsPosition(QsciScintilla.CallTipsBelowText)  # 设置提示位置
        self.textEdit.setCallTipsStyle(QsciScintilla.CallTipsNoContext)  # 设置提示样式
        # 设置折叠样式
        self.textEdit.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)  # 代码折叠
        self.textEdit.setFoldMarginColors(QColor(233, 233, 233), Qt.white)
        # 折叠标签颜色
        self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK,
                                    QsciScintilla.SC_MARKNUM_FOLDERSUB, QColor('0xa0a0a0'))
        self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK,
                                    QsciScintilla.SC_MARKNUM_FOLDERMIDTAIL, QColor('0xa0a0a0'))
        self.textEdit.SendScintilla(QsciScintilla.SCI_MARKERSETBACK,
                                    QsciScintilla.SC_MARKNUM_FOLDERTAIL, QColor('0xa0a0a0'))
        # 设置当前行背景
        self.textEdit.setCaretLineVisible(True)
        self.textEdit.setCaretLineBackgroundColor(QColor(232, 232, 255))

        # 设置选中文本颜色
        # self.textEdit.setSelectionForegroundColor(QColor(192, 192, 192))
        # self.textEdit.setSelectionBackgroundColor(QColor(192, 192, 192))

        # 括号匹配
        self.textEdit.setBraceMatching(QsciScintilla.StrictBraceMatch)  # 大括号严格匹配
        self.textEdit.setMatchedBraceBackgroundColor(Qt.blue)
        self.textEdit.setMatchedBraceForegroundColor(Qt.white)
        self.textEdit.setUnmatchedBraceBackgroundColor(Qt.red)
        self.textEdit.setUnmatchedBraceForegroundColor(Qt.white)

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
        self.textEdit.setIndentationGuidesForegroundColor(QColor(192, 192, 192))
        self.textEdit.setIndentationGuidesBackgroundColor(Qt.white)

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
        self.textEdit.setWhitespaceVisibility(
            QsciScintilla.WsVisible)  # 空白的可见性。默认的是空格是无形的
        self.textEdit.setWhitespaceForegroundColor(QColor(255, 181, 106))

    def _init_lexer(self):
        """
        初始化语法解析器
        Returns:
        """
        self._lexer = QsciLexerPython(self.textEdit)
        self._lexer.setFont(self.textEdit.font())
        self.textEdit.setLexer(self._lexer)

    def _init_apis(self):
        """
        加载自定义智能提示文件
        Returns:
        """
        self._apis = QsciAPIs(self._lexer)
        for path in Path(os.path.dirname(__file__)).rglob('*.api'):
            self._apis.load(str(path.absolute()))
        self._apis.prepare()

    def _init_signals(self):
        """
        初始化信号绑定
        Returns:
        """
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

    def slot_cursor_position_changed(self, line: int, column: int):
        """
        光标变化槽函数
        Args:
            line:
            column:

        Returns:
        """
        self.label_status_ln_col.setText(self.tr('行：{0}  列：{1}').format(line + 1, column + 1))

    def slot_text_changed(self):
        """
        内容变化槽函数
        Returns:
        """
        self.label_status_length.setText(
            self.tr('长度：{0}  行数：{1}').format(self.textEdit.length(), self.textEdit.lines()))

    def slot_selection_changed(self):
        """
        选中内容变化槽函数
        Returns:
        """
        lineFrom, indexFrom, lineTo, indexTo = self.textEdit.getSelection()
        lines = 0 if lineFrom == lineTo == -1 else lineTo - lineFrom + 1
        self.label_status_sel.setText(self.tr('选中：{0} | {1}').format(len(self.textEdit.selectedText()), lines))

    def slot_modification_changed(self, modified: bool):
        """
        内容被修改槽函数
        Args:
            modified:

        Returns:
        """
        title = self.windowTitle()
        if modified:
            if not title.startswith('*'):
                self.setWindowTitle('*' + title)
        else:
            if title.startswith('*'):
                self.setWindowTitle(title[1:])

    def slot_custom_context_menu_requested(self, pos: QPoint):
        """
        右键菜单修改
        Args:
            pos:

        Returns:
        """
        # 创建默认菜单
        menu = self.textEdit.createStandardContextMenu()
        country = QLocale.system().country()
        is_china = QLocale.system().language() == QLocale.Chinese or country in (
            QLocale.China, QLocale.HongKong, QLocale.Taiwan)
        # 遍历本身已有的菜单项做中文翻译处理
        # 前提是要加载了Qt自带的翻译文件
        for action in menu.actions():
            if is_china:
                action.setText(QCoreApplication.translate('QTextControl', action.text()))
        menu.exec_(self.textEdit.mapToGlobal(pos))
        del menu


class PMCodeEditTabWidget(QTabWidget):

    def __init__(self, *args, **kwargs):
        super(PMCodeEditTabWidget, self).__init__(*args, **kwargs)

    def init_toolbar(self):
        """
        新建一个toolbar并且插入到主界面中
        Returns:
        """

    def get_current_text_edit(self) -> PMCodeEditor:
        """
        返回当前编辑器对象
        Returns: `PMCodeEditor`
        """
        return self.currentWidget().textEdit

    def get_current_text(self) -> str:
        """
        返回当前编辑器内容
        Returns: str
        """
        try:
            return self.get_current_text_edit().text()
        except Exception as e:
            print(e)
            return ''

    def get_current_filename(self) -> str:
        """
        返回当前编辑器文件路径
        Returns:
        """
        try:
            return self.get_current_text_edit().filename
        except Exception as e:
            print(e)
            return ''

    def run(self):
        """
        运行当前代码
        Returns:
        """
        text = self.get_current_text()
        if text.strip():
            PluginInterface.get_console().execute_command(text, False, hint_text='运行： %s' % self.get_current_filename())

    def do_comment(self):
        pass

    def do_indent(self):
        pass

    def do_unindent(self):
        pass

    def setup_ui(self):
        self.init_toolbar()

        self.create_new_editor_tab()

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tab_close_request)
        PluginInterface.get_toolbar_widget('code_editor_toolbar', 'button_new_script').clicked.connect(
            lambda: self.create_new_editor_tab())
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_open_script').clicked.connect(self.open_file)
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_run_script').clicked.connect(self.run)
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_indent').clicked.connect(self.do_indent)
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_unindent').clicked.connect(self.do_unindent)
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_comment').clicked.connect(self.do_comment)
        PluginInterface.get_toolbar_widget(
            'code_editor_toolbar', 'button_uncomment').clicked.connect(self.do_comment)

    def create_new_editor_tab(self, text='', path='',
                              filename='*', modified: bool = True):

        editor_widget = PMCodeEditor(self)
        edit = editor_widget.textEdit
        edit.path = path
        edit.filename = filename
        # edit.signal_save.connect(self.refresh_modified_status)
        edit.setText(text)
        edit.modified = modified

        self.addTab(editor_widget, edit.filename)
        # 2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
        PluginInterface.show_log('info', 'CodeEditor', '新建文件')
        self.setCurrentWidget(editor_widget)

    def open_file(self, path=''):
        try:
            path = QFileDialog.getOpenFileName(
                self, "选择打开的文件", PluginInterface.get_root_dir(), filter='*.py')[0]
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    bytestream = f.read()
                    coding = chardet.detect(bytestream)['encoding']
                    s = bytestream.decode(coding)
                filename = os.path.basename(path)
                self.create_new_editor_tab(
                    text=s, path=path, filename=filename, modified=False)
            else:
                PluginInterface.show_log('error', 'CodeEditor', '文件路径\'%s\'不存在！' % path)
        except:
            import traceback
            traceback.print_exc()

    def on_tab_close_request(self, close_index: int):
        tab_to_close = self.widget(close_index)
        tab_to_close.deleteLater()
        tab_to_close.edit.on_close_request()
        self.removeTab(close_index)

    def refresh_modified_status(self, filename: str):
        self.setTabText(self.currentIndex(), filename)

    def closeEvent(self, event: 'QCloseEvent') -> None:
        widgets = [self.widget(i) for i in range(self.count())]
        for _ in range(self.count()):
            self.removeTab(0)
        for w in widgets:
            w.close()
            w.deleteLater()


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = PMCodeEditor()
    w.show()

    sys.exit(app.exec_())
