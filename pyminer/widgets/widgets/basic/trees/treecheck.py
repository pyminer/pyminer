"""
树状选择
作者：侯展意
"""
import os
from typing import Dict
from PySide2.QtCore import Qt, QLocale
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QTreeWidgetItemIterator
import sys
from widgets.utilities.source.translation import create_translator


class PMCheckTree(QTreeWidget):
    def __init__(self, parent=None, data: Dict = None):
        super().__init__(parent)
        self.translator = create_translator(
            path=os.path.join(os.path.dirname(__file__), 'translations',
                              'qt_{0}.qm'.format(QLocale.system().name())))  # translator
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
            print(self.tr(k))
            parent.setText(0, self.tr(k))
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.tr('Program Scripts')
    app.tr('Documents')
    app.tr('Data Files')
    foods = {
        'Program Scripts': {'.pyx': True, '.py': True, '.c': True, '.pyi': True, '.dll': True,
                            '.h': True, '.cpp': True, '.ipynb': True},
        'Documents': {'.txt': True, '.md': True, '.doc': True, '.docx': True, '.ppt': True, '.pptx': True},
        'Data Files': {'.csv': True, '.xls': True, '.xlsx': True, '.tab': True, '.dat': True, '.tsv': True,
                       '.sav': True, '.zsav': True, '.sas7bdat': True}
    }

    tree = PMCheckTree(data=foods)
    tree.show()
    sys.exit(app.exec_())
