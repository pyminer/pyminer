#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/9/10
@author: Irony
@email: 892768447@qq.com
@file: get_yapf_output
@description: test yapf and get output
"""

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 'Version 1.0'

import os

from yapf.yapflib import py3compat
from yapf.yapflib import yapf_api

source = open(os.path.abspath('../pythoneditor.py'), 'rb').read().decode()
source = py3compat.removeBOM(source)

try:
    reformatted_source, _ = yapf_api.FormatCode(
        source,
        filename='pythoneditor.py',
        print_diff=True,
        style_config=os.path.abspath('../.style.yapf')
    )
    print(reformatted_source)
except Exception as e:
    raise e
