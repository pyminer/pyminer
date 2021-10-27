from unittest import TestCase

import numpy
from pandas import DataFrame

from features.workspace.data_adapter.data_frame import DataFrameAdapter


class TestDataFrame(TestCase):
    def setUp(self) -> None:
        self.df = DataFrame(numpy.ones((20, 10)).cumsum().reshape((20, 10)),
                            index=[f'row-{i}' for i in range(10, 30)],
                            columns=[f'col-{col}' for col in range(40, 50)])
        self.adapter = DataFrameAdapter(self.df)

    def test_shape(self):
        self.assertTupleEqual(self.adapter.shape, (20, 10))

    def test_rw(self):
        data = self.adapter.dump()
        adapter = DataFrameAdapter.load(data)
        self.assertListEqual(adapter.get_array()[:, 4].to_list(), [i * 10 + 5 for i in range(20)])

    def test_column_names(self):
        self.assertListEqual(self.adapter.get_header_name(0).to_list(), [f'row-{i}' for i in range(10, 30)])

    def test_row_names(self):
        self.assertListEqual(self.adapter.get_header_name(1).to_list(), [f'col-{i}' for i in range(40, 50)])

    def test_get_array(self):
        for row1, row2 in zip(self.adapter.get_array(), range(20)):
            for v1, v2 in zip(row1, range(10)):
                self.assertEqual(v1, row2 * 10 + v2 + 1)

    def test_get_item(self):
        self.assertEqual(self.adapter.get_array()[2, 4], 25)
        self.assertEqual(self.adapter.get_array()[1, 4], 15)
        self.assertEqual(self.adapter.get_array()[1, 3], 14)
