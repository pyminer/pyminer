"""
作者：侯展意
协议：LGPL
"""
import json
import os
import sys
import time
from typing import TYPE_CHECKING

t0 = time.time()
path = os.path.dirname(__file__)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
root_path = os.path.dirname(root_path)
from PySide2.QtWidgets import QApplication

sys.path.append(root_path)

from widgets import PMDataProcessFlowWidget

if TYPE_CHECKING:
    from .plugin_nodes.nodes import VariableSetter, VariableGetter
else:
    from plugin_nodes.nodes import VariableSetter, VariableGetter


class DataProcessWidget(PMDataProcessFlowWidget):
    def load_nodes_library(self):
        super().load_nodes_library()
        self.node_manager.register_node_content(VariableGetter, 'io', 'GetVariable')
        self.node_manager.register_node_content(VariableSetter, 'io', 'SetVariable')


if __name__ == '__main__':
    import cgitb

    t1 = time.time()
    cgitb.enable()
    app = QApplication(sys.argv)

    graphics = DataProcessWidget()
    path = os.path.normcase(os.path.join(os.path.dirname(__file__), 'examples', 'drop_duplicated.pmfc'))
    graphics.load(path)
    graphics.show()
    t2 = time.time()
    print(t2 - t1, t1 - t0)
    sys.exit(app.exec_())
