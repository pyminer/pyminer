"""
TODO:DEPRECATED。这个文件将被废弃！
settings.py负责设置文件的输入输出。
Settings继承字典类，另外写了存储函数。
还有其他设置的函数
设置文件：
~/.pyminer文件夹存储设置文件。
~/.pyminer/pyminer_config存储全局界面的设置文件
~/.pyminer/packages下存储插件的文件夹，插件的文件也放在下面。

插件获取的方式：
extension_lib.Program.get_plugin_data_path(plugin_name)
比如：

extension_lib.Program.get_plugin_data_path('code_editor')
返回的路径就是~/.pyminer/packages/code_editor文件夹。

其中的文件敬请插件开发者管理。建议不要向其中放太多数据，避免过多占用用户的磁盘空间。
TODO：未来我们会增加一个插件读写设置的接口。可以将插件的文件放到里面。
===============================
方案1：
settings = Extension.create_default_settings() # 创建默认设置。
settings = Extension.read_settings('settings.json') #  settings值为一个字典，{'width':100,'height':161}
Extension.save_settings(settings,'settings.json')  # 需要手动调用这个回调函数。
===============================
方案2：
创建一个默认的属性Extension.settings，与插件目录下的extsettings.json保持关联。
启动时，插件加载之前调用：
ext = Extension()
ext.create_default_settings() # 创建默认设置
ext.update_settings() # 从设置文件中读取设置并且更新设置
ext.save_settings() # pyminer 关闭时自动调用

此时直接拿到settings就可以使用了。
对于多进程插件，可以在启动的子进程中直接获取相关的设置路径。但一般的科学计算插件，是无需保存设置的。
"""
import logging
import os
import json
import platform
from typing import Dict

from PySide2.QtWidgets import QApplication

import qdarkstyle
import utils

logger = logging.getLogger(__name__)


def get_pyminer_data_path() -> str:
    path = os.path.join(os.path.expanduser('~'), '.pyminer')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def load_theme(style: str):
    """
    设置主题。
    :param style:
    :return:
    """
    from utils import get_main_window
    app = QApplication.instance()
    mw = get_main_window()
    style = style.lower()
    if style == 'fusion':
        mw.setStyleSheet('')
        app.setStyleSheet('')
        standard_ss = mw.get_stylesheet('standard')
        fusion_ss = mw.get_stylesheet('Fusion')
        app.setStyleSheet(standard_ss + '\n' + fusion_ss)
        mw.setStyleSheet(standard_ss + '\n' + fusion_ss)
        # app.setStyle('Fusion')

    elif style == 'qdarkstyle':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        black_ss = mw.get_stylesheet('Qdarkstyle')
        app.setStyleSheet(qdarkstyle.load_stylesheet())  # qt_api='pyqt5'))
        app.setStyleSheet(app.styleSheet() + '\n' + black_ss)
        mw.setStyleSheet(app.styleSheet() + '\n' + black_ss)
        # app.setStyle('Windows')

    elif style.lower() == 'windowsvista':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        app.setStyleSheet(mw.get_stylesheet('windowsvista'))
        mw.setStyleSheet(mw.get_stylesheet('windowsvista'))
        # app.setStyle("windowsvista")

    elif style.lower() == 'windows':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        app.setStyleSheet(mw.get_stylesheet('Windows'))
        mw.setStyleSheet(mw.get_stylesheet('Windows'))
        # app.setStyle("Windows")


# class Settings(dict):
#     """
#     单例！
#     """
#
#     @classmethod
#     def __new__(cls, *args):
#         if not hasattr(cls, 'instance'):
#             instance = super().__new__(cls)
#             cls.instance = instance
#         return cls.instance
#
#     def __init__(self):
#         super(Settings, self).__init__()
#         self.check_pyminer_settings_dir()
#         self.update(self.load())
#
#     def check_pyminer_settings_dir(self):
#         self.data_path = get_pyminer_data_path()
#         path = os.path.join(self.data_path, 'pyminer_config')
#         self.settings_path = path
#         if not os.path.exists(path):
#             os.mkdir(path)
#
#     @staticmethod
#     def get_instance() -> 'Settings':
#         return Settings.instance
#
#     def load(self) -> Dict[str, str]:
#         """
#         加载设置项。
#         default_settings是默认设置项
#         :return:
#         """
#         with open(os.path.join(utils.get_root_dir(), 'configuration', 'default_settings.json'), 'r') as f:
#             default_settings = json.load(f)
#             if platform.system().lower() == 'windows':
#                 default_settings['work_dir'] = os.path.expanduser('~')
#             else:
#                 default_settings['work_dir'] = os.environ['HOME']
#             if not os.path.exists(default_settings['work_dir']):
#                 os.mkdir(default_settings['work_dir'])
#
#         try:
#             with open(os.path.join(self.settings_path, 'pyminer_settings.json'), 'r') as f:
#                 settings = json.load(f)
#         except BaseException:
#             settings = {}
#
#         pmsettings = default_settings
#         pmsettings.update(settings)
#         if not os.path.exists(pmsettings['work_dir']):
#             pmsettings['work_dir'] = os.path.expanduser('~')
#         return pmsettings
#
#     def save(self):
#         """
#         保存
#         :return:
#         """
#         import json
#         try:
#             config_file = os.path.join(self.settings_path, 'pyminer_settings.json')
#             with open(config_file, 'w') as f:
#                 json.dump(self, f, indent=4)
#         except FileNotFoundError as e:
#             logging.warning(e)


if __name__ == '__main__':
    s1 = Settings()
    s2 = Settings()
    s3 = Settings.instance
    print(s3)
    print(id(s1), id(s2), s1 is s2, id(s3))
