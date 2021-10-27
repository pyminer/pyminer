"""
这是一个用来调用，自动生成翻译文件的脚本。
"""
import os

from utils import get_python_modules_directory

pylupdate_path = os.path.join(get_python_modules_directory(), 'PySide2', "pyside2-lupdate.exe")


def update_ts(packages_path):
    translation_folder = os.path.join(os.path.dirname(__file__), r'languages\zh_CN')
    translation_file = os.path.join(translation_folder, os.path.relpath(packages_path) + '_qt_zh_CN.ts')
    filenames = ''
    for root, dirs, files in os.walk(packages_path, topdown=False):

        for name in files:
            filename = os.path.join(root, name)
            if filename.endswith('.py'):
                with open(filename, 'rb') as f:
                    bs = f.read()
                    if not (bs.find(b'.tr') != -1 or bs.find(b'translate') != -1):
                        continue
                filenames += ' ' + os.path.relpath(filename, os.path.dirname(__file__)) + ' '

    if filenames.strip() != '':
        cmd = '%s -verbose %s -ts %s' % (pylupdate_path, filenames, translation_file)
        # print(len(cmd))
        os.system(cmd)


folders = ["widgets", "pmtoolbox"]
for folder in folders:
    update_ts(os.path.join(os.path.dirname(__file__), folder))

os.system("%s -verbose pyminer.pro" % pylupdate_path)
