import os
import sys

path = r'E:\Python\pyminer_bin\PyMiner\bin\pyminer2'
for root, dirs, files in os.walk(path):
    for name in files:
        path = os.path.join(root, name)
        if path.endswith('.py'):
            path = r'E:\Python\pyminer_bin\PyMiner\bin\pyminer2\extensions\packages\code_editor\codeeditor\pythoneditor.py'
            cmd = '%s -m mccabe --min 1 %s' % (sys.executable, path)
            # print(path)
            os.system(cmd)
            sys.exit(0)
