"""
说明：
dialog无需写在json里面，直接调用主界面的控件就可以了。
"""
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface


class Extension(BaseExtension):

    def on_load(self):
        app_toolbar_interface = self.extension_lib.get_interface('applications_toolbar')
        import os
        path = os.path.dirname(__file__)
        app_toolbar_interface.add_process_action('统计分析', 'DataMiner',
                                                 os.path.join(path, 'logo.ico'),
                                                 ['python', '-u', os.path.join(path, 'run_data_miner.py')])


class Interface(BaseInterface):
    pass
