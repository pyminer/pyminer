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
import os
import sys
import time
from typing import List, Dict, Callable, Union
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QSpacerItem, QSizePolicy, QGraphicsView, \
    QFrame, QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QMenu, QGraphicsSceneContextMenuEvent, QFileDialog, \
    QMessageBox, QListWidget, QPushButton, QDialog, QLineEdit, QToolBox
from PyQt5.QtCore import QSize, QCoreApplication, pyqtSignal, QLineF, Qt, QPointF, QThread, QTimer
from PyQt5.QtGui import QPen, QColor, QKeyEvent, QWheelEvent
from pmgwidgets import SettingsPanel

from pmgwidgets.flowchart.flow_items import CustomPort, CustomLine, CustomMidPoint, CustomRect
from pmgwidgets.flowchart.flow_node import Node
from pmgwidgets.flowchart.flow_content import FlowContentEditableFunction, FlowContentForFunction, flowcontent_types
from pmgwidgets.normal.undomanager import UndoManager

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)


class PMGraphicsScene(QGraphicsScene):
    signal_item_dragged = pyqtSignal(str)  # 拖拽控件发生的事件。
    signal_port_clicked = pyqtSignal(str)  # 点击端口的事件
    signal_clear_selection = pyqtSignal()  # 清除选择的事件

    def __init__(self, parent=None, graphics_view: 'QGraphicsView' = None, flow_widget: 'PMFlowWidget' = None):
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

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        super(PMGraphicsScene, self).contextMenuEvent(event)
        self.menu = QMenu()
        self.menu.addAction('New').triggered.connect(lambda x: self.add_node())
        self.menu.addAction('Delete Selected').triggered.connect(lambda x: self.delete_selected_item())
        base_rect = self.get_rect_under_mouse()
        if base_rect is not None:
            self.menu.addAction('Edit').triggered.connect(lambda x: base_rect.node.on_edit_properties_requested())
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
        if node is None:
            node_id = self.new_id()
            input_ports = [CustomPort(node_id + ':input:1'),
                           CustomPort(node_id + ':input:2')]
            output_ports = [CustomPort(node_id + ':output:1', port_type='output'),
                            CustomPort(node_id + ':output:2', port_type='output'),
                            CustomPort(node_id + ':output:3', port_type='output')]
            node = Node(self, node_id, input_ports=input_ports, output_ports=output_ports)
            node.set_content()
            node.set_pos(200, 50)
        else:
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

    def delete_selected_item(self):
        """
        删除被选中的物品
        :return:
        """
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
                        icon_path=node_icon_path)
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


class PMGraphicsView(QGraphicsView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)  # 是否可以切换模式？

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


class NodeManagerWidget(QWidget):
    signal_new_node = pyqtSignal(Node)

    def __init__(self, parent: QWidget = None, scene: 'PMGraphicsScene' = None):
        super().__init__(parent)
        self.groups = ['simple_calc', 'logic', 'matrix', 'plot', 'io']
        self.node_info_dic: Dict[str, List[Dict[str, object]]] = {key: [] for key in self.groups}

        self.setLayout(QVBoxLayout())
        self.top_layout = QHBoxLayout()
        self.layout().addLayout(self.top_layout)
        self.button_edit = QPushButton('Edit')
        self.button_add = QPushButton('Add')
        self.top_layout.addWidget(self.button_edit)
        self.top_layout.addWidget(self.button_add)
        self.button_edit.clicked.connect(self.on_edit)
        self.button_add.clicked.connect(self.on_add)
        self.toolbox = QToolBox()
        self.list_widgets: Dict[str, QListWidget] = {}
        for text in self.groups:
            list_widget = QListWidget()
            list_widget.doubleClicked.connect(self.on_item_double_clicked)
            self.layout().addWidget(self.toolbox)
            self.toolbox.addItem(list_widget, text)
            self.list_widgets[text] = list_widget
        self.scene: 'PMGraphicsScene' = scene
        self.load_nodes()

    def on_add(self):
        group = self.get_current_list_widget_group()
        self.add_node_info(
            {'text': 'untitled', 'inputs': ['input1'], 'outputs': ['output1'], 'code': '', 'params': [], 'icon': '',
             'group': group, 'ports_changeable': [False, False]})

    def on_edit(self):
        list_widget = self.toolbox.currentWidget()
        curr_row = list_widget.currentRow()

        if curr_row >= 0:
            dic = self.node_info_dic[self.toolbox.itemText(self.toolbox.currentIndex())][curr_row]
            edit_layout = QHBoxLayout()
            input_widget = QLineEdit()
            edit_layout.addWidget(input_widget)
            check_button = QPushButton(text='check')
            edit_layout.addWidget(check_button)
            input_widget.setText(repr(dic['params']))
            views = [
                ('line_edit', 'text', 'Node Text', dic['text']),
                ('bool', 'inputs_changeable', 'Input Ports Changeable', dic['ports_changeable'][0]),
                ('bool', 'outputs_changeable', 'Output Ports Changeble', dic['ports_changeable'][1]),
                ('text_edit', 'code', 'Input Python Code', dic['code'], 'python'),
                ('entry_list', 'inputs', 'Set Inputs', [[None] * len(dic['inputs']), dic['inputs']], lambda: None),
                ('entry_list', 'outputs', 'Set Outputs', [[None] * len(dic['outputs']), dic['outputs']], lambda: None),
                ('file', 'icon', 'Set Icon', dic['icon']),
                ('choose_box', 'group', 'Group Name', dic['group'], self.groups)
            ]
            sp = SettingsPanel(parent=None, views=views)
            dialog = QDialog(self)

            def verify():
                try:
                    text = input_widget.text()
                    l = eval(text)
                    if isinstance(l, list):
                        dialog2 = QDialog(dialog)
                        sp2 = SettingsPanel(parent=None, views=l)
                        dialog2.setLayout(QHBoxLayout())
                        dialog2.layout().addWidget(sp2)
                        dialog2.layout().addLayout(edit_layout)
                        dialog2.exec_()

                except:
                    import traceback
                    traceback.print_exc()

            check_button.clicked.connect(verify)
            dialog.setLayout(QVBoxLayout())
            dialog.layout().addWidget(sp)
            dialog.layout().addLayout(edit_layout)
            dialog.exec_()
            dic = sp.get_value()
            params = None
            try:
                params = eval(input_widget.text())
            except:
                import traceback
                traceback.print_exc()
            group = self.get_current_list_widget_group()
            if isinstance(params, list):
                self.node_info_dic[group][curr_row]['params'] = params
            self.node_info_dic[group][curr_row]['text'] = dic['text']
            self.node_info_dic[group][curr_row]['icon'] = dic['icon']
            self.node_info_dic[group][curr_row]['code'] = dic['code']
            self.node_info_dic[group][curr_row]['inputs'] = dic['inputs'][1]
            self.node_info_dic[group][curr_row]['outputs'] = dic['outputs'][1]
            self.node_info_dic[group][curr_row]['group'] = dic['group']
            self.node_info_dic[group][curr_row]['ports_changeable'] = [dic['inputs_changeable'],
                                                                       dic['outputs_changeable']]
            list_widget.item(curr_row).setText(dic['text'])

            self.save_node_templetes()
            self.load_nodes()
        else:
            return

    def add_node(self, text: str, inputs: List[str], outputs: List[str], ports_changeable: List[bool],
                 params_str: str = '', icon_path: str = '',
                 func_str: str = ''):
        """
        添加新的节点
        """
        node_id = self.scene.new_id()
        input_ports = [CustomPort(node_id + ':input:%d' % int(i + 1), text=name, port_type='input') for i, name in
                       enumerate(inputs)]
        output_ports = [CustomPort(node_id + ':output:%d' % int(i + 1), text=name, port_type='output') for i, name in
                        enumerate(outputs)]
        node = Node(canvas=self.scene, node_id=node_id, text=text, input_ports=input_ports, output_ports=output_ports,
                    icon_path=icon_path)
        content = FlowContentForFunction(node)
        content.set_function(func_str, 'function')
        content.set_params(params_str)
        content.ports_changable = ports_changeable
        node.set_content(content)
        self.scene.add_node(node)

    def on_item_double_clicked(self):
        list_widget: QListWidget = self.toolbox.currentWidget()
        group = self.get_current_list_widget_group()
        curr_row = list_widget.currentRow()
        if curr_row >= 0:
            node_info = self.node_info_dic[group][curr_row]
            text: str = node_info.get('text')
            inputs: List[str] = node_info.get('inputs')
            outputs: List[str] = node_info.get('outputs')
            code: str = node_info.get('code')
            params: str = node_info.get('params')
            icon_path: str = node_info.get('icon')
            ports_changeable: List[bool] = node_info.get('ports_changeable')

            self.add_node(text, inputs, outputs, ports_changeable, params, icon_path, code)

    def add_node_info(self, info_dic: Dict[str, object]):
        """
        add new infomation of node
        """
        group = self.get_current_list_widget_group()
        text = info_dic.get('text')
        self.get_current_list_widget().addItem(text)
        print(group)
        self.node_info_dic[group].append(info_dic)
        pass

    def get_current_list_widget(self) -> QListWidget:
        return self.toolbox.currentWidget()

    def get_current_list_widget_group(self) -> str:
        return self.toolbox.itemText(self.toolbox.currentIndex())

    def load_nodes(self):
        """
        加载节点
        加载节点之后，可以
        """
        import pandas
        self.node_info_dic = {key: [] for key in self.groups}
        df = pandas.read_csv(os.path.join(os.path.dirname(__file__), 'lib', 'test.csv'))
        # for k in self.node_info_dic:
        for i in range(df.shape[0]):
            row = df.loc[i]
            dic = {
                'text': row['text'] if not pandas.isna(row['text']) else '',
                'code': row['code'] if not pandas.isna(row['code']) else '',
                'inputs': json.loads(row['inputs']),
                'outputs': json.loads(row['outputs']),
                'params': json.loads(row['params'])
            }
            dic['icon'] = row['icon'] if not pandas.isna(row['icon']) else ''
            dic['group'] = row['group'] if not pandas.isna(row.get('group')) else 'simple_calc'
            ports_changeable = row.get('ports_changeable')
            dic['ports_changeable'] = json.loads(ports_changeable) if ports_changeable is not None else [False, False]
            self.node_info_dic[dic['group']].append(dic)
        self.refresh_list()

    def save_node_templetes(self):
        import pandas

        columns = ['text', 'inputs', 'outputs', 'ports_changeable', 'params', 'icon', 'group', 'code']
        content = []
        node_infos = []
        for k in self.node_info_dic:
            node_infos += self.node_info_dic[k]

        for node_info in node_infos:
            text = node_info.get('text')
            icon = node_info.get('icon')
            inputs = json.dumps(node_info.get('inputs'))
            outputs = json.dumps(node_info.get('outputs'))
            ports_changeable = json.dumps(node_info.get('ports_changeable'))
            params = json.dumps(node_info.get('params'))
            code = node_info.get('code')
            group = node_info.get('group')
            content.append([text, inputs, outputs, ports_changeable, params, icon, group, code])
        df = pandas.DataFrame(content, columns=columns)

        df.to_csv(os.path.join(os.path.dirname(__file__), 'lib', 'test.csv'))

    def refresh_list(self):
        for k in self.node_info_dic:
            node_infos = self.node_info_dic[k]
            list_widget = self.list_widgets[k]
            list_widget.clear()
            for info in node_infos:
                list_widget.addItem(info['text'])


class PMFlowWidget(QWidget):
    def __init__(self, parent=None, path=''):
        self._path = path
        _translate = QCoreApplication.translate
        super().__init__()
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

        self.tool_button_run = QToolButton(self.widget_3)
        self.tool_button_run.setText('Run_bg')
        self.tool_button_run.setIconSize(QSize(25, 25))
        self.tool_button_run.setObjectName("toolButton_4")

        self.horizontal_layout.addWidget(self.tool_button_run)

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
        self.scene.load_flowchart(self._path)
        self.graphicsView.setScene(self.scene)

        self.tool_button_run.clicked.connect(self.run)
        self.tool_button_undo.clicked.connect(self.scene.undo)
        self.tool_button_redo.clicked.connect(self.scene.redo)
        # self.tool_button_open.clicked.connect(self.open)
        self.tool_button_reset.clicked.connect(self.reset)
        self.tool_button_save.clicked.connect(self.save)
        self.tool_button_run_fg.clicked.connect(lambda: self.run_in_fg())

    def on_error_occurs(self, error: str):
        QMessageBox.warning(self, self.tr('Error Occurs'), error)

    def reset(self):
        # self.scene.drawing_lines = False
        self.scene.reset_status()
        # self.scene.clear()
        self.scene.load_flowchart(self._path)
        # self.graphicsView.setScene(self.scene)

    def open(self):
        file_name, ext = QFileDialog.getOpenFileName(self, '选择文件', '', '流程图文件(*.pmcache *.json)')
        if file_name == '':
            return
        try:
            self.reset()
            self.load_flowchart(file_name)
        except:
            import traceback
            traceback.print_exc()
            pass

    def save(self):
        self.scene.dump_flowchart(self._path)
        self.node_manager.save_node_templetes()

    def pre_run(self):
        call_id_list = self.scene.topo_sort()
        for i in call_id_list:
            self.scene.find_node(i).content.refresh_input_port_indices()

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
        # result_dic = {}
        # for i, node_id in enumerate(call_id_list):
        #     n = self.scene.find_node(node_id)
        #     node_result = [n.content.results[i] for i, p in enumerate(n.output_ports)]
        #
        #     result_dic[str(i) + '-' + n.text] = node_result
        # print(result_dic)
        return self.scene.find_node(call_id_list[-1]).content.results

    def run(self):
        """
        运行代码
        """
        call_id_list = self.scene.topo_sort()
        self.scene.call_id_list = call_id_list

        thread = QThread()
        for node in self.scene.nodes:
            node.reset()
            node.content.moveToThread(thread)
        worker = self.scene.find_node(call_id_list[0]).content
        worker.moveToThread(thread)
        thread.started.connect(worker._process)
        thread.start()
        self.worker = worker
        self.thread = thread

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        """
        当文件名为示例文件的时候，不可自动存储，但是可以手动点击保存。
        :param a0:
        :return:
        """
        if not self._path.endswith('.json'):
            self.scene.dump_flowchart(self._path)
        self.node_manager.save_node_templetes()


if __name__ == '__main__':
    import cgitb

    cgitb.enable()
    app = QApplication(sys.argv)
    graphics = PMFlowWidget(path='flowchart_stat.pmcache')
    graphics.show()
    # graphics2 = PMFlowWidget(path='examples/flowchart_stat_demo.json')
    # graphics2.show()
    sys.exit(app.exec_())
