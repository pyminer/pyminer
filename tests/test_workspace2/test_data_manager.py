from pyminer2.workspace2 import data_manager
from pyminer2.data_adapter import ArrayAdapter, UniversalAdapter
import numpy

import pytest


def test_curd():
    """测试数据管理工具的增删改查的基本功能"""
    dm = data_manager.DataManager()

    # 变量赋值后可以直接按字典的方式访问
    dm['a'] = ArrayAdapter(numpy.zeros((3, 4)))
    dm['b'] = ArrayAdapter(numpy.ones((4, 5)))
    dm['c'] = ArrayAdapter(numpy.ones((3, 4)).cumsum().reshape((3, 4)))
    assert dm['a'].data[2, 3] == 0
    assert dm['b'].data[3, 4] == 1
    assert dm['c'].data[2, 3] == 12

    # 变量删除后不可再访问，会报KeyError
    del dm['a']
    with pytest.raises(KeyError):
        _ = dm['a']

    # 变量删除后仍可再重新赋值
    dm['a'] = ArrayAdapter(numpy.ones((4, 5)).cumsum().reshape((4, 5)))
    assert dm['a'].data[3, 4] == 20

    # 变量再删除再重新赋值后，不影响结果
    del dm['a']
    with pytest.raises(KeyError):
        _ = dm['a']
    dm['a'] = ArrayAdapter(numpy.ones((6, 7)).cumsum().reshape((6, 7)))
    assert dm['a'].data[5, 6] == 42


def test_history():
    """
    测试历史记录功能和回收站功能在正常情况下的使用情况
    """
    dm = data_manager.DataManager()
    for i in range(20):  # 循环赋值20次，由于历史记录仅保留15个，前5个值会被抛弃
        dm['a'] = UniversalAdapter(i)
        assert dm['a'].data == i
    assert dm['a'].data == 19  # 最新的值应该是19
    for i in range(14):  # 循环撤销14次
        assert dm.back('a') is True  # 这14次撤销都是可以成功的
        assert dm['a'].data == 18 - i  # 每一次撤销，值都在发生改变
    assert dm.back('a') is False  # 第15次撤销失败，因为已不能再撤销
    assert dm['a'].data == 5
    for i in range(14):  # 循环重做14次
        assert dm.forward('a') is True  # 这14次都是可以成功重做的
        assert dm['a'].data == 6 + i  # 重做前是5，因此重做一次后就变成了6，依次累加
    assert dm.forward('a') is False  # 第15次重做失败，因为已不能再进一步重做

    # 以下内容用于测试重做过程中的数据链的变化
    dm['b'] = UniversalAdapter(1)
    assert dm['b'].data == 1  # [1],[]
    dm['b'] = UniversalAdapter(2)
    assert dm['b'].data == 2  # [1,2],[]
    dm['b'] = UniversalAdapter(3)
    assert dm['b'].data == 3  # [1,2,3],[]
    assert dm.back('b') is True
    assert dm['b'].data == 2  # [1,2],[3]
    assert dm.forward('b') is True
    assert dm['b'].data == 3  # [1,2,3],[]
    assert dm.back('b') is True
    assert dm['b'].data == 2  # [1,2],[3]
    dm['b'] = UniversalAdapter(4)
    assert dm['b'].data == 4  # [1,2,4],[]
    assert dm.forward('b') is False  # 此时由于已重新赋值，因此缓存区中待重做的值被清空了

    # 以下内容用于测试回收站
    dm['c'] = UniversalAdapter(1)
    dm['c'] = UniversalAdapter(2)
    dm['c'] = UniversalAdapter(3)
    assert dm.back('c') is True
    assert dm['c'].data == 2
    del dm['c']
    with pytest.raises(KeyError):
        _ = dm['c']
    dm.restore_from_recycle_bin('c')
    assert dm['c'].data == 2
    assert dm.forward('c') is True  # 从回收站中拾回的变量，仍保存其自己的历史记录状态
    assert dm['c'].data == 3


def test_methods():
    """
    测试字典的常用方法
    """
    dm = data_manager.DataManager()
    dm['a'] = UniversalAdapter(1)
    dm['a'] = UniversalAdapter(2)
    dm['b'] = UniversalAdapter(3)
    assert dm.keys() == ['a', 'b']
    assert dm.values()[0].data == 2
    assert dm.values()[1].data == 3
    assert dm.items()[0][0] == 'a'
    assert dm.items()[0][1].data == 2
    assert dm.items()[1][0] == 'b'
    assert dm.items()[1][1].data == 3
