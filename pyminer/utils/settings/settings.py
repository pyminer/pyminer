import ast
import os
import shutil
from typing import Any

from PySide2.QtCore import QSettings

# from features.ui.base.Preferences import Ui_Form

Ui_Form = object

SETTINGS_FILES = {"config.ini"}


def get_settings_from_file(file_name: str) -> QSettings:
    """
    从文件中获取设置
    Args:
        file_name:

    Returns:

    """
    from ..path import get_config_file_dir
    return QSettings(get_config_file_dir(file_name), QSettings.IniFormat)


def get_settings_item_from_file(file_name: str, item: str, mode="user") -> Any:
    """
    从文件中获取设置。如果用户目录下没有，就去默认目录下面寻找。
    这样可以解决软件更新时引入的问题。
    在此时会调用ast.literal_eval函数进行数据类型转换。
    Args:
        file_name:
        item:
        mode: 两种选项，有user和default。

    Returns:

    """
    assert mode in {"user", "default"}
    assert file_name in SETTINGS_FILES
    from utils.path import get_user_config_dir, get_default_config_dir
    user_cfg_file_path = os.path.join(get_user_config_dir(), file_name)
    default_cfg_file_path = os.path.join(get_default_config_dir(), file_name)
    if mode == "user":
        if not os.path.exists(user_cfg_file_path):
            shutil.copy(default_cfg_file_path, user_cfg_file_path)
        val = QSettings(user_cfg_file_path, QSettings.IniFormat).value(item)
        if val is None:
            val = QSettings(default_cfg_file_path, QSettings.IniFormat).value(item)
    else:
        val = QSettings(default_cfg_file_path, QSettings.IniFormat).value(item)
    assert val is not None, (default_cfg_file_path, item, mode)
    try:
        val = ast.literal_eval(val)
    except:
        pass
    return val


def write_settings_item_to_file(file_name: str, item: str, value: Any):
    """
    带有类型转换地写入。
    一般的，设置类型只能是
    int,float,str以及由他们repr之后组成的结果。

    Args:
        file_name:
        item:
        value:

    Returns:

    """
    assert file_name in SETTINGS_FILES
    from utils.path import get_config_file_dir

    value_str = ""
    if isinstance(value, str):
        value_str = value
    else:
        value_str = repr(value)
    QSettings(os.path.join(get_config_file_dir(file_name)), QSettings.IniFormat).setValue(item, value_str)


if __name__ == '__main__':
    print(get_settings_item_from_file("config.ini", "RUN/EXTERNAL_INTERPRETERS"))
