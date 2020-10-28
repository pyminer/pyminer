import logging
logger = logging.getLogger(__name__)

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface
from .server_by_socket import run
class Extension(BaseExtension):
    def on_load(self):
        run(self.extension_lib)
        logger.debug(self.settings)


class Interface(BaseInterface):
    pass
