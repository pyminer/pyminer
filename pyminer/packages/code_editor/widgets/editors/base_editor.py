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

import logging
import os
import time
from typing import Dict, Callable, TYPE_CHECKING, Type

from PySide2.QtCore import SignalInstance, Signal, QDir
from PySide2.QtGui import QTextDocument, QTextCursor
from PySide2.QtWidgets import QWidget, QMessageBox, QLabel, QVBoxLayout, QFileDialog

from lib.extensions.extensionlib.extension_lib import ExtensionLib
from ..dialogs.find_dialog import PMFindDialog
from ..dialogs.goto_line_dialog import PMGotoLineDialog
from ..text_edit.base_text_edit import PMBaseCodeEdit
from ...utils.base_object import CodeEditorBaseObject
from ...utils.utils import decode

logger = logging.getLogger(__name__)


class PMBaseEditor(CodeEditorBaseObject, QWidget):
    """
    这个类仅作为布局管理一些辅助内容，例如显示行号、列号等内容。
    所有实际的代码操作都应写在TextEdit里面。
    """

    # 用于子类继承时的配置项
    text_edit_class: Type['PMBaseCodeEdit'] = None  # 定义实际的代码编辑区对象
    text_edit: 'PMBaseCodeEdit'

    signal_focused_in: SignalInstance  # 编辑器获得焦点，是TextEdit的相关信号的直接引用
    signal_new_requested: SignalInstance = Signal(str, int)  # 文件路径；文件的打开模式（目前都是0）
    signal_save_requested: SignalInstance = Signal()
    signal_request_find_in_path: SignalInstance = Signal(str)

    # 子控件的类型提示
    find_dialog: 'PMFindDialog'
    goto_line_dialog: 'PMGotoLineDialog'
    find_dialog: 'PMFindDialog'
    extension_lib: 'ExtensionLib'

    # 为PySide2内置函数添加代码提示
    if TYPE_CHECKING:
        layout: Callable[[], QVBoxLayout]

    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 设置实际的代码编辑区
        assert self.text_edit_class is not None
        self.text_edit: 'PMBaseCodeEdit' = self.text_edit_class(self)
        self.signal_focused_in = self.text_edit.signal_focused_in
        self.text_edit.signal_save.connect(self.save)
        self.text_edit.signal_text_modified.connect(lambda: self.slot_modification_changed(True))

        # 代码发生变化后，改变代码行号的显示
        self.text_edit.cursorPositionChanged.connect(self.show_cursor_pos)

        self.text_edit.signal_file_dropped.connect(lambda name: self.signal_new_requested.emit(name, 0))
        self.layout().addWidget(self.text_edit)

        # 设置底部状态栏
        self.status_bar = QLabel()
        self.layout().addWidget(self.status_bar)

        # 设置各个对话框
        self.find_dialog = PMFindDialog(parent=self)
        self.goto_line_dialog = PMGotoLineDialog(parent=self)

        self.last_save_time = 0
        self._indicator_dict: Dict[str, str] = {}

    @property
    def _path(self):
        return self.text_edit.path

    @_path.setter
    def _path(self, value):
        self.text_edit.path = value

    def set_lib(self, extension_lib):
        self.extension_lib = extension_lib

    def show_cursor_pos(self):
        row, col = self.text_edit.cursor_position
        self.status_bar.setText(f'行：{row + 1},列:{col + 1}')

    def goto_line(self, line_no: int):
        """跳转到对应行列

        TODO 这个函数应当是属于text_edit的功能"""
        self.text_edit.go_to_line(line_no)

    def search_word(self, text_to_find: str, wrap: bool, regex: bool, case_sensitive: bool, whole_word: bool,
                    forward: bool, index=-1, line=-1, **kwargs) -> bool:
        find_flags = 0
        # if wrap:
        #     find_flags = find_flags | QTextDocument.FindFlags
        if case_sensitive:
            find_flags = find_flags | QTextDocument.FindCaseSensitively
        if whole_word:
            find_flags = find_flags | QTextDocument.FindWholeWords
        if not forward:
            find_flags = find_flags | QTextDocument.FindBackward
        if find_flags == 0:
            find_flags = QTextDocument.FindFlags
        # print(find_flags)
        ret = self.text_edit.find(text_to_find, options=find_flags)
        cursor_pos = self.text_edit.get_cursor_position()
        if wrap and (not ret):
            cursor = self.text_edit.textCursor()
            cursor.clearSelection()
            if forward:
                cursor.movePosition(QTextCursor.Start)
                print('cursor to start!')

            else:
                cursor.movePosition(QTextCursor.End)
            self.text_edit.setTextCursor(cursor)
            ret = self.text_edit.find(text_to_find, options=find_flags)
            # print(ret,cursor)
            if not ret:
                cursor = self.text_edit.textCursor()
                cursor.setPosition(cursor_pos)
                self.text_edit.setTextCursor(cursor)
        return ret

    def auto_completion(self):
        pass

    def set_text(self, text: str) -> None:
        """
        设置编辑器内容

        :type text: str
        :param text: 文本内容
        :return: None
        """
        self.text_edit.setPlainText(text)

    def set_modified(self, modified: bool) -> None:
        """
        设置内容是否被修改

        :param modified: 是否被修改 True or False
        :type: bool
        :return: None
        """
        self.text_edit.modified = modified
        self.slot_modification_changed(modified)

    def load_file(self, path: str) -> None:
        """加载文件

        Args:
            path: str, 需要打开的文件路径
        """
        self._path = ''
        try:
            # 读取文件内容并加载
            with open(path, 'rb') as fp:
                text = fp.read()
                text, coding = decode(text)
                self.set_text(text)
                self.set_modified(False)
                self.text_edit.set_eol_status()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning(str(e))

        self._path = path
        self.setWindowTitle(self.filename())
        self.last_save_time = time.time()
        self.set_modified(False)

    def slot_about_close(self, save_all=False) -> QMessageBox.StandardButton:
        """
        是否需要关闭以及保存

        :param save_all: 当整个窗口关闭时增加是否全部关闭
        :return:QMessageBox.StandardButton
        """
        if not self.is_modified:
            return QMessageBox.Discard
        buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        if save_all:
            buttons |= QMessageBox.SaveAll  # 保存全部
            buttons |= QMessageBox.NoToAll  # 放弃所有
        ret = QMessageBox.question(self, self.tr('Save'), self.tr('Save file "{0}"?').format(self.filename()), buttons,
                                   QMessageBox.Save)
        if ret == QMessageBox.Save or ret == QMessageBox.SaveAll:
            if not self.save():
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

    def slot_save(self) -> None:
        """
        保存时触发的事件。
        :return:
        """
        self.save()
        self.set_modified(False)

    @property
    def default_save_directory(self):
        """默认的存储路径"""
        return self.extension_lib.Program.get_work_dir()

    def save(self) -> bool:
        """保存文件时调用的方法

        If the file is not saved yet, the qfiledialog will open save dialog at default_dir,generated by get_default_dir
        method.
        """
        path = self._path.replace(os.sep, '/')
        default_dir = self.default_save_directory
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            assert os.path.exists(default_dir) or default_dir == ''
            # 弹出对话框要求选择真实路径保存
            path, ext = QFileDialog.getSaveFileName(self, self.tr('Save file'),
                                                    default_dir,
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
            self.set_modified(False)
            self.last_save_time = time.time()
            return True
        except Exception as e:
            # 保存失败
            logger.warning(str(e))
        return False

    @property
    def is_modified(self):
        return self.text_edit.modified

    def modified(self) -> bool:
        """
        返回内容是否被修改

        :rtype: bool
        :return: 返回内容是否被修改
        """
        return self.is_modified

    def is_temp_file(self) -> bool:
        """
        返回文件是否为临时文件
        :return:
        """
        tmp_path = QDir.tempPath().replace('\\', '/')
        if self._path.replace('\\', '/').startswith(tmp_path):
            return True
        else:
            return False

    def filename(self) -> str:
        """返回当前文件名"""
        return os.path.basename(self._path)

    def path(self) -> str:
        """返回当前文件路径"""
        return self._path

    def set_path(self, path: str) -> None:
        """
        设置文件路径

        :param path: 设置文件路径
        :type path: str
        :return: None
        """
        self._path = path

        title = self.windowTitle()
        new_title = os.path.basename(self._path)
        if title.startswith('*'):
            self.setWindowTitle('*' + new_title)
        else:
            self.setWindowTitle(new_title)

    def text(self, selected: bool = False) -> str:
        """返回编辑器选中或者全部内容。

        Args:
            selected: True则返回选中的内容，False则返回全部内容

        Returns:
            str, 选中的或全部的代码
        """
        if selected:
            return self.text_edit.selected_code
        else:
            return self.text_edit.code

    def slot_file_modified_externally(self):
        self.last_save_time = time.time()

    def change_color_scheme(self, color_scheme_name: str):
        if color_scheme_name == 'dark':
            self.text_edit.load_color_scheme({'keyword': '#b7602f'})
        elif color_scheme_name == 'light':
            self.text_edit.load_color_scheme({'keyword': '#101e96'})
        else:
            raise ValueError('unrecognized input color scheme name %s' % color_scheme_name)

    def slot_find_in_path(self):
        selected_text = self.text_edit.selected_code
        self.signal_request_find_in_path.emit(selected_text)

    def slot_find(self):
        self.find_dialog.show_replace_actions(replace_on=False)
        self.find_dialog.show()

    def slot_replace(self):
        self.find_dialog.show_replace_actions(replace_on=True)
        self.find_dialog.show()

    def slot_goto_line(self):
        self.goto_line_dialog.set_current_line(self.text_edit.textCursor().blockNumber())
        self.goto_line_dialog.set_max_row_count(self.text_edit.blockCount())
        ret = self.goto_line_dialog.exec_()
        if ret:
            self.text_edit.go_to_line(self.goto_line_dialog.get_line())

    def set_indicators(self, msg, clear=True):
        """
        qtextedit 的indicators ,但是目前还不支持。
        :return:
        """
        pass

    def instant_boot(self):
        """快速启动，暂不理解其作用"""
        self._not_implemented_error(self.tr('instant boot'))
