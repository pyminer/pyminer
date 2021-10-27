from typing import TYPE_CHECKING

from PySide2.QtGui import QPaintEvent
from PySide2.QtWidgets import QWidget

if TYPE_CHECKING:
    from packages.code_editor.widgets.text_edit.base_text_edit import PMBaseCodeEdit


class QLineNumberArea(QWidget):
    """
    处理编辑器的行号区域相关的一些内容
    """
    if TYPE_CHECKING:
        codeEditor: PMBaseCodeEdit

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def paintEvent(self, event: QPaintEvent):
        self.codeEditor.lineNumberAreaPaintEvent(event)

    def slot_update(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())
