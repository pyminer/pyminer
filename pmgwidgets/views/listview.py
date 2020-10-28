# Create a Qt application
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QListView

app = QApplication(sys.argv)

# Our main window will be a QListView
list = QListView()
list.setWindowTitle('Example List')
list.setMinimumSize(600, 400)

# Create an empty model for the list's data
model = QStandardItemModel(list)

# Add some textual items
foods = [
    '.pyx', '.py', '.c', '.pyi', '.dll', '.h', '.cpp', '.ipynb',
    '.txt', '.md', '.doc', '.docx', '.ppt', '.pptx',
    '.csv', '.xls', '.xlsx','.tab','.dat','.tsv',
    '.sav', '.zsav', '.sas7bdat'
]

for food in foods:
    # create an item with a caption
    item = QStandardItem(food)

    # add a checkbox to it
    item.setCheckable(True)
    item.setTristate(False)
    item.setCheckState(Qt.Checked)

    # Add the item to the model
    model.appendRow(item)
for i in range(model.rowCount()):
    txt = model.item(i).text()
    checked = QStandardItem.checkState(model.item(i))
    print(txt, checked)
# Apply the model to the list view
list.setModel(model)

# Show the window and run the app
list.show()
app.exec_()
