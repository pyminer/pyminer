# -*- coding:utf-8 -*-
# @Time: 2021/1/25 9:29
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: find_kernel_spec.py

import jupyter_client
M = jupyter_client.kernelspec.KernelSpecManager()
res = M.find_kernel_specs()
print(res)