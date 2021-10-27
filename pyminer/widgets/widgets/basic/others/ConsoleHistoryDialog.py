import os

from PySide2 import QtCore
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtWidgets import QApplication, QDialog
from .Ui_ConsoleHistoryDialog import Ui_ConsoleHistoryDialog


class ConsoleHistoryDialog(QDialog, Ui_ConsoleHistoryDialog):
    """
    Class implementing the shell history dialog.
    """

    def __init__(self, console):
        super().__init__()
        self.setupUi(self)
        self.__console = console

        self.deleteButton.clicked.connect(self.on_deleteButton_clicked)
        self.copyButton.clicked.connect(self.on_copyButton_clicked)
        self.reloadButton.clicked.connect(self.on_reloadButton_clicked)
        self.historyList.itemSelectionChanged.connect(
            self.on_historyList_itemSelectionChanged)

        self.reloadButton.click()

    @QtCore.Slot(QtCore.QModelIndex)
    def select(self, item):
        print(item.data())

    @QtCore.Slot()
    def on_historyList_itemSelectionChanged(self):
        """
        Private slot to handle a change of the selection.
        """
        selected = len(self.historyList.selectedItems()) > 0
        self.deleteButton.setEnabled(selected)
        self.copyButton.setEnabled(selected)
        self.executeButton.setEnabled(selected)

    @QtCore.Slot()
    def on_deleteButton_clicked(self):
        """
        Private slot to delete the selected entries from the history.
        """
        for itm in self.historyList.selectedItems():
            ditm = self.historyList.takeItem(self.historyList.row(itm))
            del ditm
        self.historyList.scrollToItem(self.historyList.currentItem())
        self.historyList.setFocus()

    @QtCore.Slot()
    def on_copyButton_clicked(self):
        cmds = self.selected_cmds()
        QApplication.clipboard().setText(cmds)

    @QtCore.Slot()
    def on_executeButton_clicked(self):
        cmds = self.selected_cmds()
        self.__console.hint_command(cmds)
        self.__console.do_execute(cmds, True, '')
        # reload the list because shell modified it
        self.on_reloadButton_clicked()

    @QtCore.Slot()
    def on_reloadButton_clicked(self):
        """
        Private slot to reload the history.
        """
        history = self.__console.history_tail(0)

        self.historyList.clear()
        self.historyList.addItems(history)
        self.historyList.setCurrentRow(
            self.historyList.count() - 1,
            QItemSelectionModel.SelectionFlag.Select)

        self.historyList.scrollToItem(self.historyList.currentItem())

    @QtCore.Slot(QtCore.QModelIndex)
    def on_historyList_doubleClicked(self, item):
        self.on_executeButton_clicked()

    def get_history(self):
        history = []
        for index in range(self.historyList.count()):
            history.append(self.historyList.item(index).text())
        return history

    def selected_cmds(self):
        lines = []
        for index in range(self.historyList.count()):
            # selectedItems() doesn't seem to preserve the order
            itm = self.historyList.item(index)
            if itm.isSelected():
                lines.append(itm.text())
        return (os.linesep.join(lines) + os.linesep).rstrip(os.linesep)
