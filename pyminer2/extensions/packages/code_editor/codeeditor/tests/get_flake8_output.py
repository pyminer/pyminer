#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/9/10
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: get_flake8_output
@description: get flake8 lint output
"""

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 'Version 1.0'

import io
import os
from contextlib import redirect_stdout

from flake8.main import application

with io.StringIO() as out, redirect_stdout(out):
    app = application.Application()
    app.initialize(
        ['flake8', '--exit-zero', '--config', os.path.abspath('../.flake8')])
    app.run_checks([os.path.abspath('../syntaxana.py')])
    app.report()
    ret = out.getvalue()
print(ret)
# report = Report(app)
# print(report.get_statistics('E'))
# print(report.get_statistics('W'))
# print(report.get_statistics('F'))
