import os
import shutil
import sys

sys.argv.append('--remote-debugging-port=10086')
from time import time
import json
import qdarkstyle
import qdarkstyle.style_rc  # 导入pdarkstyle资源文件
from PySide2 import QtCore
from PySide2.QtCore import Qt, QPoint, QUrl, Signal, QTimer, QEventLoop
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot

strategy_path = os.path.join(os.getcwd(), 'strategy')  # 用于存放编辑文件的文件夹
editor_path = os.path.join(os.path.dirname(__file__), 'quant', 'python_editor', 'editor.htm')


class WebEngineView(QWebEngineView):
    customSignal = Signal(str, str)
    saveSignal = Signal()
    signal_open_file = Signal(str, str)
    signal_request_text = Signal()
    signal_text_got = Signal(str)
    signal_save_as = Signal(str)
    signal_set_autocomplete_apis = Signal(str)

    def __init__(self, *args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        self._untitled_id = 0
        self.initSettings()
        self.channel = QWebChannel(self)
        # 把自身对象传递进去
        self.channel.registerObject('Bridge', self)
        # 设置交互接口
        self.page().setWebChannel(self.channel)

        # self.signal_set_autocomplete_apis.emit({"keywords": ["aaaaa", "bbbbbb"]})

    @Slot(str, str)
    def on_text_received(self, path, text):
        print(text)
        self.signal_text_got.emit(text)

    # 注意pyqtSlot用于把该函数暴露给js可以调用
    @Slot(str)
    def print_from_js(self, text):
        print('print from js', text)

    @Slot(str, str)
    def callFromJs(self, file, text):
        print('call from js!')
        try:
            with open(file, mode='w', encoding='utf-8') as f:
                f.write(text.replace('\r', ''))
                f.close()
        except Exception as e:
            print(e)

    @Slot(str, str)
    def on_save(self, file_name: str, text: str):
        if os.path.isabs(file_name):
            pass
        else:
            file_name, ext = QFileDialog.getSaveFileName(self, "aaa", "/home/hzy/Desktop", "All Files(*)")
        print(file_name, text)
        with open(file_name, 'w') as f:
            f.write(text)
        self.signal_save_as.emit(file_name)

    def open_file(self, file: str):
        """
        打开文件
        Args:
            file:

        Returns:

        """
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        self.signal_open_file.emit(file, text)

    def new_file(self):
        self._untitled_id += 1
        self.signal_open_file.emit("Untitled-%d.py" % self._untitled_id, "")

    def sendCustomSignal(self, file):
        # 发送自定义信号
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        self.customSignal.emit(file, text)

    def sendSaveSignal(self):
        self.saveSignal.emit()

    # @Slot(str)
    # @Slot(QUrl)
    def load(self, url):
        '''
        eg: load("https://PySide2.com")
        :param url: 网址
        '''
        return super(WebEngineView, self).load(QUrl(url))

    def initSettings(self):
        '''
        eg: 初始化设置
        '''
        # 获取浏览器默认设置
        settings = QWebEngineSettings.globalSettings()
        # 设置默认编码utf8
        settings.setDefaultTextEncoding("utf-8")
        # 自动加载图片,默认开启
        # settings.setAttribute(QWebEngineSettings.AutoLoadImages,True)
        # 自动加载图标,默认开启
        # settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage,True)
        # 开启js,默认开启
        # settings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
        # js可以访问剪贴板
        settings.setAttribute(
            QWebEngineSettings.JavascriptCanAccessClipboard, True)
        # js可以打开窗口,默认开启
        # settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,True)
        # 链接获取焦点时的状态,默认开启
        # settings.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain,True)
        # 本地储存,默认开启
        # settings.setAttribute(QWebEngineSettings.LocalStorageEnabled,True)
        # 本地访问远程
        settings.setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        # 本地加载,默认开启
        # settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls,True)
        # 监控负载要求跨站点脚本,默认关闭
        # settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled,False)
        # 空间导航特性,默认关闭
        # settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled,False)
        # 支持平超链接属性,默认关闭
        # settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled,False)
        # 使用滚动动画,默认关闭
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        # 支持错误页面,默认启用
        # settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        # 支持插件,默认关闭
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # 支持全屏应用程序,默认关闭
        settings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True)
        # 支持屏幕截屏,默认关闭
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        # 支持html5 WebGl,默认开启
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        # 支持2d绘制,默认开启
        settings.setAttribute(
            QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        # 支持图标触摸,默认关闭
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)


class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QGridLayout()  # 上方布局
        self.bottomLayout = QGridLayout()  # 下方布局
        self.create_stragety_vbox()
        self.create_content_vbox()
        self.mainLayout = QGridLayout()  # 主布局为垂直布局
        self.mainLayout.setSpacing(5)  # 主布局添加补白

        self.mainLayout.addWidget(self.strategy_vbox, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.content_vbox, 0, 1, 1, 1)

        self.mainLayout.setColumnStretch(0, 2)
        self.mainLayout.setColumnStretch(1, 6)

        self.setLayout(self.mainLayout)
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle('编辑器')
        self.show()

        # 策略信息
        self.strategy_path = None

        with open(r'qdark.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def create_stragety_vbox(self):
        # 策略树
        self.strategy_vbox = QGroupBox('策略')
        self.strategy_layout = QHBoxLayout()
        self.strategy_tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())
        self.strategy_tree.setModel(self.model)
        self.strategy_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.strategy_tree.setRootIndex(self.model.index(r'/home/hzy/Desktop'))
        # self.strategy_tree.setColumnCount(1)
        # self.strategy_tree.setHeaderLabels(['策略'])
        self.strategy_tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.model.setReadOnly(False)
        self.strategy_tree.setHeaderHidden(True)
        self.strategy_tree.hideColumn(1)
        self.strategy_tree.hideColumn(2)
        self.strategy_tree.hideColumn(3)

        self.strategy_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.strategy_tree.customContextMenuRequested[QPoint].connect(self.strategy_tree_right_menu)

        # for d in os.listdir(strategy_path):
        #     root = QTreeWidgetItem(self.strategy_tree)
        #     root.setText(0, d)
        #     for file in os.listdir(os.path.join(strategy_path, d)):
        #         child = QTreeWidgetItem(root)
        #         child.setText(0, file)
        # self.list_strategy(strategy_path, self.strategy_tree)
        self.strategy_tree.doubleClicked.connect(self.strategy_tree_clicked)
        self.strategy_layout.addWidget(self.strategy_tree)
        self.strategy_vbox.setLayout(self.strategy_layout)

    # 策略右键菜单
    def strategy_tree_right_menu(self, point):
        self.strategy_tree.popMenu = QMenu()
        self.strategy_tree.addType = QMenu(self.strategy_tree.popMenu)
        self.strategy_tree.addType.setTitle('新建')
        rename = QAction('重命名', self.strategy_tree)
        delete = QAction('删除', self.strategy_tree)
        add_strategy = QAction('新建策略')
        add_group = QAction('新建分组')
        refresh = QAction('刷新', self.strategy_tree)
        self.strategy_tree.popMenu.addMenu(self.strategy_tree.addType)
        self.strategy_tree.addType.addAction(add_strategy)
        self.strategy_tree.addType.addAction(add_group)
        self.strategy_tree.popMenu.addAction(rename)
        self.strategy_tree.popMenu.addAction(delete)
        self.strategy_tree.popMenu.addAction(refresh)

        # 右键动作
        action = self.strategy_tree.popMenu.exec_(self.strategy_tree.mapToGlobal(point))
        if action == add_strategy:
            index = self.strategy_tree.currentIndex()
            model = index.model()  # 请注意这里可以获得model的对象
            item_path = model.filePath(index)
            if item_path and os.path.isdir(item_path):
                value = ''
                while True:
                    value, ok = QInputDialog.getText(self, '新建文件', '策略名称', QLineEdit.Normal)
                    path = os.path.join(item_path, value + '.py')
                    if os.path.exists(path) and ok:
                        QMessageBox.warning(self, '提示', '策略名在选择的分组%s已经存在！！！' % value, QMessageBox.Yes)
                    elif not ok:
                        break
                    else:
                        with open(path, 'w', encoding='utf-8') as w:
                            pass
                        break
            elif not os.path.isdir(item_path):
                value = ''
                while True:
                    value, ok = QInputDialog.getText(self, '新建文件', '策略名称', QLineEdit.Normal)
                    path = os.path.join(os.path.split(item_path)[1], value + '.py')
                    if os.path.exists(path) and ok:
                        QMessageBox.warning(self, '提示', '策略名在选择的分组%s已经存在！！！' % value, QMessageBox.Yes)
                    elif not ok:
                        break
                    else:
                        with open(path, 'w', encoding='utf-8') as w:
                            pass
                        break
            else:
                QMessageBox.warning(self, '提示', '请选择分组！！！', QMessageBox.Yes)

        elif action == add_group:
            value = ''
            flag = self.strategy_tree.indexAt(point)  # 判断鼠标点击位置标志位
            while True:
                if not flag.isValid():  # 鼠标点击位置不在目录树叶子上
                    item_path = strategy_path  # 新建文件夹位置在根目录
                else:
                    index = self.strategy_tree.currentIndex()
                    model = index.model()  # 请注意这里可以获得model的对象
                    item_path = model.filePath(index)
                value, ok = QInputDialog.getText(self, '新建文件夹', '分组名称', QLineEdit.Normal, value)
                if os.path.isdir(item_path):
                    path = os.path.join(item_path, value)
                else:
                    path = os.path.join(os.path.split(item_path)[0], value)
                if os.path.exists(path) and ok:
                    QMessageBox.warning(self, '提示', '分组%s已经存在！！！' % value, QMessageBox.Yes)
                elif not ok:
                    break
                else:
                    os.mkdir(path)
                    break

        elif action == refresh:
            index = self.strategy_tree.currentIndex()
            model = index.model()  # 请注意这里可以获得model的对象
            model.dataChanged.emit(index, index)
        elif action == rename:
            index = self.strategy_tree.currentIndex()
            model = index.model()  # 请注意这里可以获得model的对象
            item_path = model.filePath(index)
            if not os.path.isdir(item_path):  # 修改策略名
                value = ''
                (file_path, filename) = os.path.split(item_path)
                while True:
                    value, ok = QInputDialog.getText(self, '修改%s策略名' % filename, '策略名称', QLineEdit.Normal, value)
                    new_path = os.path.join(file_path, value + '.py')
                    if os.path.exists(new_path) and ok:
                        QMessageBox.warning(self, '提示', '策略名在此分组中%s已经存在！！！' % value, QMessageBox.Yes)
                    elif not ok:
                        break
                    else:
                        os.rename(item_path, new_path)
                        break
            else:
                value = ''
                (dir_path, dir_name) = os.path.split(item_path)
                while True:
                    value, ok = QInputDialog.getText(self, '修改%s文件夹' % dir_name, '分组名称', QLineEdit.Normal, value)
                    new_path = os.path.join(dir_path, value)
                    if os.path.exists(new_path) and ok:
                        QMessageBox.warning(self, '提示', '分组%s已经存在！！！' % value, QMessageBox.Yes)
                    elif not ok:
                        break
                    else:
                        os.rename(item_path, new_path)
                        break
        elif action == delete:
            index = self.strategy_tree.currentIndex()
            model = index.model()  # 请注意这里可以获得model的对象
            item_path = model.filePath(index)
            if item_path and os.path.isdir(item_path):
                reply = QMessageBox.question(self, '提示', '确定删除分组及目录下的所有文件吗？', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    shutil.rmtree(item_path)
            elif item_path and not os.path.isdir(item_path):
                reply = QMessageBox.question(self, '提示', '确定删除文件%s吗？' % item_path, QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    os.remove(item_path)
            else:
                pass
        else:
            pass

    def create_content_vbox(self):
        self.content_vbox = QGroupBox('内容')
        self.content_layout = QGridLayout()
        self.save_btn = QPushButton('保存')
        self.run_btn = QPushButton('运行')
        self.update_api = QPushButton('更新api')
        self.refresh_btn = QPushButton('重新加载')
        self.new_btn = QPushButton('新建')
        self.refresh_btn.clicked.connect(
            lambda: self.contentEdit.load(QUrl.fromLocalFile(os.path.abspath(editor_path))))
        self.contentEdit = WebEngineView()
        self.contentEdit.load(QUrl.fromLocalFile(os.path.abspath(editor_path)))
        self.save_btn.setMaximumSize(80, 60)
        self.run_btn.setMaximumSize(80, 60)
        self.content_layout.addWidget(self.run_btn, 0, 1, 1, 1)
        self.content_layout.addWidget(self.save_btn, 0, 2, 1, 1)
        self.content_layout.addWidget(self.refresh_btn, 0, 3, 1, 1)
        self.content_layout.addWidget(self.new_btn, 0, 4, 1, 1)
        self.content_layout.addWidget(self.update_api, 0, 5, 1, 1)
        self.content_layout.addWidget(self.contentEdit, 2, 0, 1, 5)
        self.content_vbox.setLayout(self.content_layout)
        self.save_btn.clicked.connect(self.emit_custom_signal)
        self.new_btn.clicked.connect(lambda: self.contentEdit.new_file())
        self.update_api.clicked.connect(
            lambda: self.contentEdit.signal_set_autocomplete_apis.emit(
                json.dumps({"python": {"keywords": {"mode": "add", "content": ["import", "def", "class"]}}})))

    def emit_custom_signal(self):
        self.contentEdit.sendSaveSignal()

    def strategy_tree_clicked(self):
        # 策略双击槽函数
        index = self.strategy_tree.currentIndex()
        model = index.model()  # 请注意这里可以获得model的对象
        item_path = model.filePath(index)
        if not os.path.isdir(item_path):
            self.contentEdit.open_file(item_path)  # sendCustomSignal(item_path)
            self.strategy_path = item_path

    def get_text(self) -> str:
        """
        获取文本内容
        :return:
        """
        self.contentEdit.signal_request_text.emit()
        self.loop = QEventLoop()
        _text = ''

        def f(text):
            self.loop.quit()
            _text = text

        self.contentEdit.signal_text_got.connect(f)
        self.loop.exec_()
        return _text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Editor()
    form.show()
    timer = QTimer()
    timer.start(1000)
    # timer.timeout.connect(lambda: print(form.get_text()))
    sys.exit(app.exec_())
