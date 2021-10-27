import os
import sys

# 项目的根路径，即pyminer项目的根文件夹
base = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, base)

html_path = os.path.join(base, 'docs', 'build', 'html')
for line in os.popen(f'ghp-import -npfr git@gitee.com:py2cn/pyminer -b pages "{html_path}"'):
    print(line, end='')
