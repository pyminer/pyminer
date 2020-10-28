from pyminer2.workspace.datamanager import recyclebin, exceptions

import numpy


def test_all():
    rb = recyclebin.RecycleBin()
    rb.discard('testName', numpy.zeros((3, 3)))
    assert rb.get_varname(0) == 'testName'

    rb.discard('newName', numpy.ones((4, 4)))
    assert rb.get_varname(0) == 'testName'
    assert rb.get_varname(1) == 'newName'

    key, value = rb.restore(0)
    assert key == 'testName'
    assert value.shape == (3, 3)

    key, value = rb.restore(0)
    assert key == 'newName'
    assert value.shape == (4, 4)
