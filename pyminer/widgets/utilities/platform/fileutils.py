import os

import chardet


def get_parent_path(path, layers=1):
    """获取父级目录

    Args:
        path: 当前目录。
        layers: 向上查找的层级数。

    Returns:
        当前目录向上 ``layers`` 级的父目录。
    """
    assert isinstance(layers, int) and layers > 0
    for i in range(layers):
        path = os.path.dirname(path)
    return path


def load_json(path) -> dict:
    """
    加载json，指定编码方式
    :param path:
    :return:
    """
    import json
    with open(path, 'rb') as f:
        byte_str = f.read()
        encoding = chardet.detect(byte_str)['encoding']
    return json.loads(byte_str.decode(encoding))


def dump_json(dic: dict, path: str, indent=4) -> None:
    """
    加载json，指定编码方式
    :param path:
    :return:
    """
    import json
    with open(path, 'wb') as f:
        byte_str = json.dumps(dic, indent=indent).encode('utf-8')
        f.write(byte_str)


def create_file_if_not_exist(abso_file_path: str, default_content: bytes = b''):
    """
    在任意可能的路径创建一个文件，倘若文件不存在。
    :param abso_file_path:
    :param default_content:
    :return:
    """
    dir_stack = []
    path = abso_file_path
    # assert os.path.isfile(abso_file_path), 'Path \'%s\' is not a file!' % abso_file_path
    if os.path.isfile(abso_file_path):
        return
    while 1:
        parent_path = os.path.dirname(path)
        if not os.path.exists(parent_path):
            dir_stack.append(parent_path)
            path = parent_path
        else:
            break
    dir_stack.reverse()
    for path in dir_stack:
        os.mkdir(path)
    with open(abso_file_path, 'wb') as f:
        f.write(default_content)
        pass


def move_to_trash(path: str) -> bool:
    """
    将文件移动到回收站。成功返回True,失败返回False
    :param path:绝对路径。
    :return:
    """
    import platform
    import send2trash
    if platform.system() == "Windows":
        path = path.replace('/', '\\')
    try:
        send2trash.send2trash(path)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def rename_file(prev_absolute_path: str, new_absolute_path: str) -> bool:
    """
    重命名文件或者文件夹
    :param prev_absolute_path:之前的绝对路径名称
    :param new_absolute_path: 之后的绝对路径名称
    :return:
    """
    import os
    try:
        os.rename(prev_absolute_path, new_absolute_path)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def copy_paste(source_path: str, target_path: str):
    """

    :param source_path: 源文件或文件夹
    :param target_path: 目标文件或文件夹
    :return:
    """
    import shutil, os
    if os.path.isfile(source_path):
        copy_func = shutil.copyfile
    else:
        copy_func = shutil.copytree

    try:
        copy_func(source_path, target_path)
    except:
        import traceback
        traceback.print_exc()
        return False
    return True


if __name__ == '__main__':
    print(get_parent_path(os.path.dirname(__file__), 2))
    print(load_json(r'/pyminer2/extensions/packages/code_editor/customized/settings.json'))
