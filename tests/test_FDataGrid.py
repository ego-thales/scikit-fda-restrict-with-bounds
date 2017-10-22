import unittest
from fda.FDataGrid import FDataGrid
import numpy
import os
from fda import math_basic
from fda import kernel_smoothers
from fda import kernels
import scipy.stats.mstats


class TestFDataGrid(unittest.TestCase):

    # def setUp(self): could be defined for set up before any test

    def test_init(self):
        fd = FDataGrid([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]])
        numpy.testing.assert_array_equal(fd.data_matrix, numpy.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]))
        self.assertSequenceEqual(fd.argvals_range, (0, 1))
        numpy.testing.assert_array_equal(fd.argvals, numpy.array([0., 0.25, 0.5, 0.75, 1.]))

    def test_mean(self):
        fd = FDataGrid([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]])
        mean = math_basic.mean(fd)
        numpy.testing.assert_array_equal(mean.data_matrix[0], numpy.array([1.5, 2.5, 3.5, 4.5, 5.5]))
        self.assertSequenceEqual(fd.argvals_range, (0, 1))
        numpy.testing.assert_array_equal(fd.argvals, numpy.array([0., 0.25, 0.5, 0.75, 1.]))

    def test_gmean(self):
        fd = FDataGrid([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]])
        mean = math_basic.gmean(fd)
        numpy.testing.assert_array_equal(mean.data_matrix[0],
                                         scipy.stats.mstats.gmean(numpy.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]])))
        self.assertSequenceEqual(fd.argvals_range, (0, 1))
        numpy.testing.assert_array_equal(fd.argvals, numpy.array([0., 0.25, 0.5, 0.75, 1.]))

if __name__ == '__main__':
    print()
    unittest.main()