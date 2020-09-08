from PyQt5.QtCore import pyqtSignal, QModelIndex,Qt
from PyQt5.QtGui import QMouseEvent, QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QTextEdit, QMessageBox
from typing import List, Tuple


class PMGCodeEdit(QTextEdit):
    signal_save = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PMGCodeEdit, self).__init__(parent)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.filename = '*'
        self.path = ''
        self.modified = True

    def hide_autocomp(self):
        self.popup_hint_widget.hide_autocomp()

    def on_text_changed(self):
        self._get_textcursor_pos()
        cursor_pos = self.cursorRect()
        self.popup_hint_widget.setGeometry(cursor_pos.x(), cursor_pos.y(), 150, 200)
        self._request_autocomp()
        if self.modified == True:
            return
        else:
            self.modified = True
            self.updateUi()

    def _insert_autocomp(self, e: 'QModelIndex' = None):
        row = self.popup_hint_widget.currentRow()
        if 0 <= row < len(self.popup_hint_widget.autocomp_list):
            self.insertPlainText(self.popup_hint_widget.autocomp_list[row])
            self.popup_hint_widget.hide()

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
        pos = self._get_textcursor_pos()
        nearby_text = self._get_nearby_text()
        hint = self._get_hint()

        if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
            self.popup_hint_widget.hide_autocomp()
            return
        self.autocomp_thread.text_cursor_pos = (pos[0] + 1, pos[1])
        self.autocomp_thread.text = self.toPlainText()

    def autocomp_show(self, completions: list):
        self.popup_hint_widget.clear()
        l = []
        if len(completions) != 0:
            for completion in completions:
                l.append(completion.complete)
                self.popup_hint_widget.addItem(QListWidgetItem(completion.name))
            self.popup_hint_widget.show()
            self.popup_hint_widget.setFocus()
            self.popup_hint_widget.setCurrentRow(0)
        else:
            self.popup_hint_widget.hide()
        self.popup_hint_widget.autocomp_list = l

    def _get_textcursor_pos(self) -> Tuple[int, int]:
        return self.textCursor().blockNumber(), self.textCursor().columnNumber()

    def updateUi(self):
        if self.modified:
            text = '未保存'
        else:
            text = '已保存'
        self.doc_tab_widget.modified_status_label.setText(text)

    def keyPressEvent(self, event: 'QKeyEvent') -> None:
        k = event.key()
        if k == Qt.Key_Tab:
            self.on_tab()
            return
        elif k == Qt.Key_Backtab:
            self.on_back_tab()
            return
        elif k == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save()
            return
        elif k == Qt.Key_Slash and event.modifiers() == Qt.ControlModifier:
            self.comment()
        elif k == Qt.Key_Return:
            self.on_return_pressed()
            event.accept()
            return
        elif k == Qt.Key_Backspace:
            self.on_backspace(event)
            event.accept()
            return

        super().keyPressEvent(event)

    def on_backspace(self,key_backspace_event:'QKeyEvent'):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        text = cursor.block().text()
        nearby_text = self._get_nearby_text()
        print('nearby_text')
        if nearby_text.isspace():
            for i in range(4):
                cursor.deletePreviousChar()

        else:
            super().keyPressEvent(key_backspace_event)
        cursor.endEditBlock()

    def on_return_pressed(self):
        '''
        按回车换行的方法
        :return:
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
        text = cursor.block().text()
        text, indent = getIndent(text)
        if text.endswith(':'):

            cursor.insertText('\n' + ' ' * (indent + 4))
        else:

            cursor.insertText('\n' + ' ' * indent)
        cursor.endEditBlock()

    def comment(self):
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
            start_line = cursor.blockNumber()

            start = cursor.position()  # 将光标移动到行首，获取行首的位置
            cursor.setPosition(end)  # 将光标设置到末尾
            cursor.movePosition(QTextCursor.StartOfLine)  # 将光标设置到选区最后一行
            end_line = cursor.blockNumber()  # 获取光标的行号

            cursor.setPosition(start)
            current_line = cursor.blockNumber()
            last_line = current_line
            print(start_line, end_line, current_line)
            while current_line <= end_line:
                line_text, indent = getIndent(cursor.block().text())
                if line_text.startswith('#'):
                    cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor, indent)
                    cursor.deleteChar()
                else:
                    cursor.insertText('#')
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.movePosition(QTextCursor.Down)
                current_line = cursor.blockNumber()
                last_line = current_line
            cursor.movePosition(QTextCursor.StartOfLine)
        else:
            cursor.movePosition(QTextCursor.StartOfLine)
            line_text, indent = getIndent(cursor.block().text())
            if line_text.startswith('#'):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor, indent)
                cursor.deleteChar()
            else:
                cursor.insertText('#')
            pass

        cursor.endEditBlock()

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
            self.editIndent()
            return
        else:
            nearby_text = self._get_nearby_text()
            hint = self._get_hint()

            if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
                cursor = self.textCursor()
                cursor.insertText("    ")
            else:
                self._request_autocomp()

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
            path = QFileDialog.getSaveFileName(self, "选择保存的文件", '', filter='*.py')[0]
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
        self.signal_save.emit(self.filename)

    def on_close_request(self):
        if self.modified == True:
            answer = QMessageBox.question(self, '保存文件', '%s有未保存的更改，是否要保存？' % self.filename,
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.No:
                return
            else:
                self.save()