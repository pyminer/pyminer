import contextlib
import logging
import os
import re
import time
from functools import cached_property
from itertools import groupby
from queue import Queue
from typing import Callable, Tuple, Dict, List, TYPE_CHECKING, Type, Any

import utils
from PySide2.QtCore import SignalInstance, Signal, Qt, QTimer, QModelIndex, QUrl, QRect, QPoint
from PySide2.QtGui import QFocusEvent, QTextCursor, QMouseEvent, QKeyEvent, QDragEnterEvent, QDropEvent, QPainter, \
    QColor, QTextFormat, QFontDatabase, QFont, QTextDocument
from PySide2.QtWidgets import QPlainTextEdit, QWidget, QApplication, QTextEdit, QLabel, QMenu, QAction
from jedi.api.classes import Completion as CompletionResult

from .line_number_area import QLineNumberArea
from ..auto_complete_dropdown.base_auto_complete_dropdown import BaseAutoCompleteDropdownWidget
from ...code_handlers.base_handler import BaseAnalyzer, BaseHandler
from ...utils.base_object import CodeEditorBaseObject
from ...utils.grammar_analyzer.get_indent import get_indent
from ...utils.grammar_analyzer.grammar_analyzer import GrammarAnalyzer
from ...utils.highlighter.python_highlighter import PythonHighlighter
from ...utils.operation import Operation

if TYPE_CHECKING:
    from ...utils.highlighter.base_highlighter import BaseHighlighter
    from ..editors.python_editor import PMPythonEditor
    from ...utils.auto_complete_thread.base_auto_complete import BaseAutoCompleteThread
    from ..editors.base_editor import PMBaseEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PMBaseCodeEdit(CodeEditorBaseObject, QPlainTextEdit):
    """
    所有与代码相关的编辑功能都应该定义在这里，包括排版、高亮等功能。
    """
    # 各个子类的配置项
    highlighter_class: 'Type[BaseHighlighter]' = None  # 语法高亮类
    auto_complete_thread_class: 'Type[BaseAutoCompleteThread]' = None  # 自动补全类

    highlighter: 'BaseHighlighter' = None
    auto_complete_thread: 'BaseAutoCompleteThread' = None

    handler_class: 'Type[BaseHandler]' = BaseHandler  # 代码核心操作类
    handler: 'BaseHandler' = None

    # cursorPositionChanged = Signal()
    signal_save: SignalInstance = Signal()  # 触发保存的事件，具体的保存操作交由给editor控件进行操作
    signal_focused_in: SignalInstance = Signal(QFocusEvent)  # 使用click代替focus，因为focus in信号触发过于频繁
    signal_idle: SignalInstance = Signal()  # 编辑器闲置，目前没有触发，也没有调用
    signal_text_modified: SignalInstance = Signal()  # 当编辑器内的文本发生改变时，触发这个信号
    signal_file_dropped: SignalInstance = Signal(str)  # 当一个文件被拖进这里时触发

    if TYPE_CHECKING:
        # PySide2的内置事件
        textChanged: SignalInstance  # 文本发生改变
        blockCountChanged: SignalInstance  # 行号发生改变
        updateRequest: SignalInstance  # 当文本文档需要更新指定的矩形时触发

        # 获取光标
        textCursor: Callable[[], QTextCursor]

        parent: Callable[[], PMBaseEditor]

        # 其他类型提示
        doc_tab_widget: 'PMPythonEditor'
        highlighter: 'PythonHighlighter'

    # 定义一系列的更新事件，不过只定义了这一个，提供了接口，其他的可以照例添加
    UPDATE_CODE_HIGHLIGHT = 1

    def __init__(self, parent=None):
        super(PMBaseCodeEdit, self).__init__(parent)
        if self.highlighter_class is not None:
            self.highlighter = self.highlighter_class(self.document())
        if self.auto_complete_thread_class is not None:
            self.auto_complete_thread = self.auto_complete_thread_class()
            self.auto_complete_thread.trigger.connect(self.on_autocomp_signal_received)
            self.auto_complete_thread.start()
        self.handler = self.handler_class()

        self.setTabChangesFocus(False)  # 不允许Tab切换焦点，因Tab有更重要的切换缩进的作用
        self.setMouseTracking(True)  # 启用鼠标跟踪，这允许在鼠标滑过该控件时捕捉到事件
        self.last_mouse_moved: float = time.time()  # 最后一次鼠标事件时间

        # 代码提示控件，使用一个Label作为代码提示
        self.hint_widget = QLabel('', parent=self)
        self.hint_widget.setVisible(False)
        self.hint_widget.setStyleSheet("background-color:#d8d8d8;padding:4px")

        fontId = QFontDatabase.addApplicationFont(
            os.path.join(utils.get_root_dir(), 'resources', 'fonts', 'SourceCodePro-Regular.ttf'))
        font_families = QFontDatabase.applicationFontFamilies(fontId)

        self.font = QFont()
        self.font.setPointSize(15)  # 设置行号的字体大小
        # font.setFamily("Microsoft YaHei UI")  # 设置行号的字体
        self.font.setFamily(font_families[0])  # 设置行号的字体
        self.setFont(self.font)

        self.line_number_area = QLineNumberArea(self)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.update_line_number_area_width(0)

        self._last_operation: float = 0.0  # 记录上次操作的时间
        self.update_request_queue = Queue()

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.doc_tab_widget = parent
        self.modified = False
        self._last_text = ''
        self.text_modified_signal_allowed = True
        self.setTabChangesFocus(False)

        # 设置代码提示的弹出框
        self.autocompletion_dropdown = BaseAutoCompleteDropdownWidget(self)
        self.autocompletion_dropdown.hide()
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # 用于更新界面的定时器，start的参数为毫秒
        self.ui_update_timer = QTimer()
        self.ui_update_timer.start(300)

        # 绑定各个信号
        self.__bind_signals()
        self.__create_operations()

    @property
    def path(self):
        return self.handler.path

    @path.setter
    def path(self, value):
        self.handler.path = value

    # noinspection PyUnresolvedReferences
    def __bind_signals(self):
        # 定时触发的事件
        self.ui_update_timer.timeout.connect(self.update_ui)

        # 行号相关的信号
        # 文本滚动后，同步更新行号
        self.updateRequest.connect(self.line_number_area.slot_update)
        self.updateRequest.connect(self.update_line_number_area_width)
        # 行数发生变化后，更新行号区域的宽度
        # TODO 行号区域应当通过设置Layout来自动控制，而现在是手动绘制在Editor里面的，需要进行调整
        self.blockCountChanged.connect(self.update_line_number_area_width)

        # 文本更新后触发的事件
        self.textChanged.connect(self.on_text_changed)
        # 文本发生改变后，保存当前时间
        self.textChanged.connect(self.update_last_operation_time)
        # 在代码提示框里面双击后，将自动补全的内容添加至代码
        self.autocompletion_dropdown.doubleClicked.connect(self._insert_autocomp)

        # 绑定右键菜单信号
        self.customContextMenuRequested.connect(self.slot_custom_context_menu_requested)

        self.textChanged.connect(self.update_handler_code)
        self.selectionChanged.connect(self.update_handler_code)

    def __create_operations(self):
        """创建操作，绑定快捷键，生成菜单项。"""

        def text_exists():
            """判断是否有文本，如果有文本才允许使用自动排版等功能"""
            return len(self.code) > 0

        def always_false():
            return False

        # 如果没有定义父对象，则直接返回，因为目前这个体系之下，大量的操作定义在了父对象中，导致单元测试跑不起来
        if not self.parent():
            return

        # TODO 将这些操作全部迁移至这个类下
        # 这里代码比较紧凑，以节省行数
        self.__menu_operations = [Operation(  # 格式化代码
            widget=self, name='format code', label=self.tr('Format Code'), key='Ctrl+Alt+F', icon_name='format.svg',
            slot=lambda: self.update_from_analyzer(self.handler.format_code()),
            conditions=[text_exists],
        ), Operation(  # 运行代码
            widget=self, name='run code', label=self.tr('Run Code'), key='Ctrl+R', icon_name='run.svg',
            # TODO 这里的path应该是本对象的属性，而非父对象的属性
            slot=lambda: self.handler.run_code(self.code, self.tr('Running {}').format(self.parent()._path)),
            conditions=[text_exists],
        ), Operation(  # 运行选中代码
            widget=self, name='run code', label=self.tr('Run Selected Code'), key='F9', icon_name='python.svg',
            slot=self.handler.run_selected_code,
            conditions=[text_exists],
        ), Operation(  # 保存代码
            widget=self, name='save code', label=self.tr('Save Code'), key='Ctrl+S', icon_name='save.svg',
            slot=self.parent().slot_save,
        ), Operation(  # 查找代码
            widget=self, name='find code', label=self.tr('Find Code'), key='Ctrl+F',
            slot=self.parent().slot_find,
        ), Operation(  # 替换代码
            widget=self, name='replace code', label=self.tr('Replace'), key='Ctrl+H',
            slot=self.parent().slot_replace,
        ), Operation(  # 在路径中查找，暂不理解这个功能的含义
            widget=self, name='find in path', label=self.tr('Find In Path'), key='Ctrl+Shift+F',
            slot=self.parent().slot_find_in_path,
        ), Operation(  # 自动补全功能是每隔一段时间自动显示的，使用快捷键可以立刻显示
            widget=self, name='auto completion', label=self.tr('AutoComp'), key='Ctrl+P',
            slot=self.parent().auto_completion,
        ), Operation(  # 跳转到行
            widget=self, name='goto line', label=self.tr('Goto Line'), key='Ctrl+G',
            slot=self.parent().slot_goto_line,
        ), Operation(
            widget=self, name='goto definition', label=self.tr('Goto Definition'), key='Ctrl+B',
            slot=self.parent().slot_goto_definition,
        ), Operation(  # 函数帮助
            widget=self, name='function help', label=self.tr('Function Help'), key='F1',
            slot=self.slot_function_help,
        ), Operation(
            widget=self, name='help in console', label=self.tr('Help in Console'), key='F2',
            slot=self.slot_help_in_console,
            conditions=[always_false],
        ), Operation(  # 添加断点
            widget=self, name='add breakpoint', label=self.tr('Add Breakpoint'), icon_name='breakpoint.svg',
        ), Operation(  # 移除断点
            widget=self, name='remove breakpoint', label=self.tr('Remove Breakpoint'),
        ), Operation(  # 查看所有断点
            widget=self, name='view breakpoints', label=self.tr('View BreakPoints'),
        )]

    def __only_for_qt_linguist_translation_and_never_need_to_be_called(self):
        self.tr('Undo'), self.tr('Redo'), self.tr('Cut'), self.tr('Copy'), self.tr('Copy'), self.tr('Paste')
        self.tr('Delete'), self.tr('Select All')

    def createStandardContextMenu(self) -> QMenu:
        menu = super().createStandardContextMenu()
        # 翻译原有的菜单项
        actions: List[QAction] = menu.actions()
        for action in actions:
            text = action.text()
            first, second = text.split('\t') if '\t' in text else (text, '')
            action.setText(f"{self.tr(first.replace('&', ''))}\t{second}")
        # 添加额外菜单
        menu.addSeparator(), [menu.addAction(operation.action) for operation in self.__menu_operations]
        return menu

    def slot_custom_context_menu_requested(self, pos: QPoint):
        """打开右键菜单"""
        self.createStandardContextMenu().exec_(self.mapToGlobal(pos))

    @property
    def line_number_area_width(self):
        return 30 + self.fontMetrics().width('9') * len(str(max(1, self.blockCount())))

    def update_line_number_area_width(self, *_):
        self.setViewportMargins(self.line_number_area_width, 0, 0, 0)

    @property
    def first_visible_line_number(self) -> int:
        return self.firstVisibleBlock().blockNumber()

    @property
    def current_line_number(self) -> int:
        return self.textCursor().blockNumber()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)

        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)

                self.font.setPointSize(10)
                painter.setFont(self.font)

                painter.drawText(0, top, self.line_number_area.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width, cr.height()))

    def highlightCurrentLine(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(235, 252, 252)  # 当前行背景色
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def update_last_operation_time(self):
        """更新上一次操作的时间"""
        self._last_operation = time.time()

    def update_ui(self):
        if not self.isVisible():
            return
        if self._last_operation <= 0.5:
            return
        if self.update_request_queue.empty():
            return
        action: int = self.update_request_queue.get()
        if action == self.UPDATE_CODE_HIGHLIGHT:
            self.text_modified_signal_allowed = False
            focus_widget: QWidget = QApplication.focusWidget()
            self.highlighter.rehighlight()
            self.text_modified_signal_allowed = True
            focus_widget is not None and focus_widget.setFocus()

    def on_autocomp_signal_received(self, text_cursor_pos: tuple, completions: 'List[CompletionResult]'):
        """当收到自动补全提示信号时，执行的函数。

        为了避免自动补全对性能的影响，采用一个独立的线程进行自动补全。自动补全的过程如下：
        1. 提交自动补全请求；
        2. 自动补全线程进行补全；
        3. 本控件接收自动补全的结果，判断是否仍在之前的位置，如仍在，则补全。
        """
        position = self.cursor_position
        if position[0] + 1 == text_cursor_pos[0] and position[1] == text_cursor_pos[1]:
            if len(completions) == 1:
                if completions[0].name == self._get_hint():
                    self.hide_autocomp()
                    return
            self.autocomp_show(completions)
        else:
            self.hide_autocomp()

    def hide_autocomp(self):
        self.autocompletion_dropdown.hide_autocomp()

    def update_handler_code(self):
        cursor = self.textCursor()
        self.handler.feed(self.code, cursor.position(), (cursor.selectionStart(), cursor.selectionEnd()))

    def update_from_analyzer(self, analyzer: 'BaseAnalyzer'):
        self.code = analyzer.code
        cursor = self.textCursor()
        cursor.setPosition(analyzer.cursor)
        self.setTextCursor(cursor)

    def on_text_changed(self):
        """文字发生改变时的方法"""
        if not self.modified:
            if self.toPlainText() != self._last_text:
                self.modified = True
                if self.text_modified_signal_allowed:
                    self.signal_text_modified.emit()
        self._last_text = self.toPlainText()

        # 代码提示
        cursor_pos = self.cursorRect()
        self.autocompletion_dropdown.setGeometry(
            cursor_pos.x() + 5, cursor_pos.y() + 20,
            self.autocompletion_dropdown.sizeHint().width(),
            self.autocompletion_dropdown.sizeHint().height())
        self._request_autocomp()

    def _insert_autocomp(self, event: QModelIndex = None):
        row = self.autocompletion_dropdown.currentRow()
        if 0 <= row < self.autocompletion_dropdown.count():
            complete, word_type = self.autocompletion_dropdown.get_complete(row)
            word = self.autocompletion_dropdown.get_text(row)
            if not word.startswith(self._get_hint()):
                return
            comp = word[len(self._get_hint()):]
            self.insertPlainText(comp)
            if word_type == 'function':
                self.insertPlainText('()')
                tc = self.textCursor()
                tc.movePosition(QTextCursor.PreviousCharacter)
                self.setTextCursor(tc)
            elif word_type == 'keyword':
                self.insertPlainText(' ')
            self.autocompletion_dropdown.hide()

    def _get_nearby_text(self):
        block_text = self.textCursor().block().text()
        col = self.textCursor().columnNumber()
        return block_text[:col]

    def _get_hint(self):
        block_text = self.textCursor().block().text()
        if block_text.lstrip().startswith('#'):  # 在注释中
            return ''
        col = self.textCursor().columnNumber()
        nearby_text = block_text[:col]
        hint = re.split('[.:;,?!\s \+ \- = \* \\ \/  \( \)\[\]\{\} ]', nearby_text)[-1]
        return hint

    def _request_autocomp(self):
        position = self.cursor_position
        nearby_text = self._get_nearby_text()
        hint = self._get_hint()

        if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
            self.autocompletion_dropdown.hide_autocomp()
            return
        self.auto_complete_thread.text_cursor_pos = (position[0] + 1, position[1])
        self.auto_complete_thread.text = self.toPlainText()

    @property
    def cursor_position(self) -> Tuple[int, int]:
        return self.textCursor().blockNumber(), self.textCursor().columnNumber()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.autocompletion_dropdown.isVisible():
            self.autocompletion_dropdown.hide_autocomp()
        self.signal_focused_in.emit(None)
        super().mousePressEvent(event)

    @cached_property
    def key_press_mapping(self) -> Dict[Tuple[Any, Any], Callable[[QKeyEvent], None]]:
        """将按键分配给各个函数的映射。

        键支持以下多种情况：

        1. str(event.text()), 例如：'(', '?'
        2. int(event.key()), 例如：Qt.Key_Backspace
        3. (int(event.key()), int(event.modifiers()))，例如：(Qt.Key_Slash, Qt.ControlModifier)

        值就是回调函数。
        """
        mapping = {
            Qt.Key_Tab: self.on_tab,
            Qt.Key_Backtab: self.on_back_tab,
            (Qt.Key_Backtab, Qt.ShiftModifier): self.on_back_tab,  # 经测试，只有这个可以表示Shift+Tab，不过另两个也可保留
            (Qt.Key_Tab, Qt.ShiftModifier): self.on_back_tab,
            # TODO 迁移至Operation体系
            # 这个就比较适合使用Operation来处理，因为可以显示在右键菜单中，而定义在key中就没有了这个优势。
            (Qt.Key_Slash, Qt.ControlModifier): self.comment,
            Qt.Key_Return: self.on_return_pressed,
            Qt.Key_Backspace: self.on_backspace,
            # 左括号、右括号分别采用同一个回调进行处理
            '(': self.on_left_parenthesis, '[': self.on_left_parenthesis, '{': self.on_left_parenthesis,
            ')': self.on_right_parenthesis, ']': self.on_right_parenthesis, '}': self.on_right_parenthesis,
        }
        return mapping

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """处理按键事件

        TODO 将按键处理逻辑写成一个独立的教程，然后在这边加引用

        按键处理的基本逻辑是，一个按键仅使用一个处理程序进行处理。
        即，如果在按键映射中找到了相应的按键的处理函数，则用该函数进行处理，而如果没有找到，则使用super进行处理。

        每个按键的处理函数都应使用如下的格式进行定义：

        def on_key_tab_pressed(self, event: QKeyEvent) -> None:
            do_some_thing()
            event.accept() # 中止事件的传递，不调用的话事件将传交给父组件再次处理

        按键处理函数不需要返回值。

        每个按键的处理函数都需要自行判断是否需要调用event.accept()，以提供足够的灵活性。

        按键处理函数与默认的super().keyPressEvent()是互斥的。
        如果仍需要使用默认的keyPressEvent进行处理，则可以在自定义的按键处理函数中进行如下调用：

        super().keyPressEvent(event)

        按键处理有两种方式：可以通过Operation进行定义，在BaseEditor中有描述，也可以在keyPressEvent内进行定义。
        具体的性能没有进行过查证，不过直观上看，使用keyPressEvent在性能上会存在优势。

        """
        self.update_handler_code()
        # TODO 按键处理逻辑仍存在bug，应当分为字符映射和键盘映射两种情况进行处理
        #  即分别通过event.text()和event.key()+event.modifier()进行处理
        text, key, modifiers = event.text(), event.key(), int(event.modifiers())
        no_modifier = modifiers == Qt.NoModifier
        callback_with_text = self.key_press_mapping.get(text, None)
        callback_with_key = self.key_press_mapping.get(key, None)
        callback_with_modifiers = self.key_press_mapping.get((key, modifiers), None)
        if no_modifier and callback_with_text is not None:
            callback = callback_with_text
        elif no_modifier and callback_with_key is not None:
            callback = callback_with_key
        elif callback_with_modifiers is not None:
            callback = callback_with_modifiers
        else:
            callback = super().keyPressEvent
        callback(event)
        self.update_handler_code()

    def on_left_parenthesis(self, event: QKeyEvent):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        string = {Qt.Key_ParenLeft: '()', Qt.Key_BracketLeft: '[]', Qt.Key_BraceLeft: '{}'}[event.key()]
        cursor.insertText(string)
        cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, 1)
        cursor.endEditBlock()
        self.setTextCursor(cursor)
        event.accept()

    @property
    def code(self):
        return self.toPlainText()

    @code.setter
    def code(self, value: str):
        self.setPlainText(value)

    def on_right_parenthesis(self, event: QKeyEvent):
        left, right = {
            Qt.Key_ParenRight: ('(', ')'),
            Qt.Key_BracketRight: ('[', ']'),
            Qt.Key_BraceRight: ('{', '}'),
        }[event.key()]
        code = self.code
        with self.editing_block_cursor() as cursor:
            position = cursor.position()
            analyzer = GrammarAnalyzer()
            analyzer.feed(code)
            length = len(code)
            if position == length or analyzer.is_not_matched(position, left) or code[position] != right:
                cursor.insertText(right)
            else:
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor, 1)
        event.accept()

    def on_backspace(self, event: QKeyEvent):
        cursor: QTextCursor = self.textCursor()
        cursor.beginEditBlock()
        previous_text = cursor.block().text()[:cursor.positionInBlock()]
        if previous_text.strip() == '':
            move_left = (cursor.columnNumber()) % 4
            if cursor.positionInBlock() == 0:
                move_left = 1  # 如果位于一行起始位置，就向左删除一个。
            else:
                if move_left == 0:  # 如果不位于起始位置且余数等于0，就向左删除一些。
                    move_left = 4

            for i in range(move_left):
                cursor.deletePreviousChar()
        else:
            cursor.deletePreviousChar()
        cursor.endEditBlock()
        event.accept()

    @contextlib.contextmanager
    def editing_block_cursor(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        yield cursor
        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def on_return_pressed(self, event: QKeyEvent):
        """按回车换行的方法

        TODO 使用parso进行解析并更新
        """
        if not self.textCursor().atBlockEnd():
            super().keyPressEvent(event)
            return
        with self.editing_block_cursor() as cursor:
            text = cursor.block().text()
            text, indent = get_indent(text)
            if text.endswith(':'):
                cursor.insertText('\n' + ' ' * (indent + 4))
            else:
                cursor.insertText('\n' + ' ' * indent)
        event.accept()

    def comment(self, _: QKeyEvent = None):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = cursor.anchor()
            end = cursor.position()

            if start > end:
                start, end = end, start

            cursor.clearSelection()

            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)

            start = cursor.position()  # 将光标移动到行首，获取行首的位置
            cursor.setPosition(end)  # 将光标设置到末尾
            cursor.movePosition(QTextCursor.StartOfLine)  # 将光标设置到选区最后一行
            end_line = cursor.blockNumber()  # 获取光标的行号

            cursor.setPosition(start)
            current_line = cursor.blockNumber()
            last_line = current_line
            while current_line <= end_line:
                line_text, indent = get_indent(cursor.block().text())
                if line_text.startswith('#'):
                    cursor.movePosition(
                        QTextCursor.NextCharacter, QTextCursor.MoveAnchor, indent)
                    cursor.deleteChar()
                else:
                    cursor.insertText('#')
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.movePosition(QTextCursor.Down)
                current_line = cursor.blockNumber()
                if current_line == last_line:
                    break
                last_line = current_line

            cursor.movePosition(QTextCursor.StartOfLine)
        else:
            cursor.movePosition(QTextCursor.StartOfLine)
            line_text, indent = get_indent(cursor.block().text())
            if line_text.startswith('#'):
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.MoveAnchor, indent)
                cursor.deleteChar()
            else:
                cursor.insertText('#')
            pass

        cursor.endEditBlock()

    def on_back_tab(self, _: QKeyEvent = None):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.edit_unindent()
        else:
            cursor = self.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfBlock)
            for i in range(4):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 1)
                if not cursor.selectedText().endswith(' '):
                    cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 1)
                    break
            cursor.removeSelectedText()

    def on_tab(self, _: QKeyEvent = None):
        with self.editing_block_cursor() as cursor:
            if cursor.hasSelection():
                self.edit_indent()
            else:
                nearby_text = self._get_nearby_text()
                hint = self._get_hint()

                if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
                    cursor = self.textCursor()
                    cursor.insertText("    ")
                else:
                    self._request_autocomp()

    def edit_indent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()

            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()

            cursor.setPosition(end)
            cursor.movePosition(QTextCursor.StartOfLine)
            end = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start = cursor.position()

            cursor.setPosition(end)
            while pos >= start:
                cursor.insertText("    ")

                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastPos = pos
                pos = cursor.position()
                if lastPos == pos:
                    break
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start)
        cursor.endEditBlock()
        return True

    def edit_unindent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start = cursor.position()
            cursor.setPosition(end)
            cursor.movePosition(QTextCursor.StartOfLine)
            end = cursor.position()
            while pos >= start:
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastpos = pos
                pos = cursor.position()
                if pos == lastpos:
                    break
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start)

        cursor.endEditBlock()

    def save(self):
        self.signal_save.emit()

    def is_modified(self):
        return self.modified

    @property
    def is_modified_prop(self):
        return self.modified

    def go_to_line(self, line: int):
        doc: QTextDocument = self.document()
        lines = doc.blockCount()
        assert 1 <= line <= lines
        pos = doc.findBlockByLineNumber(line - 1).position()
        text_cursor: QTextCursor = self.textCursor()
        text_cursor.setPosition(pos)
        self.setTextCursor(text_cursor)

    @property
    def selected_code(self):
        """获取光标选中的代码，或当前行"""
        return self.handler.analyzer.selected_code

    @property
    def current_line_code(self):
        """当前行的代码，包括尾换行符"""
        lines = self.code.splitlines(keepends=True)
        row = self.textCursor().blockNumber()
        return '' if row >= len(lines) else lines[row]

    def get_selected_row_numbers(self) -> Tuple[int, int]:
        """返回选中的行号范围"""
        start = self.textCursor().selectionStart()
        end = self.textCursor().selectionEnd()
        start_block_id = self.document().findBlock(start).blockNumber()
        end_block_id = self.document().findBlock(end).blockNumber()
        return start_block_id, end_block_id

    def set_eol_status(self):
        """根据文件内容中的换行符设置底部状态"""
        eols = re.findall(r'\r\n|\r|\n', self.toPlainText())
        if not eols:
            # self.label_status_eol.setText('Unix(LF)')
            # self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行
            return
        grouped = [(len(list(group)), key) for key, group in groupby(sorted(eols))]
        eol = sorted(grouped, reverse=True)[0][1]
        if eol == '\r\n':
            return
            # self.label_status_eol.setText('Windows(CR LF)')
            # self.textEdit.setEolMode(QsciScintilla.EolWindows)  # \r\n换行
            # return QsciScintilla.EolWindows
        if eol == '\r':
            # self.label_status_eol.setText('Mac(CR)')
            # self.textEdit.setEolMode(QsciScintilla.EolMac)  # \r换行
            return
        # self.label_status_eol.setText('Unix(LF)')
        # self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行

    @staticmethod
    def load_color_scheme(scheme: Dict[str, str]):
        PythonHighlighter.font_cfg.load_color_scheme(scheme)

    def get_cursor_position(self) -> int:
        # QTextCursor.position()
        return self.textCursor().position()

    def set_selection(self):
        raise NotImplementedError

    @property
    def is_text_selected(self):
        return self.textCursor().hasSelection()

    def replace_selection(self, replacement: str):
        cursor: QTextCursor = self.textCursor()
        cursor.removeSelectedText()
        cursor.insertText(replacement)
        # self.textCursor().replace(replacement, self.textCursor())
        self.setTextCursor(cursor)

    def get_word(self, row=-1, col=0) -> str:
        """获取某个行列位置下的文本.若row=-1则获取光标之下的文本"""
        if row == -1:
            line_no = self.current_line_number
            text_cursor: QTextCursor = self.textCursor()
            col = text_cursor.positionInBlock()
        else:
            line_no = row
        text: str = self.document().findBlockByLineNumber(line_no).text()

        col_forward = col
        col_backward = col
        seps_set = ' \n,()[]{}\'\";:\t!+-*/\\=.'
        try:
            while 1:
                if col_forward >= 0 and text[col_forward] in seps_set:
                    break
                if col_forward > 0:
                    col_forward -= 1
                else:
                    break
            length = len(text)
            while 1:
                if col_backward < length and text[col_backward] in seps_set:
                    break
                if col_backward < length - 1:
                    col_backward += 1
                else:
                    break
            word = text[col_forward:col_backward + 1].strip(seps_set)
            return word
        except Exception as exception:
            logger.exception(exception)

    def register_highlight(self, line: int, start: int, length: int, marker: int, hint: str):
        """
        注册高亮
        :param line: 要高亮的行号
        :param start: 从line行的哪一列开始高亮
        :param length: 高亮区域的长度
        :param marker: 使用的标记颜色等
        :param hint: 使用的提示文字
        :return:
        """
        self.highlighter.registerHighlight(line, start, length, marker, hint)

    def clear_highlight(self):
        """清除高亮"""
        self.highlighter.highlight_marks = {}

    def rehighlight(self):
        self.update_request_queue.put(self.UPDATE_CODE_HIGHLIGHT)

    def dragEnterEvent(self, event: QDragEnterEvent):  # 3
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, drop_event: QDropEvent):  # 6
        urls: List[QUrl] = drop_event.mimeData().urls()
        for url in urls:
            try:
                file = url.toLocalFile()
                self.signal_file_dropped.emit(file)
            except Exception as exception:
                logger.exception(exception)

    def autocomp_show(self, completions: List['CompletionResult']):
        result = []
        if len(completions) != 0:
            self.autocompletion_dropdown.set_completions(completions)
        else:
            self.autocompletion_dropdown.hide()
        self.autocompletion_dropdown.autocomp_list = result

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        鼠标移动事件
        移动到marker上的时候，便弹出提示框。
        编辑器的提示位置。
        """
        super().mouseMoveEvent(event)
        cursor: QTextCursor = self.cursorForPosition(event.pos())

        # 如果代码量过大，则跳过
        if not len(self.toPlainText()) < 10000 * 120:
            return
        line, col = cursor.blockNumber(), cursor.positionInBlock()
        flag = False
        text = ''
        if line in self.highlighter.highlight_marks:
            marker_propertys = self.highlighter.highlight_marks.get(line)
            for marker_property in marker_propertys:
                start = marker_property[0]
                if marker_property[1] == -1:
                    end = len(cursor.block().text())
                else:
                    end = start + marker_property[1]
                if start <= col < end:
                    flag = True
                    text += marker_property[3] + '\n'
                    break
            self.hint_widget.setGeometry(event.x(), event.y() + 20,
                                         self.hint_widget.sizeHint().width(), self.hint_widget.sizeHint().height())

            self.hint_widget.setText(text.strip())
        self.hint_widget.setVisible(flag)
        event.ignore()

    def slot_function_help(self):
        return self.parent().get_help()

    def slot_help_in_console(self):
        return self.parent().get_help_in_console()
