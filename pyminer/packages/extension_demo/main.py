from features.extensions.extensionlib import BaseExtension, BaseInterface
import logging
logger = logging.getLogger(__name__)


class Extension(BaseExtension):
    def on_load(self):
        print("插件热更新测试!-修改后")
        logger.debug(self.settings)


class Interface(BaseInterface):
    pass
