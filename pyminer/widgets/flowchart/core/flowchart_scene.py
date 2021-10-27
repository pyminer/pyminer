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
import logging
import os
import time
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from widgets import PMGFlowContent
from widgets.flowchart.core.flow_content import FlowContentForFunction, flowcontent_types
from widgets.flowchart.core.flow_items import CustomPort, CustomLine, CustomMidPoint, CustomRect
from widgets.flowchart.core.flow_node import Node
from widgets.utilities.uilogics.undomanager import UndoManager
from PySide2.QtCore import QLineF, Qt, QPointF, Signal
from PySide2.QtGui import QPen, QColor, QKeyEvent
from PySide2.QtWidgets import QGraphicsView, \
    QGraphicsScene, QGraphicsSceneMouseEvent, QMenu, QGraphicsSceneContextMenuEvent

logger = logging.getLogger(__name__)
COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)


class PMGraphicsScene(QGraphicsScene):
    signal_item_dragged = Signal(str)  # 拖拽控件发生的事件。
    signal_port_clicked = Signal(str)  # 点击端口的事件
    signal_clear_selection = Signal()  # 清除选择的事件

    def __init__(self, parent=None, graphics_view: 'QGraphicsView' = None, flow_widget: 'PMFlowWidget' = None,
                 allow_multiple_input=False):
        super().__init__(parent)
        self.undo_manager = UndoManager()
        self.call_id_list: List = []
        self.lines: List[CustomLine] = []
        self.nodes: List['Node'] = []
        self.selected_items = []
        self.drawing_lines = False
        self.line_start_port = None
        self.line_start_point = None
        self.line_end_port = None
        self.node_index_to_execute = 0
        self.line = self.addLine(0, 0, 1, 1, QPen())
        self.graphics_view = graphics_view
        self.flow_widget: 'PMFlowWidget' = flow_widget
        self.allow_multiple_input = allow_multiple_input

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        super(PMGraphicsScene, self).contextMenuEvent(event)
        self.menu = QMenu()
        node = self.get_rect_under_mouse().node

        self.menu.addAction('Delete Selected').triggered.connect(lambda x: self.delete_selected_item())
        print(node)
        if node is not None:
            self.menu.addAction('Invert').triggered.connect(lambda x: self.invert_node(node))
        base_rect = self.get_rect_under_mouse()
        if base_rect is not None:
            self.menu.addAction('Edit').triggered.connect(lambda x: base_rect.node.on_edit_properties_requested())
            self.menu.addAction('Edit Ports').triggered.connect(lambda x: base_rect.node.on_edit_ports())
        self.menu.exec_(event.screenPos())

    def keyPressEvent(self, event: 'QKeyEvent') -> None:
        if event.key() == Qt.Key_Delete:
            self.delete_selected_item()
        elif event.key() == Qt.Key_Escape:
            if self.drawing_lines:
                self.drawing_lines = False
                self.line.hide()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)
        self.update_viewport()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(PMGraphicsScene, self).mouseMoveEvent(event)
        if self.drawing_lines:
            self.line.show()
            self.line_end_point = event.scenePos()
            self.line.setLine(QLineF(self.line_end_point, self.line_start_point))
        self.sceneRect()
        self.update_viewport()

    def connect_port(self, end_port):
        self.line.hide()
        line = CustomLine(self.line_start_port, end_port, self)
        self.lines.append(line)
        self.addItem(line)
        self.signal_item_dragged.connect(line.refresh)
        self.drawing_lines = False
        self.add_stat()

    def find_port(self, port_id: int):
        for n in self.nodes:
            for p in n.input_ports + n.output_ports:
                if p.id == port_id:
                    return p
        return None

    def find_node(self, node_id: str) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def new_id(self) -> str:
        max_id = 0
        for n in self.nodes:
            a = int(n.id)
            if a > max_id:
                max_id = a
        new_id = max_id + 1
        return str(new_id)

    def add_node(self, node: 'Node' = None):
        """
        添加节点
        Args:
            node:

        Returns:

        """
        assert isinstance(node, Node)

        self.nodes.append(node)
        self.add_stat()

    def get_rect_under_mouse(self) -> CustomRect:
        # items =[]
        for n in self.nodes:
            if n.base_rect.isUnderMouse():
                return n.base_rect
        return None

    def get_selected_base_rects(self) -> List[CustomRect]:
        items = []
        for selected_item in self.selected_items:
            print(self.selected_items)
            if isinstance(selected_item, CustomRect):
                items.append(selected_item)
        return items

    def invert_node(self, node: Node):
        if node is not None:
            node.invert()
            self.update_viewport()

    def delete_selected_item(self):
        """
        删除被选中的物品
        :return:
        """
        self.add_stat()
        for selected_item in self.selected_items:
            if hasattr(selected_item, 'on_delete'):
                selected_item.on_delete()
        self.selected_items = []

    def unselect_item(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)

    def select_item(self, item):
        if item not in self.selected_items:
            self.selected_items.append(item)

    def topo_sort(self, draw_graph=False):
        """
        拓扑排序
        :return:
        """
        lines = []
        for l in self.lines:
            start_id, end_id = l.start_port.node.id, l.end_port.node.id
            lines.append((start_id, end_id))
        import networkx

        DG = networkx.DiGraph(lines)
        if draw_graph:
            networkx.draw_spring(DG, with_labels=True)
            import matplotlib.pyplot as plt
            plt.show()
        return list(networkx.topological_sort(DG))

    def load_flowchart(self, path=''):

        file = './examples/flowchart_stat_demo.json' if path == '' else path
        if not os.path.exists(file):
            return

        with open(file, 'r') as f:
            text = f.read()
            self.flowchart_from_json(text)

    def add_stat(self):
        self.undo_manager.push(self.flowchart_to_json())

    def undo(self):
        """
        重做
        :return:
        """
        result = self.undo_manager.undo()
        print('undo', result)
        if result is not None:
            self.reset_stat(result)

    def redo(self):
        """
        撤销
        :return:
        """
        result = self.undo_manager.redo()
        print(result)
        if result is not None:
            self.reset_stat(result)

    def dump_flowchart(self, path=''):
        t0 = time.time()
        file = './examples/flowchart_stat_demo.json' if path == '' else path
        json_str = self.flowchart_to_json()
        with open(file, 'w') as f:
            f.write(json_str)
        t1 = time.time()
        print('time elapsed for dumping flowchart', t1 - t0)

    def flowchart_from_json(self, json_str):
        t0 = time.time()
        fc_info_dic: Dict[str, Dict] = json.loads(json_str)
        nodes_dic = fc_info_dic['nodes']
        connections: List = fc_info_dic['connections']

        for k in nodes_dic.keys():
            node_property = nodes_dic[k]
            node_name = node_property['id']
            node_pos = node_property['pos']
            node_text = node_property['text']
            node_icon_path = node_property['icon']
            node_content = node_property['content']
            node_look = node_property.get('look')
            node_look = node_look if node_look is not None else {}
            input_ports = []
            for input_port_id in node_property['input_ports'].keys():
                port_property = node_property['input_ports'][input_port_id]
                port = CustomPort(port_id=input_port_id, text=port_property['text'], content=port_property['contents'],
                                  port_type='input')
                input_ports.append(port)
            output_ports = []
            for output_port_id in node_property['output_ports'].keys():
                port_property = node_property['output_ports'][output_port_id]
                port = CustomPort(port_id=output_port_id, text=port_property['text'], content=port_property['contents'],
                                  port_type='output')
                output_ports.append(port)

            node = Node(self, node_name, text=node_text, input_ports=input_ports, output_ports=output_ports,
                        icon_path=node_icon_path, look=node_look)
            content_type = flowcontent_types.get(node_content.get('type'))
            if content_type is not None:
                content: 'FlowContentForFunction' = content_type(node=node)
                code = node_content['code']
                content.set_function(code, 'function')
                params = node_content.get('params')
                content.set_params([] if params is None else params)
                ports_changable = node_content.get('ports_changable')
                ports_changable = ports_changable if ports_changable is not None else [False, False]
                content.ports_changable = ports_changable
            else:
                content: 'PMGFlowContent' = self.flow_widget.node_manager.content_classes.get(
                    node_content.get('type'))()
                content.node = node
                content.class_name = node_content.get('type')
                content.load_info(node_content.get('info'))
            node.set_content(content)
            node.set_pos(*node_pos)
            self.nodes.append(node)
        for line_property in connections:
            start_id, end_id = line_property['start_id'], line_property['end_id']
            start_port, end_port = self.find_port(start_id), self.find_port(end_id)
            mid_positions = line_property['mid_positions']
            mid_points = []
            for pos in mid_positions:
                mid_points.append(CustomMidPoint(pos=QPointF(*pos)))

            line = CustomLine(canvas=self, start_port=start_port, end_port=end_port, mid_points=mid_points)
            self.addItem(line)
            self.signal_item_dragged.connect(line.refresh)
            self.lines.append(line)
        t1 = time.time()
        print('time elapsed for loading flowchart:', t1 - t0)
        # self.add_stat()

    def reset_status(self):
        self.drawing_lines = False
        self.nodes = []
        self.lines = []
        self.selected_items = []
        self.clear()
        self.line_start_port = None
        self.line_start_point = None
        self.line_end_port = None
        self.node_index_to_execute = 0
        self.line = self.addLine(0, 0, 1, 1, QPen())

    def reset_stat(self, json_str: str):
        self.reset_status()
        self.flowchart_from_json(json_str)

    def flowchart_to_json(self) -> str:
        fc_info = {}
        connections = []
        nodes_dic = {}
        fc_info['nodes'] = nodes_dic
        fc_info['connections'] = connections
        for line in self.lines:
            line_properties = {}
            start_id = line.start_port.id
            end_id = line.end_port.id
            line_properties['start_id'] = start_id
            line_properties['end_id'] = end_id
            mid_positions = line.get_central_points_positions()
            line_properties['mid_positions'] = mid_positions
            connections.append(line_properties)
        for node in self.nodes:
            node_properties = {}
            node_properties['text'] = node.text
            node_properties['id'] = node.id
            node_properties['pos'] = node.get_pos()
            node_properties['icon'] = node.icon_path
            node_properties['content'] = node.content.dump()
            node_properties['look'] = node.look
            input_ports_dic = {}
            output_ports_dic = {}
            for port in node.input_ports:
                input_ports_dic[port.id] = {'id': port.id, 'pos': port.get_pos(), 'contents': {}, 'text': port.text}
            for port in node.output_ports:
                output_ports_dic[port.id] = {'id': port.id, 'pos': port.get_pos(), 'contents': {}, 'text': port.text}
            node_properties['input_ports'] = input_ports_dic
            node_properties['output_ports'] = output_ports_dic
            nodes_dic[node.id] = node_properties
        return json.dumps(fc_info, indent=4)

    def reset(self):
        self.clear()
        self.call_id_list: List = []
        self.lines: List[CustomLine] = []
        self.nodes: List['Node'] = []
        self.drawing_lines = False
        self.line_start_port = None
        self.line_start_point = None
        self.line_end_port = None
        self.node_index_to_execute = 0
        self.line = self.addLine(0, 0, 1, 1, QPen())

    def update_viewport(self):
        self.graphics_view.viewport().update()
