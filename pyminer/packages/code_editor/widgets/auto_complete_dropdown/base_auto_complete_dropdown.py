import logging
import os
import time
from functools import cached_property
from typing import List, Tuple, TYPE_CHECKING, Callable, Dict

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap, QKeyEvent
from PySide2.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from ...utils.base_object import CodeEditorBaseObject

if TYPE_CHECKING:
    from jedi.api.classes import Completion as CompletionResult
    from ..text_edit.base_text_edit import PMBaseCodeEdit

logger = logging.getLogger('code_editor.auto_complete_dropdown.base')
logger.setLevel(logging.DEBUG)


class BaseAutoCompleteDropdownWidget(CodeEditorBaseObject, QTableWidget):
    ROLE_NAME = 15
    ROLE_TYPE = 16
    ROLE_COMPLETE = 17
    ROLE_COMPLETION = 18

    # 为原生PySide2的类型添加类型提示
    parent: 'Callable[[], PMBaseCodeEdit]'
    verticalHeader: 'Callable[[], QHeaderView]'

    def __init__(self, parent: 'PMBaseCodeEdit' = None):
        super().__init__(parent)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().hide()
        self.setStyleSheet("AutoCompList{selection-background-color: #999999;}")
        self.verticalHeader().setMinimumWidth(20)
        # self.horizontalHeader().setMinimumWidth(300)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    @cached_property
    def icons(self) -> Dict[str, QIcon]:
        icons = {}
        icon_folder = self.settings.icons_dir / 'autocomp'
        for icon_file_name in os.listdir(icon_folder):
            icon_abso_path = icon_folder / icon_file_name
            icon1 = QIcon()  # create_icon(icon_abso_path)
            icon1.addPixmap(QPixmap(str(icon_abso_path)), QIcon.Normal, QIcon.Off)
            logger.debug(f'loading icon {icon_file_name}')
            icons[icon_file_name[:-4]] = icon1
        return icons

    def hide_autocomp(self):
        """隐藏自动补全菜单并且主界面设置焦点。"""
        self.hide()
        self.parent().setFocus()

    def count(self):
        return self.rowCount()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        parent = self.parent()
        if self.isVisible():
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab:
                parent._insert_autocomp()
                parent.setFocus()
                event.accept()
                return
            elif event.key() == Qt.Key_Escape:
                self.hide()
                parent.setFocus()
                return
            elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                super().keyPressEvent(event)
                event.accept()
                return
            elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
                self.hide_autocomp()
            elif event.key() == Qt.Key_Control or event.key() == Qt.Key_Alt:  # 按下Ctrl键时，不关闭界面，因为可能存在快捷键。
                pass
            else:
                if (Qt.Key_0 <= event.key() <= Qt.Key_9) and (
                        event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.AltModifier):
                    index = event.key() - Qt.Key_0
                    if 0 <= index < self.count():
                        self.setCurrentItem(self.item(index, 0))
                        parent._insert_autocomp()
                        parent.setFocus()
                        self.hide()
                        event.accept()
                        return
                self.hide_autocomp()
                event.ignore()
                return
        super().keyPressEvent(event)
        event.ignore()

    def set_completions(self, completions: List['CompletionResult']):
        """module, class, instance, function, param, path, keyword, property and statement."""
        t0 = time.time()
        self.setRowCount(0)
        self.setRowCount(len(completions))
        self.setColumnCount(1)
        labels = []
        for i, completion in enumerate(completions):
            item = QTableWidgetItem(completion.name)
            item.setData(BaseAutoCompleteDropdownWidget.ROLE_NAME, completion.name)

            item.setData(BaseAutoCompleteDropdownWidget.ROLE_COMPLETION, completion)
            item.setText(completion.name)
            if i < 30:  # 当条目数太多的时候，不能添加图标，否则速度会非常慢
                icon = self.icons.get(completion.type)
                if icon is not None:
                    item.setIcon(icon)

            self.setItem(i, 0, item)
            if 0 <= i <= 9:
                labels.append(str(i))
            else:
                labels.append('')
        self.setVerticalHeaderLabels(labels)
        self.show()
        self.setFocus()
        self.setCurrentItem(self.item(0, 0))
        t1 = time.time()
        logger.info(f'completion time:{t1 - t0},completion list length:{len(completions)}')

    def get_complete(self, row: int) -> Tuple[str, str]:
        return self.item(row, 0).data(BaseAutoCompleteDropdownWidget.ROLE_COMPLETION).complete, self.item(row, 0).data(
            BaseAutoCompleteDropdownWidget.ROLE_COMPLETION).type

    def get_text(self, row: int) -> str:
        return self.item(row, 0).text()
