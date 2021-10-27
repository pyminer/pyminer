import hashlib
import json
import os
import pathlib
from typing import Dict

import pathspec

import utils
from utils import is_mac_platform, is_linux_platform, is_windows_platform

WINDOWS_X64 = 0
LINUX_X64 = 1
MAC_X64 = 2
CURRENT_PLATFORM = -1
if is_mac_platform():
    STRIP_LINEEND_FCN = lambda b: b.replace(b'\r', b'\n')
elif is_linux_platform():
    STRIP_LINEEND_FCN = lambda b: b
elif is_windows_platform():
    STRIP_LINEEND_FCN = lambda b: b.replace(b'\r', b'')

PROJ_ROOT = utils.get_root_dir()

FOLDERS_TO_IGNORE = [".git"]
FOLDER_NAMES_TO_IGNORE = ["__pycache__"]
FILE_NAMES_TO_IGNORE = ["__latest.json"]

FOLDERS_TO_IGNORE = [os.path.join(PROJ_ROOT, f) for f in FOLDERS_TO_IGNORE]

GITIGNORE_PATH = os.path.join(PROJ_ROOT, '.gitignore')


def get_filter_list():
    """从gitignore获取忽略文件"""
    with open(GITIGNORE_PATH, 'r') as f:
        filter_list = f.read().splitlines()
    filter_list.append("__latest.json")
    return filter_list


spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, get_filter_list())


def should_be_recorded(path: pathlib.Path) -> bool:
    """

    :return:
    """
    if path.is_dir():
        return False  # 文件夹不记录
    if '.git' in str(path):
        return False
    if spec.match_file(path):
        return False
    return True


def get_file_md5(path):
    if not os.path.isfile(path):
        return ""
    myhash = hashlib.md5()
    f = open(path, 'rb')
    while True:
        b = f.read(8096)

        b = STRIP_LINEEND_FCN(b)  # 这里是因为git会自动转换\r\n，为了保证多平台统一，在计算md5码时去除\r
        if not b:
            break
        myhash.update(b)
    f.close()
    md5 = myhash.hexdigest()
    return md5


if __name__ == '__main__':
    d: Dict[str, str] = {}
    for root, dirs, files in os.walk(PROJ_ROOT):
        # if folder_should_be_ignored(root):
        #     continue
        for file in files:

            abso_path = os.path.join(root, file)

            path = pathlib.Path(abso_path)
            re_path = str(path.relative_to(PROJ_ROOT)).replace('\\', '/')
            if not should_be_recorded(pathlib.Path(abso_path)):
                continue
            d[re_path] = get_file_md5(abso_path)
            if file.startswith("."):
                print("aaaaaa", file)
                print(re_path)
                print(d[re_path])
    print(d)
    with open(os.path.join(PROJ_ROOT, "__latest.json"), "w", encoding="utf8") as f:
        json.dump({"files": d}, f)
