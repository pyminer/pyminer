"""
Pyminer服务包
--------------

Pyminer服务包主要用于解决以下问题：

#. 与工作空间通信，实现工作空间的数据添加和修改；
    #. get_var: 从工作空间获取变量；
    #. set_var: 更新工作空间的变量；
#. 通过Web端口自动化操作Pyminer（未实现）：


Notes
--------
使用本包中的方法依赖于Pyminer主程序。当主程序不启动时，会报出`ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接。`
这样的错误。如果出现，请检查Pyminer主程序是否已经启动！
"""
from .communication import *