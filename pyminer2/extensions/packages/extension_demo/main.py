import logging
logger = logging.getLogger(__name__)

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

class Extension(BaseExtension):
    def on_load(self):
        logger.debug(self.settings)


class Interface(BaseInterface):
    pass
