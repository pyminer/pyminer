"""
uiutil子包
这些是用于和PyMiner界面进行交互的函数包定义。这些方式无需用面向对象的方法重写控件，可以直接用面向过程的方法绑定。
workspaceutil中定义了和工作空间交互的方式。比如获取用户输入的变量名、将combobox的变量名与工作空间绑定等。
datashowutil中定义了在qt的控件中显示数据的方式，比如在QTableWidget里面直接显示DataFrame。

"""
from .workspaceutil import *
from .datashowutil import *
from .formatting import *
