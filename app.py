import os
import logging

# 导入功能组件

__Author__ = """
By: PyMiner Development Team
QQ: 454017698
Email: aboutlong@qq.com
"""
__Copyright__ = 'Copyright (c) 2020 PyMiner Development Team'
__Version__ = '1.0.1'

root_dir = os.path.dirname(os.path.abspath(__file__)) + r'\pyminer'

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

# ====================================窗体测试程序============================
if __name__ == '__main__':
    from pyminer.pmstart import boot

    boot()
