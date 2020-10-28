"""
作者：@吴宫幽径
说明：
dialog无需写在json里面，直接调用主界面的控件就可以了。
"""
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface


class Extension(BaseExtension):

    def on_load(self):
        app_toolbar_interface = self.extension_lib.get_interface('applications_toolbar')
        import os
        path = os.path.dirname(__file__)
        app_toolbar_interface.add_app( group='应用测试', text='测试插件',
        icon_path=':/pyqt/source/images/lc_searchdialog.png', callback=lambda :print('this is app'), hint='')

        app_toolbar_interface.add_process_action('应用测试', '测试对话框',
                                      ':/pyqt/source/images/lc_searchdialog.png',
                                    ['python','-u',os.path.join(path,'run_dialog.py')])

class Interface(BaseInterface):
    pass


