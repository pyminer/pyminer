class AuthManager():
    """
    用户认证管理类
    """

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self):
        self.login_status = False
        self.browser_id = None

    def show_login_page(self):
        from features.extensions.extensionlib.extension_lib import extension_lib
        extension_lib.get_interface('embedded_browser').open_url(url='http://localhost:5000/auth/login', side='right')

    def show_register_page(self):
        from features.extensions.extensionlib.extension_lib import extension_lib
        extension_lib.get_interface('embedded_browser').open_url(url='http://localhost:5000/auth/register', side='right')

    @staticmethod
    def get_instance() -> 'AuthManager':
        return AuthManager.instance


_am = AuthManager()

from lib.localserver.server import server
from .authlocalserver import auth

server.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    am = AuthManager()
    AuthManager.get_instance().login_status = True
    assert True == AuthManager.get_instance().login_status
    AuthManager.get_instance().login_status = False
    assert False == AuthManager.get_instance().login_status
