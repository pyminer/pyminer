"""
node properties:
id:str
text:str
icon:str(path of icon)
ports:{}
content:{}

properties of contents:
code:str
type:str
params:List[str]
"""
import json
import os
import sys
import time
from typing import List, Dict

from widgets.flowchart.core.flow_content import FlowContentForFunction, flowcontent_types, PMGFlowContent

from widgets.flowchart.core.flow_node import Node
from widgets.flowchart.core.nodemanager import NodeManagerWidget
from widgets.flowchart.core.flowchart_scene import PMGraphicsScene
from widgets.flowchart.core.flowchart_widget import PMGraphicsView
from PySide2.QtCore import QSize, QCoreApplication, QLineF, Qt, QThread, Signal
from PySide2.QtGui import QColor, QKeyEvent, QWheelEvent, QCloseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QSpacerItem, QSizePolicy, QGraphicsView, \
    QFrame, QApplication, QFileDialog, QMessageBox
from widgets.flowchart.core import PMFlowWidget

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)


class PMGSimulationWidget(PMFlowWidget):
    def __init__(self, parent=None, path=''):
        super().__init__(parent, path)
        self._path = path
        _translate = QCoreApplication.translate
        self.setObjectName("tab_flow")
        self.base_layout = QHBoxLayout(self)
        self.verticalLayout_6 = QVBoxLayout()
        self.base_layout.addLayout(self.verticalLayout_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_3 = QWidget(self)
        self.widget_3.setMinimumSize(QSize(0, 30))
        self.widget_3.setObjectName("widget_3")

        # self.horizontal_layout_down = QHBoxLayout(self.widget_3)
        self.horizontal_layout = QHBoxLayout(self.widget_3)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(1)
        self.horizontal_layout.setObjectName("horizontalLayout_6")

        self.tool_button_run_fg = QToolButton(self.widget_3)
        self.tool_button_run_fg.setText('Run_fg')
        self.horizontal_layout.addWidget(self.tool_button_run_fg)

        self.tool_button_save = QToolButton(self.widget_3)
        self.tool_button_save.setText('Save')
        self.horizontal_layout.addWidget(self.tool_button_save)

        self.tool_button_reset = QToolButton(self.widget_3)
        self.tool_button_reset.setText('Reset')
        self.horizontal_layout.addWidget(self.tool_button_reset)

        self.tool_button_undo = QToolButton(self.widget_3)
        self.tool_button_undo.setText('Undo')
        self.horizontal_layout.addWidget(self.tool_button_undo)

        self.tool_button_redo = QToolButton(self.widget_3)
        self.tool_button_redo.setText('Redo')
        self.horizontal_layout.addWidget(self.tool_button_redo)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.widget_3)

        self.graphicsView = PMGraphicsView(self)

        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_6.addWidget(self.graphicsView)

        self.scene = PMGraphicsScene(graphics_view=self.graphicsView, flow_widget=self, allow_multiple_input=True)
        self.scene.setSceneRect(-1000, -1000, 2000, 2000)

        self.node_manager = NodeManagerWidget(scene=self.scene)
        # self.node_manager.scene = self.scene
        self.base_layout.addWidget(self.node_manager)
        self.nodes: List[Node] = self.scene.nodes
        self.lines = self.scene.lines

        self.node_manager.register_node_content(PMGFlowContent, 'simple_calc', 'UserDefinedFunc')
        self.load_nodes_library()
        self.graphicsView.setScene(self.scene)

        self.tool_button_undo.clicked.connect(self.scene.undo)
        self.tool_button_redo.clicked.connect(self.scene.redo)
        # self.tool_button_open.clicked.connect(self.open)
        self.tool_button_reset.clicked.connect(self.reset)
        self.tool_button_save.clicked.connect(self.save)
        self.tool_button_run_fg.clicked.connect(lambda: self.run_in_fg())
        if self._path != '':
            self.scene.load_flowchart(self._path)

    # def load_nodes_library(self):
    #     import widgets.flowchart.nodes.simulation as package_sim
    #     import inspect
    #     for class_name in dir(package_sim):
    #         cls = eval('package_sim.' + class_name)
    #         if inspect.isclass(cls) and issubclass(cls, package_sim.BaseLigralGenerator):
    #             self.node_manager.register_node_content(cls, 'simple_calc')

    def run_in_fg(self, input_args_list: List[object] = None) -> List[object]:
        """
        前端直接进行数据处理，而非在后台线程执行。
        这样不能做耗时操作（因为会卡住界面），但是可以直接获取运行后的数据，并且结果相对简单一些。
        :return:
        """
        from widgets.flowchart.nodes.simulation import BaseLigralGenerator
        j_list = []
        for node in self.scene.nodes:
            content: BaseLigralGenerator = node.content
            j_list.append(content.generate_ligjson())
            print(content.generate_ligjson())
        text = json.dumps(j_list, indent=4)
        print(text)
        ligral_path = r'c:\users\12957\Desktop\ligral.exe'
        file_path = os.path.join(os.path.dirname(__file__), 'temp.lig.json')
        with open(file_path, 'w')as f:
            f.write(text)
        from widgets.utilities.platform import run_command_in_terminal_block
        run_command_in_terminal_block('%s %s --json' % (ligral_path, file_path))


if __name__ == '__main__':
    import cgitb

    cgitb.enable()
    app = QApplication(sys.argv)
    graphics = PMGSimulationWidget()
    graphics.load('flowchart_stat.pmcache')
    graphics.show()
    sys.exit(app.exec_())
