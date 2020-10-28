import cgitb
import os
import sys
import time
import logging

from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSplashScreen
from typing import TYPE_CHECKING
from pyminer2.pmappmodern import load_fonts, load_translator, MainWindow

t0 = time.time()  # 开始时间
# 异常处理设置
cgitb.enable(format='text')

# 日志设置
logger = logging.getLogger(__name__)

t2 = time.time()  # 结束时间
logging.info(f'time spent for importing modules {t2 - t0}')  # 打印日志，启动耗时


def test_settings_change():

    from pyminer2.extensions.extensionlib.extension_lib import extension_lib
    button_settings = extension_lib.UI.get_toolbar('toolbar_home').get_control_widget('button_settings')
    print(button_settings)
    button_settings.click()

def test_open_app():
    from pyminer2.extensions.extensionlib.extension_lib import extension_lib

    if TYPE_CHECKING:
        from pyminer2.extensions.packages.applications_toolbar.applications_toolbar import PMDrawingsToolBar

    tb:'PMDrawingsToolBar' = extension_lib.UI.get_toolbar('applications_toolbar')
    tb.show_apps_button_bar.buttons[0].click()



def main(test_func):
    from pyminer2 import pmutil
    app = QApplication(sys.argv)
    path_logo = os.path.join(pmutil.get_root_dir(), r'ui\source\icons\logo.png')
    app.setWindowIcon(QIcon(path_logo))  # 设置应用logo

    path_splash = os.path.join(pmutil.get_root_dir(), r'ui\source\images\splash.png')
    splash = QSplashScreen(QPixmap(path_splash))
    splash.showMessage("正在加载pyminer... 0%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()  # 显示启动界面

    pmutil._application = app
    load_fonts(app)
    load_translator(app)
    # font = os.path.join(os.path.dirname(__file__), 'ui', 'source', 'font', 'SourceCodePro-Regular.ttf')
    app.default_font = 'Deng'
    f = QFont(app.default_font, 10)
    app.setFont(f)
    demo = MainWindow()
    demo.events_ready_signal.connect(test_func)
    splash.finish(demo)  # 修复故障 I1VYVO 程序启动完成后,关闭启动界面   liugang 20200921
    id(demo)


    sys.exit(app.exec_())


main(test_settings_change)
# main(test_open_app)