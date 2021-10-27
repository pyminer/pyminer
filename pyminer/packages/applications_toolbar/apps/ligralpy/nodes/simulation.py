import sys
from typing import List, Dict

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit
from widgets import PMFlowWidget, PMGFlowContent, PMGPanelDialog


class BaseLigralGenerator(PMGFlowContent):
    def __init__(self):
        super(PMGFlowContent, self).__init__()
        self.input_args_labels = ['input1']
        self.output_ports_labels = ['output1', 'output2']
        self.class_name = self.__class__.__name__
        self.text = self.class_name
        self.icon_path = ''
        self.parameters = []

    def on_settings_requested(self, parent):
        '''

        Args:
            parent:

        Returns:

        '''
        # self.parameters = '' [{'name': 'start', 'required': False, 'type': 'signal'}, {'name': 'level', 'required': False, 'type': 'signal'}]
        views = []
        for para in self.parameters:
            edit = None
            if para['type'] == 'signal':
                if para['required']:
                    ini = self.info.get(para['name'])
                    ini = ini if ini is not None else 0
                    edit = ['number_ctrl', para['name'], para['name'], ini]
                # else:
                #     edit = ['number_ctrl', para['name'], para['name'], 1]
            elif para['type'] == 'string':
                if para['required']:
                    edit = ['line_ctrl', para['name'], para['name'], 'Undefined']

                # else:
                #     edit = ['line_ctrl', para['name'], para['name'], 1]

            if edit is not None:
                views.append(edit)
        print(views)
        dlg = PMGPanelDialog(parent=parent, views=views)

        dlg.setMinimumSize(600, 480)
        dlg.exec_()

        self.info = dlg.panel.get_value()
        print(self.info)

    def format_param(self) -> str:
        return repr(self.info)

    def generate_ligjson(self) -> Dict:
        output_ports = []
        for out_port in self.node.output_ports:
            destinations = []
            for conn_line in out_port.get_connected_lines():
                in_port = conn_line.end_port.text
                destination_id = conn_line.end_port.node.id
                destinations.append({'id': destination_id,
                                     'in-port': in_port})
            # node2 = out_port.connected_lines
            output_ports.append(
                {'name': out_port.text,
                 'destination': destinations
                 })
        return {
            'id': self.node.id,
            'type': self.__class__.__name__,
            'parameters': [{'name': k, 'value': v} for k, v in self.info.items()],
            'out-ports': output_ports
        }
