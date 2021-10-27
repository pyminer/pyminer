"""
这个文件需要在提交之前运行，从而正确的生成更新包。

在更新之后，需要检查：
1、最新的版本启动后，是否还会提示要更新。如果是，那么说明可能文件存在错误，或者并未正确执行此文件。
2、最新打包的版本，其中是否因为某些包的更新而发生错误。典型例子就是Matplotlib升级成3.4.1版本之后，废止了旧的某个类，导致PMAgg不能运行。

还有一些问题：
是否需要发布大版本更新的提示？比如，当版本更新中包含pip包版本升级的时候，是否需要提示用户？
如何处理用户升级解释器中包的问题？是否要提示，默认解释器不得安装requirements.txt中已有的包？

是否需要支持切换解释器的工作空间？

"""

import os
import sys

from utils import get_root_dir

os.system(f"{sys.executable} {os.path.join(get_root_dir(), 'features', 'util', 'make_update.py')}")
print("已经运行完成。现在还需要进行一次更新测试，确认已是最新版本，便可以提交到主分支了。")
