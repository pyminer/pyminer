from typing import Callable
import json


def parse_doc(function: Callable):
    doc: str = function.__doc__
    row_iter = filter(lambda s: s != '', doc.split('\n'))
    dic = {}
    for row in row_iter:
        split_list = row.split(':')
        if len(split_list) == 2:
            var_name, value_str = split_list
            var_name = var_name.strip()
            value_str = value_str.strip()
            if var_name == 'input' or var_name == 'output':
                assert value_str.startswith('[') and value_str.endswith(']')
                try:
                    dic[var_name] = json.loads(value_str.strip())
                except:
                    raise Exception(repr(value_str.strip()) + ' cannot be parsed as a list!')
            else:
                dic[var_name] = value_str
        else:
            continue
    assert isinstance(dic.get('input'), list), '\'input\' is not defined.'
    assert isinstance(dic.get('output'), list) is not None, '\'output\' is not defined.'
    print(dic)


if __name__ == '__main__':
    from pmgwidgets.flowchart.nodes.reliabilities import relia_and

    doc = relia_and.__doc__
    print(doc)
    parse_doc(relia_and)
