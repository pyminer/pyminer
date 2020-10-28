import json
import time
import copy
from PyQt5.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING, Callable, List, Union, Tuple, Dict

if TYPE_CHECKING:
    from pmgwidgets.flowchart.flow_node import Node
    from pmgwidgets.flowchart.flowchart_widget import PMGraphicsScene


class FlowContentForFunction(QObject):
    signal_exec_started = pyqtSignal(str)
    signal_exec_doing = pyqtSignal(str)
    signal_exec_finished = pyqtSignal(str)
    signal_error_occurs = pyqtSignal(str)

    def __init__(self, node):
        super(FlowContentForFunction, self).__init__()
        self.ports_changable = [False, False]
        self.input_args = []

        self.results = []
        self.node: 'Node' = node
        self.node.content = self

        self.code: str = None
        self.params: List[Union[Tuple, int, float, str]] = []
        self.func: Callable = None
        self.input_port_indices: List[List] = []
        self.vars: Dict[str, Union[int, str, float, object]] = {}

    def format_param(self) -> str:
        keys = list(self.vars.keys())
        if len(keys) == 1:
            return str(self.vars[keys[0]])
        else:
            try:
                return json.dumps(self.vars, indent=4)
            except:
                return str(self.vars)

    def set_params(self, params: Union[str]):
        try:
            if isinstance(params, str):
                params = eval(params)

            if isinstance(params, list):
                self.params = params
                for i in range(len(params)):
                    self.params[i] = tuple(self.params[i])
                    param_name = self.params[i][1]
                    param_obj = self.params[i][3]
                    self.vars[param_name] = param_obj
                self.node.display_internal_values(self.format_param())
        except:
            import traceback
            traceback.print_exc()

    def set_function(self, function_def: str = None, func_name: str = None):
        import time
        t1 = time.time()
        self.code: str = function_def
        g = globals()
        g.update(self.vars)
        exec(self.code, g)
        self.func: Callable = globals().get(func_name)
        t2 = time.time()

    def refresh_input_port_indices(self):
        input_port_list = [p.get_connected_port()[0] for p in self.node.input_ports if len(p.get_connected_port()) > 0]
        self.input_port_indices = []
        try:
            for p in input_port_list:
                index = p.node.get_port_index(p)
                self.input_port_indices.append([p, index])
        except:
            import traceback
            traceback.print_exc()
            self.signal_error_occurs.emit('')
            return

    def get_settings_params(self):
        return self.params

    def update_settings(self, settings_dic: dict):
        print(self.params)
        # self.ports_changable[0]= settings_dic['inputs_changeable']
        # self.ports_changable[1]= settings_dic['outputs_changeable']

        for i, tup in enumerate(self.params):
            param_name = tup[1]
            l = list(self.params[i])
            l[3] = settings_dic[param_name]
            self.params[i] = tuple(l)
            self.vars[param_name] = settings_dic[param_name]
        self.node.display_internal_values(self.format_param())

    def _process(self, input_args: list = None):
        if input_args is None:
            input_args = []
            try:
                for p, index in self.input_port_indices:
                    val = p.node.content.results[index]
                    val = copy.deepcopy(val)
                    input_args.append(val)

            except:
                import traceback
                traceback.print_exc()
                self.signal_error_occurs.emit('')
                return
        self.input_args = input_args
        self.signal_exec_started.emit('started')
        if not isinstance(input_args, list):
            self.signal_error_occurs.emit('input list is not instance of list')
            return None
        t1 = time.time()
        try:
            result = self.process(*input_args)
        except:
            import traceback
            exc = traceback.format_exc()
            self.signal_error_occurs.emit('Module:%s\nInfo:%s' % (self.node.text, exc))
            return None
        self.results = copy.deepcopy(result)
        next_content = self.get_next_content()
        # self.signal_exec_finished.emit(
        #     'finished\ninput value:%s\noutput value:%s' % (repr(input_list), repr(self.results)))
        self.signal_exec_finished.emit('finished')
        if next_content is None:
            return
        else:
            next_content._process()

    def dump(self):
        return {'code': self.code, 'type': 'function', 'params': self.params, 'ports_changable': self.ports_changable}

    def process(self, *args):
        assert self.func is not None
        globals().update(self.vars)
        return self.func(*args)

    def get_next_content(self) -> 'FlowContentForFunction':
        scene: 'PMGraphicsScene' = self.node.base_rect.scene()
        scene.node_index_to_execute += 1
        node_index = scene.node_index_to_execute
        if node_index >= len(scene.call_id_list):
            scene.node_index_to_execute = 0
            return None
        node_id = scene.call_id_list[node_index]
        return scene.find_node(node_id).content


class FlowContentEditableFunction(FlowContentForFunction):
    def __init__(self, node, code: str = ''):
        super().__init__(node)
        self.ports_changable = [True, True]
        self.input_args = []
        self.results = []
        self.node: 'Node' = node
        self.node.content = self
        if code == '':
            code = """
import time
def function(x,y):
    return y*2,x+2
        """
        self.code = code
        self.set_function(code, 'function')

    def get_settings_params(self) -> List[Union[Tuple, List]]:
        return [('text_edit', 'code', 'Input Python Code', self.code, 'python')]

    def update_settings(self, settings_dic: dict):
        self.code = settings_dic['code']

    def process(self, *args):
        globals().update({'self': self})
        # exec(self.code, globals())
        # return function(*args)

        return self.func(*args)

    def dump(self):
        return {'code': self.code, 'type': 'custom_function'}


flowcontent_types = {'function': FlowContentForFunction,
                     'custom_function': FlowContentEditableFunction}
if __name__ == '__main__':
    def process():
        self = 123455
        code = """
def function():
    print(123)
        """
        # locals().update({'self':self})
        loc = locals()
        exec(code)
        print(loc['function'])


    process()
