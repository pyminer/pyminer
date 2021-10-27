import os
import sys
from typing import Tuple, List, Dict, Union, TYPE_CHECKING, Callable
import json
from PySide2.QtWidgets import QGraphicsTextItem, QGraphicsPixmapItem, QMessageBox
from PySide2.QtCore import QObject, QPointF
from PySide2.QtGui import QPixmap

from widgets.flowchart.core.flow_items import CustomRect, CustomPort
from widgets import get_parent_path, assert_in

if TYPE_CHECKING:
    from widgets.flowchart.core.flowchart_widget import PMGraphicsScene, PMFlowWidget
from widgets.flowchart.core.flow_content import FlowContentEditableFunction, FlowContentForFunction, FlowContentError
from widgets.flowchart.nodes.docparser import parse_doc


class Node(QObject):
    """
    Node是一个节点的抽象
    """

    def __init__(self, canvas: 'PMGraphicsScene', node_id, text: str = '', input_ports: List[CustomPort] = None,
                 output_ports: List[CustomPort] = None, icon_path=r'', look: Dict[str, str] = None):
        super(Node, self).__init__()
        assert isinstance(look, dict)
        self.look = look
        direction = self.look.get('direction')
        self.direction = 'E' if direction is None else direction  # 输出端口的方向
        assert_in(self.direction, ['E', 'W'])
        self.look['direction'] = self.direction

        self.id = node_id
        self.text = text if text != '' else node_id
        self.base_rect = CustomRect(self)

        icon_path = os.path.join(get_parent_path(__file__), 'icons', 'logo.png') if icon_path == '' else icon_path
        self.icon_path = icon_path
        pix_map = QPixmap(icon_path)
        self.pix_map_item = QGraphicsPixmapItem(pix_map, parent=self.base_rect)
        self.pix_map_item.setPos(20, 20)

        self.text_item = QGraphicsTextItem(parent=self.base_rect)

        start_left = 50
        self.text_item.setPos(start_left, 10)
        self.text_item.setPlainText(self.text)

        self.internal_value_text = QGraphicsTextItem(parent=self.base_rect)
        self.internal_value_text.setPos(start_left, 30)
        self.internal_value_text.setPlainText('')

        self.status_text = QGraphicsTextItem(parent=self.base_rect)
        self.status_text.setPos(start_left, 100)
        self.status_text.setPlainText('wait')

        self.input_ports = input_ports
        self.output_ports = output_ports

        self.input_ports_dic = {p.id: p for p in input_ports}
        self.output_ports_dic = {p.id: p for p in output_ports}
        self.canvas = canvas
        # self.set_content(content)
        self.setup()

    def display_internal_values(self, val_str: str = ''):
        self.internal_value_text.setPlainText(val_str)

    def set_content(self, content: 'FlowContentEditableFunction' = None):
        self.content: 'FlowContentEditableFunction' = content if content is not None else FlowContentEditableFunction(
            self, '')
        self.content.signal_exec_finished.connect(self.on_exec_finished)
        self.content.signal_exec_started.connect(self.on_exec_started)
        self.content.signal_error_occurs.connect(self.on_error_occurs)
        self.display_internal_values(self.content.format_param())

    def on_error_occurs(self, error: FlowContentError):
        flow_widget: PMFlowWidget = self.canvas.flow_widget
        flow_widget.on_error_occurs(error)

    def on_exec_started(self, content):
        """
        执行前进行的操作
        :param content:
        :return:
        """
        self.status_text.setPlainText(content)

    def on_exec_finished(self, content: str):
        """
        执行完成后进行的操作
        :param content:
        :return:
        """
        self.status_text.setPlainText(content)

    #
    def reset(self):
        self.status_text.setPlainText('wait')

    def get_port_index(self, port: CustomPort):
        """
        获取端口的索引
        :param port:
        :return:
        """
        return self.input_ports.index(port) if port.port_type == 'input' else self.output_ports.index(port)

    def set_icon(self, icon_path: str):
        pass

    def set_pos(self, x: int, y: int):
        """
        设置位置，左上角角点
        :param x:
        :param y:
        :return:
        """
        self.base_rect.setPos(x, y)
        self.refresh_pos()

    def get_pos(self) -> Tuple[int, int]:
        """
        获取位置，左上角角点
        :return:
        """
        pos = self.base_rect.pos()
        return pos.x(), pos.y()

    def refresh_pos(self):
        """
        刷新位置。当节点被拖动的时候，此方法会被触发。
        """
        y = self.base_rect.y()
        dy_input = self.base_rect.boundingRect().height() / (1 + len(self.input_ports))
        dy_output = self.base_rect.boundingRect().height() / (1 + len(self.output_ports))
        if self.direction == 'E':
            x_input = self.base_rect.x() + 5
            x_output = self.base_rect.x() + self.base_rect.boundingRect().width() - 15
        elif self.direction == 'W':
            x_input = self.base_rect.x() + self.base_rect.boundingRect().width() - 15
            x_output = self.base_rect.x() + 5
        else:
            raise NotImplementedError
        for i, p in enumerate(self.input_ports):
            p.setPos(QPointF(x_input, y + int(dy_input * (1 + i))))
        for i, p in enumerate(self.output_ports):
            p.setPos(QPointF(x_output, y + int(dy_output * (1 + i))))
        self.canvas.signal_item_dragged.emit('')

    def setup(self):
        self.base_rect.setPos(80, 80)
        self.canvas.signal_clear_selection.connect(self.base_rect.on_clear_selection)
        self.canvas.addItem(self.base_rect)
        for p in self.input_ports + self.output_ports:
            self.canvas.addItem(p)
            p.port_clicked.connect(self.on_port_clicked)
            p.node = self
        self.refresh_pos()

    def on_port_clicked(self, port: 'CustomPort'):

        if self.canvas.drawing_lines:
            if self.canvas.line_start_port is not port:
                if not port.port_type == self.canvas.line_start_port.port_type:
                    if self.canvas.allow_multiple_input or (
                            (not self.canvas.allow_multiple_input) and len(port.connected_lines) == 0):
                        self.canvas.connect_port(port)

        else:
            if port.port_type == 'output':
                self.canvas.drawing_lines = True
                # if self.canvas.item

                self.canvas.line_start_point = port.center_pos
                self.canvas.line_start_port = port

    def on_delete(self):
        for port in self.input_ports + self.output_ports:
            port.canvas = self.canvas
            port.on_delete()
        self.canvas.removeItem(self.base_rect)
        self.canvas.nodes.remove(self)
        self.deleteLater()

    def __repr__(self):
        s = super(Node, self).__repr__()
        return s + repr(self.input_ports) + repr(self.output_ports)

    def get_port(self, port_id: str) -> 'CustomPort':
        for port in self.input_ports + self.output_ports:
            if port_id == port.id:
                return port
        return None

    def add_port(self, port: CustomPort):
        """
        添加一个端口
        :param port:
        :return:
        """

        port_type = port.port_type
        if port_type == 'input':
            self.input_ports.append(port)
            self.input_ports_dic[port.id] = port
        elif port_type == 'output':
            self.output_ports.append(port)
            self.output_ports_dic[port.id] = port
        else:
            raise ValueError('port type invalid')
        if port.node is None:
            port.node = self
        self.refresh_pos()
        self.canvas.addItem(port)
        port.port_clicked.connect(self.on_port_clicked)

        return port

    def remove_port(self, port: CustomPort):
        """
        删除一个端口
        :param port:
        :return:
        """

        port_type = port.port_type
        if port_type == 'input':
            self.input_ports.remove(port)
            self.input_ports_dic.pop(port.id)
        elif port_type == 'output':
            self.output_ports.remove(port)
            self.output_ports_dic.pop(port.id)
        else:
            raise ValueError('port type invalid')

        port.on_delete()
        self.refresh_pos()

    def change_property(self, property: Dict[str, Union[int, str]]):
        """
        改变各个端口的文字、端口的数目以及文字。
        :param property:
        :return:
        """
        self.text = property['text']
        self.text_item.setPlainText(self.text)
        self.content.update_settings(property)
        self.valid_port_ids = []
        if property.get('inputs') is not None:
            for input_id, input_text in zip(property['inputs'][0], property['inputs'][1]):
                self.valid_port_ids.append(input_id)
                p = self.get_port(input_id)
                if p is None:
                    p = self.add_port(CustomPort(port_id=input_id, text=input_text, port_type='input'))
                p.set_text(input_text)
            for p in self.input_ports:
                if p.id not in self.valid_port_ids:
                    self.remove_port(p)

        if property.get('outputs') is not None:
            for output_id, output_text in zip(property['outputs'][0], property['outputs'][1]):
                self.valid_port_ids.append(output_id)
                p = self.get_port(output_id)
                if p is None:
                    p = self.add_port(CustomPort(port_id=output_id, text=output_text, port_type='output'))
                p.set_text(output_text)

            for p in self.output_ports:
                if p.id not in self.valid_port_ids:
                    self.remove_port(p)

    def change_ports_property(self, property: Dict[str, Union[int, str]]):
        """
        改变各个端口的文字、端口的数目以及文字。
        :param property:
        :return:
        """
        self.text = property['text']
        self.text_item.setPlainText(self.text)
        self.valid_port_ids = []
        if property.get('inputs') is not None:
            for input_id, input_text in zip(property['inputs'][0], property['inputs'][1]):
                self.valid_port_ids.append(input_id)
                p = self.get_port(input_id)
                if p is None:
                    p = self.add_port(CustomPort(port_id=input_id, text=input_text, port_type='input'))
                p.set_text(input_text)
            for p in self.input_ports:
                if p.id not in self.valid_port_ids:
                    self.remove_port(p)

        if property.get('outputs') is not None:
            for output_id, output_text in zip(property['outputs'][0], property['outputs'][1]):
                self.valid_port_ids.append(output_id)
                p = self.get_port(output_id)
                if p is None:
                    p = self.add_port(CustomPort(port_id=output_id, text=output_text, port_type='output'))
                p.set_text(output_text)

            for p in self.output_ports:
                if p.id not in self.valid_port_ids:
                    self.remove_port(p)

    def on_edit_ports(self):
        from widgets import PMGPanel
        from PySide2.QtWidgets import QDialog, QVBoxLayout
        dlg = QDialog(self.base_rect.scene().flow_widget)
        sp = PMGPanel()
        p: 'CustomPort' = None
        input_ids, output_ids = [], []
        input_texts, output_texts = [], []
        self._last_var = 0

        def new_id_input():
            node_id = self.id
            max_val = 0
            for p in self.input_ports:
                n, t, p = p.parse_id()
                if max_val < int(p):
                    max_val = int(p)
            self._last_var += 1
            return '%s:input:%d' % (node_id, max_val + self._last_var)

        def new_id_output():
            node_id = self.id
            max_val = 0
            for p in self.output_ports:
                n, t, p = p.parse_id()
                if max_val < int(p):
                    max_val = int(p)
            self._last_var += 1
            return '%s:output:%d' % (node_id, max_val + self._last_var)

        for p in self.input_ports:
            input_ids.append(p.id)
            input_texts.append(p.text)

        for p in self.output_ports:
            output_ids.append(p.id)
            output_texts.append(p.text)

        views = []
        # views += self.content.get_settings_params()
        views += [('line_ctrl', 'text', 'Node Text', self.text),
                  ]
        if self.content.ports_changable[0]:
            views.append(('list_ctrl', 'inputs', 'Set Inputs', [input_ids, input_texts], new_id_input))
        if self.content.ports_changable[1]:
            views.append(('list_ctrl', 'outputs', 'Set Outputs', [output_ids, output_texts], new_id_output))
        sp.set_items(views)
        dlg.setLayout(QVBoxLayout())
        dlg.layout().addWidget(sp)
        dlg.exec_()

        dic = sp.get_value()
        self.change_ports_property(dic)

    def on_edit_properties_requested(self):
        """
        Show Settings Panel.
        If It was customized node,it will call the function of the content.
        Or the default settings parameters will be got.
        Returns:

        """
        from widgets import PMGPanel
        from PySide2.QtWidgets import QDialog, QVBoxLayout

        if isinstance(self.content, FlowContentForFunction):
            dlg = QDialog(self.base_rect.scene().flow_widget)
            sp = PMGPanel()
            p: 'CustomPort' = None
            input_ids, output_ids = [], []
            input_texts, output_texts = [], []
            self._last_var = 0

            def new_id_input():
                node_id = self.id
                max_val = 0
                for p in self.input_ports:
                    n, t, p = p.parse_id()
                    if max_val < int(p):
                        max_val = int(p)
                self._last_var += 1
                return '%s:input:%d' % (node_id, max_val + self._last_var)

            def new_id_output():
                node_id = self.id
                max_val = 0
                for p in self.output_ports:
                    n, t, p = p.parse_id()
                    if max_val < int(p):
                        max_val = int(p)
                self._last_var += 1
                return '%s:output:%d' % (node_id, max_val + self._last_var)

            for p in self.input_ports:
                input_ids.append(p.id)
                input_texts.append(p.text)

            for p in self.output_ports:
                output_ids.append(p.id)
                output_texts.append(p.text)

            views = []
            views += self.content.get_settings_params()
            views += [('line_ctrl', 'text', 'Node Text', self.text),
                      ]
            if self.content.ports_changable[0]:
                views.append(('list_ctrl', 'inputs', 'Set Inputs', [input_ids, input_texts], new_id_input))
            if self.content.ports_changable[1]:
                views.append(('list_ctrl', 'outputs', 'Set Outputs', [output_ids, output_texts], new_id_output))
            sp.set_items(views)
            dlg.setLayout(QVBoxLayout())
            dlg.layout().addWidget(sp)
            dlg.exec_()

            dic = sp.get_value()
            self.change_property(dic)
        else:
            try:
                self.content.settings_window_requested(self.canvas.flow_widget)
            except Exception as e:
                import traceback
                exc = traceback.format_exc()
                print(exc)
                QMessageBox.warning(self.canvas.flow_widget, 'Error', str(e))

    def invert(self):
        self.direction = 'W' if self.direction == 'E' else 'E'
        self.refresh_pos()
        self.look['direction'] = self.direction


def make_calculation_node(node_function: Callable) -> 'Node':
    info = parse_doc(node_function)
    content = FlowContentEditableFunction(code=0)
