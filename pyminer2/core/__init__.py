import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 导入基本数学变量和函数
from math import (
    ceil,
    comb,
    copysign,
    fabs,
    factorial,
    floor,
    fmod,
    frexp,
    fsum,
    gcd,
    isclose,
    isfinite,
    isinf,
    isnan,
    isqrt,
    ldexp,
    modf,
    perm,
    prod,
    remainder,
    trunc,
    exp,
    expm1,
    log,
    log1p,
    log2,
    log10,
    pow,
    sqrt,
    acos,
    asin,
    atan,
    atan2,
    cos,
    dist,
    hypot,
    sin,
    tan,
    degrees,
    radians,
    acosh,
    asinh,
    atanh,
    cosh,
    sinh,
    tanh,
    erf,
    erfc,
    gamma,
    lgamma,
    pi,
    e,
    tau,
    inf,
    nan
)

# 导入numpy 统计函数
from numpy import (
    sum,
    mean,
    average,
    std,
    var,
    min,
    max,
    median
)

# 导入numpy 随机数
from numpy.random import (
    rand,
    randn,
    randint,
    random_integers,
    random_sample,
    random,
    ranf,
    sample,
    choice,
    seed
)

# from .pyminer_algorithms.linear_algebra import *

# 导入数据读取相关模块
from pandas.io.api import (
    # excel
    ExcelFile,
    ExcelWriter,
    read_excel,
    # parsers
    read_csv,
    read_fwf,
    read_table,
    # pickle
    read_pickle,
    to_pickle,
    # pytables
    HDFStore,
    read_hdf,
    # sql
    read_sql,
    read_sql_query,
    read_sql_table,
    # misc
    read_clipboard,
    read_parquet,
    read_orc,
    read_feather,
    read_gbq,
    read_html,
    read_json,
    read_stata,
    read_sas,
    read_spss,
)

# 导入模型相关模块
from sklearn.model_selection import train_test_split  # 将数据分为测试集和训练集

# 分类 Classification
# from sklearn import SomeClassifier
# from sklearn.linear_model import SomeClassifier
# from sklearn.ensemble import SomeClassifier

# 回归 Regression
# from sklearn import SomeRegressor
# from sklearn.linear_model import SomeRegressor
# from sklearn.ensemble import SomeRegressor

# 聚类 Clustering
# from sklearn.cluster import SomeModel

# 降维 Dimensionality Reduction
# from sklearn.decomposition import SomeModel

# 模型选择 Model Selection
# from sklearn.model_selection import SomeModel


# 预处理 Preprocessing
# from sklearn.preprocessing import SomeModel

from sklearn.linear_model import LinearRegression  # 引入线性回归模型
from sklearn.model_selection import cross_val_score  # 交叉验证
from sklearn.neighbors import KNeighborsClassifier


def plot(x, y) -> None:
    """
    提供类似MATLAB的方式进行绘图

    参数
    ----------
    x : np.array
    y : np.array
    """
    plt.plot(x, y)
    plt.show()


def version():
    print("1.0.1")


def size(x) -> np.array:
    """
    获取矩阵的行数和列数

    参数
    ----------
    x : np.array
    """
    if type(x) is np.ndarray:
        return x.shape
    else:
        try:
            return np.array(x).shape
        except:
            return "data type is not support"

import numpy as np


def magic(n)-> np.array:
    """
    用于产生魔方矩阵，它的每行、列以及对角线的数之和相等。该和的值为1+2+3+.....+n^2的和再除以n，n必须为大于或等于3的整数。

    参数
    ----------
    x : int
    """
    n = int(n)
    if n < 3:
        raise ValueError("Size must be at least 3")
    if n % 2 == 1:
        p = np.arange(1, n + 1)
        return n * np.mod(p[:, None] + p - (n + 3) // 2, n) + np.mod(p[:, None] + 2 * p - 2, n) + 1
    elif n % 4 == 0:
        J = np.mod(np.arange(1, n + 1), 4) // 2
        K = J[:, None] == J
        M = np.arange(1, n * n + 1, n)[:, None] + np.arange(n)
        M[K] = n * n + 1 - M[K]
    else:
        p = n // 2
        M = magic(p)
        M = np.block([[M, M + 2 * p * p], [M + 3 * p * p, M + p * p]])
        i = np.arange(p)
        k = (n - 2) // 4
        j = np.concatenate((np.arange(k), np.arange(n - k + 1, n)))
        M[np.ix_(np.concatenate((i, i + p)), j)] = M[np.ix_(np.concatenate((i + p, i)), j)]
        M[np.ix_([k, k + p], [0, k])] = M[np.ix_([k + p, k], [0, k])]
    return M


def mode(x,y)->int:
    """
    返回x/y的余数

    参数
    ----------
    x : int
    y : int
    """
    return x%y