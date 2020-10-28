import pytest

from pyminer2.workspace.datamanager import dataset, exceptions


# 以下测试用例用于测试compare函数是否可以正确进行比较
def test_compare_builtin():
    dataset.DataSet().compare(123, 'int')
    dataset.DataSet().compare('test string', 'str')
    dataset.DataSet().compare(123.4, 'float')
    dataset.DataSet().compare([1, 2, 3, 4], 'list')
    dataset.DataSet().compare({1: 2, 3: 4}, 'dict')
    with pytest.raises(AssertionError):
        dataset.DataSet().compare(123, 'float')


def test_compare_type_not_exists():
    """如果类型不存在，则应报错"""
    with pytest.raises(AssertionError):
        dataset.DataSet().compare(123, 'nosuchtype')


# 以下测试用例用于测试各个数据类型的有效性检测是否正确

def test_matrix():
    d = dataset.DataSet()

    # 正常用法
    assert d.is_valid({'type': 'Matrix', 'value': [[1, 2, 3], [4, 5, 6]]})

    # TODO (panhaoyu) 这里并不是一个合法的矩阵，行列数无法确定，但是却通过了测试
    assert d.is_valid({'type': 'Matrix', 'value': [[1, 2, 3], [4, 5]]})

    # 一维的矩阵，但是格式有误，不是二维的格式，不应当通过测试
    assert not d.is_valid({'type': 'Matrix', 'value': [1, 2, 3, 3, 2, 1]})

    # 包含其他类型，不应该通过测试
    assert not d.is_valid({'type': 'Matrix', 'value': [[2, 4, 5], ['23', 5, 6.2]]})


def test_time_series():
    d = dataset.DataSet()

    # 正常用法
    assert d.is_valid({
        'type': 'TimeSeries',
        'time': [1, 2, 3],
        'data': [3, 2, 1]
    })

    # 找不到data键，不应当通过测试
    assert not d.is_valid({
        'type': 'TimeSeries',
        'time': [1, 2, 3],
        'mdata': [3, 2, 1]
    })

    # type的大小写错误，不应当通过测试
    assert not d.is_valid({
        'type': 'timeseries',
        'time': [1, 2, 3],
        'mdata': [3, 2, 1]
    })


def test_state_space():
    d = dataset.DataSet()
    # 正常用法
    assert d.is_valid({
        'type': 'StateSpace',
        'A': {'type': 'Matrix', 'value': [[2], [1]]},
        'B': {'type': 'Matrix', 'value': [[2], [1]]},
        'C': {'type': 'Matrix', 'value': [[1, 2]]},
        'D': {'type': 'Matrix', 'value': [[0]]},
        'x': ['x1', 'x2'],
        'y': ['column'],
        'u': ['u'],
        'sys': 'str'})

    # 子结构不符合要求，A应该是Matrix而非TimeSeries
    assert not d.is_valid({
        'type': 'StateSpace',
        'A': {'type': 'TimeSeries', 'time': [1, 2, 3], 'mdata': [3, 2, 1]},
        'B': {'type': 'Matrix', 'value': [[2], [1]]},
        'C': {'type': 'Matrix', 'value': [[1, 2]]},
        'D': {'type': 'Matrix', 'value': [[0]]},
        'x': ['x1', 'x2'],
        'y': ['y'],
        'u': ['u'],
        'sys': 'str',
    })


def test_complex():
    d = dataset.DataSet()

    # TODO (panhaoyu) 正常用法，应注意实部或虚部需要支持float退化为int，目前不支持
    assert not d.is_valid({
        'type': 'Complex',
        'real': 2,
        'imag': 3.4,
    })

    # 值类型错误，不应通过测试
    assert not d.is_valid({
        'type': 'Complex',
        'real': 'wrong value',
        'imag': 123.5
    })


def test_vector():
    d = dataset.DataSet()

    # 正常用法
    assert d.is_valid({
        'type': 'Vector',
        'value': [
            1, 2, 3, 2.5, 21.34,
            {'type': 'Complex', 'real': 123.4, 'imag': 532.1}
        ]})

    # 不支持字符串，不应通过测试
    assert not d.is_valid({
        'type': 'Vector',
        'value': [1, 2, 3, 'wrong'],
    })


def test_data_frame():
    d = dataset.DataSet()

    # 正常用法：每一列的行都是相等的
    assert d.is_valid({
        'type': 'DataFrame',
        'table': [
            [1, 2, 3, 4],
            ['asd', 'gds', 'sda', 'asq'],
            [1.2, 5.3, 5, 5.2],
        ],
        'columns': ['index', 'name', 'price'],
    })

    # TODO (panhaoyu) 每一列的行不完全相等，不应通过测试
    assert d.is_valid({
        'type': 'DataFrame',
        'table': [
            [1, 2, 3, 4],
            ['asd', 'gds', 'sda', 'asq'],
            [1.2, 5.3, 5],
        ],
        'columns': ['index', 'name', 'price'],
    })

    # TODO (panhaoyu) 列数与列名数不相等，不应当通过测试
    assert d.is_valid({
        'type': 'DataFrame',
        'table': [
            [1, 2, 3, 4],
            ['asd', 'gds', 'sda', 'asq'],
            [1.2, 5.3, 5, 5.2],
        ],
        'columns': ['index', 'name'],
    })


def test_series():
    d = dataset.DataSet()

    # 正常用法
    assert d.is_valid({
        'type': 'Series',
        'value': [
            [1.2, 3, 452.1, 6.12, -1235],
            [2.135, 5321.5, 6632, 2134, 51.21],
        ]
    })

    # TODO (panhaoyu) Series内的数据类型是否需要统一？


# 以下内容为对于dataset的功能的测试

def test_operations():
    d = dataset.DataSet()
    d.write('NewType', {
        'type': 'Type',
        'structure': {
            'value': [['float']]
        }
    })
    assert d.read('NewType')['structure']['value'][0][0] == 'float'

    d.write('test', {
        'type': 'Matrix',
        'value': [[1, 2, 3], [4, 5, 6], [7.7, 8.8, 9.9]],
    })
    assert d.read('test')['value'][1][1] == 5

    # TODO (panhaoyu) 是否应当支持覆盖？若支持，synchronise的意义是什么？
    d.write('test', {
        'type': 'Matrix',
        'value': [[1, 2, 3], [7, 8, 9], [1, 1, 1], [6, 6, 7]],
    })
    assert d.read('test')['value'][1][1] == 8

    d.synchronise('test', {
        'type': 'Matrix',
        'value': [[1, 2, 4], [2, 2, 2], [9, 6, 10]],
    })
    assert d.read('test')['value'][1][1] == 2


def test_write_builtin_types():
    d = dataset.DataSet()
    with pytest.raises(exceptions.ConflictError):
        d.write('Matrix', {
            'type': 'Type',
            'structure': [['float']]
        })


def test_write_illegal_name():
    d = dataset.DataSet()
    with pytest.raises(AssertionError):
        d.write('123abcABC', {
            'type': 'Type',
            'structure': [['float']],
        })
