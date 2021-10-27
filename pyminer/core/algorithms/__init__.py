
from .linear_algebra import *
from .pyminer_util import *

# 在通过 ``from sub_package import *`` 导入的过程中，会将 ``sub_package`` 本身也导入到 ``algorithms`` 总包的命名空间中。
# 以 ``linear_algebra`` 为例，我们需要的是 ``linear_algebra.array`` 等函数，而不是 ``linear_algebra`` 本身。
# 因此我们并不希望将 ``linear_algebra`` 引入到 ``pyminer`` 的命名空间中。
# __all__就是用于控制 ``from package import *`` 语句需要导入哪些变量的。
# 下面的这个 ``__all__`` 的主要作用是，分析局部命名空间内的所有变量，判断有哪些变量需要导入到命名空间中。
# 可以导入到命名空间中的变量的要求目前有两点：
# 1. 变量是可以调用的，也就是 ``callable(x) == True`` ；
# 1. 函数名不以下划线 ``_`` 开头，也就是 ``_array`` 不会被导入而 ``array`` 会被导入。
# 为了避免在运算的过程中引入新的变量名，所有的内容采用闭包进行操作，通过 ``lambda`` 匿名函数避免对命名空间产生污染。
__all__ = (
    lambda items: [
        k
        for k, v in items
        if callable(v) and (not k.startswith('_'))
    ]
)(locals().items())
