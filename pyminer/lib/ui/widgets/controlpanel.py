import os
import webbrowser

# 也就是widget_right
from PySide2.QtWidgets import QWidget, QSizePolicy, QListWidget, QListWidgetItem, \
    QHBoxLayout, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMenu, QTableWidget, QTableWidgetItem
from PySide2.QtGui import QPixmap, QCursor
from PySide2.QtCore import Qt, QSize
from widgets import PMDockObject
from lib.extensions.extensions_manager.manager import extensions_manager


class ExtInfoWidget(QWidget):
    """
    扩展信息组件,扩展列表中的一项
    """

    def __init__(self, parent, ext, ext_manager):
        """
        parent:父组件
        ext:信息组件对应扩展
        ext_manager:扩展管理器
        """
        super().__init__(parent)
        self.ext = ext
        self.ext_manager = ext_manager
        self.page = parent
        self.init_ui()

    def uninstall(self):
        """卸载操作"""
        self.ext_manager.uninstall(self.ext.info.name)
        self.page.init_extensions()

    def refresh(self):
        """刷新操作"""
        self.ext_manager.refresh(self.ext.info.name)

    def show_menu(self, p):
        """右键菜单"""
        menu = QMenu(self)
        action_info = menu.addAction('卸载')
        action_info.triggered.connect(self.uninstall)
        action_refresh = menu.addAction('刷新')
        action_refresh.triggered.connect(self.refresh)
        menu.exec_(QCursor.pos())

    def info(self):
        """展示扩展信息(扩展商店中的)"""
        url = f'http://py2cn.com/extensions?name={self.ext.info.name}'
        webbrowser.open(url)

    def init_ui(self):
        """初始化ui"""
        self.layout = QHBoxLayout(self)

        # 扩展图标
        img = QLabel(self)
        img_path = os.path.join(self.ext.info.path, self.ext.info.icon)
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaledToHeight(50)
        img.setPixmap(pixmap)
        self.layout.addWidget(img)

        # 扩展名称
        ext_name = QLabel(self)
        ext_name.setText(self.ext.info.display_name)
        self.layout.addWidget(ext_name)

        # 设置菜单模式,关联菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setLayout(self.layout)
        self.show()

    def mouseDoubleClickEvent(self, *args):
        self.info()


class PMPageExt(QWidget, PMDockObject):
    """
    扩展选项卡页
    """

    def __init__(self, main_window):
        """
        main_window:主窗口
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.main_window = main_window
        self.ext_manager = extensions_manager
        self.init_ui()

    # def sizeHint(self) -> QSize:
    #     return QSize(100,300)
    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     self.setMaximumWidth(300)
    #     super().resizeEvent(a0)

    def install(self):
        """安装扩展"""
        path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption='请选择要安装的压缩包',
            directory='C:/',
            filter='所有文件(*.*);;zip文件(*.zip)',
            initialFilter='zip文件(*.zip)'
        )
        self.ext_manager.install(path)
        # 刷新扩展列表
        self.init_extensions()

    def init_extensions(self):
        self.ext_list.clear()  # 先清空
        for ext in self.ext_manager.extensions.values():
            item = QListWidgetItem(self.ext_list, 0)
            item.setSizeHint(QSize(self.ext_list.width() - 20, 50))
            w = ExtInfoWidget(self, ext, self.ext_manager)
            self.ext_list.addItem(item)
            self.ext_list.setItemWidget(item, w)

    def init_ui(self):
        """初始化ui"""
        self.layout = QVBoxLayout(self)

        # 扩展列表
        self.ext_list = QListWidget(self)
        self.init_extensions()
        self.ext_list.show()
        self.layout.addWidget(self.ext_list)

        # 从本地安装按钮
        self.install_btn = QPushButton(self)
        self.install_btn.setText('安装 - 从本地')
        self.install_btn.clicked.connect(self.install)
        self.layout.addWidget(self.install_btn)

        self.setLayout(self.layout)


class PMWorkspaceInspectWidget(QTableWidget):
    def __init__(self, parnet=None):
        super().__init__(parent=None)
        self.setRowCount(4)
        self.setColumnCount(10)
        for i, name in enumerate(['名称', '类型', '大小', '值']):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(name))
            # self.setCellWidget()
        # self.setItem(0,0,QTableWidgetItem('123123123'))

    def set_data_view(self):
        pass


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    sa = PMWorkspaceInspectWidget()
    sa.show()
    sys.exit(app.exec_())
