import os
import sys

from .env_manager import *
from .package_install import *
from .package_remove import *
from .package_update import *

# 获取项目相关目录添加到path中
plugins_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
features_dir = os.path.dirname(plugins_dir)
patata_dir = os.path.dirname(features_dir)
ui_dir = patata_dir + '\\ui'
# 把目录加入环境变量
sys.path.insert(0, plugins_dir)
sys.path.insert(0, patata_dir)
sys.path.insert(0, features_dir)
sys.path.insert(0, ui_dir)