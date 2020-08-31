from pyminer.pmapp import Application, MyMainForm, TextStyle
from pyminer.pmutil import _application, _root_dir, _main_window  # [TODO]这一行可能会被标记为灰色，但是不能删去
from PyQt5.QtWidgets import QSplashScreen, qApp
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
import sys
import pyminer.pmutil as pmutil


def boot():
    # global _root_dir, _application, _main_window

    pmutil._root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = pmutil.get_root_dir()

    app = Application(sys.argv)

    pmutil._application = app
    app.setWindowIcon(QIcon(root_dir + '/ui/source/icons/logo.png'))
    # 通过QSS样式的方式设置按钮文字
    app.setStyleSheet(TextStyle)

    splash = QSplashScreen(QPixmap(root_dir + '/ui/source/images/splash.png'))
    splash.showMessage("加载pyminer... 0%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()  # 显示启动界面
    qApp.processEvents()  # 处理主进程事件

    myWin = MyMainForm()
    myWin.load_data(splash)
    pmutil._main_window = myWin

    myWin.data_import_file_test('class.csv')

    # 窗口美化设置
    # QssTools.set_qss_to_obj(root_dir + "/ui/source/qss/pyminer.qss", app)
    # 设置窗口风格

    myWin.actionFusion.triggered.connect(app._slot_setStyle)
    myWin.actionWindows.triggered.connect(app._slot_setStyle)
    myWin.actionQdarkstyle.triggered.connect(app._slot_setStyle)
    myWin.actionWindowsVista.triggered.connect(app._slot_setStyle)
    myWin.show()
    splash.finish(myWin)  # 隐藏启动界面
    sys.exit(app.exec_())


if __name__ == '__main__':
    boot()
