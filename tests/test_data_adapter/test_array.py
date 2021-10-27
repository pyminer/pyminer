import numpy
import pytest

from features.workspace.data_adapter import ArrayAdapter


def test_1d_normal():
    """
    对一维数组进行功能的测试。本测试仅保证正常情况下的功能可用，不考虑复杂情况。
    # TODO 请有时间的朋友做一下复杂条件下的测试。
    """
    # 新建一个一维数组
    ar = ArrayAdapter(numpy.array([-1, 10, 52, 13, 562, -122]))  # 从numpy矩阵新建

    # 可以正常获取其形状，一维数组的shape就只有一项
    assert ar.shape == (6,)

    # 获取一维数组的摘要信息，用于进行快速传输
    assert ar.abstract['shape'] == [6, ]

    # 获取一维数组的值
    assert ar.data[1] == 10
    assert ar.data[-1] == -122

    # 将一维数组进行序列化及反序列化
    data = ar.dump()
    assert numpy.all(ArrayAdapter.load(data).data == ar.data)

    # 获取一维数组的显示格式
    assert ar.get_array().to_list() == [-1, 10, 52, 13, 562, -122]
    assert list(ar.get_header_name(0)) == ['0', '1', '2', '3', '4', '5']
    assert list(ar.get_header_name(1)) == ['0']


def test_2d_normal():
    """
    对二维数组进行功能测试。
    """
    ar = ArrayAdapter(numpy.array([[1, 2, 3], [6, 5, 4], [-1.1, -2, -3], [-8, -7, -6]]))
    assert ar.shape == (4, 3)
    assert ar.abstract['shape'] == [4, 3]
    assert ar.data[0, 0] == 1
    assert ar.data[2, 2] == -3
    assert ar.data[2, 0] == -1.1
    assert numpy.all(ar.load(ar.dump()).data == ar.data)
    assert [[j for j in i] for i in ar.get_array()] == [[1, 2, 3], [6, 5, 4], [-1.1, -2, -3], [-8, -7, -6]]
    assert list(ar.get_header_name(0)) == ['0', '1', '2', '3']
    assert list(ar.get_header_name(1)) == ['0', '1', '2']


def test_3d_normal():
    """对三维数组进行功能测试"""
    ar = ArrayAdapter(numpy.ones((3, 4, 5)).cumsum().reshape((3, 4, 5)))
    assert ar.shape == (3, 4, 5)
    assert ar.abstract['shape'] == [3, 4, 5]
    assert ar.data[0, 0, 0] == 1
    assert ar.data[0, 0, 4] == 5
    assert ar.data[2, 3, 4] == 60
    assert numpy.all(ar.load(ar.dump()).data == ar.data)
    for row1, row2 in zip(ar.get_array()[0, 2:4, 2:4].to_list(), [[13, 14], [18, 19]]):
        for v1, v2 in zip(row1, row2):
            assert v1 == v2
    ar = ArrayAdapter(numpy.ones((3, 4, 5, 6, 7, 8)).cumsum().reshape((3, 4, 5, 6, 7, 8)))
    # 下面这一行实际上是选择了六维数组的最后两个维度的(2,4,6)行和(2,4,6)列
    assert ar.get_array()[0, 1, 2, 3, 2:7:2, 2:7:2].to_list() == \
           [[2539, 2541, 2543], [2555, 2557, 2559], [2571, 2573, 2575]]


def test_get_header_name():
    """对于获取表头的函数进行详细的测试，包括各种特殊情况以及各种报错"""
    # TODO 这里只是一个示例，表示如何进行报错的检测，没有进行详细的开发
    ar = ArrayAdapter(numpy.ones((3, 4, 5)).cumsum().reshape((3, 4, 5)))
    assert ar.get_header_name(2).to_list() == ['0', '1', '2', '3', '4']
    with pytest.raises(AssertionError):  # 表示必然会发生这个报错
        ar.get_header_name(3)
