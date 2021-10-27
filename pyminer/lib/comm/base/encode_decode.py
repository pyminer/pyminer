import cloudpickle
import base64
import typing
import json


def encode_objects(var_dic: typing.Dict[str, typing.Any], protocol: int) -> str:
    assert isinstance(var_dic, dict)
    send_dic = {}
    for k, v in var_dic.items():
        try:
            send_dic[k] = cloudpickle.dumps(v, protocol=protocol)
        except Exception:
            import traceback
            traceback.print_exc()
    return base64.b64encode(cloudpickle.dumps(send_dic, protocol=protocol)).decode('ascii')


def decode_objects(pkl_str: str) -> typing.Dict[str, typing.Any]:
    pkl_dic = cloudpickle.loads(base64.b64decode(pkl_str.encode('ascii')))
    var_dic = {}
    for k, v in pkl_dic.items():
        var_dic[k] = cloudpickle.loads(v)
    return var_dic


def dict_to_b64(vars: typing.Dict[str, typing.Any], protocol) -> str:
    msg = {'content': encode_objects(vars, protocol), 'status': 'succeeded'}
    return base64.b64encode(json.dumps(msg).encode('ascii')).decode('ascii')


def b64_to_dict(vars_dic_str: str) -> typing.Dict[str, typing.Any]:
    """
    pickle自动检测协议，无需声明，只要支持即可。
    Args:
        vars_dic_str:

    Returns:

    """
    try:
        msg = json.loads(base64.b64decode(vars_dic_str))
        s = msg.get('content')
        return decode_objects(s)
    except:
        import traceback
        traceback.print_exc()
        return None


def dict_to_pickle(dic: dict, protocol: int = 4) -> bytes:
    assert isinstance(dic, dict)
    send_dic = {}
    for k, v in dic.items():
        try:
            send_dic[k] = cloudpickle.dumps(v, protocol=protocol)
        except Exception:
            import traceback
            traceback.print_exc()
    return cloudpickle.dumps(send_dic)


def pickle_to_dict(pkl: bytes) -> dict:
    """
    加载的时候，pickle的协议会被自动检测，所以，无需声明协议！
    Args:
        pkl:

    Returns:

    """
    d = cloudpickle.loads(pkl)
    assert isinstance(d, dict)
    d1 = {}
    for k, v in d.items():
        d1[k] = cloudpickle.loads(v)
    return d1


if __name__ == '__main__':
    import time
    import numpy as np

    a = np.random.rand(100, 100, 100)
    t0 = time.time()
    m = encode_objects({'a': a, 'b': 123, 'c': 'abcf'})
    d = decode_objects(m)
    print(d)
    t1 = time.time()
    print(t1 - t0)
