# 服务器插件开发教程

服务器插件是指需要进行前后端交互的一类插件，可以为引入前端技术时，起到辅助作用。本教程以qt_vditor插件为例(qt_vditor是一个Markdown编辑器，引入了浏览器端比较流行的vditor编辑器)，展示一个服务器类型的插件的开发流程。

再本教程之前，您应该知悉插件的开发流程

在`pyminer/lib/localserver`文件夹下有一个`server.py`文件，如代码所示，它会创建一个线程，在线程中运行本地flask服务器，**这个文件一般不需要改动，它会在所有插件加载完成后再启动**

```python
from flask import Flask

from flask_cors import CORS
import threading

server = Flask(__name__)
CORS(server, supports_credentials=True)  # 解决跨域

server_thread = threading.Thread(target=server.run)  # 这个线程与主界面没有任何交互，直接用系统内建的线程库即可，保证其安全性。
server_thread.setDaemon(True)


if __name__ == '__main__':
    server_thread.start()
```

在`pyminer2/extensions/packages/qt_vditor`文件夹下有一个`main.py`，我们可以在其中**注册蓝图**，因为该文件会在插件加载过程中自动执行，这样在该插件中写的路由就可以生效了。

```python
import logging
logger = logging.getLogger('qt_vditor')
from features.extensions.extensionlib import BaseExtension, BaseInterface
from lib.localserver.server import server
from .route import qt_vditor

class Extension(BaseExtension):
    def on_load(self):
        server.register_blueprint(qt_vditor) # 注册蓝图
        logger.info('默认使用 qt vditor')


class Interface(BaseInterface):
    def hello(self):
        print("Hello")
```

flask典型的路由文件`route.py`（叫其他名字也可以）代码结构如下，你可以在里面写路由函数

```python
from flask import Blueprint
from flask import Flask

qt_vditor = Blueprint('qt_vditor',
                      __name__,
                      url_prefix='/qt_vditor',
                      template_folder='templates')


@qt_vditor.route('/', methods=['POST'])
def index():
    pass
```

后台这一块逻辑就是这样，至于前端用什么技术发post，get请求，采用什么技术封装html就随便发挥了。



