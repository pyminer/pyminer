"""
作者:demo
创建日期:2020-01-01
说明:示例描述信息
"""
from features.extensions.extensionlib import BaseExtension, BaseInterface


class Extension(BaseExtension):

    def on_load(self):
        app_toolbar_interface = self.extension_lib.get_interface('applications_toolbar')
        import os
        path = os.path.dirname(__file__)
        app_toolbar_interface.add_process_action('应用分类', '应用名称',
                                                 os.path.join(path, '应用图标'),
                                                 ['python', '-u', os.path.join(path, '入口文件')])


class Interface(BaseInterface):
    pass
