"""
树状选择
作者：侯展意
"""
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication,QTreeWidgetItemIterator
import sys


class PMTreeCheckWidget(QTreeWidget):
    def __init__(self, parent=None, data: Dict = None):
        super().__init__(parent)
        self.tree_data = data
        self.set_data(data)
        self.clicked.connect(self.on_item_clicked)
        self.expandAll()

    def set_data(self, data: Dict[str, Dict]):
        self.tree_data = data
        self.refresh_tree()

    def refresh_tree(self):
        data = self.tree_data
        for k in data.keys():
            parent = QTreeWidgetItem(self)
            parent.setText(0, k)
            parent.setFlags(parent.flags()
                            | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for x in data[k].keys():
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, x)
                child.k = k
                child.x = x
                if data[k][x] == True:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)

    def on_item_clicked(self, index):

        item = self.itemFromIndex(index)
        if hasattr(item, 'x') and hasattr(item, 'k'):
            if item.checkState(0) == Qt.Checked:
                self.tree_data[item.k][item.x] = True
            else:
                self.tree_data[item.k][item.x] = False
            print(self.tree_data)

    def get_data(self):
        iter = QTreeWidgetItemIterator(self)
        while iter.value():
            item = iter.value()
            if hasattr(item, 'x') and hasattr(item, 'k'):
                if item.checkState(0) == Qt.Checked:
                    self.tree_data[item.k][item.x] = True
                else:
                    self.tree_data[item.k][item.x] = False
            iter.__iadd__(1)
        return self.tree_data

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        pass
        # print(self.get_data())

foods = {
    'Program Scripts': {'.pyx': True, '.py': True, '.c': True, '.pyi': True, '.dll': True,
                        '.h': True, '.cpp': True, '.ipynb': True},
    'Documents': {'.txt': True, '.md': True, '.doc': True, '.docx': True, '.ppt': True, '.pptx': True},
    'Data Files': {'.csv': True, '.xls': True, '.xlsx': True, '.tab': True, '.dat': True, '.tsv': True,
                   '.sav': True, '.zsav': True, '.sas7bdat': True}}


def main():
    app = QApplication(sys.argv)
    tree = PMTreeCheckWidget(data=foods)
    tree.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
