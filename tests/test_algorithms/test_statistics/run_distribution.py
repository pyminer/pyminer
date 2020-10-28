from pyminer_algorithms import cumulative_distribution, probability_density, \
    percent_point, random_variates
import unittest
import numpy as np
from scipy import stats


class Test(unittest.TestCase):  # 继承unittest.TestCase

    def test_cdf(self):
        x = 0.2
        cdf_val = cumulative_distribution('normal', x)  # python 还有^符号，可以用来进行位运算
        assert abs(cdf_val - stats.norm.cdf(x)) < 1 * 10 ** -8
        assert abs(cumulative_distribution(stats.norm(), x) - stats.norm.cdf(x)) < 1 * 10 ** -8

        for weibull_c in [0.5, 1, 1.5, 2, 3, 10]:
            cdf_val_weibull = cumulative_distribution('weibull', x, c=weibull_c)
            assert abs(cdf_val_weibull - stats.weibull_min.cdf(x, c=weibull_c)) < 1 * 10 ** -8

        for expon_scale in [0.5, 1, 2, 10.5]:
            cdf_val_weibull = cumulative_distribution('expon', x, scale=expon_scale)
            assert abs(cdf_val_weibull - stats.expon.cdf(x, scale=expon_scale)) < 1 * 10 ** -8

    def test_pdf(self):
        pdf_val = probability_density('normal', np.array([1, 2, 3]), loc=0, scale=2)
        pdf_val = probability_density('normal', np.array([1, 2, 3]), mu=0, sigma=2)
        print(pdf_val)
        x = 0.2
        pdf_val = probability_density('normal', x)  # python 还有^符号，可以用来进行位运算
        assert abs(pdf_val - stats.norm.pdf(x)) < 1 * 10 ** -8
        assert abs(probability_density(stats.norm(), x) - stats.norm.pdf(x)) < 1 * 10 ** -8

        for weibull_c in [0.5, 1, 1.5, 2, 3, 10]:
            pdf_val_weibull = probability_density('weibull', x, c=weibull_c)
            assert abs(pdf_val_weibull - stats.weibull_min.pdf(x, c=weibull_c)) < 1 * 10 ** -8

        for expon_scale in [0.5, 1, 2, 10.5]:
            pdf_val_weibull = probability_density('expon', x, scale=expon_scale)
            assert abs(pdf_val_weibull - stats.expon.pdf(x, scale=expon_scale)) < 1 * 10 ** -8

    def test_ppf(self):
        x = 0.2
        ppf_val = percent_point('normal', x)  # python 还有^符号，可以用来进行位运算
        assert abs(ppf_val - stats.norm.ppf(x)) < 1 * 10 ** -8
        assert abs(percent_point(stats.norm(), x) - stats.norm.ppf(x)) < 1 * 10 ** -8

        for weibull_c in [0.5, 1, 1.5, 2, 3, 10]:
            ppf_val_weibull = percent_point('weibull', x, c=weibull_c)
            assert abs(ppf_val_weibull - stats.weibull_min.ppf(x, c=weibull_c)) < 1 * 10 ** -8

        for expon_scale in [0.5, 1, 2, 10.5]:
            ppf_val_weibull = percent_point('expon', x, scale=expon_scale)
            assert abs(ppf_val_weibull - stats.expon.ppf(x, scale=expon_scale)) < 1 * 10 ** -8

    def test_rvs(self):
        size = (2, 2, 3, 4)
        rvs = random_variates('normal', size=size)
        print('rvs is:', rvs)

        for i in range(4):
            if size[i] != rvs.shape[i]:
                raise


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
