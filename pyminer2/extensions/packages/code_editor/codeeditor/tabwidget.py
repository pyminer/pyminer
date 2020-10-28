#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/9/7
@author: Irony
@email: 892768447@qq.com
@file: widget
@description: Code Editor TabWidget
"""

__version__ = '0.1'

import logging
import os
import re
from contextlib import redirect_stdout
from io import StringIO
from queue import Queue

from PyQt5.QtCore import QDir, QLocale, QObject, pyqtSignal, QThread, QTemporaryFile, QTranslator, QTimer
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QMessageBox, QApplication, QSizePolicy
from PyQt5.Qsci import QsciScintilla
# TODO to remove (use extensionlib)
from flake8.main.application import Application
from typing import TYPE_CHECKING, Dict

from pmgwidgets import PMDockObject

if TYPE_CHECKING:
    from pyminer2.extensions.packages.code_editor.codeeditor.pythoneditor import PMPythonEditor
    from pyminer2.extensions.packages.code_editor.codeeditor.baseeditor import PMBaseEditor
    from pyminer2.extensions.packages.code_editor.codeeditor.cppeditor import PMCPPEditor
    from pyminer2.extensions.packages.code_editor.codeeditor.cythoneditor import PMCythonEditor
else:
    from codeeditor.pythoneditor import PMPythonEditor
    from codeeditor.cppeditor import PMCPPEditor
    from codeeditor.cythoneditor import PMCythonEditor

logger = logging.getLogger(__name__)


class CodeCheckWorker(QObject):
    """
    代码检查
    """
    checked = pyqtSignal(object, list)

    def __init__(self, *args, **kwargs):
        super(CodeCheckWorker, self).__init__(*args, **kwargs)
        self._queue = Queue()
        self._running = True
        self.background_checking = True

    def add(self, widget, code):
        """
        添加需要检测的对象

        :param widget: 目标编辑器
        :param code: 目标编辑器代码
        :return:
        """
        self._queue.put_nowait((widget, code))

    def stop(self):
        """
        停止线程标志
        """
        self._running = False

    def run(self):
        """
        代码检测工作函数
        """
        while 1:
            if not self._running:
                logger.info('code checker quit')
                break
            if not self.background_checking:
                QThread.msleep(500)
                continue
            if self._queue.qsize() == 0:
                QThread.msleep(500)
                continue
            try:
                widget, code = self._queue.get(False, 0.5)
                # 创建临时文件
                file = QTemporaryFile(self)
                file.setAutoRemove(True)
                if file.open():
                    with open(file.fileName(), 'wb') as fp:
                        fp.write(code.encode())
                    file.close()
                    # 使用flake8检测代码
                    results = []
                    with StringIO() as out, redirect_stdout(out):
                        app = Application()
                        app.initialize(
                            ['flake8', '--exit-zero', '--config',
                             os.path.join(os.path.dirname(__file__), 'config', '.flake8')])
                        app.run_checks([file.fileName()])
                        app.report()
                        results = out.getvalue().split('\n')
                    results = [ret for ret in results if re.search(r'\d+:\d+:[EFW]\d+:.*?', ret)]
                    # if results:
                    self.checked.emit(widget, results)  # 如果为空，也应该这样做。将空列表传入可以清空所有的标记。
                file.deleteLater()
                del file
            except Exception as e:
                logger.warning(str(e))


class PMCodeEditTabWidget(QTabWidget, PMDockObject):
    """
    多标签页编辑器控件
    """
    extension_lib = None

    def __init__(self, *args, **kwargs):
        super(PMCodeEditTabWidget, self).__init__(*args, **kwargs)
        # 设置其尺寸政策为x,y轴均膨胀。
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(200)
        self._index = 0
        self._keywords = []
        self._old_code = ''
        self._thread_check = None
        self._worker_check = None
        self._timer_check = None
        self._trans_editor = None
        self.settings: Dict[str, object] = {}

    def setup_ui(self):
        """
        被插件管理器调用

        :return:
        """
        self._trans_editor = QTranslator()
        self._trans_editor.load(os.path.join(os.path.dirname(__file__), 'translations',
                                             'codeeditor_{0}.qm'.format(QLocale.system().name())))
        QApplication.instance().installTranslator(self._trans_editor)
        # 文档模式
        self.setDocumentMode(True)
        # 标签页可关闭
        self.setTabsClosable(True)
        # 标签页可移动
        self.setMovable(True)
        self._init_signals()
        # 创建默认空白页
        self.slot_new_script()

        # 初始化后台检测代码线程
        self._timer_check = QTimer(self)
        self._timer_check.timeout.connect(self.slot_check_code)
        self._thread_check = QThread(self)
        self._worker_check = CodeCheckWorker()
        self._worker_check.moveToThread(self._thread_check)
        self._worker_check.checked.connect(self.slot_checked_code)
        self._thread_check.finished.connect(self._worker_check.deleteLater)
        self._thread_check.finished.connect(self._thread_check.deleteLater)
        self._thread_check.started.connect(self._worker_check.run)
        self._thread_check.start()
        self._timer_check.start(2000)

    def keywords(self) -> list:
        """
        返回自定义的关键词

        :rtype: list
        :return: 返回自定义的关键词
        """
        return self._keywords

    def set_keywords(self, keywords: list):
        """
        增加额外的关键词

        :param keywords: 关键词列表
        :type: list
        :return:
        """
        if not isinstance(keywords, (tuple, list)):
            return
        self._keywords = list(keywords)

    def get_current_editor(self) -> 'PMBaseEditor':
        try:
            return self.currentWidget()
        except Exception as e:
            logger.warning(str(e))
        return None

    def get_current_edit(self) -> QsciScintilla:
        """
        返回当前编辑器对象


        """
        try:
            return self.currentWidget().textEdit
        except Exception as e:
            logger.warning(str(e))
        return None

    def get_current_text(self, selected: bool = False) -> str:
        """
        返回当前编辑器选中或者全部内容

        :param selected: 是否获取选中的内容 True or False
        :type: bool
        :return: 返回当前编辑器选中或者全部内容
        """
        try:
            return self.currentWidget().text(selected)
        except Exception as e:
            logger.warning(str(e))
            return ''

    def get_current_filename(self) -> str:
        """
        返回当前编辑器文件名

        :rtype: str
        :return: 返回当前编辑器文件名
        """
        try:
            return self.currentWidget().filename()
        except Exception as e:
            logger.warning(str(e))
            return ''

    def get_current_path(self) -> str:
        """
        返回当前编辑器文件路径

        :rtype: str
        :return: 返回当前编辑器文件路径
        """
        try:
            return self.currentWidget().path()
        except Exception as e:
            logger.warning(str(e))
            return ''

    def slot_set_tab_text(self, title: str):
        """
        设置标签页标题

        :param title: 标题
        :type title: str
        :return:
        """
        widget = self.sender()  # 获取来自哪个编辑器
        self.setTabText(self.indexOf(widget), title)

    def slot_new_script(self, path: str = ''):
        """
        创建新文件或者打开已有文件

        :param path: 空或者已有文件路径
        :type: Union[None, str]
        :return:
        """
        if not path:
            # 创建临时文件
            while True:
                self._index += 1
                path = os.path.join(QDir.tempPath(), 'Untitled-%d' % self._index).replace(os.sep, '/')
                try:
                    open(path, 'w', encoding='utf-8', errors='ignore').write('')
                    break
                except IOError as e:
                    logger.warning(str(e))

        for i in range(self.count()):
            w: 'PMBaseEditor' = self.widget(i)
            if w.path() == path:
                self.setCurrentWidget(w)
                return
        widget: 'PMBaseEditor' = None
        if path.endswith('.py') or path == os.path.join(QDir.tempPath(),
                                                        'Untitled-%d' % self._index).replace(os.sep, '/'):
            widget = PMPythonEditor(parent=self)
        elif path.endswith(('.c', '.cpp', '.h')):
            widget = PMCPPEditor(parent=self)
        elif path.endswith('.pyx'):
            widget = PMCythonEditor(parent=self)
        else:
            logger.warning('Editor Cannot open path:%s!!' % path)
            return
        if self.settings is not None:
            widget.update_settings(self.settings)
        widget.extension_lib = self.extension_lib
        widget.load_file(path)
        widget.windowTitleChanged.connect(self.slot_set_tab_text)
        self.addTab(widget, widget.filename())
        self.setCurrentWidget(widget)

    def slot_open_script(self):
        """
        弹出对话框选择文件

        :return:
        """
        path, _ = QFileDialog.getOpenFileName(self, self.tr('Open File'), self.extension_lib.Program.get_work_dir(),
                                              filter='*.py')
        if not path or not os.path.exists(path):
            return
        self.slot_new_script(path)

    def slot_search_for_file(self):
        """
        搜索文件内容

        :return:
        """

    def slot_clipboard(self):
        """
        剪贴板操作

        :return:
        """

    def slot_print(self):
        """
        打印预览以及打印

        :return:
        """

    def slot_search(self):
        """
        文本查找

        :return:
        """
        self.currentWidget().slot_find_or_replace()

    def slot_replace(self):
        """
        文本替换

        :return:
        """

    def slot_goto(self):
        """
        跳转到指定行

        :return:
        """

    def slot_indent(self):
        """
        批量缩进
        (实际上连接的是同一个函数)
        :return:
        """
        self.get_current_editor().indent()

    def slot_unindent(self):
        """
        取消缩进

        :return:
        """
        self.get_current_editor().unindent()

    def slot_check_code(self):
        """
        代码检查

        :return:
        """

        if not self._thread_check:
            return
        widget = self.currentWidget()
        if not isinstance(widget, PMPythonEditor):
            # 目前暂时支持python代码检测
            return
        code = self.get_current_text().strip()
        if not code or code == self._old_code:
            return
        self._old_code = code
        self._worker_check.add(widget, code)

    def slot_checked_code(self, widget, msgs):
        """
        代码检测更新

        :param widget: 目标编辑器
        :param msgs: 提示信息
        :return:
        """
        widget.set_indicators(msgs, True)

    def slot_toggle_comment(self):
        self.get_current_editor().commenter.toggle_commenting()

    def slot_run_script(self, text=''):
        """
        执行文件

        :return:
        """
        if not text:
            text = self.get_current_text(True)
            if not text:
                text = self.get_current_text()
        text = text.strip()
        if not text:
            return
        self.extension_lib.get_interface('ipython_console').run_command(command=text, hint_text=self.tr(
            'Run: %s') % self.get_current_filename(), hidden=False)

    def slot_run_sel(self, sel_text):
        """
        运行选中代码片段或光标所在行
        :param sel_text:
        :return:
        """
        self.extension_lib.get_interface('ipython_console').run_command(command=sel_text, hint_text=sel_text,
                                                                        hidden=False)

    def slot_tab_close_request(self, index: int):
        """
        关闭标签页

        :param index: 标签当前索引
        :type index: int
        :return:
        """
        widget = self.widget(index)
        if not widget:
            return
        if self.count() == 1 and not widget.modified() and not widget.text():
            # 不关闭
            return
        if widget.slot_about_close() == QMessageBox.Cancel:
            return
        self.removeTab(index)
        widget.close()
        widget.deleteLater()
        if self.count() == 0:
            self._index = 0
            self.slot_new_script()

    def slot_run_in_terminal(self):
        """
        在终端中运行
        :return:
        """
        editor: 'PMPythonEditor' = self.currentWidget()
        editor.slot_run_in_terminal()

    def run_python_file_in_terminal(self, file_path: str):
        self.extension_lib.Program.run_python_file(file_path)

    def run_sys_command(self):
        pass

    def _init_signals(self):
        # 标签页关闭信号
        self.tabCloseRequested.connect(self.slot_tab_close_request)
        self.currentChanged.connect(self.on_tab_switched)

        try:
            self.extension_lib.UI.get_toolbar_widget('toolbar_home', 'button_new_script').clicked.connect(
                self.slot_new_script)
            self.extension_lib.UI.get_toolbar('toolbar_home').append_menu(
                'button_new', self.tr('Script'), self.slot_new_script)
            self.extension_lib.UI.get_toolbar('toolbar_home').append_menu('button_open', self.tr('Script'),
                                                                          self.slot_open_script)
            # 创建新文档

            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_new_script').clicked.connect(
                self.slot_new_script)
            # 打开文件
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_open_script').clicked.connect(
                self.slot_open_script)
            # 查找文件
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_search_for_file').clicked.connect(
                self.slot_search_for_file)
            # 剪贴板
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_clipboard').clicked.connect(
                self.slot_clipboard)
            # 打印
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_print').clicked.connect(
                self.slot_print)
            # 查找内容&替换
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_search').clicked.connect(
                self.slot_search)
            # 跳转到行
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_goto').clicked.connect(
                self.slot_goto)
            # 批量注释
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_comment').clicked.connect(
                self.slot_toggle_comment)
            # 取消注释
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_uncomment').clicked.connect(
                self.slot_toggle_comment)
            # 增加缩进
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_indent').clicked.connect(
                self.slot_indent)
            # 减少缩进
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_unindent').clicked.connect(
                self.slot_unindent)
            # 运行代码
            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_run_script').clicked.connect(
                self.slot_run_script)

            self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_run_in_terminal').clicked.connect(
                self.slot_run_in_terminal)
        except Exception as e:
            logger.warning(str(e))

    def on_tab_switched(self, index: int) -> None:
        for i in range(self.count()):
            if i != index:
                w: 'PMBaseEditor' = self.widget(i)
                if w.find_dialog is not None:
                    w.find_dialog.hide()

    def set_background_syntax_checking(self, checking: bool):
        self._worker_check.background_checking = checking

    def set_smart_autocomp_stat(self, smart_autocomp_on: bool):
        for i in range(self.count()):
            # if i != index:
            w: 'PMBaseEditor' = self.widget(i)
            w.set_smart_autocomp_stat(smart_autocomp_on)

    def update_settings(self, settings: Dict[str, object]):
        self.settings = settings
        self.set_background_syntax_checking(settings['check_syntax_background'])
        for i in range(self.count()):
            w: 'PMBaseEditor' = self.widget(i)
            w.update_settings(settings)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._thread_check and self._thread_check.isRunning():
            self._worker_check.stop()
            self._thread_check.quit()
            self._thread_check.wait(500)
        widgets = [self.widget(i) for i in range(
            self.count()) if self.widget(i).modified()]
        if not widgets:
            return
        save_all = False
        for widget in widgets:
            if save_all:
                # 保存全部则直接进入保存文件流程
                widget.slot_save()
                continue
            ret = widget.slot_about_close(True)
            save_all = ret == QMessageBox.SaveAll


if __name__ == '__main__':
    import sys
    import cgitb
    import logging

    cgitb.enable(format='text')
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)
    app.setStyleSheet("""
    PMBaseEditor {
        qproperty-theme: "Material-Dark";
    }
    """)

    app.trans_qt = QTranslator()
    app.trans_qt.load('../../../../translations/qt_{0}.qm'.format(QLocale.system().name()))
    app.installTranslator(app.trans_qt)

    w = PMCodeEditTabWidget()
    w.show()
    w.setup_ui()
    w.currentWidget().load_file(__file__)

    sys.exit(app.exec_())
