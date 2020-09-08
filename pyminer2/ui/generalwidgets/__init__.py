'''
generalwidgets是PyMiner继承于PyQt5的标准控件库。这个控件库封装PyQt中的标准控件，进行样式或者布局等等的设置，最终得到PyMiner需要的部件。

'''
from .table import PMTableView, PMGTableTabWidget, PMGTableWidget
from .containers import PMTabWidget, PMScrollArea, PMFlowArea
from .window import PMDockWidget, BaseMainWindow
from .toolbars import PMToolBar, TopToolBar, ActionWithMessage
from .basicwidgets import PMToolButton, PMPushButtonPane, PMDockObject
from .layouts import PMFlowLayoutWithGrid, PMFlowLayout
from .sourcemgr import create_icon
from .textctrls import PMGCodeEdit, PythonHighlighter, PMEditorWithLineNumber
