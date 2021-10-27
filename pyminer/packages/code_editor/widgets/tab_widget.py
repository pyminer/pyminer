import logging
import os
import sys
import time
from typing import Dict, Optional, Tuple, Any, Union, Callable, TYPE_CHECKING, Iterator

from PySide2.QtCore import QTimer, QThread, QDir
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QTabWidget, QSizePolicy, QMessageBox, QFileDialog, QComboBox, QWidget

import widgets
from widgets import PMDockObject, UndoManager, PMGFileSystemWatchdog, in_unit_test
from .editors.python_editor import PMPythonEditor
from .ui.findinpath import FindInPathWidget
from ..utils.base_object import CodeEditorBaseObject
from ..utils.code_checker.base_code_checker import CodeCheckWorker
from ..utils.highlighter.python_highlighter import PythonHighlighter

if TYPE_CHECKING:
    from lib.extensions.extensionlib.extension_lib import ExtensionLib
    from .editors.base_editor import PMBaseEditor
    from .editors.markdown_editor import PMMarkdownEditor

    EDITOR_TYPE = Optional[Union[PMBaseEditor, PMPythonEditor, PMMarkdownEditor, QWidget]]
logger = logging.getLogger(__name__)


class PMCodeEditTabWidget(CodeEditorBaseObject, QTabWidget, PMDockObject):
    """
    多标签页编辑器控件
    """
    extension_lib: 'ExtensionLib' = None
    watchdog: Optional['PMGFileSystemWatchdog'] = None

    if TYPE_CHECKING:
        widget: Callable[[int], EDITOR_TYPE]
        currentWidget: Callable[[], EDITOR_TYPE]

    def __init__(self, *args, **kwargs):
        super(PMCodeEditTabWidget, self).__init__(*args, **kwargs)
        # 设置其尺寸策略为x,y轴均膨胀。
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(200)
        self._color_scheme = 'light'
        self._index = 0
        self._current_executable = sys.executable  # 设置当前可执行文件的路径。
        self._old_code = ''
        self._thread_check = None
        self._worker_check = None
        self._timer_check = None
        self._last_cursorpos_requested_time = 0
        self._find_in_path_widget: "FindInPathWidget" = None
        self.settings: Dict[str, object] = {}

        self.debug_widget: Optional['PMDebugConsoleTabWidget'] = None

        self.cursor_pos_manager = UndoManager(stack_size=30)

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib
        self.extension_lib.Data.add_data_changed_callback(lambda name, var, source: self.slot_check_code(True))
        self.extension_lib.Data.add_data_deleted_callback(lambda name, provider: self.slot_check_code(True))

    def setup_ui(self) -> None:
        """将被插件管理器直接调用，不需要手动调用"""
        self.setDocumentMode(True)  # 文档模式
        self.setTabsClosable(True)  # 标签页可关闭
        self.setMovable(True)  # 标签页可移动
        self._init_signals()
        self.slot_new_script()  # 创建默认空白页

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

    def on_work_dir_changed(self, path: str) -> None:
        """处理工作路径改变时候的信号

        TODO 存在问题，watchdog的检测情况不够准鹕，有几种情况需要特殊考虑：
         文件在工作空间下的移动需要在工作空间文件夹下进行检测；
         外部的文件需要仅对该文件进行监测

        Args:
            path: 新的工作路径
        """
        last_path = ''
        if self.watchdog is not None:
            last_path = self.watchdog.path
        if os.path.normcase(last_path) != os.path.normcase(path):
            self.watchdog is not None and self.watchdog.stop()
            self.watchdog = PMGFileSystemWatchdog(path)
            self.watchdog.signal_file_modified.connect(self.on_file_modified)
            self.watchdog.signal_file_moved.connect(self.signal_file_moved)

    def signal_file_moved(self, path1, path2):
        """文件被移动（或者重命名）时触发的事件。"""
        for i in range(self.count()):
            editor = self.widget(i)
            if os.path.normcase(path1) == os.path.normcase(editor._path):
                if os.path.splitext(path1)[1] == os.path.splitext(path2)[1]:  # 如果扩展名相同，则直接更改文件名即可
                    editor.set_path(path2)
                else:
                    self.slot_tab_close_request(i)
                    self.slot_new_script(path2)
                break

    def on_file_modified(self, path: str) -> None:
        """
        处理文件在编辑器外部被修改的事件。
        编辑器内部保存的时候，会将被编辑的内容写入磁盘。写入事件发生时，编辑器设置`last_save_time`为当前时间戳。
        当`on_file_modified`方法调用时，此方法将获取调用时的时间戳，并与编辑器内部的`last_save_time`时间戳进行对比，
        如果`on_file_modified`方法在编辑器内部时间戳`last_save_time`以后的1秒以内进行调用，那么将忽略此事件（因为此事件极大概率是由编辑器发出的。）
        由于看门狗可能对同一次文件更改操作发送多个信号，所以这个函数可能在短时间（毫秒级别）内对同一文件调用多次，所以每次调用这个事件的时候，都会刷新一下last_save_time 以防
        短时间内调用多次的问题发生。

        Handles events where the file has been modified outside the editor.

        When saved internally, the editor writes the edited content to disk.
        When a write event occurs, the editor sets last_save_time to the current timestamp.
        When the `on_file_modified` method is called, this method gets the timestamp at the time of the call and compares it to the last_save_time timestamp inside the editor,
        If the `on_file_Modified` method is called within 1 second of the internal timestamp `last_save_time` of the editor, this event is ignored (because it is highly likely to have been issued by the editor).
        Since the watchdog can send multiple signals to the same file change operation, this function can be called to the same file multiple times in a short period of time (at the millisecond level), so each time the event is called, last_save_time is refreshed to prevent it
        Problems with multiple calls in a short period of time occur.
        """
        logger.warning(f'file modified:{path} at time:{str(time.time())}')
        editor = self.get_editor_tab_by_path(path)
        if editor is not None:
            if time.time() - editor.last_save_time > 1:
                editor.slot_file_modified_externally()

    def get_editor_tab_by_path(self, path) -> 'EDITOR_TYPE':
        """通过路径获取编辑器。如果没有打开，则返回None"""
        path = os.path.normcase(path)
        editors = [w for w in self.all_editors if os.path.normcase(w.path()) == path]
        return editors[0] if editors else None

    @property
    def current_editor(self):
        return self.currentWidget()

    @property
    def current_text_edit(self):
        return self.current_editor.text_edit

    @property
    def all_editors(self) -> Iterator['EDITOR_TYPE']:
        yield from (self.widget(i) for i in range(self.count()))

    @property
    def all_other_editors(self):
        current = self.current_editor
        yield from (e for e in self.all_editors if e is not current)

    def get_current_editor(self) -> 'EDITOR_TYPE':
        """
        get current editor
        Returns:

        """
        return self.current_editor

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

    def slot_set_tab_text(self, title: str) -> None:
        """
        设置标签页标题
        Args:
            title: 标题文字，str

        Returns:

        """
        widget = self.sender()  # 获取来自哪个编辑器
        self.setTabText(self.indexOf(widget), title)

    def slot_new_script(self, path: str = ''):
        """
        创建新文件或者打开已有文件
        当文件已经打开时，跳转到该文件
        Args:
            path:

        Returns:

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
        w = self.get_editor_tab_by_path(path)
        if w is not None:
            self.setCurrentWidget(w)
            return
        widget: 'PMBaseEditor' = None
        if path.endswith('.py') or path == os.path.join(QDir.tempPath(),
                                                        'Untitled-%d' % self._index).replace(os.sep, '/'):
            widget = PMPythonEditor(parent=self)
        # elif path.endswith(('.c', '.cpp', '.h')):
        #     widget = PMCPPEditor(parent=self)
        # elif path.endswith('.pyx'):
        #     widget = PMCythonEditor(parent=self)
        elif path.endswith('.md'):
            widget = PMMarkdownEditor(parent=self)
        else:
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('Editor does not support file:\n%s') % path)
            logger.warning('Editor Cannot open path:%s!!' % path)
        widget.set_lib(self.extension_lib)
        widget.load_file(path)
        widget.windowTitleChanged.connect(self.slot_set_tab_text)
        if isinstance(widget, PMPythonEditor):
            try:
                widget.signal_focused_in.connect(self.slot_focused_in)
                widget.signal_new_requested.connect(lambda path, mode: self.slot_new_script(path))
                widget.signal_goto_definition.connect(self.slot_goto_file)
            except:
                import traceback
                traceback.print_exc()
            # widget.textEdit.cursorPositionChanged.connect(self.slot_cursor_position_changed)
            # widget.signal_cursor_next_pos.connect(self.slot_goto_next_cursor_pos)
            # widget.signal_cursor_last_pos.connect(self.slot_goto_last_cursor_pos)

            if hasattr(widget, 'signal_request_find_in_path'):
                widget.signal_request_find_in_path.connect(self.slot_find_in_path)
        self.addTab(widget, widget.filename())
        self.setCurrentWidget(widget)
        if not widgets.in_unit_test():  # 如果不在单元测试，则切换工具条。
            self.extension_lib.UI.raise_dock_into_view('code_editor')
            self.extension_lib.UI.switch_toolbar('code_editor_toolbar', switch_only=True)

    def slot_cursor_position_changed(self, line, col):
        logger.warning('changed:' + str(time.time() - self._last_cursorpos_requested_time))
        logger.warning(self.cursor_pos_manager.last_value())
        if self.cursor_pos_manager.last_value() is not None:
            if abs(self.cursor_pos_manager.last_value()[
                       1] - line) > 5 and time.time() - self._last_cursorpos_requested_time > 0.1:
                current_path = self.currentWidget().path()
                self.cursor_pos_manager.push((current_path, line, col))
        else:
            current_path = self.currentWidget().path()
            self.cursor_pos_manager.push((current_path, line, col))

    def slot_goto_last_cursor_pos(self):
        logger.warning(self.cursor_pos_manager.content + self.cursor_pos_manager.pointer)
        last_pos_result: Tuple[str, int, int] = self.cursor_pos_manager.undo()
        self._last_cursorpos_requested_time = time.time()
        if last_pos_result is not None:
            if last_pos_result[1] == self.currentWidget().textEdit.get_cursor_position()[0]:
                last_pos_result = self.cursor_pos_manager.undo()
                if last_pos_result is None:
                    return
            self.on_gotoline_requested(*last_pos_result)

    def slot_goto_next_cursor_pos(self):
        """
        前往下一个指针位置。
        Returns:

        """
        next_pos_result: Tuple[str, int, int] = self.cursor_pos_manager.redo()
        self._last_cursorpos_requested_time = time.time()
        if next_pos_result is not None:
            if next_pos_result[1] == self.currentWidget().textEdit.get_cursor_position()[0]:
                next_pos_result = self.cursor_pos_manager.redo()
                if next_pos_result is None:
                    return
            self.on_gotoline_requested(*next_pos_result)

    def on_gotoline_requested(self, file_path: str, line_no: int, col_no: int = 0, count_from_zero=True):
        """
        前往某个文件的某个位置。
        Args:
            file_path:
            line_no:
            col_no:
            count_from_zero:

        Returns:

        """
        self.slot_new_script(file_path)
        current_widget = self.currentWidget()
        if count_from_zero:
            current_widget.goto_line(line_no + 1)
        else:
            current_widget.goto_line(line_no)

    def slot_open_script(self):
        """弹出对话框，打开选中的文件"""
        path, _ = QFileDialog.getOpenFileName(self, self.tr('Open File'), self.extension_lib.Program.get_work_dir(),
                                              filter='*.py')
        if not path or not os.path.exists(path):
            return

        self.slot_new_script(path)

    def slot_goto_file(self, path: str, row: int, col: int):
        self.slot_new_script(path)
        self.current_text_edit.go_to_line(row)

    def slot_check_code(self, force_update=False):
        """代码检查"""
        if not self._thread_check:
            return
        widget = self.currentWidget()
        if not isinstance(widget, PMPythonEditor):
            # 目前暂时支持python代码检测
            return
        code = self.get_current_text()  # .strip() is not needed because there should be a empty line at the end of file
        if (not code or code == self._old_code) and (not force_update):
            return
        self._old_code = code
        self._worker_check.add(widget, code)

    @staticmethod
    def slot_checked_code(widget, msgs):
        """
        代码检测更新

        :param widget: 目标编辑器
        :param msgs: 提示信息
        :return:
        """
        widget.set_indicators(msgs, True)

    def slot_run_script(self, code: str = '', hint: str = ''):
        """
        执行文件

        :return:
        """
        if isinstance(self.currentWidget(), PMPythonEditor):
            if not code:
                code = self.get_current_text(True)
                if not code:
                    code = self.get_current_text()
            code = code.strip()

            if hint == '':
                hint = self.tr('Run: %s') % self.get_current_filename()
        elif isinstance(self.currentWidget(), PMMarkdownEditor):
            code = self.currentWidget().get_code()
            code = code.strip()
            if hint == '':
                hint = self.tr('Run Python Code inside %s') % self.get_current_filename()
        else:
            return
        if not code:
            return
        if not in_unit_test():
            self.interfaces.ipython_console.run_command(command=code, hint_text=hint, hidden=False)
        else:
            logger.info("In Unit test at method 'slot_run_script'.code is :\n%s,\nhint is :%s" % (code, hint))

    def slot_tab_close_request(self, index: int):
        """
        关闭标签页

        :param index: 标签当前索引
        :type index: int
        :return:
        """
        editor = self.widget(index)
        if not editor:
            return
        if self.count() == 1 and not editor.is_modified and not editor.text():
            # 不关闭
            return
        if editor.slot_about_close() == QMessageBox.Cancel:
            return
        self.removeTab(index)
        editor.close()
        editor.deleteLater()
        if self.count() == 0:
            self._index = 0
            self.slot_new_script()

    def slot_run_isolated(self):
        editor: 'PMPythonEditor' = self.currentWidget()
        path = editor.path()
        self.interfaces.application_toolbar.create_python_file_process(path, self._current_executable)

    def _init_signals(self):
        # 标签页关闭信号
        self.tabCloseRequested.connect(self.slot_tab_close_request)
        self.currentChanged.connect(self.on_tab_switched)
        if not in_unit_test():
            try:
                self.extension_lib.UI.get_toolbar_widget('toolbar_home', 'button_new_script').clicked.connect(
                    self.slot_new_script)
                # self.extension_lib.UI.get_toolbar('toolbar_home').append_menu(
                #     'button_new', self.tr('Script'), self.slot_new_script)
                self.extension_lib.UI.get_toolbar('toolbar_home').append_menu('button_open', self.tr('Script'),
                                                                              self.slot_open_script)
                # 创建新文档

                self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_new_script').clicked.connect(
                    self.slot_new_script)
                # 打开文件
                self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'button_open_script').clicked.connect(
                    self.slot_open_script)
                interpreters = self.extension_lib.Program.get_settings_item_from_file("config.ini",
                                                                                      "RUN/EXTERNAL_INTERPRETERS")
                interpreter_names = [self.tr('Builtin (3.8.5)')] + [d['name'] for d in interpreters]
                combo_box: QComboBox = self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar',
                                                                                'combobox_interpreter')
                combo_box.addItems(interpreter_names)
                mouse_pressed_evt = combo_box.mousePressEvent

                def mouse_pressed(e):
                    current_selection_text = combo_box.currentText()
                    self.update_interpreter_selections(combo_box)
                    for i in range(combo_box.count()):
                        if combo_box.itemText(i) == current_selection_text:
                            combo_box.setCurrentIndex(i)
                    mouse_pressed_evt(e)

                combo_box.mousePressEvent = mouse_pressed
                combo_box.currentIndexChanged.connect(lambda: self.change_current_interpreter(combo_box.currentIndex()))
                self.update_interpreter_selections(combo_box)
                self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', 'combobox_interpreter')

                for widget_name, callback in (
                        ('button_save', lambda: self.currentWidget().slot_save()),
                        ('button_search', lambda: self.currentWidget().slot_find()),
                        ('button_goto', lambda: self.currentWidget().slot_goto_line()),
                        ('button_comment', lambda: self.current_text_edit.comment()),
                        ('button_indent', lambda: self.current_text_edit.on_tab()),
                        ('button_unindent', lambda: self.current_text_edit.on_back_tab()),
                        ('button_run_script', self.slot_run_script),
                        ('button_run_isolated', self.slot_run_isolated),
                        ('button_run_in_terminal', lambda: self.current_editor.slot_run_in_terminal()),
                        ('button_instant_boot', lambda: self.current_editor.instant_boot()),
                ):
                    self.extension_lib.UI.get_toolbar_widget('code_editor_toolbar', widget_name) \
                        .clicked.connect(callback)
            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.warning(str(e))

    def update_interpreter_selections(self, combo: QComboBox):
        """刷新所有解释器状态"""
        interpreters = self.extension_lib.Program.get_settings_item_from_file("config.ini", 'RUN/EXTERNAL_INTERPRETERS')
        combo.clear()
        combo.addItem(self.tr('Builtin (%s)' % sys.version.split()[0]))
        for interpreter in interpreters:
            combo.addItem(interpreter['name'] + ' (%s)' % interpreter['version'])

    def change_current_interpreter(self, interpreter_index: int):
        """切换当前解释器"""
        if interpreter_index == -1:
            return
        elif interpreter_index == 0:
            self._current_executable = sys.executable
        else:
            self._current_executable = \
                self.extension_lib.Program.get_settings_item_from_file("config.ini", 'RUN/EXTERNAL_INTERPRETERS')[
                    interpreter_index - 1]['path']

    def on_tab_switched(self, index: int) -> None:
        current = self.widget(index)
        for editor in self.all_editors:
            if editor is not current and hasattr(editor, 'find_dialog') and editor.find_dialog is not None:
                editor.find_dialog.hide()

    def set_background_syntax_checking(self, checking: bool):
        self._worker_check.background_checking = checking

    def update_settings(self, settings: Dict[str, Any]):
        self.settings = settings
        self.set_background_syntax_checking(settings['check_syntax_background'])

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._thread_check and self._thread_check.isRunning():
            self._worker_check.stop()
            self._thread_check.quit()
            self._thread_check.wait(500)
        [editor.close() for editor in self.all_editors]
        # TODO:这里结构不行！
        widgets = [widget for widget in self.all_editors if widget.is_modified]
        save_all = False
        for widget in widgets:
            if save_all:  # 保存全部则直接进入保存文件流程
                widget.slot_save()
            else:
                save_all = widget.slot_about_close(True) == QMessageBox.SaveAll

    def get_all_breakpoints(self, language='python') -> str:
        if language == 'python':
            breakpoints_str = ''
            for i in range(self.count()):
                editor = self.widget(i)
                if editor.path().endswith('.py'):
                    path = editor.path()
                    break_points = editor.get_all_breakpoints()
                    for bp_line in break_points:
                        breakpoints_str += 'b %s:%d' % (path, bp_line + 1) + '\n'
                    logger.warning('break_points are:' + str(break_points))
            return breakpoints_str

    def set_debug_widget(self, debug_widget):
        self.debug_widget = debug_widget

    def slot_debug(self):
        w = self.currentWidget()
        path = w.path()
        if self.debug_widget is not None:
            self.debug_widget.new_debug(os.path.basename(path), path, self)
            self.extension_lib.UI.raise_dock_into_view('debugger')

    def get_widget_text(self) -> str:
        return self.tr('Editor')

    def slot_find_in_path(self, word: str):
        path = self.extension_lib.Program.get_work_dir()
        if not self.extension_lib.UI.widget_exists('find_in_path'):
            w: FindInPathWidget = self.extension_lib.insert_widget(
                FindInPathWidget, 'new_dock_window',
                {
                    "name": "find_in_path",
                    "side": "bottom",
                    "text": self.tr("Find In Path")
                }
            )
            w.set_word(word)
            w.signal_open_file_line.connect(lambda path, row: self.slot_goto_file(path, row + 1, 0))
            self._find_in_path_widget = w
        self._find_in_path_widget.set_path(path)
        self.extension_lib.UI.raise_dock_into_view('find_in_path')

    def slot_focused_in(self, e):
        if not in_unit_test():
            self.extension_lib.UI.switch_toolbar('code_editor_toolbar', switch_only=True)

    def set_color_scheme(self, scheme: str):
        self._color_scheme = scheme
        if scheme == 'dark':
            PythonHighlighter.font_cfg.load_color_scheme(
                {'keyword': '#b7602f', 'normal': '#a8b4c2'}
            )
        else:
            PythonHighlighter.font_cfg.load_color_scheme({'keyword': '#101e96', 'normal': '#000000'})

        # for editor_index in range(self.count()):
        #     self.widget(editor_index).change_color_scheme(scheme)
