"""
This is node manager.

"""
import copy
import json
import os
import sys
from typing import List, Dict, Tuple, Union, TYPE_CHECKING, Type

from widgets import PMGPanel
from widgets.flowchart.core.flow_content import FlowContentForFunction
from widgets.flowchart.core.flow_items import CustomPort
from widgets.flowchart.core.flow_node import Node
from PySide2.QtCore import Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QDialog, QToolBox, QTextEdit

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)

if TYPE_CHECKING:
    from widgets.flowchart.core.flowchart_widget import PMGraphicsScene
    from widgets.flowchart.core.flow_content import PMGBaseFlowContent, PMGFlowContent


class NodeManagerWidget(QWidget):
    signal_new_node = Signal(Node)

    def __init__(self, parent: QWidget = None, scene: 'PMGraphicsScene' = None):
        super().__init__(parent)
        self.content_classes: Dict[str, Type[PMGFlowContent]] = {}
        self.text_to_class_name: Dict[str, str] = {}
        self.groups = ['simple_calc', 'dataset', 'plot', 'linear_algebra', 'io']
        self.trans_dic = {'simple_calc': '计算',
                          'dataset': '数据集',
                          'plot': '绘图',
                          'logic': '逻辑',
                          'linear_algebra': '线性代数',
                          'io': '输入输出'
                          }
        self.node_info_dic: Dict[str, Dict[str, Dict[str, object]]] = {key: dict() for key in self.groups}

        self.setLayout(QVBoxLayout())
        self.top_layout = QHBoxLayout()
        self.layout().addLayout(self.top_layout)
        # self.button_edit = QPushButton('Edit')
        # self.button_add = QPushButton('Add')
        # self.top_layout.addWidget(self.button_edit)
        # self.top_layout.addWidget(self.button_add)
        # self.button_edit.clicked.connect(self.on_edit)
        # self.button_add.clicked.connect(self.on_add)

        self.toolbox = QToolBox()
        self.list_widgets: Dict[str, QListWidget] = {}
        for text in self.groups:
            list_widget = QListWidget()
            list_widget.doubleClicked.connect(self.on_item_double_clicked)
            self.layout().addWidget(self.toolbox)
            self.toolbox.addItem(list_widget, self.trans_dic[text])
            self.list_widgets[text] = list_widget
        self.scene: 'PMGraphicsScene' = scene
        self.setMinimumWidth(300)
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
            group_name = self.toolbox.itemText(self.toolbox.currentIndex())
            curr_text = list_widget.currentItem().text()
            dic = self.node_info_dic[group_name][curr_text]
            edit_layout = QHBoxLayout()
            input_widget = QTextEdit()
            edit_layout.addWidget(input_widget)
            check_button = QPushButton(text='check')
            edit_layout.addWidget(check_button)
            input_widget.setText(repr(dic['params']))
            views = [
                ('line_ctrl', 'text', 'Node Text', dic['text']),
                ('check_ctrl', 'inputs_changeable', 'Input Ports Changeable', dic['ports_changeable'][0]),
                ('check_ctrl', 'outputs_changeable', 'Output Ports Changeble', dic['ports_changeable'][1]),
                ('editor_ctrl', 'code', 'Input Python Code', dic['code'], 'python'),
                ('list_ctrl', 'inputs', 'Set Inputs', [[None] * len(dic['inputs']), dic['inputs']], lambda: None),
                ('list_ctrl', 'outputs', 'Set Outputs', [[None] * len(dic['outputs']), dic['outputs']], lambda: None),
                ('file_ctrl', 'icon', 'Set Icon', dic['icon']),
                ('combo_ctrl', 'group', 'Group Name', dic['group'], self.groups)
            ]
            sp = PMGPanel(parent=None, views=views)
            dialog = QDialog(self)

            def verify():
                try:
                    text = input_widget.document().toPlainText()
                    l = eval(text)
                    if isinstance(l, list):
                        dialog2 = QDialog(dialog)
                        sp2 = PMGPanel(parent=None, views=l)
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
                params = eval(input_widget.document().toPlainText())
            except:
                import traceback
                traceback.print_exc()
            group = self.get_current_list_widget_group()
            if isinstance(params, list):
                self.node_info_dic[group][curr_text]['params'] = params
            self.node_info_dic[group][curr_text]['text'] = dic['text']
            self.node_info_dic[group][curr_text]['icon'] = dic['icon']
            self.node_info_dic[group][curr_text]['code'] = dic['code']
            self.node_info_dic[group][curr_text]['inputs'] = dic['inputs'][1]
            self.node_info_dic[group][curr_text]['outputs'] = dic['outputs'][1]
            self.node_info_dic[group][curr_text]['group'] = dic['group']
            self.node_info_dic[group][curr_text]['ports_changeable'] = [dic['inputs_changeable'],
                                                                        dic['outputs_changeable']]
            list_widget.item(curr_row).setText(dic['text'])
            self.save_node_templetes()
            self.load_nodes()
        else:
            return

    def add_node(self, text: str, inputs: List[str], outputs: List[str], ports_changeable: List[bool],
                 params: List[Union[List, Tuple]] = '', icon_path: str = '', func_str: str = ''):
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
        content.set_params(params)
        content.ports_changable = ports_changeable
        node.set_content(content)
        self.scene.add_node(node)

    def on_item_double_clicked(self):
        list_widget: QListWidget = self.toolbox.currentWidget()
        group = self.get_current_list_widget_group()
        curr_row = list_widget.currentRow()

        if curr_row >= 0:
            curr_text = list_widget.currentItem().text()
            if curr_text in self.node_info_dic[group]:
                node_info = self.node_info_dic[group][curr_text]
                text: str = node_info.get('text')
                inputs: List[str] = node_info.get('inputs')
                outputs: List[str] = node_info.get('outputs')
                code: str = node_info.get('code')
                params: List = node_info.get('params')
                icon_path: str = node_info.get('icon')
                ports_changeable: List[bool] = node_info.get('ports_changeable')
                params = copy.deepcopy(params)  # 需要复制一份再传过去，否则会是一个对象。
                self.add_node(text, inputs, outputs, ports_changeable, params, icon_path, code)
            else:
                content: PMGFlowContent = self.content_classes.get(self.text_to_class_name[curr_text])()

                node_id = self.scene.new_id()
                input_ports = [CustomPort(node_id + ':input:%d' % int(i + 1), text=name, port_type='input') for i, name
                               in enumerate(content.input_args_labels)]
                output_ports = [CustomPort(node_id + ':output:%d' % int(i + 1), text=name, port_type='output') for
                                i, name in
                                enumerate(content.output_ports_labels)]
                node = Node(canvas=self.scene, node_id=node_id, text=content.text, input_ports=input_ports,
                            output_ports=output_ports,
                            icon_path=content.icon_path,
                            look={})
                content.node = node
                # content.class_name = curr_text
                node.set_content(content)
                self.scene.add_node(node)
                pass

    def add_node_info(self, info_dic: Dict[str, object]):
        """
        add new infomation of node
        """
        group = self.get_current_list_widget_group()
        text = info_dic.get('text')
        self.get_current_list_widget().addItem(text)
        self.node_info_dic[group][text](info_dic)

    def get_current_list_widget(self) -> QListWidget:
        return self.toolbox.currentWidget()

    def get_current_list_widget_group(self) -> str:
        text = self.toolbox.itemText(self.toolbox.currentIndex())
        for k, v in self.trans_dic.items():
            if text == v:
                return k
        return ''

    def load_nodes(self):
        """
        加载节点
        加载节点之后，可以
        """
        import pandas
        self.node_info_dic = {key: dict() for key in self.groups}
        return
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
            self.node_info_dic[dic['group']][dic['text']] = dic

        self.refresh_list()

    def save_node_templetes(self):
        return
        import pandas

        columns = ['text', 'inputs', 'outputs', 'ports_changeable', 'params', 'icon', 'group', 'code']
        content = []
        node_infos = []
        for k in self.node_info_dic:
            for k1 in self.node_info_dic[k]:
                node_infos += [self.node_info_dic[k][k1]]  # self.node_info_dic[k]

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
            for k1, info in node_infos.items():
                list_widget.addItem(info['text'])

    def register_node_content(self, content_class: Type['PMGFlowContent'], group_name: str, text: str = ''):
        content = content_class()
        self.list_widgets[group_name].addItem(content.text)
        self.content_classes[content.class_name] = content_class
        self.text_to_class_name[content.text] = content.class_name
