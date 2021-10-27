"""
线性代数算法包
--------------

线性代数算法包主要用于解决以下问题：

#. 生成常见矩阵；
    #. zeros: 零矩阵；
    #. ones: 1矩阵；
    #. magic: 幻方矩阵（未找到对应实现，在 ``miner2/core/__init__`` 下有一个临时的实现需要迁移）；
    #. range: 按自然数生成的矩阵（未实现）；
    #. array/matrix: 根据列表生成矩阵；
    #. linear_space: 生成等间距的向量；
    #. log_space: 生成对数间距的向量（未实现）；
    #. matrix_diagonal: 生成对角矩阵或者获取对角元素；
#. 实现矩阵的基本运算：
    #. sum: 矩阵的和（未实现）；
    #. product: 矩阵的积（未实现）；
    #. reshape: 改变矩阵的形状；
    #. matrix_transpose: 转置；
    #. matrix_dot: 点积；
    #. matrix_cross: 叉积；
    #. matrix_multiply: 矩阵的乘法；
    #. matrix_divide: 矩阵的除法；
    #. matrix_inverse: 矩阵的逆；
#. 进行矩阵的分解：
    #. matrix_decomposition: 矩阵分解（未实现）；
    #. matrix_triangular_upper: 获取矩阵的上三角部分（未实现）；
    #. matrix_triangular_lower: 获取矩阵的下三角部分（未实现）；
    #. matrix_diagonal: 获取矩阵的对角线部分/按对角线生成矩阵（未实现）；
#. 判断矩阵的结构：
    #. is_matrix_diagonal: 判断矩阵是否是对角矩阵（未实现）；
    #. is_matrix_symmetric: 判断矩阵是否是对称矩阵（未实现）；
    #. is_matrix_triangular_upper: 判断矩阵是否是上三角矩阵（未实现）；
    #. is_matrix_triangular_lower: 判断矩阵是否是下三角矩阵（未实现）；
#. 计算矩阵的属性：
    #. shape: 获取矩阵的结构；
    #. matrix_determinant: 计算矩阵的行列式；
    #. matrix_eigenvalue: 计算矩阵的特征值及特征向量；
    #. matrix_condition_number: 计算矩阵的条件数（未实现）；

Notes
--------
关于函数命名的考虑：
由于函数库采用统一的命名空间，为了避免与其他函数发生命名冲突，
暂是考虑对于仅对二维矩阵进行操作的函数通过添加一个 ``matrix`` 前缀进行区分。
在 ``PyMiner`` 的算法库中， ``numpy.ndarray`` 应当是第一类对象，
因此对任意维度的矩阵进行操作时，不加前缀。
**由于能力限制，不清楚高维空间内是否也存在这些矩阵相关的函数**，
如果哪里写的不对还望各位大佬指教。

如果您有很强的线性代数基础，欢迎您和我一起进行此算法包的封装。
线性代数博大精深，在下以一个工科生的线性代数水平，显然是不足以完成此包的。
关于范数等内容，在下没有能力实现，还望您的帮助。

本函数包主要参考以下两组函数包进行设计与开发： [1]_ [2]_ 。

References
---------------

.. [1] MATLAB中的线性代数工具箱. MATLAB. https://ww2.mathworks.cn/help/matlab/linear-algebra.html
.. [2] Numpy中的线性代数工具箱. Numpy. https://numpy.org/doc/stable/reference/routines.linalg.html
"""

from .array import array
from .linear_space import linear_space
from .matrix_cross import matrix_cross
from .matrix_determinant import matrix_determinant
from .matrix_diagonal import matrix_diagonal
from .matrix_divide import matrix_divide
from .matrix_dot import matrix_dot
from .matrix_eigenvalue import matrix_eigenvalue
from .matrix_inverse import matrix_inverse
from .matrix_multiply import matrix_multiply
from .matrix_transpose import matrix_transpose
from .ones import ones
from .reshape import reshape
from .shape import shape
from .zeros import zeros

matrix = array
