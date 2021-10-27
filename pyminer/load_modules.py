import logging
import os

from PySide2.QtCore import QTranslator, QSettings
from PySide2.QtGui import QFontDatabase
from PySide2.QtWidgets import QApplication

from utils import get_root_dir, get_config_file_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_translator(app: QApplication):
    """加载翻译文件

    Args:
        app: PyQt的Application。
    """
    # 注意需要保留trans变量的引用
    app.translator = QTranslator()
    app.translator2 = QTranslator()

    settings = QSettings(get_config_file_dir("config.ini"), QSettings.IniFormat)

    language = settings.value("MAIN/LANGUAGE")
    logger.debug("获取设置项MAIN/LANGUAGE: %s" % language)
    path_lang = os.path.join(get_root_dir(), 'languages', '{}'.format(language), '{}.qm'.format(language))
    logger.debug("翻译文件的路径：%s" % path_lang)
    if os.path.isfile(path_lang):
        app.translator.load(path_lang)
        app.installTranslator(app.translator)
        logger.debug("翻译文件已经加载！")
    else:
        raise FileNotFoundError("Translation file for language %s was not found!" % language)


def load_fonts(app: QApplication):
    """
    注册字体文件
    """
    app.font_dir = path = os.path.join(get_root_dir(), 'resources', 'fonts')
    for name in os.listdir(path):
        QFontDatabase.addApplicationFont(os.path.join(path, name))
    font_db = QFontDatabase()
