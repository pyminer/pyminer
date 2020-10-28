import numpy
import pytest

from pyminer2.workspace.datamanager import converter, datamanager, exceptions
import pandas


def test_ndarray_1d():
    cvt = converter.Converter(datamanager.DataManager())
    result = cvt.convert_ndarray(numpy.array([1, 2, 3, 4]))
    assert result['type'] == 'Vector'
    assert result['value'] == [1, 2, 3, 4]


def test_ndarray_2d():
    cvt = converter.Converter(datamanager.DataManager())
    result = cvt.convert_ndarray(numpy.array([[1, 2, 3, 4], [5, 6, 7, 8]]))
    assert result['type'] == 'Matrix'
    assert result['value'] == [[1, 2, 3, 4], [5, 6, 7, 8]]


def test_ndarray_3d():
    # TODO (panhaoyu) 三维数组应当添加支持
    cvt = converter.Converter(datamanager.DataManager())
    with pytest.raises(exceptions.ConvertError):
        cvt.convert_ndarray(numpy.zeros((3, 3, 3)))


def test_ndarray_long():
    # TODO (panhaoyu) 这里应当添加其他类型的支持
    cvt = converter.Converter(datamanager.DataManager())
    with pytest.raises(exceptions.ConvertError):
        cvt.convert_ndarray(numpy.zeros((3, 3), dtype=numpy.longlong))


def test_list():
    cvt = converter.Converter(datamanager.DataManager())
    result = cvt.convert_list([1, 2, 3])
    assert result['type'] == 'Vector'

    result = cvt.convert_list([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert result['type'] == 'Matrix'


def test_dataframe():
    cvt = converter.Converter(datamanager.DataManager())
    df = pandas.DataFrame(data=[[1, 2], [3, 4], [5, 6]], columns=['key', 'value'])
    result = cvt.convert_dataframe(df)
    assert result['type'] == 'DataFrame'
    assert result['table'] == [[1, 2], [3, 4], [5, 6]]
    assert result['columns'] == ['key', 'value']


def test_all():
    dm = datamanager.DataManager()
    cvt = converter.Converter(dm)
    array = numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mat = cvt.convert_to_data(array)
    assert mat['type'] == 'Matrix'
