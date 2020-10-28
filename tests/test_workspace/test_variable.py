from pyminer2.workspace.datamanager import variable, exceptions


def test_all():
    v = variable.Variable('Matrix', {})
    assert v.type == 'Matrix'

    # TODO (panhaoyu) 进行 dump, dumps, load, loads 的单元检测
    # 目前由于不太清楚这个类是做什么的，因此没法进行检测
    # 这是在dataset中的一行测试代码，不知道有何用
    # matvar = variable.Variable('Matrix', mat)
