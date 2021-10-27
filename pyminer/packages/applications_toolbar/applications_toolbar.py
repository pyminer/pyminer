import json
import os
from typing import TYPE_CHECKING, Callable, Dict
from PySide2.QtCore import QSize, Qt, Signal
from PySide2.QtGui import QPixmap, QContextMenuEvent
from PySide2.QtWidgets import QHBoxLayout, QWidget, QSpacerItem, QToolButton, QSizePolicy, QFrame, \
    QListWidget, QListWidgetItem, QAction, QMenu, QApplication, QMessageBox, QFileDialog
from widgets import PMGToolBar, create_icon, QIcon, QDialog, QVBoxLayout, PMGPanelDialog, open_file_manager, \
    assert_not_in, assert_in
from utils import unzip_file, make_zip
from lib.main_window import base
from .manage_apps import APPManager, ToolAppDesc
from .dev_tools import DevelopTools

if TYPE_CHECKING:
    from lib.extensions.extensionlib import extension_lib


class ApplicationsList(QListWidget):
    """
    应用列表
    """
    signal_start_app = Signal(str)
    signal_show_help = Signal(str)
    signal_open_as_work_dir = Signal(str)
    signal_open_in_explorer = Signal(str)

    def __init__(self, apps: Dict[str, ToolAppDesc]):
        super(ApplicationsList, self).__init__()
        self.items_dict = {}
        self.ROLE_NAME = 5
        for name, app in apps.items():
            item = QListWidgetItem()
            item.setData(self.ROLE_NAME, name)
            item.setText(app.text)
            item.setIcon(create_icon(app.icon_path))
            self.addItem(item)
        self.itemDoubleClicked.connect(self.item_double_clicked)

    def contextMenuEvent(self, evt: 'QContextMenuEvent'):
        """

        Args:
            evt:

        Returns:

        """
        current_item = self.currentItem()
        if current_item is not None:
            menu = QMenu()
            action_open_in_explorer = menu.addAction(self.tr('Open In Explorer'))
            action_open_in_explorer.triggered.connect(
                lambda: self.signal_open_in_explorer.emit(self.currentItem().data(self.ROLE_NAME)))

            action_open_as_work_dir = menu.addAction(self.tr('Open Folder As Work Dir'))
            action_open_as_work_dir.triggered.connect(
                lambda: self.signal_open_as_work_dir.emit(self.currentItem().data(self.ROLE_NAME)))

            action_open_help = menu.addAction(self.tr('Plugin Introduction'))
            action_open_help.triggered.connect(
                lambda: self.signal_show_help.emit(self.currentItem().data(self.ROLE_NAME))
            )
            menu.exec_(evt.globalPos())

    def item_double_clicked(self, item: QListWidgetItem):
        """

        Args:
            item:

        Returns:

        """
        self.signal_start_app.emit(item.data(self.ROLE_NAME))


class PMMenuToolPanel(QFrame):
    """
    面板控件，用于放置绘图按钮或其他插件按钮
    """
    signal_start_app = Signal(str)
    signal_show_help = Signal(str)
    signal_open_as_work_dir = Signal(str)
    signal_open_in_explorer = Signal(str)

    def __init__(self):
        super(PMMenuToolPanel, self).__init__()
        self.setup_ui()
        self.buttons: Dict[str, QToolButton] = {}
        self.btn_down.clicked.connect(self.show_all_apps)

    def setup_ui(self):
        """
        初始化界面
        Returns:

        """
        self.setMinimumSize(QSize(500, 85))
        self.setMaximumSize(QSize(16777215, 85))
        self.setObjectName("frame")
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        self.widget_panel = QWidget()
        self.widget_panel.setStyleSheet("margin:1px;")
        self.widget_panel_hbox = QHBoxLayout()
        self.widget_panel_hbox.setContentsMargins(0, 0, 0, 0)
        self.widget_panel_hbox.setSpacing(10)
        self.widget_panel.setLayout(self.widget_panel_hbox)

        self.hspace = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_down = QToolButton()
        self.btn_down.setObjectName("btn_tool_select")
        self.btn_down.setToolTip("查看更多")
        self.btn_down.setMinimumSize(QSize(25, 85))
        self.btn_down.setMaximumSize(QSize(25, 85))
        self.btn_down.setStyleSheet("""#btn_tool_select{
            border:1px solid rgb(189,189,189);
            border-top-left-radius:0px;
            border-top-right-radius:5px;
            border-bottom-left-radius:0px;
            border-bottom-right-radius:5px;
            background-color: rgb(230,230,230);
            padding:0px 0px 0px 0px;}
            #btn_tool_select:hover{background:lightgray;}
            """)

        current_path = os.path.dirname(__file__)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(os.path.join(current_path, 'source/down.svg')), QIcon.Normal,
                        QIcon.Off)
        self.btn_down.setIcon(icon1)

        self.btn_down.setAutoRaise(True)

        # 添加按钮和弹簧到水平布局
        self.hbox.addWidget(self.widget_panel)
        self.hbox.addItem(self.hspace)
        self.hbox.addWidget(self.btn_down)
        self.setLayout(self.hbox)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)
        self.setStyleSheet(
            "#frame{border:1px solid rgb(189,189,189);padding: -5px -10px 0px 20px;margin: 0px 0px 0px 0px;border-radius:5px;}")

        self.btn_down.clicked.connect(self.close)

    def add_button(self, name, btn_text: str, icon_path: str, btn_action: Callable = None) -> QToolButton:
        """
        添加一个按钮
        Args:
            name: 按钮名称（唯一，一般与应用名称相同）
            btn_text: 按钮的文字
            icon_path: 图标路径
            btn_action: 点击按钮触发的函数（只是以回调的形式方便写代码，实现还是靠信号。）

        Returns:

        """
        sub_widget = QToolButton()
        assert_not_in(name, self.buttons.keys())
        self.buttons[name] = sub_widget
        icon = QIcon()
        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        sub_widget.setIcon(icon)
        sub_widget.setIconSize(QSize(50, 40))
        sub_widget.setMinimumSize(QSize(85, 75))
        sub_widget.setMaximumSize(QSize(85, 75))
        sub_widget.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        sub_widget.setAutoRaise(True)
        sub_widget.setText(btn_text)
        self.widget_panel_hbox.addWidget(sub_widget)
        if btn_action is not None:
            sub_widget.clicked.connect(btn_action)
        sub_widget.clicked.connect(lambda: self.signal_start_app.emit(name))
        return sub_widget

    def remove_button(self, name):
        """
        移除应用按钮。
        Args:
            name:

        Returns:

        """
        self.buttons.pop(name).deleteLater()

    def clear_buttons(self):
        """
        移除全部应用按钮
        Returns:

        """
        keys_list = list(self.buttons.keys())
        for button_name in keys_list:
            self.remove_button(button_name)

    def show_all_apps(self):
        """

        Returns:

        """
        dlg = QDialog()
        dlg.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Popup)  # 无边框、弹出式
        dlg.setLayout(QVBoxLayout())
        al = ApplicationsList(APPManager.get_instance().apps)
        dlg.layout().addWidget(al)
        al.signal_start_app.connect(self.signal_start_app.emit)
        al.signal_open_as_work_dir.connect(self.signal_open_as_work_dir.emit)
        al.signal_open_in_explorer.connect(self.signal_open_in_explorer.emit)
        al.signal_show_help.connect(self.signal_show_help.emit)
        al.signal_start_app.connect(dlg.close)
        dlg.exec_()


class PMApplicationsToolBar(PMGToolBar):
    """
    应用工具栏
    """
    app_item_double_clicked_signal: 'Signal' = Signal(str)
    extension_lib: 'extension_lib' = None
    variable = None
    widgets = {}
    console_tab_widget = None

    def __init__(self):
        super(PMApplicationsToolBar, self).__init__()

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        src_path = os.path.join(os.path.dirname(__file__), 'source')
        self.open_qtdesigner_button = \
            self.add_tool_button('open_qtdesigner_button', self.tr('Designer'),
                                 icon=create_icon(os.path.join(src_path, 'qt-logo.png')))
        self.packup_app_button = \
            self.add_tool_button('packup_app_button', self.tr('Develop'),
                                 icon=create_icon(os.path.join(src_path, 'package.svg')))

        self.publish_app_button = \
            self.add_tool_button('publish_app_button', self.tr('Distribute'),
                                 icon=create_icon(os.path.join(src_path, 'install.svg')))
        self.get_app_button = \
            self.add_tool_button('install_app_button', self.tr('Market'),
                                 icon=create_icon(os.path.join(src_path, 'appstore.svg')))
        self.get_app_button.setEnabled(False)
        self.manage_app_button = \
            self.add_tool_button('manage_app_button', self.tr('Manage Apps'),
                                 icon=create_icon(os.path.join(src_path, 'settings.png')))
        self.append_menu('manage_app_button', self.tr('Apps Settings'), self.show_settings_panel)
        self.append_menu('manage_app_button', self.tr('Refresh Apps'), self.refresh_apps)
        self.append_menu('manage_app_button', self.tr('Install App'), self.install_app)
        self.append_menu('manage_app_button', self.tr('Packup App'), self.packup_app)
        # self.manage_app_button.clicked.connect(self.show_settings_panel)
        self.addSeparator()

        self.show_apps_button_bar = PMMenuToolPanel()  # 设置工具条按钮组合
        self.addWidget(self.show_apps_button_bar)

        self.dev_tools = DevelopTools()

    def install_app(self):
        """
        将app安装到自己选定的安装路径之一。
        Returns:

        """
        work_dir = self.extension_lib.Program.get_work_dir()
        app_paths = APPManager.get_instance().get_app_paths()
        path_index = 1 if len(app_paths) > 1 else 0
        dlg = PMGPanelDialog(parent=self, views=[])
        views = [
            ('file_ctrl', 'pack_path', self.tr('Pack Path(*.zip)'), '', 'ZIP(*.zip)', work_dir),
            ('combo_ctrl', 'install_path', self.tr('Install Path'), app_paths[path_index], app_paths)
        ]
        dlg.panel.set_items(views)
        ret = dlg.exec_()
        if ret == QDialog.Accepted:
            values = dlg.get_value()
            pack_path = values['pack_path']
            install_path = values['install_path']
            if os.path.exists(pack_path):
                if os.path.exists(install_path):
                    unzip_file(pack_path, install_path)
                    QMessageBox.information(self, self.tr('Information'), self.tr('Installing Succeeded!'))
                    self.refresh_apps()
                else:
                    QMessageBox.warning(self, self.tr('Warning'), self.tr('Install path %s not exist!') % install_path)
            else:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Package %s not exist!') % pack_path)

    def packup_app(self):
        """
        将当前工作路径下的应用进行打包
        Returns:

        """
        work_dir = self.extension_lib.Program.get_work_dir()
        dev_path = QFileDialog.getExistingDirectory(self, self.tr('Select Packup App Developing Folder'),
                                                    directory=work_dir)

        if not os.path.exists(dev_path):
            QMessageBox.warning(self, self.tr('Warning'), self.tr('App Developing Folder %s not exist!') % dev_path)

        json_path = os.path.join(dev_path, 'package.json')
        if not os.path.exists(json_path):
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('App description json file package.json is not found in path %s') % (dev_path))
            return
        try:
            with open(json_path, 'rb') as f:
                d = json.load(f)
        except json.JSONDecodeError:
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('Json decoding error occured when parsing APP json file %s' % json_path))

        dist_pack_path, _ = QFileDialog.getSaveFileName(self, self.tr('Distribute As..'),
                                                        directory=os.path.join(work_dir, '%s.pmapp.zip' % d['name']),
                                                        filter='ZIP File(*.zip)')

        make_zip(dev_path, dist_pack_path, root=d['name'])
        QMessageBox.information(self, self.tr('Information'), self.tr('Packup succeeded!'))

    def refresh_apps(self):
        """

        Returns:

        """
        APPManager.get_instance().load_tool_apps()
        self.show_apps_button_bar.clear_buttons()
        for k, app in APPManager.get_instance().apps.items():
            self.add_tool_app(app)

    def init_apps(self):
        """
        初始化应用工具栏
        Returns:

        """
        app_manager = APPManager().get_instance()
        app_manager.load_tool_apps()
        for k, app in app_manager.apps.items():
            self.add_tool_app(app)


    def show_settings_panel(self):
        """

        Returns:

        """
        paths = APPManager.get_instance().get_app_external_paths()
        views = [{'type': 'list_ctrl',
                  'name': 'app_paths',
                  'title': self.tr('App Paths'),
                  'init': [[None] * len(paths), paths]
                  }]

        dlg = PMGPanelDialog(self, views)
        dlg.exec_()
        APPManager.get_instance().set_app_external_paths(dlg.get_value()['app_paths'][1])

    def show_app_help(self, app_name):
        """

        Args:
            app_name:

        Returns:

        """
        app = APPManager.get_instance().get_app(app_name)
        path = app.readme_file
        if os.path.exists(path):
            self.extension_lib.get_interface("code_editor").open_script(path)
        else:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('File not found,path:%s') % path)

    def start_app(self, app_name: str):
        """

        Args:
            app_name:

        Returns:

        """
        app = APPManager.get_instance().get_app(app_name)
        self.console_tab_widget.create_process(app.text, app.get_args())
        self.extension_lib.UI.raise_dock_into_view('process_console_tab')

    def get_toolbar_text(self) -> str:
        """

        Returns:

        """
        return self.tr('Applications')

    def insert_after(self) -> str:
        """

        Returns:

        """
        return 'drawings_toolbar'

    def on_close(self):
        """

        Returns:

        """
        APPManager.get_instance().save_settings()
        self.hide()
        self.deleteLater()

    def main_appstore_dispaly(self):
        """
        显示"应用商店"窗口
        """
        self.appstore = base.AppstoreForm()
        self.appstore.show()

    def open_in_designer(self, path: str):
        """
        在Qt设计师中打开
        Args:
            path:

        Returns:

        """
        self.dev_tools.open_in_designer(path)

    def open_in_linguist(self, path: str):
        """
        在语言家中打开
        Args:
            path:

        Returns:

        """
        self.dev_tools.open_in_linguist(path)

    def bind_events(self):
        """
        绑定事件。这个将在界面加载完成之后被调用。
        """
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)
        self.open_qtdesigner_button.clicked.connect(self.open_designer)
        self.dev_tools.extension_lib = self.extension_lib

        menu_open_wizard = self.append_menu('packup_app_button', self.tr('New Project'),
                                            self.dev_tools.open_app_wizard)
        menu_open_wizard.setToolTip(self.tr('New Project'))
        self.append_menu('packup_app_button', self.tr('Open Translator'), self.dev_tools.open_translator)
        menu = self.append_qmenu('packup_app_button', self.tr('Translations'))
        action_show_update_translation_panel: QAction = menu.addAction(self.tr('Update..'))
        action_show_update_translation_panel.triggered.connect(self.dev_tools.show_update_panel)
        action_update_translation_by_sourcecode = menu.addAction(self.tr('Update by Source Code'))
        action_update_translation_by_sourcecode.triggered.connect(lambda: self.dev_tools.run_pylupdate())

        self.append_menu('packup_app_button', self.tr('Run PyUIC'), self.dev_tools.run_pyuic)
        self.append_menu('packup_app_button', self.tr('Run PyRCC'), self.dev_tools.run_pyrcc)

        self.publish_app_button.clicked.connect(self.open_app_publish)
        self.get_app_button.clicked.connect(self.open_app_store)

        self.show_apps_button_bar.signal_start_app.connect(self.start_app)
        self.show_apps_button_bar.signal_show_help.connect(self.show_app_help)
        self.show_apps_button_bar.signal_open_as_work_dir.connect(self.open_app_as_work_dir)
        self.init_apps()

    def open_app_dir_in_explorer(self, app_name: str):
        """

        Args:
            app_name:

        Returns:

        """
        app_path = APPManager.get_instance().get_app_install_path(app_name)

        open_file_manager(app_path)

    def open_app_as_work_dir(self, app_name: str):
        """

        Args:
            app_name:

        Returns:

        """
        app_path = APPManager.get_instance().get_app_install_path(app_name)
        self.extension_lib.Program.set_work_dir(app_path)

    def open_app_publish(self):
        """
        应用发布的计划，暂时打成zip包。
        Returns:

        """
        self.packup_app()

    def open_app_store(self):
        """

        Returns:

        """
        print("你点击了应用商店")

    def open_designer(self):
        """
        打开qtDesigner进行ui编辑，要求有qt5_applications包
        Returns:

        """
        self.dev_tools.open_designer()

    def refresh_outer_buttons(self):
        """
        刷新显示在按纽条上面的按钮们。
        首先全部移除，然后添加进来。
        这些按钮不是由用户控制添加的，而是自动的呈现listwidget的前最多10项。
        """
        return

    def add_tool_app(self, app: 'ToolAppDesc') -> QToolButton:
        """
        添加一个工具应用
        Args:
            app:

        Returns:

        """

        return self.show_apps_button_bar.add_button(app.name, app.text, app.icon_path)


if __name__ == '__main__':
    test_app = QApplication([])
    alist = ApplicationsList()
    alist.show()
    test_app.exec_()
