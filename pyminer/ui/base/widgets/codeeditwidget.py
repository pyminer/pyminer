#!/usr/bin/env python3
'''
来源：
https://blog.csdn.net/xiaoyangyang20/article/details/68923133
'''
import os
import sys
from typing import List

sys.path.append('/media/hzy/程序/novalide/forgitcommit/pyminer/pyminer')

from PyQt5.QtCore import QEvent, QFile, QFileInfo, QIODevice, QRegExp, QTextStream, Qt
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QMessageBox, QTextEdit, QTabWidget, \
    QVBoxLayout, QMessageBox, QWidget, QPushButton, QMenu, QToolBar, QToolButton
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QCursor, \
    QKeyEvent, QPixmap, QFocusEvent, QMouseEvent

# import pyqtresource_rc
from pyminer.features.extensions.extensionlib.pmext import PluginInterface

__version__ = "1.1.0"


def create_icon(icon_path: str = ":/pyqt/source/images/New.png"):
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
    return icon


class PushButtonPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def add_buttons(self, button_num: int = 2, text: list = None, icon_path: list = None,
                    menu: list = None) -> List[QPushButton]:
        if text is None:
            text = [''] * button_num
        if icon_path == None:
            icon_path = [None] * button_num
        if menu == None:
            menu = [None] * button_num
        if len(text) != button_num or len(icon_path) != button_num or len(menu) != button_num:
            raise Exception('text,icon和menu参数都必须为长为2的可迭代对象。')
        if button_num == 2:
            height = 30
            font_size = 12
        else:
            height = 25
            font_size = 12
        btn_list = []
        for i in range(button_num):
            b = self.add_button(text=text[i], icon=create_icon(icon_path[i]), menu=menu[i], height=height,
                                font_size=font_size)
            btn_list.append(b)
        return btn_list

    def add_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None, height: int = 30,
                   font_size: int = 14) -> QPushButton:
        b = QPushButton()
        b.setText(text)
        if icon is not None:
            b.setIcon(icon)
        if menu is not None:
            b.setMenu(menu)
        b.setStyleSheet(
            'QPushButton{border:0px;font-size:%dpx;padding:2px 2px;width:80px;height:%dpx;text-align:left;}' % (
                font_size, height) + \
            'QPushButton:hover{background-color:#ededed;}')
        self.layout.addWidget(b)
        return b


class PMToolBar(QToolBar):
    tab_button: QPushButton = None
    widget_dic = {}

    def __init__(self):
        super().__init__()
        self.setFixedHeight(90)

    def add_tool_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None):
        tb = QToolButton()
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setText(text)
        tb.setStyleSheet('QToolButton{height:60px;width:50px;border:0px;}QToolButton::hover{background-color:#ededed;}')
        if QIcon is not None:
            tb.setIcon(icon)
        self.addWidget(tb)
        return tb


class PythonHighlighter(QSyntaxHighlighter):
    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["and", "as", "assert", "break", "class",
                    "continue", "def", "del", "elif", "else", "except",
                    "exec", "finally", "for", "from", "global", "if",
                    "import", "in", "is", "lambda", "not", "or", "pass",
                    "print", "raise", "return", "try", "while", "with",
                    "yield"]
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                    "callable", "chr", "classmethod", "cmp", "compile",
                    "complex", "delattr", "dict", "dir", "divmod",
                    "enumerate", "eval", "execfile", "exit", "file",
                    "filter", "float", "frozenset", "getattr", "globals",
                    "hasattr", "hex", "id", "int", "isinstance",
                    "issubclass", "iter", "len", "list", "locals", "map",
                    "max", "min", "object", "oct", "open", "ord", "pow",
                    "property", "range", "reduce", "repr", "reversed",
                    "round", "set", "setattr", "slice", "sorted",
                    "staticmethod", "str", "sum", "super", "tuple", "type",
                    "vars", "zip"]
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                                        "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                                        "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % constant
                      for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
            r"\b[+-]?[0-9]+[lL]?\b"
            r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
            r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                                        "number"))
        PythonHighlighter.Rules.append((QRegExp(
            r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                                        "decorator"))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')

    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily("courier")
        baseFormat.setFontPointSize(12)
        for name, color in (("normal", Qt.black),
                            ("keyword", Qt.darkBlue), ("builtin", Qt.darkRed),
                            ("constant", Qt.darkGreen),
                            ("decorator", Qt.darkBlue), ("comment", Qt.darkGreen),
                            ("string", Qt.darkYellow), ("number", Qt.darkMagenta),
                            ("error", Qt.darkRed), ("pyqt", Qt.darkCyan)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format

    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()

        self.setFormat(0, textLength,
                       PythonHighlighter.Formats["normal"])

        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return
        if (prevState == ERROR and
                not (text.startswith(sys.ps1) or text.startswith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,
                               PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        if not text:
            pass
        elif text[0] == "#":
            self.setFormat(0, len(text),
                           PythonHighlighter.Formats["comment"])
        else:
            stack = []
            for i, c in enumerate(text):
                if c in ('"', "'"):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, len(text),
                                   PythonHighlighter.Formats["comment"])
                    break

        self.setCurrentBlockState(NORMAL)

        if self.stringRe.indexIn(text) != -1:
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = text.length()
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3,
                               PythonHighlighter.Formats["string"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, text.length(),
                               PythonHighlighter.Formats["string"])

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(
            Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()


class PMCodeEdit(QTextEdit):

    def __init__(self, parent=None):
        super(PMCodeEdit, self).__init__(parent)
        self.doc_tab_widget = parent
        self.filename = '*'
        self.path = ''
        self.modified = True
        self.highlighter = PythonHighlighter(self.document())
        self.setTabChangesFocus(False)
        self.textChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        print(self.modified, 'modified')
        if self.modified == True:
            return
        else:
            self.modified = True
            self.updateUi()

    def updateUi(self):
        self.doc_tab_widget.refresh()
        self.doc_tab_widget.is_all_files_saved()
        print('refresh!')
        # self.fileSaveAction.setEnabled(self.document().isModified())
        # enable = not self.editor.document().isEmpty()
        # self.fileSaveAsAction.setEnabled(enable)
        # self.editIndentAction.setEnabled(enable)
        # self.editUnindentAction.setEnabled(enable)
        # enable = self.editor.textCursor().hasSelection()
        # self.editCopyAction.setEnabled(enable)
        # self.editCutAction.setEnabled(enable)
        # self.editPasteAction.setEnabled(self.editor.canPaste())
        return

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        PluginInterface.switch_tool_bar('toolbar_editor')
        super().mousePressEvent(a0)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Tab:
            self.on_tab()
            return
        if event.key() == Qt.Key_Backtab:
            self.on_back_tab()
            return
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save()
            return
        super().keyPressEvent(event)

    def on_back_tab(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.editUnindent()

        else:
            cursor = self.textCursor()
            cursor.clearSelection()

            cursor.movePosition(QTextCursor.StartOfBlock)

            for i in range(4):
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 1)
                if not cursor.selectedText().endswith(' '):
                    cursor.movePosition(QTextCursor.PreviousCharacter,
                                        QTextCursor.KeepAnchor, 1)
                    break
            # print('cursor.selected',cursor.selectedText())
            cursor.removeSelectedText()

    def on_tab(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # print('has selection')
            self.editIndent()
            return
            # return True
        else:
            cursor = self.textCursor()
            cursor.insertText("    ")

    def editIndent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            start_line = self.document().findBlock(start)
            end = cursor.position()

            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()

            cursor.setPosition(end)
            cursor.movePosition(QTextCursor.StartOfLine)
            end = cursor.position()
            # print(end)
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start = cursor.position()

            cursor.setPosition(end)
            while pos >= start:
                # print(pos, start)
                cursor.insertText("    ")

                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastPos = pos
                pos = cursor.position()
                if lastPos == pos:
                    break

                print('end loop', pos, start)
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        cursor.endEditBlock()
        return True

    def editUnindent(self):
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
            print(start, end)
            while pos >= start:
                # print('a',start,pos)
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastpos = pos
                pos = cursor.position()
                if pos == lastpos:
                    break
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)

        cursor.endEditBlock()

    def save(self):
        print(self.toPlainText())
        if not os.path.isfile(self.path):
            print(os.getcwd())
            path = QFileDialog.getSaveFileName(self, "选择保存的文件", '/home/hzy/Desktop', filter='*.py')[0]
            print('path', path)
            if not path:  # 说明对话框被关闭，未选择文件,则直接返回。
                return
            if not path.endswith('.py'):
                path += '.py'
            self.path = path
            self.filename = os.path.basename(path)

        with open(self.path, 'w') as f:
            f.write(self.toPlainText())
        self.modified = False
        self.updateUi()

    def on_close_request(self):
        if self.modified == True:
            answer = QMessageBox.question(self, '保存文件', '%s有未保存的更改，是否要保存？' % self.filename,
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.No:
                return
            else:
                self.save()


class PMCodeEditTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.show_directly = True

    def init_toolbar(self):
        '''
        新建一个toolbar并且插入到主界面中。
        Returns:

        '''
        toolbar = PMToolBar()
        new_script_btn = toolbar.add_tool_button('新建\n脚本', create_icon(':/pyqt/source/images/lc_newdoc.png'))
        new_script_btn.clicked.connect(self.create_new_editor_tab)

        toolbar.add_tool_button('打开\n脚本', create_icon(':/pyqt/source/images/lc_open.png')).clicked.connect(
            self.open_file)
        toolbar.add_tool_button('打开\n脚本', create_icon(':/pyqt/source/images/lc_save.png'))
        pp = PushButtonPane()
        pp.add_buttons(3, ['查找文件', '剪贴板', '打印'],
                       [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png",
                        ':/pyqt/source/images/lc_print.png'])
        toolbar.addWidget(pp)
        toolbar.addSeparator()

        pp = PushButtonPane()
        buttons = pp.add_buttons(3, ['查找', '替换', '跳转到行'],
                                 [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png",
                                  ':/pyqt/source/images/lc_print.png'])
        buttons[0].clicked.connect(lambda: print('查找！'))
        buttons[1].clicked.connect(lambda: print('替换！'))
        buttons[2].clicked.connect(lambda: print('跳转！'))
        toolbar.addWidget(pp)

        pp = PushButtonPane()
        pp.add_buttons(2, ['批量注释', '缩进'],
                       [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])
        toolbar.addWidget(pp)
        pp = PushButtonPane()
        pp.add_buttons(2, ['取消注释', '减少缩进'],
                       [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])
        toolbar.addWidget(pp)
        toolbar.addSeparator()
        toolbar.add_tool_button('运行', create_icon(':/pyqt/source/images/run_exc.png')).clicked.connect(self.run)
        self.toolbar = toolbar

    def run(self):
        w: PMCodeEdit = self.currentWidget()
        text = w.document().toPlainText()
        PluginInterface.get_console().execute_command(text, False)

    def setup_ui(self):
        self.init_toolbar()

        PluginInterface.add_tool_bar('toolbar_editor', self.toolbar, text='编辑器')
        self.create_new_editor_tab()
        self.is_all_files_saved()

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tab_close_request)

    def create_new_editor_tab(self, text='', path='', filename='*', modified: bool = True):
        edit_widget = PMCodeEdit(self)
        edit_widget.path = path
        edit_widget.filename = filename
        edit_widget.setText(text)
        edit_widget.modified = modified

        self.addTab(edit_widget, edit_widget.filename)
        PluginInterface.show_log('info', 'CodeEditor', '新建文件')  # 2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
        self.setCurrentWidget(edit_widget)

    def open_file(self, path=''):
        path = QFileDialog.getOpenFileName(self, "选择打开的文件", '/home/hzy/Desktop', filter='*.py')[0]
        if os.path.exists(path):
            with open(path, 'r') as f:
                s = f.read()
            filename = os.path.basename(path)
            self.create_new_editor_tab(text=s, path=path, filename=filename, modified=False)

    def on_tab_close_request(self, close_index: int):
        tab_to_close = self.widget(close_index)
        tab_to_close.deleteLater()
        tab_to_close.on_close_request()
        self.removeTab(close_index)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        return

    def is_all_files_saved(self):
        for tab_id in range(self.count()):
            modified = self.widget(tab_id).modified
            print(modified)
        print(self.widget(0), self.count())
        # cursor.movePosition(QTextCursor.NextCharacter,
        #                     QTextCursor.KeepAnchor, 1)

    def refresh(self):
        for tab_id in range(self.count()):
            modified = self.widget(tab_id).modified
            filename = self.widget(tab_id).filename
            if not modified:
                self.setTabText(tab_id, filename)
            else:
                if filename != '*':
                    self.setTabText(tab_id, filename + ' *')
        print(self.widget(0), self.count())





# from pyminer.ui.base.widgets.menu_tool_stat_bars import PMModernToolbar


class MainWindow(QMainWindow):

    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setCentralWidget(PMCodeEditTabWidget())  # PMCodeEditTabWidget())
        # font = QFont("Courier", 11)
        # font.setFixedPitch(True)
        # self.editor = TextEdit()
        # self.editor.setFont(font)
        # self.highlighter = PythonHighlighter(self.editor.document())
        # self.setCentralWidget(self.editor)
        #
        # status = self.statusBar()
        # status.setSizeGripEnabled(False)
        # status.showMessage("Ready", 5000)
        #
        # fileNewAction = self.createAction("&New...", self.fileNew,
        #                                   QKeySequence.New, "filenew", "Create a Python file")
        # fileOpenAction = self.createAction("&Open...", self.fileOpen,
        #                                    QKeySequence.Open, "fileopen",
        #                                    "Open an existing Python file")
        # self.fileSaveAction = self.createAction("&Save", self.fileSave,
        #                                         QKeySequence.Save, "filesave", "Save the file")
        # self.fileSaveAsAction = self.createAction("Save &As...",
        #                                           self.fileSaveAs, icon_path="filesaveas",
        #                                           tip="Save the file using a new name")
        # fileQuitAction = self.createAction("&Quit", self.close,
        #                                    "Ctrl+Q", "filequit", "Close the application")
        # self.editCopyAction = self.createAction("&Copy",
        #                                         self.editor.copy, QKeySequence.Copy, "editcopy",
        #                                         "Copy text to the clipboard")
        # self.editCutAction = self.createAction("Cu&t", self.editor.cut,
        #                                        QKeySequence.Cut, "editcut",
        #                                        "Cut text to the clipboard")
        # self.editPasteAction = self.createAction("&Paste",
        #                                          self.editor.paste, QKeySequence.Paste, "editpaste",
        #                                          "Paste in the clipboard's text")
        # self.editIndentAction = self.createAction("&Indent",
        #                                           self.editIndent, "Ctrl+]", "editindent",
        #                                           "Indent the current line or selection")
        # self.editUnindentAction = self.createAction("&Unindent",
        #                                             self.editUnindent, "Ctrl+[", "editunindent",
        #                                             "Unindent the current line or selection")
        #
        # fileMenu = self.menuBar().addMenu("&File")
        # self.addActions(fileMenu, (fileNewAction, fileOpenAction,
        #                            self.fileSaveAction, self.fileSaveAsAction, None,
        #                            fileQuitAction))
        # editMenu = self.menuBar().addMenu("&Edit")
        # self.addActions(editMenu, (self.editCopyAction,
        #                            self.editCutAction, self.editPasteAction, None,
        #                            self.editIndentAction, self.editUnindentAction))
        # fileToolbar = self.addToolBar("File")
        # fileToolbar.setObjectName("FileToolBar")
        # self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
        #                               self.fileSaveAction))
        # editToolbar = self.addToolBar("Edit")
        # editToolbar.setObjectName("EditToolBar")
        # self.addActions(editToolbar, (self.editCopyAction,
        #                               self.editCutAction, self.editPasteAction, None,
        #                               self.editIndentAction, self.editUnindentAction))
        #
        #
        #
        # self.resize(800, 600)
        # self.setWindowTitle("Python Editor")
        # self.filename = filename
        # if self.filename is not None:
        #     self.loadFile()
        # self.updateUi()

    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(
            self.editor.document().isModified())
        enable = not self.editor.document().isEmpty()
        self.fileSaveAsAction.setEnabled(enable)
        self.editIndentAction.setEnabled(enable)
        self.editUnindentAction.setEnabled(enable)
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()

    def okToContinue(self):
        if self.editor.document().isModified():
            reply = QMessageBox.question(self,
                                         "Python Editor - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No |
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True

    def fileNew(self):
        if not self.okToContinue():
            return
        document = self.editor.document()
        document.clear()
        document.setModified(False)
        self.filename = None
        self.setWindowTitle("Python Editor - Unnamed")
        self.updateUi()

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        fname = str(QFileDialog.getOpenFileName(self,
                                                "Python Editor - Choose File", dir,
                                                "Python files (*.py *.pyw)")[0])
        if fname:
            self.filename = fname
            self.loadFile()

    def loadFile(self):
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Load Error",
                                "Failed to load {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle("Python Editor - {0}".format(
            QFileInfo(self.filename).fileName()))

    def fileSave(self):
        if self.filename is None:
            return self.fileSaveAs()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Save Error",
                                "Failed to save {0}: {1}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True

    def fileSaveAs(self):
        filename = self.filename if self.filename is not None else "."
        filename, filetype = QFileDialog.getSaveFileName(self,
                                                         "Python Editor -- Save File As", filename,
                                                         "Python files (*.py *.pyw)")
        if filename:
            self.filename = filename
            self.setWindowTitle("Python Editor - {0}".format(
                QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


if __name__ == '__main__':

    app = QApplication(sys.argv)
    print(4465)
    app.setWindowIcon(QIcon(":/icon_path.png"))
    fname = None

    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec_()
