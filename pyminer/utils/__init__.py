# -*- coding: utf-8 -*-
# Copyright (c) 2020 PyMiner Development Team <team@py2cn.com>
# 
# 通用工具，可以在全局进行调用。

import webbrowser

from .debug import *
from .environ import (
    get_python_version,
    get_python_modules_directory,
    get_pysidemodules_directory,
    get_pysideplugins_directory,
    get_scripts_path,
    get_designer_path
)
from .io import *
from .path import (
    get_root_dir,
    get_resources_dir,
    get_user_dir,
    get_desktop_dir,
    get_documents_dir,
    get_pyminer_data_dir,
    get_user_config_dir,
    get_default_config_dir,
    get_config_file_dir
)
from .platform import (
    is_windows_platform,
    is_mac_platform,
    is_linux_platform,
    is_kde_desktop,
    is_gnome_desktop
)
from .settings import *
from .ui import *

if TYPE_CHECKING:
    import app2
    from PySide2.QtWidgets import QApplication
# version = 'v2.1.0 Beta'  这里原有version ，但是考虑到这些信息写在静态文件中较好，所以就写在了文件中。

_application = Optional["QApplication"]
_root_dir = None
_main_window: Optional["app2.MainWindow"] = None


def get_application() -> "QApplication":
    """
    获取QApplication
    Returns:

    """
    assert _application is not None
    return _application


def get_main_window() -> "app2.MainWindow":
    """
    获取主窗口或者主控件。
    Returns:
    """
    assert _main_window is not None
    return _main_window


def get_work_dir() -> 'str':
    """
    获取主窗口或者主控件。
    Returns:
    """
    return get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR")


def open_url(url):
    """
    打开网址
    """
    try:
        webbrowser.get('chrome').open_new_tab(url)
    except Exception as e:
        webbrowser.open_new_tab(url)

# def unzip_file(zip_src: str, dst_dir: str):
#     """
#     解压文件
#     Args:
#         zip_src:
#         dst_dir:
#
#     Returns:
#
#     """
#     r = zipfile.is_zipfile(zip_src)
#     if r:
#         fz = zipfile.ZipFile(zip_src, 'r')
#         for file in fz.namelist():
#             fz.extract(file, dst_dir)
#     else:
#         print('This is not zip')
#
#
# def make_zip(src_path, zip_dist_path, root='', rules=None):
#     """
#     创建zip包
#     Args:
#         src_path:
#         zip_dist_path:
#         root:
#         rules:
#
#     Returns:
#
#     """
#     if rules is None:
#         rules = []
#     z = zipfile.ZipFile(zip_dist_path, 'w', zipfile.ZIP_DEFLATED)
#     for dirpath, dirnames, filenames in os.walk(src_path):
#         relpath = os.path.relpath(dirpath, src_path)
#         if is_neglect_path(relpath, rules):
#             continue
#         fpath = os.path.relpath(dirpath, src_path)
#         for filename in filenames:
#             filepath = os.path.join(dirpath, filename)
#             z.write(filepath, os.path.join(root, fpath, filename))
#     z.close()
