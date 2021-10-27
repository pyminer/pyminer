from typing import Callable, List

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QWidget, QAction, QShortcut

from packages.code_editor.utils.base_object import CodeEditorBaseObject


class Operation(CodeEditorBaseObject):
    def __init__(self, widget: QWidget, name: str, label: str, slot: Callable = None,
                 conditions: List[Callable[[], bool]] = None,
                 key: str = None, icon_name: str = None):
        """绑定一个快捷键操作。

        这个操作可以在widget环境下直接访问，也可以添加到QMenu中。

        Args:
            widget: 需要绑定事件的小部件，似乎text_edit可以用而QWidget不行，具体没有详查
            name: 快捷键的名称，用于后面显示在设置项中，可以根据这个Name来设置并查找快捷键
            label: 显示在界面中的标签
            slot: 回调事件，如不定义回调事件，则在Menu中永远显示为不可用状态
            conditions: 根据这些条件判断是否可以调用，是一个函数的列表，每个函数都应返回一个布尔值，指示是否可用
            key: 快捷键，QSequence的参数
            icon_name: 在code_editor/assets/icons下面查找的路径
        """
        super(Operation, self).__init__()
        self.widget: QWidget = widget
        self.__conditions = conditions
        self.name: str = name

        has_slot = slot is not None

        # 设置Action的图标
        if icon_name is None:
            # 用于进行缓存，以免每次都要重新创建一个action对象
            self.__action: QAction = QAction(label, widget)
        else:
            icon = QIcon(self.settings.get_icon(icon_name))
            self.__action: QAction = QAction(icon, label, widget)
        # noinspection PyUnresolvedReferences
        has_slot and self.__action.triggered.connect(slot)

        # 设置QAction和QShortcut快捷键
        if key is not None:
            qt_sequence: QKeySequence = QKeySequence(key)
            self.__action.setShortcut(qt_sequence)
            # noinspection PyArgumentList
            has_slot and QShortcut(key, widget, context=Qt.WidgetShortcut).activated.connect(slot)

        # 如果没有定义回调事件，则直接设置这个控件为不可用状态，不过仍然显示在菜单中
        if not has_slot:
            self.__action.setEnabled(False)
            self.__conditions = None

    @property
    def action(self) -> QAction:
        """获取action对象用于创建menu，并根据当前是否可用，判断是否显示为可用状态

        这里采用实时计算属性来实现，因为在每次打开右键菜单时都需要判断其是否可用。
        """
        assert self.__conditions is None or len(self.__conditions) >= 1
        self.__conditions is not None and self.__action.setEnabled(all(c() for c in self.__conditions))
        return self.__action
