from typing import List, Callable

from PySide2.QtCore import Qt, QStringListModel
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QPushButton, QLineEdit
from PySide2.QtWidgets import QListWidgetItem, QCompleter

from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGListCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: List[List[str]] = None,
                 new_id_func: Callable = None):
        super().__init__(layout_dir)
        self.choices = []
        initial_value = initial_value if initial_value is not None else [[], []]
        self.text_list = []
        lab_title = QLabel(text=title)
        layout = QHBoxLayout()
        self.central_layout.addWidget(lab_title)
        self.on_check_callback = None
        self.list_widget = QListWidget()
        self.list_widget.mouseDoubleClickEvent = self.on_listwidget_double_cicked
        # if initial_value is not None:

        self.set_value(initial_value)
        layout_tools = QVBoxLayout()
        self.button_add_item = QPushButton('+')
        self.button_delete_item = QPushButton('-')
        self.button_delete_item.clicked.connect(self.delete_row)
        self.button_add_item.clicked.connect(self.add_row)
        self.button_add_item.setMaximumWidth(20)
        self.button_delete_item.setMaximumWidth(20)
        layout_tools.addWidget(self.button_add_item)
        layout_tools.addWidget(self.button_delete_item)
        layout.addLayout(layout_tools)
        layout.addWidget(self.list_widget)
        self.central_layout.addLayout(layout)
        self.data = initial_value
        self.new_id_func = new_id_func

        self.text_edit = QLineEdit(parent=self.list_widget)
        self.text_edit.setWindowFlags(self.text_edit.windowFlags() | Qt.Dialog | Qt.FramelessWindowHint)
        self.text_edit.hide()
        self.completer = QCompleter()
        self.text_edit.setCompleter(self.completer)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

    def set_completions(self, completions: List[str]):
        """
        设置补全内容
        Args:
            completions:

        Returns:

        """
        self.completer.setModel(QStringListModel(completions))

    def new_id(self):
        if callable(self.new_id_func):
            return self.new_id_func()
        else:
            return None

    def add_row(self):
        self.data = self.get_value()
        self.data[0].append(self.new_id())
        self.data[1].append('Unnamed')
        self.list_widget.addItem(QListWidgetItem('Unnamed'))

    def delete_row(self):
        index = self.list_widget.currentIndex().row()
        self.data[0].pop(index)
        self.data[1].pop(index)
        self.list_widget.takeItem(index)

    def on_listwidget_double_cicked(self, evt: QMouseEvent):
        print('edit', evt)
        pos = evt.globalPos()
        current_item: QListWidgetItem = self.list_widget.currentItem()

        def set_value():
            current_item.setText(self.text_edit.text())
            self.text_edit.hide()
            self.text_edit.returnPressed.disconnect(set_value)

        item: QListWidgetItem = self.list_widget.currentItem()

        self.text_edit.setGeometry(pos.x(), pos.y(), 200, 20)
        self.text_edit.returnPressed.connect(set_value)
        self.text_edit.show()
        # self.list_widget.editItem(item)

    def get_value(self):
        text = []
        for i in range(self.list_widget.count()):
            text.append(self.list_widget.item(i).text())
        self.data[1] = text
        assert len(self.data[1]) == len(self.data[0]), repr(self.data)
        return self.data

    def set_value(self, data: List[List[str]]):
        assert isinstance(data, list), data
        self.list_widget.clear()
        self.list_widget.addItems(data[1])
        self.data = data
        for index in range(self.list_widget.count()):
            item: QListWidgetItem = self.list_widget.item(index)
