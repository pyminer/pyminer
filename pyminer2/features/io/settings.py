"""
settings.py负责设置文件的输入输出。
Settings继承字典类，另外写了存储函数。
还有其他设置的函数
"""
import logging
import os
import json
from typing import Dict

from PyQt5.QtWidgets import QApplication
import qdarkstyle

logger = logging.getLogger(__name__)


def load_theme(style: str):
    """
    设置主题。
    :param style:
    :return:
    """
    from pyminer2.pmutil import get_main_window

    app = QApplication.instance()
    mw = get_main_window()
    if style == 'Fusion':
        mw.setStyleSheet('')
        app.setStyleSheet('')
        standard_ss = mw.get_stylesheet('standard')
        fusion_ss = mw.get_stylesheet('Fusion')
        app.setStyleSheet(standard_ss + '\n' + fusion_ss)
        app.setStyle('Fusion')

    elif style == 'Qdarkstyle':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        black_ss = mw.get_stylesheet('Qdarkstyle')
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        app.setStyleSheet(app.styleSheet() + '\n' + black_ss )
        app.setStyle('Windows')

    elif style.lower() == 'windowsvista':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        app.setStyleSheet(mw.get_stylesheet('windowsvista'))
        app.setStyle("windowsvista")
    elif style.lower() == 'windows':
        app.setStyleSheet('')
        mw.setStyleSheet('')
        app.setStyleSheet(mw.get_stylesheet('Windows'))
        app.setStyle("Windows")


class Settings(dict):
    """
    单例！
    """

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self):
        super(Settings, self).__init__()
        self.update(self.load())

    @staticmethod
    def get_instance() -> 'Settings':
        return Settings.instance

    def load(self) -> Dict[str, str]:
        """
        加载设置项。
        default_settings是默认设置项
        :return:
        """
        from pyminer2.pmutil import get_root_dir
        with open(os.path.join(get_root_dir(), 'config', 'features', 'default_settings.json'), 'r') as f:
            default_settings = json.load(f)
            default_settings['work_dir'] = get_root_dir()

        try:
            with open(os.path.join(get_root_dir(), 'config', 'customized', 'ui_settings.json'), 'r') as f:
                settings = json.load(f)

        except BaseException:
            settings = {}

        pmsettings = default_settings
        pmsettings.update(settings)
        return pmsettings

    def save(self):
        """
        保存
        :return:
        """
        import json
        from pyminer2.pmutil import get_root_dir
        try:
            config_file = os.path.join(
                get_root_dir(),
                'config',
                'customized',
                'ui_settings.json')
            if not os.path.exists(os.path.join(
                    get_root_dir(), 'config', 'customized')):
                os.mkdir(os.path.join(get_root_dir(), 'config', 'customized'))
            with open(config_file, 'w') as f:
                json.dump(self, f, indent=4)
        except FileNotFoundError as e:
            logging.warning(e)


if __name__ == '__main__':
    s1 = Settings()
    s2 = Settings()
    s3 = Settings.instance
    print(s3)
    print(id(s1), id(s2), s1 is s2, id(s3))
