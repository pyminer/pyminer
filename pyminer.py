import os
import sys
import logging
import webbrowser
import time
import datetime
import getpass
import base64
import pandas as pd

# 导入PyQt5模块
from PyQt5.Qt import *

# 导入功能组件

from pyminer.share import threads  # 导入多线程处理模块
from pyminer.features.sample import io  # 导入数据相关操作模块
from pyminer.features.visualize import base as plot  # 导入可视化相关操作模块
from pyminer.features.statistics import basic_stats  # 导入统计相关操作模块
from pyminer.features.modelling import base as model  # 导入模型相关操作模块
from pyminer.features.extensions.package_manager import package_manager  # 导入插件模块
from pyminer.features.report import pyreport  # 导入输出报告模块
from pyminer.features.preprocess import preprocess  # 导入数据预处理模块

# 导入UI相关模块
from pyminer.ui.base.mainForm import Ui_MainWindow
from pyminer.ui.base.newItem import Ui_Form as New_Ui_Form
from pyminer.ui.base.aboutMe import Ui_Form as AboutMe_Ui_Form
from pyminer.ui.base.option import Ui_Form as Option_Ui_Form
from pyminer.ui.source.qss.qss_tools import QssTools
import qdarkstyle

__Author__ = """
By: PyMiner Development Team
QQ: 454017698
Email: aboutlong@qq.com
"""
__Copyright__ = 'Copyright (c) 2020 PyMiner Development Team'
__Version__ = '1.0.1'

root_dir = os.path.dirname(os.path.abspath(__file__)) + r'\pyminer'

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

TextStyle = """
QMessageBox QPushButton[text="OK"] {
    qproperty-text: "确认";
}
QMessageBox QPushButton[text="Open"] {
    qproperty-text: "打开";
}
QMessageBox QPushButton[text="Save"] {
    qproperty-text: "保存";
}
QMessageBox QPushButton[text="Cancel"] {
    qproperty-text: "取消";
}
QMessageBox QPushButton[text="Close"] {
    qproperty-text: "关闭";
}
QMessageBox QPushButton[text="Discard"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Don't Save"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Apply"] {
    qproperty-text: "应用";
}
QMessageBox QPushButton[text="Reset"] {
    qproperty-text: "重置";
}
QMessageBox QPushButton[text="Restore Defaults"] {
    qproperty-text: "恢复默认";
}
QMessageBox QPushButton[text="Help"] {
    qproperty-text: "帮助";
}
QMessageBox QPushButton[text="Save All"] {
    qproperty-text: "保存全部";
}
QMessageBox QPushButton[text="&Yes"] {
    qproperty-text: "是";
}
QMessageBox QPushButton[text="Yes to &All"] {
    qproperty-text: "全部都是";
}
QMessageBox QPushButton[text="&No"] {
    qproperty-text: "不";
}
QMessageBox QPushButton[text="N&o to All"] {
    qproperty-text: "全部都不";
}
QMessageBox QPushButton[text="Abort"] {
    qproperty-text: "终止";
}
QMessageBox QPushButton[text="Retry"] {
    qproperty-text: "重试";
}
QMessageBox QPushButton[text="Ignore"] {
    qproperty-text: "忽略";
}
"""


class Application(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)

    def _slot_setStyle(self):
        """
        设置app样式
        """
        app.setStyleSheet('')  # 重置当前app样式
        tmp = self.sender().objectName()[6:]
        print(QStyleFactory.keys())
        if tmp in QStyleFactory.keys():
            app.setStyle(tmp)
        elif tmp == 'Qdarkstyle':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class NotificationIcon:
    Info, Success, Warning, Error, Close = range(5)
    Types = {
        Info: None,
        Success: None,
        Warning: None,
        Error: None,
        Close: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.Info] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC5ElEQVRYR8VX0VHbQBB9e/bkN3QQU0FMBSEVYFcQ8xPBJLJ1FWAqOMcaxogfTAWQCiAVRKkgTgfmM4zRZu6QhGzL0p0nDPr17e7bt7tv14RX/uiV48MJgAon+8TiAMRtMFogaqUJxADPwRRzg67kl8+xbWJWANR40iPQSSFgtX/mGQkaDr56V3VAKgGos4s2JXwJoF3naMPvMS+SrpTHs032GwGkdF+DsFMVnJm/oyGGeHico0EjIjpYes+YMyVd6R/flfkpBWCCQ9zaZM2LZDfLMGXsZ5kdI/lYBmINgHHyyLd1mWdBbAFAM/GY7K2WYx1AeB4T6L1N9umbGxZ0qktATaEAdCps48D39oq/LwEw3U5CN92LfczJoewfT7MAywDCaEbAuxeLrh0zz4L+0e4aAJfGy+sP3IMxlH1vpMJoSMCJDXgWtJeJVc6ACs9HBBrYODCJAFdYvAmkPJxnNqMwYht7Bn+T/lGg3z4DGEd3RPhQ54DBvwAOVkeqagRXfTLjh+x7+8sALOtfHLuiYzWOAiLoKbD58mnIGbCmLxUepS6NQmYlUGE0JeCTTXT9JvA9E9sZgO5iIpoyc6/YzcqSwQzgGgBXB7oXpH9klpRSkxY1xW/b7Iu2zk34PILPnazCqEPAtTWA8iZ0HsOu9L0bw4DzCJeNocMGNDpQ3IKO+6NUiJ4ysZNiBv5I3zPnmJmG5oM+wbS+9+qkvGi7NAXGmeUy0ioofa+XA0jH0UaMKpdRWs/adcwMqfV/tenqpqHY/Znt+j2gJi00RUzA201dXaxh9iZdZloJS+9H1otrkbRrD5InFqpPskxEshJQ468CkSmJC+i1HigaaxCAuCljgoDhwPdOjf7rFVxxuJrMkXScjtKc1rOLNpJk6nii5XmYzbngzlZn+RIb40kPJPTBYXUt6VEDJ8Pi6bWpNFb/jFYY6YGpDeKdjBmTKdMcxDGEmP73v2a2Gr/NOycGtglQZ/MPzEqCMLGckJEAAAAASUVORK5CYII=')))
        cls.Types[cls.Success] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACZUlEQVRYR8VXS3LTQBDtVsDbcAPMCbB3limkcAKSG4QFdnaYE2BOQLKzxSLJCeAGSUQheSnfwLmB2VJhXmpExpFHI2sk2RWv5FJPv9evP9NieuIfPzE+VSJw8qt3IMDvmahDoDYxt2UAACXMWIIowR5ffn8TJbaBWRE4CXvHAH9RgKXOgQUI48CfXZbZbiTw8Xe/w3d0zkydMkem91IZpyWOJu5sUXS+kEAqt3B+MNOLOuDqDEBLxxFHk7eza5MfIwEJDjhXTYD1s8zinYlEjsCD7FdNI9cJpEq0RFdPR47AMOzLCn69zegz6UgCP+pmfa8RSKudnPNdgCufTOLDxJtdPP7PoA1Cd8HEL5sSUCCD0B0x8bc1f8Bi6sevcgS2VXh6hMOwDz0gsUddNaxWKRjeuKfE/KlJ9Dq4UYH/o/Ns6scj+bgiMAjdayb26xLQwTfVEwg3gRcf6ARq578KuLo7VDc8psCQqwfjr4EfjYvkrAquFJ56UYpdSkAZSmNd1rrg0leOQFELgvA58OJTxVyRaAJORPOpF6UXnFUR5sDiXjs7UqsOMGMRlrWhTkJXpFL3mNrQZhA1lH3F0TiI5FurUQyMpn58VjhkSqQA4Tbw4nSVW6sBU5VXktXSeONlJH3s8jrOVr9RgVSFuNcWfzlh5n3LoKzMAPxxWuiULiQpiR2sZNnCyzIuWUr5Z1Ml0sgdHFZaShVDuR86/0huL3VXtDk/F4e11vKsTHLSCeKx7bYkW80hjLOrV1GhWH0ZrSlyh2MwdZhYfi8oZeYgLBmUiGd8sfVPM6syr2lUSYGaGBuP3QN6rVUwYV/egwAAAABJRU5ErkJggg==')))
        cls.Types[cls.Warning] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACmElEQVRYR8VXTW7TUBD+xjYSXZFukOIsSE9AskNJJMoJmq4r7OYEwAkabhBOkB/Emt4gVIojdpgbpIumEitX6gKB7UHPkauXxLHfc4F6Z3l+vvnmm/fGhAd+6IHzQwvA9cfOITMfAdQAcx1EdVEAM/tEFADsWyaPn57MfdXClABcT1qnzHSWJiwMzrwgoF91vXGRbS6AH59ajd8hDYmoURQo67tgxoij42rv62KX/04Agu44xmciVMokT32YERgGjquvZ1+y4mQCWPUa0/sk3vQlwqssEFsAVrQbU4XKL/ai2+5PPK6waQ4AOsoDnDARh83NdmwBuJq0fQI9L6p+L7rd3+/5gbAToMPI+FbkIzRRc72mbLcGIFE7jGFRIPHddmZrvstJh1X8CHGv6sxHqe1GkPYCoGcqgcoCAPPCdr2DLQC6wqMoPEj7qdqCNKllxs30sLpjYDluDUDGG5XqhY2sal3w4PiD7c7fJnHShMtJR8zpy/8CALiwndnhBgD1/t+XAXkaZAaUVHwnHulg0W6BNEWlAQD8zna8gQB0Ne70iXCm2j55jCUAei1gxvuaO+uXAcDg7zXHSy640iKUAehOEDJFqDmGQkiPLO5Fv+KADXOqvCuIsrPGsIyQdHou22YeRMJgOdHTQTkAfGk7XrLKrWlAvOhcRgBfWiZ3RQti0zxXuUFXCXMuo0TRitfxugjbIxC5RYzI6s9kIGFh+KLOpiW22id5AUuI8IaisFG4kCQg/sFKJgtPLix3KWXGeRETRbQDuCFCV2spTYMm+2FEI1WBbYIRPTeiqFtqLZeDraaD+qrbkpgQAvfl1WsXU0p/RjIjYYhTkNFgcCVlRlRKoAAc+5aF0V//NVPoc2kTLQZKZ8lx/AMXBmMwuXUwOAAAAABJRU5ErkJggg==')))
        cls.Types[cls.Error] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACrklEQVRYR82XW27aQBSG/4PtiNhIpStouoImKwjZAV1B07coWCpZQcgK6kh2lLeSFZSsIOwgdAdkBaUSEBQDpxpjU9vM+EJR03nDzJz/mzm3GcIrD3plfZQCeD47O1ho2jERNRmoE9AQG2BgBGBAwIiZe5Zh3JPjiG+5oxCAEF5q2iWITnMtRhOYu5XF4mr/9naYtSYXYGLbHQCXhYVTEwlom657rVqvBOB2uz71/a+ldq1SYe6ahnEhc4sSYGzbfQKOt915eh0D/ZrrnqS/SwEmrVYXRJ92Jb4OC+C65rrtuN0NgIltNwF837V4zN5Hy3V70e9NgFZrCKJ3CQDmJ9MwDsW36XzeB/AhA/CHqeuN2WxWX2paX2JraHneeynA+Pz8lCqVbxLjV5brimxAEJxqiEA8CjZVBvFy+bl2c9MV9hInoAw85qFpGEeRYQVEQjzMokcQHWxsiPne8jzh6j8AodGfyqNlHpiGcaKAkIk/gChwm2yYuv5W2FqfwLNtN5bAQ2bwySB83zENo50A8/1McaFRAU72XVek+mpk+D/JlIKI/xkee654uCbIhjVAqZIrgSgpLhiCwN4OAEj4vEB2yDybBCjsAol4ZD0nRdMQSRcUCsKUeNSw4o2mKMRGEOamoVx8FXDZKVosDYNMUHXAsBRnppo8RQcbpTgIGEkhykpFjnWxzGhPQYxt2yHgS/oIlKVYTJxImpG482nz+VG1Wh1N84pMCCGa0ULXHwmoJwCYnyzPW5fn/68dh7EgPbrMMl3gz7gro+n/7EoWD7w4a96l1NnJ1Yz5Lt6wCgFEk0r1CIkbiPnC9DxH5aHcd4FYGD5MOqVOg/muslh0/vphkm63k5eXZvA0I6qD+ZCI3jDzLxANiHn1NNvb6+30aVYgwLeeUsgFW1svsPA3Ncq4MHzVeO8AAAAASUVORK5CYII=')))
        cls.Types[cls.Close] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeElEQVQ4T2NkoBAwUqifgboGzJy76AIjE3NCWmL0BWwumzV/qcH/f38XpCfHGcDkUVwAUsDw9+8GBmbmAHRDcMlheAGbQnwGYw0DZA1gp+JwFUgKZyDCDQGpwuIlrGGAHHAUGUCRFygKRIqjkeKERE6+oG5eIMcFAOqSchGwiKKAAAAAAElFTkSuQmCC')))

    @classmethod
    def icon(cls, ntype):
        return cls.Types.get(ntype)


class NotificationItem(QWidget):
    closed = pyqtSignal(QListWidgetItem)

    def __init__(self, title, message, item, *args, ntype=0, callback=None, **kwargs):
        super(NotificationItem, self).__init__(*args, **kwargs)
        self.item = item
        self.callback = callback
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.bgWidget = QWidget(self)  # 背景控件, 用于支持动画效果
        layout.addWidget(self.bgWidget)

        layout = QGridLayout(self.bgWidget)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        # 标题左边图标
        layout.addWidget(
            QLabel(self, pixmap=NotificationIcon.icon(ntype)), 0, 0)

        # 标题
        self.labelTitle = QLabel(title, self)
        font = self.labelTitle.font()
        font.setBold(True)
        font.setPixelSize(22)
        self.labelTitle.setFont(font)

        # 关闭按钮
        self.labelClose = QLabel(
            self, cursor=Qt.PointingHandCursor, pixmap=NotificationIcon.icon(NotificationIcon.Close))

        # 消息内容
        self.labelMessage = QLabel(
            message, self, cursor=Qt.PointingHandCursor, wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
        font = self.labelMessage.font()
        font.setPixelSize(20)
        self.labelMessage.setFont(font)
        self.labelMessage.adjustSize()

        # 添加到布局
        layout.addWidget(self.labelTitle, 0, 1)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        layout.addWidget(self.labelClose, 0, 3)
        layout.addWidget(self.labelMessage, 1, 1, 1, 2)

        # 边框阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setColor(QColor(0, 0, 0, 25))
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)

        self.adjustSize()

        # 5秒自动关闭
        self._timer = QTimer(self, timeout=self.doClose)
        self._timer.setSingleShot(True)  # 只触发一次
        self._timer.start(5000)

    def doClose(self):
        try:
            # 可能由于手动点击导致item已经被删除了
            self.closed.emit(self.item)
        except:
            pass

    def showAnimation(self, width):
        # 显示动画
        pass

    def closeAnimation(self):
        # 关闭动画
        pass

    def mousePressEvent(self, event):
        super(NotificationItem, self).mousePressEvent(event)
        w = self.childAt(event.pos())
        if not w:
            return
        if w == self.labelClose:  # 点击关闭图标
            # 先尝试停止计时器
            self._timer.stop()
            self.closed.emit(self.item)
        elif w == self.labelMessage and self.callback and callable(self.callback):
            # 点击消息内容
            self._timer.stop()
            self.closed.emit(self.item)
            self.callback()  # 回调

    def paintEvent(self, event):
        # 圆角以及背景色
        super(NotificationItem, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)
        painter.fillPath(path, Qt.white)


class NotificationWindow(QListWidget):
    _instance = None

    def __init__(self, *args, **kwargs):
        super(NotificationWindow, self).__init__(*args, **kwargs)
        self.setSpacing(20)
        self.setMinimumWidth(412)
        self.setMaximumWidth(412)
        QApplication.instance().setQuitOnLastWindowClosed(True)
        # 隐藏任务栏,无边框,置顶等
        self.setWindowFlags(self.windowFlags() | Qt.Tool |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 去掉窗口边框
        self.setFrameShape(self.NoFrame)
        # 背景透明
        self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 不显示滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕高宽
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.setMinimumHeight(rect.height())
        self.setMaximumHeight(rect.height())
        self.move(rect.width() - self.minimumWidth() - 18, 0)

    def removeItem(self, item):
        # 删除item
        w = self.itemWidget(item)
        self.removeItemWidget(item)
        item = self.takeItem(self.indexFromItem(item).row())
        w.close()
        w.deleteLater()
        del item

    @classmethod
    def _createInstance(cls):
        # 创建实例
        if not cls._instance:
            cls._instance = NotificationWindow()
            cls._instance.show()
            NotificationIcon.init()

    @classmethod
    def info(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Info, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def success(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Success, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def warning(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Warning, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def error(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Error, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)


class CustomRect(QGraphicsObject):
    def __init__(self):
        super(CustomRect, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动

    def boundingRect(self):
        return QRectF(0, 0, 200, 50)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(QColor(212, 227, 242))
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def mousePressEvent(self, evt):
        print('鼠标按下')
        if evt.button() == Qt.LeftButton:
            print("左键被按下")
        elif evt.button() == Qt.RightButton:
            print("左键被按下")
        elif evt.button() == Qt.MidButton:
            print("中间键被按下")

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()


class RewriteQFileSystemModel(QFileSystemModel):
    def __init__(self,parent = None):
        super().__init__(parent)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if((p_int == 0) and (role == Qt.DisplayRole)):
            return u'名称'
        elif((p_int == 1) and (role == Qt.DisplayRole)):
            return u'大小'
        elif((p_int == 2) and (role == Qt.DisplayRole)):
            return '类型'
        elif ((p_int == 3) and (role == Qt.DisplayRole)):
            return '修改日期'
        else:
            return super().headerData(p_int,Qt_Orientation,role)

class MyMainForm(QMainWindow, Ui_MainWindow):
    """
    主窗体
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # self = Ui_MainWindow()
        self.setupUi(self)
        self.center()

        self.__file_path_choose = ""
        self.__all_dataset = dict()  # 定义字典，保存全部数据集的基本信息
        self.__all_dataset_name = set()  # 定义集合，保存全部数据集名称，确保不会重复
        self.__current_dataset_name = ""
        self.__current_dataset = pd.DataFrame()
        self.__current_dataset_dtype = set()  # 定义集合，保存当前数据集中存在的数据类型，确保不会重复
        self.__result_path = ''  # 结果文件保存路径
        self.__setting = dict()  # 设置文件
        self.slot_flush_console('info', 'system', 'pyminer已准备就绪')

        # 任务栏图标设置
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("pyminer数据分析")
        self.tray_icon.setIcon(QIcon(root_dir + '/ui/source/icons/logo.png'))

        title_action = QAction("pyminer数据分析", self)
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        hide_action = QAction("隐藏", self)
        title_action.triggered.connect(self.main_help_display)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(title_action)
        tray_menu.addSeparator()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.action_minitray.triggered.connect(self.minitray_show)

        self.action_info.triggered.connect(self.info_show)
        self.action_success.triggered.connect(self.success_show)
        self.action_warning.triggered.connect(self.warning_show)
        self.action_error.triggered.connect(self.error_show)

        self.action_menu_data_merge_h.triggered.connect(self.data_merge_horizontal_display)
        self.action_menu_data_merge_v.triggered.connect(self.data_merge_vertical_display)

        # 文件管理器
        # my_dir = QDir.rootPath()
        my_dir = ''
        self.model = RewriteQFileSystemModel()
        self.model.setRootPath(my_dir)
        # self.treeView_files.setRootIndex(self.model.index(QDir.homePath()))

        self.treeView_files.setModel(self.model)
        self.treeView_files.setRootIndex(self.model.index(my_dir))
        self.treeView_files.setAnimated(False)
        self.treeView_files.setSortingEnabled(True)  # 启用排序
        self.treeView_files.header().setSortIndicatorShown(True)  # 启用标题排序
        self.treeView_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView_files.customContextMenuRequested.connect(self.treeViewFilesShowContextMenu)



        # 流程图
        self.rect = CustomRect()
        self.rect.setPos(50, 50)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 300, 300)
        self.scene.addItem(self.rect)
        self.tab_flow.graphicsView.setScene(self.scene)

        # self.btn_data_row_filter.setGraphicsEffect(self.eff) #特效测试。
        # 与page_data有关的全部事件，都移动到了ui.base.widgets.controlpanel的PMPageData类之中。

        # 打开"菜单-文件导入"窗口
        self.action_menu_import_file.triggered.connect(self.data_import_file_display)
        # 打开"菜单-打开"窗口
        self.action_menu_open.triggered.connect(self.main_open_data_chooseFile)

        # 打开"从数据库导入"窗口
        self.action_menu_database.triggered.connect(self.data_import_database_display)
        # 打开"新建"窗口
        self.action_menu_new.triggered.connect(self.main_new_display)
        # 打开"选项"窗口
        self.action_menu_option.triggered.connect(self.main_option_display)

        # 打开"关于"窗口
        self.action_about.triggered.connect(self.main_aboutme_display)
        # 打开"模型WOE"窗口
        self.action_menu_woe_iv.triggered.connect(self.model_woe_display)

        # 打开"数据-行筛选"窗口
        self.action_menu_data_row_filter.triggered.connect(self.data_row_filter_display)
        self.page_data.btn_data_row_filter.clicked.connect(self.data_row_filter_display)

        # "快速退出"
        self.action_menu_quick_exit.triggered.connect(qApp.quit)

        # 隐藏右侧工具栏
        self.action_hide_right.triggered.connect(self.right_widget_hide)

        # 更新主页面的显示数据
        self.action_data.triggered.connect(self.change_stacked_page)
        self.action_stats.triggered.connect(self.change_stacked_page)
        self.action_plot.triggered.connect(self.change_stacked_page)
        self.action_model.triggered.connect(self.change_stacked_page)
        self.action_assess.triggered.connect(self.change_stacked_page)

        self.action_menu_data_filter.triggered.connect(self.data_row_filter_display)

        # 排序数据
        self.action_menu_sort.triggered.connect(self.data_sort_display)

        self.action_menu_tree.triggered.connect(self.model_tree_display)  # 打开"模型-决策树"窗口

        self.action_menu_stat_describe.triggered.connect(self.stats_base_display)  # 显示“描述统计”窗口

        # 显示“官方网站”
        self.action_officesite.triggered.connect(self.main_officesite_display)
        # 显示“官方网站-帮助”
        self.action_help.triggered.connect(self.main_help_display)

        # 显示“Python包管理工具”
        self.action_package_manager.triggered.connect(self.package_manager_display)

        # 显示“Jupyter-notebook”
        self.action_jupyter_notebook.triggered.connect(self.jupyter_notebook_display)
        # self.action_ipython.triggered.connect(self.func_test)

        # self.action_menu_result.triggered.connect(self.send_signal)
        # self.action_menu_dataset.triggered.connect(self.accept_signal)
        # self.action_menu_dataset.triggered.connect(self.data_import_file_display)
        # self.accept_signal()

        # 隐藏工具栏、状态栏
        self.action_menu_toolbar.triggered.connect(self.menu_toolbar_hide)
        self.action_menu_statusbar.triggered.connect(self.menu_statusbar_hide)

        # 隐藏工作区间 任务列表
        self.action_menu_workdir.triggered.connect(self.menu_workdir_hide)
        self.action_menu_todolist.triggered.connect(self.menu_todolist_hide)

        # 隐藏工具窗口
        self.action_menu_toolbox.triggered.connect(self.right_widget_hide)

    #  ================================事件处理函数=========================
    def closeEvent(self, event):
        """
        退出时弹出确认消息提示
        """
        reply = QMessageBox.question(self, '注意', '确认退出吗？', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        # 添加按钮，可用中文
        if reply == QMessageBox.Ok:
            event.accept()
            # os.system(r"taskkill /F /IM pyminer.exe")  # 结束进程
        else:
            event.ignore()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def minitray_show(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def info_show(self):
        NotificationWindow.info('提示', '这是一条会自动关闭的消息')

    def success_show(self):
        NotificationWindow.success('提示', '这是一条会自动关闭的消息')

    def warning_show(self):
        NotificationWindow.warning('提示', '这是一条会自动关闭的消息')

    def error_show(self):
        NotificationWindow.error('提示',
                                 '<html><head/><body><p><span style=" font-style:italic; color:teal;">这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案</span></p></body></html>')

    def menu_toolbar_hide(self):
        self.toolBar_left.setVisible(False) if self.toolBar_left.isVisible() else self.toolBar_left.setVisible(True)

    def menu_statusbar_hide(self):
        self.statusBar.setVisible(False) if self.statusBar.isVisible() else self.statusBar.setVisible(True)

    def menu_workdir_hide(self):
        if self.widget_left.isHidden():
            self.widget_left.setVisible(True)

        self.treeWidget_storehouse.setVisible(
            False) if self.treeWidget_storehouse.isVisible() else self.treeWidget_storehouse.setVisible(True)

        if self.treeWidget_storehouse.isHidden() and self.treeWidget_history.isHidden():
            self.widget_left.setVisible(False)

    def menu_todolist_hide(self):
        if self.widget_left.isHidden():
            self.widget_left.setVisible(True)

        self.treeWidget_history.setVisible(
            False) if self.treeWidget_history.isVisible() else self.treeWidget_history.setVisible(True)

        if self.treeWidget_storehouse.isHidden() and self.treeWidget_history.isHidden():
            self.widget_left.setVisible(False)

    def right_widget_hide(self):
        self.widget_right.setVisible(False) if self.widget_right.isVisible() else self.widget_right.setVisible(True)

    def test_report(self):
        print("查看测试报告")
        data = pd.read_csv("c:/demo/uci.csv")
        data_name = 'class.csv'
        new = data.describe().T
        pd.set_option('precision', 2)
        self.slot_flush_report("info", "描述统计:Age", new, data_name, precision=2)

    #  ================================自定义功能函数=========================
    def treeViewFilesShowContextMenu(self, pos):  # 创建右键菜单
        self.treeView_files.contextMenu = QMenu(self.treeView_files)
        self.openAction = self.treeView_files.contextMenu.addAction(u'打开')
        self.importAction = self.treeView_files.contextMenu.addAction(u'导入')
        self.renameAction = self.treeView_files.contextMenu.addAction(u'重命名')
        self.deleteAction = self.treeView_files.contextMenu.addAction(u'删除')
        self.openAction.triggered.connect(self.openActionHandler)
        self.importAction.triggered.connect(self.importActionHandler)
        self.renameAction.triggered.connect(self.renameActionHandler)
        self.deleteAction.triggered.connect(self.deleteActionHandler)
        self.treeView_files.contextMenu.popup(QCursor.pos())
        self.treeView_files.contextMenu.show()

    def openActionHandler(self):
        print("打开功能的函数是openActionHandler")

    def importActionHandler(self):
        print("打开功能的函数是importActionHandler")

    def renameActionHandler(self):
        print("打开功能的函数是renameActionHandler")

    def deleteActionHandler(self):
        print("打开功能的函数是deleteActionHandler")

    def setting_check(self):
        setting_path = root_dir + r'\settings.json'
        logging.info("配置文件加载完成，路径:{}".format(setting_path))
        if os.path.exists(setting_path):
            with open(setting_path, 'r', encoding='utf-8') as f:
                self.__setting = json.load(f)
        else:
            reply = QMessageBox.critical(self,
                                         'pyminer 出现错误',
                                         "在指定位置<br>" + setting_path + "<br>找不到配置文件",
                                         QMessageBox.Yes,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()

    #  ================================自定义槽函数=========================
    def slot_dataset_reload(self, dataset_name, dataset, path, create_time, update_time, remarks, file_size):
        """
        :param dataset_name:数据集名称
        :param dataset: 数据集
        :param path: 数据文件路径
        :param create_time: 创建时间
        :param update_time: 更新时间
        :param remarks: 备注
        :param file_size: 文件大小
        :return: 刷新主窗体中当前显示的数据
        """
        print("开始更新数据")
        all_data = pd.DataFrame(dataset)
        self.alter_current_dataset(dataset_name, all_data, path, create_time, update_time, remarks, file_size)
        # 获取已经导入页面获取的数据集
        data = all_data.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        print("更新数据完成")

        # 添加数据集节点
        # 判断是否已经存在同名节点则先删除原节点，再进行添加，否则直接添加节点
        node_dataset = self.get_node_dataset()
        childCount = node_dataset.childCount()
        print("childCount:", childCount)
        if childCount > 0:
            if_exists = 0
            for i in range(childCount):
                txt = node_dataset.child(i).text(0)
                print("txt:", txt)
                if txt == dataset_name:
                    if_exists = 1
            if if_exists == 1:
                print("同名节点已存在，无需添加节点")
            else:
                child_dataset = QTreeWidgetItem(node_dataset)
                child_dataset.setText(0, dataset_name)
                child_dataset.setIcon(0, QIcon(root_dir + '/ui/source/images/sc_viewdatasourcebrowser.png'))
                print("添加节点完成")
        else:
            child_dataset = QTreeWidgetItem(node_dataset)
            child_dataset.setText(0, dataset_name)
            child_dataset.setIcon(0, QIcon(root_dir + '/ui/source/images/sc_viewdatasourcebrowser.png'))
            print("添加节点完成")

    def slot_result_reload(self, result_name, result_path):
        self.__result_path = result_path
        self.inner_browser_display()

        # 添加结果节点
        node_result = self.treeWidget_storehouse.topLevelItem(6)
        child_model = QTreeWidgetItem(node_result)
        child_model.setText(0, result_name)
        child_model.setIcon(0, QIcon(root_dir + '/ui/source/images/lc_optimizetable.png'))
        print("添加节点完成")

    def slot_flush_console(self, level, module, content):
        """
        刷新主窗体执行情况日志
        :return:
        level:文本，warnning error info
        module:业务模块名称，例如 数据获取，数据处理，数据探索，统计，模型，可视化，评估
        """
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 日志记录时间
        user = getpass.getuser()
        msg = create_time + ' ' + user + ' ' + level.upper() + ' [' + module + ']' + ':' + content
        if level == "error":
            html = "<a style='font-family:verdana;color:red;font-size:11;'>" + msg + "</a>"
        else:
            html = "<a style='font-family:verdana;color:black;font-size:11;'>" + msg + "</a>"

        console = self.text_edit_console_tab.textEdit_console  # 由于代码重构，这里出现了不同。
        # [!TODO]应当创建方法，一次性的完成这个工作。
        console.moveCursor(QTextCursor.End)
        console.append(html)

    def slot_flush_result(self, dataset):
        pass

    def slot_flush_report(self, header_1, header_2, dataset, dataset_name, index=True, precision=-1):
        """
        :param header_1: 主标题，例如 描述性统计量: Age
        :param header_2:副标题，例如 统计量
        :param dataset:数据集
        :param dataset_name:数据集名称
        :param index:数据集是否包含指定索引
        :param precision:显示精度，-1表示自动设置，否则为指定精度
        :return:html
        """
        template = open(root_dir + r"\template\report.html", 'r', encoding='utf-8').read()

        # 根据原始数据是否包含列名，分别处理html
        if index:  # 包含索引
            th = "<th>变量</th>"  # 标题行新增索引名
            for c in dataset.columns:
                col = "<th>" + c + "</th>"
                th = th + col

            td = str()
            for r in range(dataset.shape[0]):  # 行
                grid = str()
                grid_index = "<td>" + str(dataset.index[r]) + "</td>"
                for c in range(dataset.shape[1]):  # 列
                    if precision == -1:
                        grid = grid + "<td>" + str(dataset.iat[r, c]) + "</td>"
                    else:
                        prec = r"{:,." + str(precision) + "f}"
                        grid = grid + "<td>" + prec.format(dataset.iat[r, c]) + "</td>"
                row = "<tr>" + grid_index + grid + "</tr>"
                td = td + row
        else:  # 标题行不指定索引名
            th = str()
            for col in dataset.columns:
                row = "<th>" + col + "</th>"
                th = th + row
            td = str()
            for r in range(dataset.shape[0]):  # 行
                grid = str()
                for c in range(dataset.shape[1]):  # 列
                    if precision == -1:
                        grid = grid + "<td>" + str(dataset.iat[r, c]) + "</td>"
                    else:
                        prec = r"{:,." + str(precision) + "f}"
                        grid = grid + "<td>" + prec.format(dataset.iat[r, c]) + "</td>"
                row = "<tr>" + grid + "</tr>"
                td = td + row

        # 生成新报告内容
        html_report = template.replace("$header_1$", header_1)
        html_report = html_report.replace("$header_2$", header_2)
        html_report = html_report.replace("$dataset_name$", dataset_name)
        html_report = html_report.replace("$th$", th)
        html_report = html_report.replace("$td$", td)

        with open(output_dir + r'\report_' + str(time.time()).split('.')[0] + '.html', 'w', encoding='utf-8') as file:
            file.write(html_report)
        print("报告输出成功")
        print("报告地址：", output_dir + r'\report_' + str(time.time()).split('.')[0] + '.html')

    def on_treeWidget_storehouse_customContextMenuRequested(self, pos):  # 右键快捷菜单
        item = self.treeWidget_storehouse.currentItem().text(0)

        self.__treeWidget_storehouse_node_parent = ""
        if item not in ("数据集", "数据处理", "统计", "可视化", "模型", "评估", "结果"):
            self.__treeWidget_storehouse_node_parent = self.treeWidget_storehouse.currentItem().parent().text(0)

        # 数据集右键菜单
        menuList = QMenu(self)  # 创建菜单
        if item == "数据集" or self.__treeWidget_storehouse_node_parent == "数据集":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbqueryedit.png'), '打开', self,
                                       triggered=self.main_open_data))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbqueryedit.png'), '导入数据集', self,
                                       triggered=self.main_open_data_chooseFile))
            menuList.addAction(
                QAction(QIcon(root_dir + '/ui/source/images/formfilternavigator.png'), '筛选', self,
                        triggered=self.main_open_data_chooseFile))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_sortascending.png'), '排序', self,
                                       triggered=self.main_open_data_chooseFile))

            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon('./ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "数据处理" or self.__treeWidget_storehouse_node_parent == "数据处理":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbviewtables.png'), '新建数据处理', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "统计" or self.__treeWidget_storehouse_node_parent == "统计":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_autosum.png'), '新建描述统计', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "可视化" or self.__treeWidget_storehouse_node_parent == "可视化":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_drawchart.png'), '新建可视化', self,
                                       triggered=self.plot_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "模型" or self.__treeWidget_storehouse_node_parent == "模型":
            menuList.addAction(
                QAction(QIcon(root_dir + '/ui/source/images/lc_switchcontroldesignmode.png'), '新建模型', self,
                        triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "评估" or self.__treeWidget_storehouse_node_parent == "评估":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_rotateleft.png'), '新建评估', self,
                                       triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))

        elif item == "结果" or self.__treeWidget_storehouse_node_parent == "结果":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_optimizetable.png'), '导出结果', self,
                                       triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))

        menuList.exec(QCursor.pos())  # 显示菜单

    def on_treeWidget_customContextMenuRequested(self, pos):  ##右键快捷菜单
        menuList = QMenu(self)

        self.stackedWidget.setCurrentIndex(4)

    def load_data(self, sp):
        for i in range(1, 2):  # 模拟主程序加载过程
            time.sleep(1)  # 加载数据
            sp.showMessage("加载... {0}%".format(i * 30), Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
            qApp.processEvents()  # 允许主进程处理事件

    def main_officesite_display(self):
        """
        打开官方网站页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.pandaxstudio.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.pandaxstudio.com")

    def main_help_display(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def main_dataset_change(self):
        # 重新加载当前数据集到主页面

        try:
            self.main_data_reload()

        except:
            pass

    def main_data_reload(self):
        # 获取已经导入页面获取的数据集
        data = self.__current_dataset.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def main_result_display(self):
        """
        显示"结果"窗口
        """
        print('test')

    def main_option_display(self):
        """
        显示"选项"窗口
        """
        self.optionForm = OptionForm()

        self.optionForm.show()

    def main_new_display(self):
        """
        显示"新建"窗口
        """
        self.new_item = NewItemForm()
        self.new_item.show()

    def main_aboutme_display(self):
        """
        显示"关于"窗口
        """
        self.aboutme = AboutMeForm()
        self.aboutme.show()

    def main_open_data(self):
        """
                :param dataset_name:数据集名称
                :param dataset: 数据集
                :return: 刷新主窗体中当前显示的数据
                """
        print("开始更新数据")
        node_name = self.treeWidget_storehouse.currentItem().text(0)
        print(node_name)
        all_data = pd.DataFrame(self.__all_dataset.get(node_name))  # 获取当前数据
        self.__current_dataset_name = node_name  # 修改当前数据名称
        # 获取已经导入页面获取的数据集
        data = all_data.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        print("更新数据完成")

    def main_open_data_chooseFile(self):

        self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                        '选择文件', '', "All Files (*);;\
                                                                文本文件 (*.txt *.csv *.tsv);;\
                                                                EXCEL文件 (*.xls *.xlsx *.xlsm *.xltx *.xltm);;\
                                                                SPSS文件 (*.sav *.zsav);;\
                                                                SAS文件 (*.sas7bdat)")  # 设置文件扩展名过滤,用双分号间隔

        if self.__file_path_choose == "":
            logging.info("\n取消选择")
            return

        if os.path.split(self.__file_path_choose)[1].endswith(('xlsx', 'xlsm', 'xltx', 'xltm')):
            if len(self.__file_path_choose) > 0:
                self.import_excel_form = io.ImportExcelForm()
                self.import_excel_form.file_path_init(self.__file_path_choose)
                self.import_excel_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_excel_form.exec_()
            else:
                logging.info("信号发射失败--导入文件已选择")

        elif os.path.split(self.__file_path_choose)[1].endswith(('sav', 'zsav')):
            if len(self.__file_path_choose) > 0:
                self.import_spss_form = io.ImportSpssForm()
                self.import_spss_form.file_path_init(self.__file_path_choose)
                self.import_spss_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_spss_form.exec_()
            else:
                logging.info("信号发射失败")


        elif os.path.split(self.__file_path_choose)[1].endswith(('sas7bdat')):
            if len(self.__file_path_choose) > 0:
                self.import_sas_form = io.ImportSasForm()
                self.import_sas_form.file_path_init(self.__file_path_choose)
                self.import_sas_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_sas_form.exec_()
            else:
                logging.info("信号发射失败")

        else:
            if len(self.__file_path_choose) > 0:
                self.import_form = io.ImportForm()
                self.import_form.file_path_init()
                self.import_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_form.exec_()
            else:
                logging.info("信号发射失败")

    def change_stacked_page(self):
        """
        显示或隐藏右侧工具栏
        """
        widget = getattr(self, self.sender().objectName().replace('action', 'page'), None)
        if widget:
            cur_widget = self.stackedWidget.currentWidget()
            if widget == cur_widget:
                self.widget_right.setVisible(not self.widget_right.isVisible())
            else:
                self.widget_right.setVisible(True)
                self.stackedWidget.setCurrentWidget(widget)

    def get_node_dataset(self):
        return self.treeWidget_storehouse.topLevelItem(0)

    def alter_current_dataset(self, dataset_name, dataset, path='',
                              create_time='', update_time='', remarks='',
                              file_size=''):
        # 修改当前正在使用的数据集
        self.__current_dataset = dataset
        self.__current_dataset_name = dataset_name
        self.__all_dataset_name.add(dataset_name)  # 保存数据集名称
        row = str(dataset.shape[0])  # 行数
        col = str(dataset.shape[1])  # 列数
        memory_size = self.__current_dataset.memory_usage().sum()
        # 内存大小
        if memory_size < 1024:
            memory_usage = str(memory_size) + ' bytes'
        elif (memory_size / 1024) < 1024:
            memory_usage = str(round(memory_size / 1024, 2)) + ' KB'
        elif (memory_size / 1024 / 1024) < 1024:
            memory_usage = str(round(memory_size / 1024 / 1024, 2)) + ' M'
        elif (memory_size / 1024 / 1024) >= 1024:
            memory_usage = str(round(memory_size / 1024 / 1024 / 1024, 2)) + ' G'

        # 文件大小
        if file_size.isdigit():
            if int(file_size) < 1024:
                file_usage = str(file_size) + ' bytes'
            elif (int(file_size) / 1024) < 1024:
                file_usage = str(round(int(file_size) / 1024, 2)) + ' KB'
            elif (int(file_size) / 1024 / 1024) < 1024:
                file_usage = str(round(int(file_size) / 1024 / 1024, 2)) + ' M'
            elif (int(file_size) / 1024 / 1024) >= 1024:
                file_usage = str(round(int(file_size) / 1024 / 1024 / 1024, 2)) + ' G'
        else:
            file_usage = file_size

        # 描述信息，包含变量名、数据类型、非空数量
        data_type = []
        data_notna_cnt = []
        for i in dataset.columns:
            data_type.append(str(dataset.loc[:, i].dtype))
            data_notna_cnt.append(dataset.loc[:, i].notna().sum())
        info = pd.DataFrame({"变量名称": list(dataset.columns), "数据类型": data_type, "非空值数量": data_notna_cnt})

        dataset_new = {dataset_name: dataset,
                       dataset_name + ".path": path,
                       dataset_name + ".create_time": create_time,
                       dataset_name + ".update_time": update_time,
                       dataset_name + ".row": row,
                       dataset_name + ".col": col,
                       dataset_name + ".remarks": remarks,
                       dataset_name + ".file_size": file_usage,
                       dataset_name + ".memory_usage": memory_usage,
                       dataset_name + ".info": info, }

        # 添加当前数据集到数据集列表中
        print("添加当前数据集到数据集列表中")
        # 检查数据集名称是否已存在，如果存在则修改相关信息，否则进行新增
        if self.__current_dataset_name in list(self.__all_dataset.keys()):
            self.__all_dataset[dataset_name] = dataset
            self.__all_dataset[dataset_name + ".path"] = path
            self.__all_dataset[dataset_name + ".create_time"] = create_time
            self.__all_dataset[dataset_name + ".update_time"] = update_time
            self.__all_dataset[dataset_name + ".row"] = row
            self.__all_dataset[dataset_name + ".col"] = col
            self.__all_dataset[dataset_name + ".remarks"] = remarks
            self.__all_dataset[dataset_name + ".file_size"] = file_size
            self.__all_dataset[dataset_name + ".memory_usage"] = memory_usage
            self.__all_dataset[dataset_name + ".info"] = info
        else:
            self.__all_dataset.update(dataset_new)
        self.tabWidget.setCurrentIndex(0)

    def add_dataset_to_workdir(self, dataset_name):
        child_dataset = QTreeWidgetItem()
        child_dataset.setText(0, dataset_name)
        child_dataset.setIcon(0, QIcon(root_dir + '/ui/source/images/sc_viewdatasourcebrowser.png'))
        return child_dataset

    def data_import_file_display(self):
        """
        显示导入文件窗口，当数据改变时，刷新主窗体中当前显示的数据
        """
        self.import_form = io.ImportForm()
        self.import_form.signal_data_change.connect(self.slot_dataset_reload)
        self.import_form.exec_()

    def data_import_file_test(self, csv_path: str):
        '''
        这是一个测试时使用的方法。当调用时，可以直接打开数据。当界面崩溃之后，可以尽可能快速的启动。
        '''
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
        path = csv_path
        print("path:", path)
        file_size = str(os.path.getsize(path))
        print("file_size:", file_size)
        remarks = ''
        current_dataset = pd.read_csv(path, engine="python",
                                      encoding='utf8')
        current_dataset_name = 'test_file'
        tmpargs = (current_dataset_name, current_dataset.to_dict(), path,
                   create_time, update_time, remarks, file_size)  # 发射信号
        logging.info("导入数据信号已发射")
        self.slot_dataset_reload(*tmpargs)

    def data_import_database_display(self):
        """
        显示"从数据库导入"窗口
        """
        self.import_database = io.ImportDatabase()
        self.import_database.all_dataset = self.__all_dataset
        self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.import_database.show()

    def data_row_filter_display(self):
        """
        显示"数据-行筛选"窗口
        """
        self.data_row_filter_form = preprocess.DataRowFilterForm()
        self.data_row_filter_form.current_dataset = self.__current_dataset
        self.data_row_filter_form.current_dataset_name = self.__current_dataset_name
        self.data_row_filter_form.all_dataset = self.__all_dataset
        self.data_row_filter_form.current_dataset_columns = self.__current_dataset.columns
        self.data_row_filter_form.comboBox_columns.addItems(list(self.__current_dataset.columns))
        for col in self.__current_dataset.columns:
            self.__current_dataset_dtype.add(str(self.__current_dataset.loc[:, col].dtype))
        self.data_row_filter_form.comboBox_dtype.addItems(list(self.__current_dataset_dtype))
        self.data_row_filter_form.dataset_init()  # 初始化预览数据
        self.data_row_filter_form.signal_data_change.connect(self.slot_dataset_reload)
        self.data_row_filter_form.exec_()

    def data_info_display(self):
        """
        显示"数据信息"窗口
        """
        self.data_info = preprocess.DataInfoForm()
        self.data_info.all_dataset = self.__all_dataset
        self.data_info.all_dataset_name = list(self.__all_dataset_name)
        self.data_info.current_dataset_name = self.__current_dataset_name
        self.data_info.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.data_info.lineEdit_path.setText(self.__all_dataset.get(self.__current_dataset_name + ".path"))
        self.data_info.lineEdit_row.setText(self.__all_dataset.get(self.__current_dataset_name + ".row"))
        self.data_info.lineEdit_col.setText(self.__all_dataset.get(self.__current_dataset_name + ".col"))
        self.data_info.lineEdit_file_size.setText(self.__all_dataset.get(self.__current_dataset_name + ".file_size"))
        self.data_info.lineEdit_memory_usage.setText(
            self.__all_dataset.get(self.__current_dataset_name + ".memory_usage"))
        self.data_info.lineEdit_create_time.setText(
            self.__all_dataset.get(self.__current_dataset_name + ".create_time"))
        self.data_info.lineEdit_update_time.setText(
            self.__all_dataset.get(self.__current_dataset_name + ".update_time"))
        self.data_info.info = self.__all_dataset.get(self.__current_dataset_name + ".info")
        self.data_info.info_init()
        self.data_info.exec_()

    def data_filter_display(self):
        """
        显示"数据筛选"窗口
        """
        self.data_filter = preprocess.DataFilterForm()
        self.data_filter.show()

    def data_role_display(self):
        """
        显示"数据-数据角色"窗口
        """
        self.data_role = preprocess.DataRoleForm()
        self.data_role.current_dataset = self.__current_dataset.copy()
        self.data_role.all_dataset = self.__all_dataset
        self.data_role.current_dataset_name = self.__current_dataset_name
        self.data_role.current_dataset_columns = self.__current_dataset.columns
        self.data_role.comboBox_columns.addItems(list(self.__current_dataset.columns))
        self.data_role.signal_data_change.connect(self.slot_dataset_reload)
        self.data_role.dataset_role()  # 初始化预览数据
        self.data_role.exec_()

    def data_merge_vertical_display(self):
        """
        显示"数据-纵向合并"窗口
        """
        self.data_merge_vertical = preprocess.DataMergeVerticalForm()
        self.data_merge_vertical.listWidget_dataset.addItems(list(self.__all_dataset_name))
        self.data_merge_vertical.all_dataset = self.__all_dataset
        self.data_merge_vertical.all_dataset_name = self.__all_dataset_name
        self.data_merge_vertical.listWidget_start.addItem(self.__current_dataset_name)
        self.data_merge_vertical.current_dataset_name = self.__current_dataset_name
        self.data_merge_vertical.signal_data_change.connect(self.slot_dataset_reload)
        self.data_merge_vertical.exec_()

    def data_merge_horizontal_display(self):
        """
        显示"数据-横向合并"窗口
        """
        self.data_merge_horizontal = preprocess.DataMergeHorizontalForm()
        self.data_merge_horizontal.listWidget_dataset.addItems(list(self.__all_dataset_name))
        self.data_merge_horizontal.all_dataset = self.__all_dataset
        self.data_merge_horizontal.all_dataset_name = self.__all_dataset_name
        self.data_merge_horizontal.listWidget_start.addItem(self.__current_dataset_name)
        self.data_merge_vertical.current_dataset_name = self.__current_dataset_name
        self.data_merge_horizontal.signal_data_change.connect(self.slot_dataset_reload)
        self.data_merge_horizontal.exec_()

    def data_partition_display(self):
        """
        显示"数据-数据分区"窗口
        """
        self.data_partition = preprocess.DataPartitionForm()
        # self.data_partition.current_dataset = self.__current_dataset
        # self.data_partition.current_dataset_name = self.__current_dataset_name
        # self.data_partition.lineEdit_dataset_name.setText(self.__current_dataset_name)
        # self.data_partition.signal_data_change.connect(self.slot_dataset_reload)

        self.data_partition.exec_()

    def data_new_column_display(self):
        """
        显示"数据-数据角色"窗口
        """
        self.data_new_column = preprocess.DataNewColumnForm()
        self.data_new_column.show()

    def data_missing_value_display(self):
        """
        显示"数据-缺失值"窗口
        """
        self.data_missing_value = preprocess.DataMissingValueForm()
        self.data_missing_value.current_dataset = self.__current_dataset
        self.data_missing_value.all_dataset = self.__all_dataset
        self.data_missing_value.current_dataset_name = self.__current_dataset_name
        self.data_missing_value.current_dataset_columns = self.__current_dataset.columns
        self.data_missing_value.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_missing_value.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_missing_value.signal_data_change.connect(self.slot_dataset_reload)
        self.data_missing_value.dataset_missing_stat()  # 初始化缺失值统计
        self.data_missing_value.exec_()

    def data_sort_display(self):
        """
        显示"数据-数据角色"窗口
        """
        self.data_sort = preprocess.DataSortForm()
        self.data_sort.show()

    def data_transpose_display(self):
        """
        显示"数据-转置"窗口
        """
        self.data_transpose = preprocess.DataTransposeForm()
        self.data_transpose.current_dataset = self.__current_dataset
        self.data_transpose.current_dataset_name = self.__current_dataset_name
        self.data_transpose.current_dataset_columns = self.__current_dataset.columns
        self.data_transpose.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_transpose.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_transpose.signal_data_change.connect(self.slot_dataset_reload)
        self.data_transpose.exec_()

    def data_standard_display(self):
        """
        显示"数据-标准化"窗口
        """
        self.data_standard = preprocess.DataStandardForm()
        self.data_standard.show()

    def data_column_encode_display(self):
        """
        显示"数据-数据编码"窗口
        """
        self.data_column_encode = preprocess.DataColumnEncodeForm()
        self.data_column_encode.show()

    def data_column_name_display(self):
        """
        显示"数据-列名处理"窗口
        """
        self.data_column_name = preprocess.DataColumnNameForm()
        self.data_column_name.current_dataset = self.__current_dataset
        self.data_column_name.dataset_edit = self.__current_dataset
        self.data_column_name.all_dataset = self.__all_dataset
        self.data_column_name.current_dataset_name = self.__current_dataset_name
        self.data_column_name.current_dataset_columns = self.__current_dataset.columns
        self.data_column_name.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_column_name.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_column_name.comboBox_columns.addItems(list(self.__current_dataset.columns))
        self.data_column_name.signal_data_change.connect(self.slot_dataset_reload)
        self.data_column_name.signal_flush_console.connect(self.slot_flush_console)
        self.data_column_name.dataset_init()  # 初始化预览数据
        self.data_column_name.exec_()

    def data_replace_display(self):
        """
        显示"数据-内容替换"窗口
        """
        self.data_replace = preprocess.DataReplaceForm()
        self.data_replace.current_dataset = self.__current_dataset
        self.data_replace.all_dataset = self.__all_dataset
        self.data_replace.current_dataset_name = self.__current_dataset_name
        self.data_replace.current_dataset_columns = self.__current_dataset.columns
        self.data_replace.comboBox_find_columns.addItems(list(self.__current_dataset.columns))
        self.data_replace.comboBox_replace_columns.addItems(list(self.__current_dataset.columns))
        self.data_replace.signal_data_change.connect(self.slot_dataset_reload)
        self.data_replace.signal_flush_console.connect(self.slot_flush_console)

        self.data_replace.show()

    def data_sample_display(self):
        """
        显示"数据-抽样"窗口
        """
        self.data_simple = preprocess.DataSampleForm()
        self.data_simple.current_dataset = self.__current_dataset
        self.data_simple.dataset_edit = self.__current_dataset
        self.data_simple.current_dataset_name = self.__current_dataset_name
        self.data_simple.current_dataset_columns = self.__current_dataset.columns
        self.data_simple.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.data_simple.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_simple.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_simple.signal_data_change.connect(self.slot_dataset_reload)
        self.data_simple.exec_()

    def data_delete_row_display(self):
        """
        显示"数据-删除行"窗口
        """
        self.data_delete_row = preprocess.DataDeleteRowForm()
        self.data_delete_row.show()

    def data_column_desc_display(self):
        """
        显示"数据-列描述"窗口
        """
        self.data_column_desc = preprocess.DataColumnDescForm()
        self.data_column_desc.current_dataset = self.__current_dataset
        self.data_column_desc.current_dataset_name = self.__current_dataset_name
        self.data_column_desc.all_dataset = self.__all_dataset
        self.data_column_desc.listWidget_var.addItems(self.__current_dataset.columns)
        self.data_column_desc.listWidget_selected.addItem(self.__current_dataset.columns[0])
        self.data_column_desc.listWidget_group.addItem(self.__current_dataset.columns[0])
        self.data_column_desc.signal_data_change.connect(self.slot_dataset_reload)
        self.data_column_desc.exec_()

    def data_delete_col_display(self):
        """
        显示"数据-删除列"窗口
        """
        self.data_delete_column = preprocess.DataDeleteColumnForm()
        self.data_delete_column.show()

    def model_woe_display(self):
        """
        显示"模型-WOE"窗口
        """
        self.model_woe_form = model.ModelWoeForm()
        self.model_woe_form.current_dataset = self.__current_dataset
        self.model_woe_form.all_dataset = self.__all_dataset
        self.model_woe_form.current_dataset_name = self.__current_dataset_name
        self.model_woe_form.current_dataset_columns = self.__current_dataset.columns
        self.model_woe_form.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.model_woe_form.lineEdit_output_path.setText(output_dir)
        self.model_woe_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.model_woe_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        # 自动添加目标变量
        for var in self.__current_dataset.columns:
            if var.lower() in ("y", "target"):
                self.model_woe_form.listWidget_dependent.addItem(var)
            else:
                self.model_woe_form.listWidget_independent.addItem(var)

        # self.model_woe_form.signal_data_change.connect(self.slot_dataset_reload)

        self.model_woe_form.exec_()

    def model_tree_display(self):
        """
        显示"模型-决策树"窗口
        """
        self.model_tree_form = model.ModelTreeForm()
        self.model_tree_form.current_dataset = self.__current_dataset
        self.model_tree_form.current_dataset_columns = self.__current_dataset.columns
        self.model_tree_form.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.model_tree_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        # 自动添加目标变量
        for var in self.__current_dataset.columns:
            if var.lower() in ("y", "target"):
                self.model_tree_form.listWidget_dependent.addItem(var)
            else:
                self.model_woe_form.listWidget_independent.addItem(var)

        self.model_tree_form.signal_result.connect(self.slot_result_reload)  # 重新加载输出结果
        self.model_tree_form.exec_()

    def model_frame_display(self):
        """
        显示"模型-框架"窗口
        """
        self.model_frame = model.ModelFrameForm()
        self.model_frame.show()

    def plot_frame_display(self):
        """
        显示"可视化-框架"窗口
        """
        self.plot_frame = plot.PlotForm()
        self.plot_frame.exec_()

    def stats_base_display(self):
        """
        显示"统计-描述统计"窗口
        """
        self.stats_base = statistics.StatsBaseForm()
        self.stats_base.show()

    def package_manager_display(self):
        self.package_manager = package_manager.PackageManagerForm()
        self.package_manager.show()

    def jupyter_notebook_display(self):
        """
        使用多线程方式打开jupyter-notebook
        :return:
        """
        jupyter_path = os.path.dirname(sys.executable) + r"\Scripts\jupyter-notebook.exe"
        self.th = ThreadJupyter(jupyter_path)
        self.th.finishSignal.connect(self.jupyter_log)
        self.th.start()

    def jupyter_log(self, msg):
        self.slot_flush_console("info", "jupyter", msg)


class NewItemForm(QWidget, New_Ui_Form):
    """
    "新建窗口"
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AboutMeForm(QWidget, AboutMe_Ui_Form):
    """
    打开"关于"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.setLogo()

    def keyPressEvent(self, evt):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if evt.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setLogo(self):
        pix = QPixmap(root_dir + '/ui/source/icons/logo.png')
        self.label_logo.setPixmap(pix)


class OptionForm(QWidget, Option_Ui_Form):
    """
    打开"选项"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        # QssTools.set_qss_to_obj(root_dir + "/ui/source/qss/pyminer.qss", self)

        # 通过combobox控件选择窗口风格
        self.comboBox_theme.activated[str].connect(self.theme_change)

        self.setting = dict()

        self.listWidget.currentRowChanged.connect(self.option_change)
        self.toolButton_workspace.clicked.connect(self.slot_change_workspace)
        self.toolButton_output.clicked.connect(self.slot_change_output)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def option_change(self, i):
        self.stackedWidget.setCurrentIndex(i)

    def theme_change(self, style):
        app.setStyleSheet('')
        if style == 'Fusion':
            app.setStyle('Fusion')
        elif style == 'Qdarkstyle':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        elif style.lower() == 'windowsvista':
            app.setStyle("windowsvista")
        elif style.lower() == 'windows':
            app.setStyle("Windows")

    def slot_change_workspace(self):
        directory = QFileDialog.getExistingDirectory(self, "选择工作区间位置", root_dir)
        self.lineEdit_workspace.setText(directory)

    def slot_change_output(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹位置", root_dir)
        self.lineEdit_output.setText(directory)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('结果')
        self.setGeometry(5, 30, 1355, 730)


class Application(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        QApplication.setStyle('Fusion')

    def _slot_setStyle(self):
        app.setStyleSheet('')
        tmp = self.sender().objectName()[6:]

        if tmp == 'Fusion':
            app.setStyle('Fusion')
        elif tmp == 'Qdarkstyle':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        elif tmp.lower() == 'windowsvista':
            app.setStyle(QStyleFactory.create("windowsvista"))
        elif tmp.lower() == 'windows':
            app.setStyle(QStyleFactory.create("Windows"))


# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = Application(sys.argv)
    app.setWindowIcon(QIcon(root_dir + '/ui/source/icons/logo.png'))
    # 通过QSS样式的方式设置按钮文字
    app.setStyleSheet(TextStyle)

    splash = QSplashScreen(QPixmap(root_dir + '/ui/source/images/splash.png'))
    splash.showMessage("加载pyminer... 0%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()  # 显示启动界面
    qApp.processEvents()  # 处理主进程事件

    myWin = MyMainForm()
    myWin.load_data(splash)

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
