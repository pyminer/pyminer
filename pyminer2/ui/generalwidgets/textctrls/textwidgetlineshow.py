from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QKeyEvent, QWheelEvent, QMouseEvent, QTextCursor


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        print('paint!!!!!')
        self.codeEditor.lineNumberAreaPaintEvent(event)


class PMEditorWithLineNumber(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.setText('aa\n' * 20)
        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.document().cursorPositionChanged.connect(self.highlightCurrentLine)
        self.verticalScrollBar().sliderMoved.connect(self.on_scroll)

        self.verticalScrollBar().sliderReleased.connect(self.on_scroll)

        self.updateLineNumberAreaWidth(0)

    def wheelEvent(self, d: 'QWheelEvent') -> None:
        self.on_scroll(d)
        super(PMEditorWithLineNumber, self).wheelEvent(d)

    def on_scroll(self, event: QWheelEvent = None):
        # print('on_scroll', event.x(), event.y())
        self.lineNumberArea.update()  # scroll(0, None)

    def keyPressEvent(self, e: QKeyEvent) -> None:

        super(PMEditorWithLineNumber, self).keyPressEvent(e)
        self.updateLineNumberArea(QRect(100, 100, 100, 100), None)
        self.lineNumberArea.update()
        # if e==Qt.Key_Return:
        #     self.updateLineNumberAreaWidth(e)

    def mousePressEvent(self, e: 'QMouseEvent') -> None:
        block_number = self.cursorForPosition(self.cursor().pos()).blockNumber()
        print(block_number)
        super().mousePressEvent(e)

        # tc = self.textCursor()
        # # position=self.document.findBlockByNumber(1).position()
        # tc.setPosition(1, QTextCursor.MoveAnchor)
        # self.setTextCursor(tc)

        self.update()

    def lineNumberAreaWidth(self):
        digits = 1
        block_count = self.document().blockCount()

        max_value = max(1, block_count)
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, e):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        # rect = self.height()
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, self.geometry().x(), 10, self.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        # cursor = QTextCursor(self.document())

        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)
        line_height = self.fontMetrics().height()
        block_number = self.cursorForPosition(QPoint(0, 1)).blockNumber()
        first_visible_block = self.document().findBlock(block_number)
        blockNumber = block_number
        # cursor.setPosition(self.cursorForPosition(QPoint(0, int(line_height / 2))).position())
        rect = self.cursorRect()
        scroll_compensation = rect.y() - int(rect.y() / line_height) * line_height  # 补偿，从光标开始。
        print('compensition', scroll_compensation)

        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()
        last_visible_block = self.document().findBlock(last_block_number)
        print(line_height)
        # if scroll_compensation < 0:
        top = -(line_height - scroll_compensation)
        # else:
        #     top =-scroll_compensation
        bottom = top + line_height  # self.blockBoundingRect(first_visible_block).height()

        # Just to make sure I use the right font

        height = self.fontMetrics().height()
        block = first_visible_block
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber < last_block_number:
            if block.isVisible():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                # print(top, self.lineNumberArea.width(), height, number)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + line_height  # self.blockBoundingRect(block).height()
            blockNumber += 1


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    codeEditor = PMEditorWithLineNumber()
    codeEditor.show()
    sys.exit(app.exec_())
