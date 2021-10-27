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
from typing import List

t0 = time.time()
from widgets.flowchart.core.flowchart_widget import PMFlowWidget
from widgets.flowchart.core.flow_node import Node
from widgets.flowchart.core.nodemanager import NodeManagerWidget
from widgets.flowchart.core.flowchart_scene import PMGraphicsScene
from PySide2.QtCore import QSize, QCoreApplication, Qt
from PySide2.QtGui import QColor, QWheelEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QSpacerItem, QSizePolicy, QGraphicsView, \
    QFrame, QApplication, QFileDialog, QMessageBox

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)


class PMGraphicsView(QGraphicsView):
    def wheelEvent(self, event: 'QWheelEvent') -> None:
        """
        鼠标滚轮事件
        :param event:
        :return:
        """
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.scale(1.1, 1.1)
            else:
                self.scale(0.9, 0.9)


class PMDataProcessFlowWidget(PMFlowWidget):
    def __init__(self, parent=None, path=''):
        self._path = path
        _translate = QCoreApplication.translate
        super().__init__(parent)
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

        self.horizontal_layout = QHBoxLayout(self.widget_3)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(1)
        self.horizontal_layout.setObjectName("horizontalLayout_6")

        self.tool_button_run_fg = QToolButton(self.widget_3)
        self.tool_button_run_fg.setText('Run')
        self.horizontal_layout.addWidget(self.tool_button_run_fg)

        self.tool_button_save = QToolButton(self.widget_3)
        self.tool_button_save.setText('Save')
        self.horizontal_layout.addWidget(self.tool_button_save)

        self.tool_button_save_as = QToolButton(self.widget_3)
        self.tool_button_save_as.setText('Save As')
        self.horizontal_layout.addWidget(self.tool_button_save_as)

        self.tool_button_open = QToolButton(self.widget_3)
        self.tool_button_open.setText('Open')
        self.horizontal_layout.addWidget(self.tool_button_open)

        self.tool_button_reset = QToolButton(self.widget_3)
        self.tool_button_reset.setText('Reset')
        self.horizontal_layout.addWidget(self.tool_button_reset)

        self.tool_button_undo = QToolButton(self.widget_3)
        self.tool_button_undo.setText('Undo')
        self.horizontal_layout.addWidget(self.tool_button_undo)
        # self.tool_button_undo.setEnabled(False)

        self.tool_button_redo = QToolButton(self.widget_3)
        self.tool_button_redo.setText('Redo')
        self.horizontal_layout.addWidget(self.tool_button_redo)
        # self.tool_button_redo.setEnabled(False)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.widget_3)

        self.graphicsView = PMGraphicsView(self)

        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_6.addWidget(self.graphicsView)

        self.scene = PMGraphicsScene(graphics_view=self.graphicsView, flow_widget=self)
        self.scene.setSceneRect(-1000, -1000, 2000, 2000)

        self.node_manager = NodeManagerWidget(scene=self.scene)
        # self.node_manager.scene = self.scene
        self.base_layout.addWidget(self.node_manager)
        self.nodes: List[Node] = self.scene.nodes
        self.lines = self.scene.lines

        self.load_nodes_library()
        self.graphicsView.setScene(self.scene)

        self.tool_button_undo.clicked.connect(self.scene.undo)
        self.tool_button_redo.clicked.connect(self.scene.redo)
        self.tool_button_open.clicked.connect(self.open)
        self.tool_button_reset.clicked.connect(self.reset)
        self.tool_button_save.clicked.connect(self.save)
        self.tool_button_save_as.clicked.connect(self.saveas)
        self.tool_button_run_fg.clicked.connect(lambda: self.run_in_fg())
        if self._path != '':
            self.scene.load_flowchart(self._path)

    def load(self, path: str):
        self._path = path
        self.scene.load_flowchart(path)

    def saveas(self):
        """

        Returns:
        """
        file_name, ext = QFileDialog.getSaveFileName(self, '选择文件', '', '流程图文件(*.pmfc)')
        if file_name == '':
            return
        self._path = file_name
        self.save()
        self.setWindowTitle(os.path.basename(file_name))

    def reset(self):
        self.scene.reset_status()
        self.scene.load_flowchart(self._path)
        self.pre_run()



    def run_in_fg(self, input_args_list: List[object] = None) -> List[object]:
        """
        前端直接进行数据处理，而非在后台线程执行。
        这样不能做耗时操作（因为会卡住界面），但是可以直接获取运行后的数据，并且结果相对简单一些。
        :return:
        """
        self.pre_run()
        if input_args_list is None:
            input_args_list = []
        for node in self.scene.nodes:
            node.reset()
        call_id_list = self.scene.topo_sort()
        self.scene.call_id_list = call_id_list
        return self.run_fg_for_one_step(input_args_list)

    def run_fg_for_one_step(self, input_args_list: List[object] = None):
        call_id_list = self.scene.call_id_list
        self.scene.find_node(call_id_list[0]).content._process(input_args_list)

        return self.scene.find_node(call_id_list[-1]).content.results

    def load_nodes_library(self):
        from widgets.flowchart.nodes.simplecalc import Constant, Add, Mul
        from widgets.flowchart.nodes.random import Random
        from widgets.flowchart.nodes.plots import HistPlot
        from widgets.flowchart.nodes.dfoperation import DataReplace
        from widgets.flowchart.nodes.dataframeoperation import DropDuplicated
        from widgets.flowchart.nodes.io import Iterator, ListDirs, PandasImport, PandasFileImport

        self.node_manager.register_node_content(Constant, 'simple_calc')
        self.node_manager.register_node_content(Add, 'simple_calc')
        self.node_manager.register_node_content(Mul, 'simple_calc')
        self.node_manager.register_node_content(Random, 'simple_calc')
        self.node_manager.register_node_content(HistPlot, 'plot')
        self.node_manager.register_node_content(DataReplace, 'dataset')
        self.node_manager.register_node_content(DropDuplicated, 'dataset')
        # self.node_manager.register_node_content(Iterator, 'simple_calc')
        self.node_manager.register_node_content(ListDirs, 'io')
        self.node_manager.register_node_content(PandasImport, 'io')
        self.node_manager.register_node_content(PandasFileImport, 'io')

    def closeEvent(self, e):
        super().closeEvent(e)


if __name__ == '__main__':
    from widgets.flowchart.core.flow_content import PMGFlowContent
    import cgitb

    cgitb.enable()
    app = QApplication(sys.argv)
    graphics = PMDataProcessFlowWidget()
    graphics.load('dataprocess.pmcache')
    graphics.show()
    sys.exit(app.exec_())
