'''
register contents
manager.register('')
'''
import json
import time
import types

from PySide2.QtCore import QObject
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Signal
from typing import TYPE_CHECKING, Callable, List, Union, Tuple, Dict

if TYPE_CHECKING:
    from widgets.flowchart.core.flow_node import Node
    from widgets.flowchart.core.flowchart_widget import PMGraphicsScene


class FlowContentError():
    def __init__(self, brief: str, detailed: str = ''):
        self.brief: str = brief
        if detailed == '':
            detailed = brief
        self.detailed: str = detailed


class PMGBaseFlowContent(QObject):
    signal_exec_started = Signal(str)
    signal_exec_doing = Signal(str)
    signal_exec_finished = Signal(str)
    signal_error_occurs = Signal(FlowContentError)

    def __init__(self):
        super(PMGBaseFlowContent, self).__init__()
        self.ports_changable: List[bool, bool] = [False, False]
        self.input_args = []

        self.results = []
        self.node: 'Node' = None

    def refresh_input_port_indices(self):
        input_port_list = [p.get_connected_port()[0] for p in self.node.input_ports if len(p.get_connected_port()) > 0]
        self.input_port_indices = []
        try:
            for p in input_port_list:
                index = p.node.get_port_index(p)
                self.input_port_indices.append([p, index])
        except Exception as e:
            import traceback
            traceback.print_exc()
            info = traceback.format_exc()
            self.signal_error_occurs.emit(FlowContentError('Module:%s,Error:%s' % (self.node.text, str(e)),
                                                           info))
            return

    def format_param(self) -> str:
        return ''

    def format_text(self) -> str:
        return ''

    def set_params(self, params: Union[str]):
        try:
            if isinstance(params, str):
                params = eval(params)

            if isinstance(params, list):
                self.params = params
                for i in range(len(params)):
                    self.params[i] = self.params[i]
                    param_name = self.params[i][1]
                    param_obj = self.params[i][3]
                    self.vars[param_name] = param_obj
                self.node.display_internal_values(self.format_param())
        except:
            import traceback
            traceback.print_exc()

    def get_settings_params(self) -> List:
        return []

    def _process(self, input_args: list = None):
        if input_args is None:
            input_args = []
            try:
                for p, index in self.input_port_indices:
                    if isinstance(p.node.content.results, types.GeneratorType):
                        input_args = []  # 对于迭代器场合，不需要任何输入值！
                    else:
                        val = p.node.content.results[index]
                        input_args.append(val)

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.signal_error_occurs.emit(FlowContentError(str(e), traceback.format_exc()))
                return
        self.input_args = input_args
        self.signal_exec_started.emit('started')
        if not isinstance(input_args, list):
            self.signal_error_occurs.emit(FlowContentError('input list is not instance of list'))
            return None
        t1 = time.time()
        try:
            result = self.process(*input_args)
        except Exception as e:
            import traceback
            exc = traceback.format_exc()
            self.signal_error_occurs.emit(
                FlowContentError('Module:%s,Error:%s' % (self.node.text, str(e)),
                                 'Info:%s' % (exc)))
            return None
        # self.results = copy.deepcopy(result)
        if isinstance(result, types.GeneratorType):  # 如果发现返回值是一个迭代器，就执行迭代器的next方法。
            step = 0
            while 1:
                try:
                    self.results = next(result)

                    next_content = self.get_next_content()
                    # self.signal_exec_finished.emit(
                    #     'finished\ninput value:%s\noutput value:%s' % (repr(input_list), repr(self.results)))
                    self.signal_exec_finished.emit('Iterating, %s' % repr(self.results))
                    QApplication.instance().processEvents()  # 调用processEvents进行处理
                    if next_content is None:
                        return
                    else:
                        next_content._process()
                except StopIteration:
                    self.signal_exec_finished.emit('finished!')
                    return

        self.results = result
        next_content = self.get_next_content()
        # self.signal_exec_finished.emit(
        #     'finished\ninput value:%s\noutput value:%s' % (repr(input_list), repr(self.results)))
        self.signal_exec_finished.emit('finished')
        if next_content is None:
            return
        else:
            next_content._process()

    def refresh(self):
        pass

    def dump(self):
        return {'code': self.code, 'type': 'function', 'params': self.params, 'ports_changable': self.ports_changable}

    def process(self, *args) -> List[object]:

        return []

    def get_next_content(self) -> 'FlowContentForFunction':
        scene: 'PMGraphicsScene' = self.node.base_rect.scene()
        scene.node_index_to_execute += 1
        node_index = scene.node_index_to_execute
        if node_index >= len(scene.call_id_list):
            scene.node_index_to_execute = 0
            return None
        node_id = scene.call_id_list[node_index]
        return scene.find_node(node_id).content

    def settings_window_requested(self, parent):
        """
        当设置窗口被请求时处理的函数。
        设置结束后，在节点表面上回显参数。需要调用format_params函数
        Args:
            parent: 父控件，若要弹出对话框就必须这样做。

        Returns:

        """
        self.on_settings_requested(parent)
        self.node.display_internal_values(self.format_param())

    def on_settings_requested(self, parent):
        pass


class PMGFlowContent(PMGBaseFlowContent):
    def __init__(self):
        super(PMGFlowContent, self).__init__()
        self.input_args_labels = ['input1']
        self.output_ports_labels = ['output1', 'output2']
        self.class_name = 'Demo Node'
        self.text = '示例节点'
        self.icon_path = ''
        self.info = {}

    def process(self, *args) -> List[object]:
        print('hello world!!!')
        return []

    def dump(self):
        return {'type': self.class_name, 'info': self.info}

    def load_info(self, info: dict):
        self.info = info

    def format_text(self) -> str:
        return self.text


class FlowContentForFunction(PMGBaseFlowContent):

    def __init__(self, node):
        super(FlowContentForFunction, self).__init__()
        self.node = node
        self.node.content = self
        self.code: str = None
        self.params: List[Union[Tuple, int, float, str]] = []
        self.refresh_func: Callable = None

        self.func: Callable = None
        self.input_port_indices: List[List] = []
        self.vars: Dict[str, Union[int, str, float, object]] = {}

    def set_function(self, function_def: str = None, func_name: str = None):
        import time
        t1 = time.time()
        self.code: str = function_def
        g = globals()
        g.update(self.vars)
        exec(self.code, g)
        self.func: Callable = globals().get(func_name)
        self.refresh_func: Callable = globals().get('refresh')
        t2 = time.time()

    def refresh_input_port_indices(self):
        input_port_list = [p.get_connected_port()[0] for p in self.node.input_ports if len(p.get_connected_port()) > 0]
        self.input_port_indices = []
        try:
            for p in input_port_list:
                index = p.node.get_port_index(p)
                self.input_port_indices.append([p, index])
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.signal_error_occurs.emit(
                FlowContentError('Module: %s,Exception:%s' %
                                 (self.node.text, str(e)), traceback.format_exc()))
            return

    def get_settings_params(self):
        return self.params.copy()

    def update_settings(self, settings_dic: dict):
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
                    # val = copy.deepcopy(val)
                    input_args.append(val)

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.signal_error_occurs.emit(FlowContentError('Module:%s,Error:%s' % (self.node.text, e),
                                                               traceback.format_exc()))
                return
        self.input_args = input_args
        self.signal_exec_started.emit('started')
        if not isinstance(input_args, list):
            self.signal_error_occurs.emit(FlowContentError(
                'input list is not instance of list',
                'input list is not instance of list,but of type ' + repr(type(input_args))))
            return None
        t1 = time.time()
        try:
            result = self.process(*input_args)
        except:
            import traceback
            exc = traceback.format_exc()
            traceback.print_exc()
            self.signal_error_occurs.emit('Module:%s\nInfo:%s' % (self.node.text, exc))
            return None
        # self.results = copy.deepcopy(result)

        if isinstance(result, types.GeneratorType):
            step = 0
            while 1:
                try:
                    self.results = next(result)

                    next_content = self.get_next_content()
                    # self.signal_exec_finished.emit(
                    #     'finished\ninput value:%s\noutput value:%s' % (repr(input_list), repr(self.results)))
                    self.signal_exec_finished.emit('finished')
                    if next_content is None:
                        return
                    else:
                        next_content._process()
                except StopIteration:
                    return

        self.results = result
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

    def format_param(self) -> str:
        keys = list(self.vars.keys())
        if len(keys) == 1:
            return str(self.vars[keys[0]])
        else:
            try:
                return json.dumps(self.vars, indent=4)
            except:
                return str(self.vars)

    def process(self, *args):
        assert self.func is not None
        globals().update(self.vars)
        return self.func(*args)

    def refresh(self):
        if callable(self.refresh_func):
            try:
                self.refresh_func(self)
            except:
                import traceback
                traceback.print_exc()


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
        loc = locals()
        exec(code)
        print(loc['function'])


    process()
