import numpy as np

from pyminer2.workspace.datamanager import datamanager


# TODO 这里的测试用例已失效，不过DataManager需要重构，暂不进一步开发

def test_variable_get_set():
    dm = datamanager.DataManager()
    dm.set_var('myArray', np.array([[1, 2, 3], [4, 5, 6]]))
    assert dm.get_var('myArray')[1, 1] == 5
    assert dm.get_var('myArray').shape == (2, 3)

    dm.set_var('myMatrix', {
        'type': 'Matrix',
        'value': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
    })
    assert dm.get_var('myMatrix')['value'][2][2] == 9


# TODO 由于不理解History相关内容的含义，没有对这部分添加测试用例


def test_all():
    # TODO (panhaoyu) 这里的代码暂时没有进行更新，先这样吧
    dm = datamanager.DataManager()

    def on_modification(varname: str, variable, data_source: str):
        print(f'detect modification: {varname} = {variable}')

    def on_deletion(varname: str):
        print(f'detect deletion: {varname}')

    dm.on_modification(on_modification)
    dm.on_deletion(on_deletion)

    dm.set_var('arr', np.array([[1, 2, 3], [3, 2, 1]]))
    print('add arr directly\n', dm.varset, '\n')

    mat = {'type': 'Matrix', 'value': [[1, 2, 3], [3, 2, 1]]}
    dm.write_data('mat', mat)
    print(
        'add mat from server\n',
        dm.varset,
        '\n',
        dm.dataset,
        '\n')

    print('metadataset\n', dm.metadataset, '\n')

    dm.set_var('mat', np.array([[1, 2, 4], [4, 2, 1]]), 'user')
    print('modify mat\n', dm.varset, '\n', dm.dataset, '\n')

    print('metadataset\n', dm.metadataset, '\n')

    dm.cancel('mat')
    print('cancel mat\n', dm.varset, '\n')

    dm.redo('mat')
    print('redo mat\n', dm.varset, '\n')

    dm.delete_data('arr')
    print(
        'cancel mat\n',
        dm.varset,
        '\nrecycle bin',
        dm.recyclebin,
        '\n')
    # noinspection PyBroadException
    try:
        var = dm.get_var('arr')
    except BaseException:
        print('cannot get arr\n')
    else:
        print('get var', var, '\n')
    # noinspection PyBroadException
    try:
        var = dm.read_data('arr')
    except BaseException:
        print('cannot read arr\n')
    else:
        print('read var', var, '\n')

    dm.set_var('arr', np.array([[1, 2, 5], [5, 2, 1]]))
    dm.restore(0)
    print(
        'cancel mat\n',
        dm.varset,
        '\nrecycle bin',
        dm.recyclebin,
        '\n')

    print('read arr', dm.read_data('arr'))
    print('get mat', dm.get_var('mat'))
