# -*- coding: utf-8 -*-
# Copyright (c) 2020 pyminer development team <team@py2cn.com>
# Get application path information
# 获取应用路径信息
import os
import shutil

from PySide2.QtCore import QStandardPaths

from .settings import SETTINGS_FILES


def get_root_dir() -> str:
    """
    获取根路径。
    Returns:

    """
    path = os.path.dirname(os.path.dirname(__file__))
    return path

def get_resources_dir() -> str:
    """
    获取根路径。
    Returns:

    """
    path = os.path.join(get_root_dir(),'resources')
    return path


def get_user_dir() -> str:
    """
    获取用户目录
    """
    path = os.path.expanduser('~')
    return path


def get_desktop_dir() -> str:
    """
    获取用户目录
    """
    path = os.path.join(os.path.expanduser('~'), 'Desktop')
    return path


def get_documents_dir() -> str:
    """
    获取用户目录
    """
    path = os.path.join(os.path.expanduser('~'), 'Documents')
    return path


def get_path_desktop() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
    return path


def get_path_documents() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
    return path


def get_path_fonts() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.FontsLocation)
    return path


def get_path_applications() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.ApplicationsLocation)
    return path


def get_path_music() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)
    return path


def get_path_movies() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
    return path


def get_path_pictures() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
    return path


def get_path_temp() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
    return path


def get_path_home() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
    return path


def get_path_data() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
    return path


def get_path_cache() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
    return path


def get_path_generic_data() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation)
    return path


def get_path_runtime() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.RuntimeLocation)
    return path


def get_path_config() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
    return path


def get_path_download() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
    return path


def get_path_generic_cache() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.GenericCacheLocation)
    return path


# def get_path_generic_config() -> str:
#     path = QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)
#     return path


# def get_path_app_data() -> str:
#     path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
#     return path


# def get_path_app_config() -> str:
#     path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
#     return path


def get_path_app_local_data() -> str:
    path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
    return path


def get_pyminer_data_dir() -> str:
    """
    获取PyMiner的数据文件存储位置，一般为.pyminer文件夹。
    Returns:

    """
    path = os.path.join(os.path.expanduser('~'), '.pyminer')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_default_config_dir() -> str:
    """
    获取PyMiner默认设置的位置。软件第一次运行时，从这里获取设置，并且将设置拷贝到用户目录下面。。
    Returns:

    """
    return os.path.join(get_root_dir(), "configuration")


def get_user_config_dir() -> str:
    """
    获取用户的设置目录。 .pyminer/pyminer_config
    Returns:

    """
    path = os.path.join(get_pyminer_data_dir(), "pyminer_config")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_config_file_dir(filename: str) -> str:
    """
    获取设置文件的路径
    Args:
        filename:

    Returns:

    """
    assert filename in SETTINGS_FILES
    user_cfg_file_path = os.path.join(get_user_config_dir(), filename)
    if not os.path.exists(user_cfg_file_path):
        default_cfg_file_path = os.path.join(get_default_config_dir(), filename)
        shutil.copy(default_cfg_file_path, user_cfg_file_path)
    return user_cfg_file_path
