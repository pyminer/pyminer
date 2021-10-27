def preprocess_shape(shape, *shapes):
    """
    对shape进行预处理
    :param shape:
    :param shapes:
    :return:
    """
    if isinstance(shape, (tuple, list)):
        assert len(shapes) == 0, 'if first param is list or tuple, only one positional parameter is allowed'
        result = shape
    elif isinstance(shape, int) and all([isinstance(s, int) for s in shapes]):
        result = (shape, *shapes)
    else:
        assert False, 'wrong parameter'
    return result


def preprocess_type(type, dtype):
    """
    对type进行预处理
    :param type:
    :param dtype:
    :return:
    """
    if type is float:
        if dtype is None:  # 没有修改过参数
            result = float
        else:  # 指定了dtypes
            result = dtype
    else:
        if dtype is None:  # 仅指定了type
            result = type
        else:
            assert False, 'only one of `type` and `dtype` could be specified'
    return result
