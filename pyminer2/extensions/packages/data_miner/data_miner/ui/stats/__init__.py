import os
import sys
#获取main 所在目录
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#把目录加入环境变量
sys.path.insert(0,parentdir)
from pyqtsource_rc import *