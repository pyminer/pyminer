import json
import logging
import os
import platform
import shutil
import subprocess
import sys
from typing import List

from PySide2.QtCore import QObject
from PySide2.QtWidgets import QWizard, QMessageBox, QFileDialog

from packages.applications_toolbar.ui.app_designer import Ui_Wizard
from widgets import PMGPanelDialog
from utils import get_python_modules_directory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DevelopTools(QObject):
    extension_lib = None

    def __init__(self, parent=None):
        super(DevelopTools, self).__init__()
        self.parent_widget = parent
        if platform.system().lower() == 'windows':
            if os.path.exists(os.path.join(get_python_modules_directory(), 'qt5_applications')):
                dir = os.path.join(get_python_modules_directory(), 'qt5_applications', 'Qt', 'bin')
                self.designer_path = os.path.join(dir, 'designer.exe').replace('/', '\\')
                self.linguist_path = os.path.join(dir, 'linguist.exe').replace('/', '\\')
                self.lupdate_command = '%s -m PyQt5.pylupdate_main -noobsolete' % sys.executable
                self.uic_command = '%s -m PyQt5.uic.pyuic -x' % sys.executable
                self.rcc_command = '%s -m PyQt5.pyrcc_main' % sys.executable

            elif os.path.exists(os.path.join(get_python_modules_directory(), 'PySide2')):

                try:
                    from PySide2.scripts.pyside_tool import uic, rcc, designer
                except:
                    pass
                dir = os.path.join(get_python_modules_directory(), 'PySide2')
                self.designer_path = os.path.join(dir, 'designer.exe').replace('/', '\\')
                self.linguist_path = os.path.join(dir, 'linguist.exe').replace('/', '\\')
                self.lupdate_command = '%s ' % os.path.join(dir, 'pyside2-lupdate.exe').replace('/', '\\')
                self.uic_command = '%s -g python ' % os.path.join(dir, 'uic.exe')
                self.rcc_command = '%s -g python' % os.path.join(dir, 'rcc.exe')
            else:
                pass
        else:
            dir = os.path.join(get_python_modules_directory(), 'qt5_applications', 'Qt', 'bin')
            self.designer_path = os.path.join(dir, 'designer')
            self.linguist_path = os.path.join(dir, 'linguist')

    def open_designer(self):
        import subprocess
        self.workdir = self.extension_lib.Program.get_work_dir()
        if self.check_installed(self.designer_path):
            subprocess.Popen(self.designer_path, cwd=self.workdir)

    def open_translator(self):
        """
        打开翻译软件
        Returns:

        """
        if self.check_installed(self.linguist_path):
            print(self.linguist_path, type(self.linguist_path))
            subprocess.Popen(self.linguist_path)

    def open_app_wizard(self):
        self.wizard = app_designer_wizard()
        self.wizard.extension_lib = self.extension_lib
        print(self.extension_lib)
        self.wizard.show()

    def open_in_designer(self, file_path: str):
        """
        打开qtDesigner进行ui编辑
        要求有qt5_applications包
        Returns:

        """
        import subprocess
        import platform
        if platform.system() == "Windows":
            if os.path.exists(self.designer_path):
                subprocess.Popen([self.designer_path, file_path],
                                 cwd=self.extension_lib.Program.get_work_dir())  # 打开中文版designer。
            else:
                raise FileNotFoundError('Designer not found in path %s' % self.designer_path)

        else:
            subprocess.Popen(['designer'])

    def open_in_linguist(self, file_path: str):
        """
        打开qtDesigner进行ui编辑
        要求有qt5_applications包
        Returns:

        """
        import subprocess
        import platform
        if platform.system() == "Windows":
            subprocess.Popen([self.linguist_path, file_path],
                             cwd=self.extension_lib.Program.get_work_dir())  # 打开中文版designer。
        else:
            raise NotImplementedError('Not implemented on this platform!')

    def check_installed(self, tool_path: str) -> bool:
        """
        检查designer和linguist是否已经安装。
        Args:
            tool_path:str,期望工具所在的路径
        Returns:

        """

        if platform.system().lower() in ['windows', 'linux']:
            if os.path.exists(tool_path):
                return True
            else:
                error_msg = self.tr(
                    'Cannot find Qt designer at %s.\n'
                    'Please make sure that \'qt5_applications\' package is installed!') % tool_path
        else:
            error_msg = self.tr('This Tool implementation is not supported yet on this platform.')
        QMessageBox.warning(self, self.tr('Warning'), error_msg)
        return False

    def run_pyuic(self):
        """
        运行pyuic,只要有PySide2包即可
        Returns:

        """
        ret = self.show_covered_message('.ui', '.py')
        if ret == QMessageBox.Ok:
            work_dir = self.extension_lib.Program.get_work_dir()
            ui_files = self.list_files(work_dir, '.ui')
            for ui_file_path in ui_files:
                try:
                    pyname = os.path.splitext(os.path.basename(ui_file_path))[0] + '.py'
                    pypath = os.path.join(os.path.dirname(ui_file_path), pyname)

                    os.system(
                        self.uic_command + ' \"%s\" ' % ui_file_path + ' -o ' + ' \"%s\" ' % pypath)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
            self.show_succeeded_message(self.tr('UI update finished!'))

    def show_update_panel(self):
        """
        显示更新翻译的面板
        Returns:

        """
        work_dir = self.extension_lib.Program.get_work_dir()
        pro_path = ''
        for name in os.listdir(work_dir):
            if name.endswith('.pro'):
                pro_path = os.path.join(work_dir, name)
                break
        ts_files = self.list_files(work_dir, '.ts')
        if len(ts_files) == 0:
            ts_path = ''
        else:
            ts_path = ts_files[0]
        if pro_path != '':
            use_pro = True
        else:
            use_pro = False
        views = [
            ('check_ctrl', 'use_pro', self.tr('Use PRO File'), use_pro),
            ('file_ctrl', 'pro_path', self.tr('Project File(*.pro)'), pro_path, 'PRO File(*.pro)', work_dir),
            ('file_ctrl', 'target', self.tr('Target File(*.ts)'), ts_path, 'TS(*.ts)', work_dir),
        ]

        panel = PMGPanelDialog(parent=self.parent_widget, views=views)
        panel.panel.get_ctrl('pro_path').setEnabled(use_pro)
        panel.panel.set_param_changed_callback('use_pro',
                                               lambda value: panel.panel.get_ctrl('pro_path').setEnabled(
                                                   value['use_pro']))

        def run_pylupdate():
            ts_path = panel.get_value()['target']
            use_pro = panel.get_value()['use_pro']
            if use_pro:
                pro_path = panel.get_value()['pro_path']
            else:
                pro_path = ''
            self.run_pylupdate(ts_path, pro_path)

        def validate(values):
            ts_path = values['target']
            use_pro = values['use_pro']
            if use_pro:
                pro_path = values['pro_path']
                return os.path.exists(ts_path) and os.path.exists(pro_path)
            else:
                return os.path.exists(ts_path)

        panel.verify = validate
        panel.accepted.connect(run_pylupdate)
        panel.exec_()

    def run_pylupdate(self, ts_path='', pro_path=''):
        """
        运行pylupdate，只要有pyqt5即可
        Returns:

        """
        work_dir = self.extension_lib.Program.get_work_dir()
        ret = self.show_covered_message(self.tr('.py files in working directory with tr() or translate() functions'),
                                        '.ts')
        if ret == QMessageBox.Ok:
            print(ts_path)
            if ts_path == '':
                ts_files = self.list_files(work_dir, '.ts')

                if len(ts_files) != 1:
                    QMessageBox.warning(self.parent_widget, self.tr('Warning'), self.tr('No or More than 1 .ts files!'))
                    return
                else:
                    ts_path = ts_files[0]
            print(ts_path)
            if pro_path == '':
                py_files = self.list_files(work_dir, '.py')
                cmd = self.lupdate_command
                for file_name in py_files:
                    try:

                        pypath = os.path.join(work_dir, file_name)
                        with open(pypath, 'rb') as f:
                            s = f.read()
                            if b'tr' in s or b'translate' in s:
                                cmd += ' ' + pypath + ' '
                    except Exception as e:
                        import traceback
                        traceback.print_exc()

                cmd += ' -ts %s' % ts_path
                print('ts', cmd)
                os.system(cmd)
            else:
                cmd = self.lupdate_command + ' ' + '%s' % (pro_path)
                print('UPDATE PRO', cmd)
                os.system(cmd)
            self.show_succeeded_message(self.tr('Translation updating finished!'))

    def run_pyrcc(self, ):
        """
        运行Pyrcc，只要有pyqt5即可
        Returns:

        """
        ret = self.show_covered_message('.qrc', '*_rc.py')
        if ret == QMessageBox.Ok:
            work_dir = self.extension_lib.Program.get_work_dir()
            qrcs = self.list_files(work_dir, '.qrc')
            for qrc_path in qrcs:
                try:
                    py_path = os.path.join(os.path.splitext(qrc_path)[0] + '_rc.py')
                    cmd = self.rcc_command + ' ' + '%s -o %s' % (qrc_path, py_path)
                    logger.info("Rcc update command:" + cmd)
                    os.system(cmd)
                except:
                    import traceback
                    traceback.print_exc()
            self.show_succeeded_message(self.tr('Resources updating finished!'))

    def list_files(self, folder: str, filter_ext: str) -> List[str]:
        """
        Args:
            folder:
            filter_ext:

        Returns:

        """
        files_list = []
        if not filter_ext.startswith('.'):
            filter_ext = '.' + filter_ext

        for home, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith(filter_ext):
                    file_path = os.path.join(home, filename)
                    files_list.append(file_path)

        return files_list

    def show_covered_message(self, ftype_src: str, ftype_dest: str):
        return QMessageBox.warning(self.parent_widget, self.tr('Warning'), self.tr(
            'All {0} files in working directory will be converted to {1} and all generated {1}'
            'files will be overwritten.\nStill continue?').format(ftype_src, ftype_dest),
                                   QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

    def show_succeeded_message(self, message: str = 'Succeeded!'):
        QMessageBox.information(self.parent_widget, self.tr("Information"), message)


class app_designer_wizard(QWizard, Ui_Wizard):
    """
    应用设计引导，通过多步骤引导用户开发扩展应用
    """

    def __init__(self):
        super(app_designer_wizard, self).__init__()
        self.extension_lib = None
        self.setupUi(self)
        self.app_dev_path.clear()
        app_types = [self.tr('Toolbox Application')]
        from packages.applications_toolbar.manage_apps import APPManager
        self.app_dev_path.addItems(APPManager.get_instance().get_app_paths())
        self.app_type.clear()
        self.app_type.addItems(app_types)

        self.app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 扩展应用所在位置
        self.current_app_path = os.path.join(self.app_path, self.app_name.text())  # 当前扩展路径,需要初始化一下防止出现问题。
        # self.intruduce.completeChanged.connect(self.package_check)
        self.btn_qtdesigner.clicked.connect(self.open_designer)
        self.icon_choose.clicked.connect(self.icon_path_choose)
        self.app_name.textChanged.connect(self.name_check)
        self.btn_open_folder.clicked.connect(self.open_app_folder)

        # 设置插件默认图标
        if len(self.icon_path.text()) == 0:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source\default.png')
            self.icon_path.setText(icon_path)

        # 设置默认应用描述
        self.app_desciption.setText("自定义开发的应用")

    def validateCurrentPage(self) -> bool:
        """
        点击Next或者Finish的时候可以触发。
        点击Finish的时候，切换当前的路径到创建的文件夹中，
        :return:
        """

        print('id', self.currentId())
        if self.currentId() == 1:
            return self.validate_project_info()
        if self.currentId() == 3 and self.extension_lib is not None:
            self.extension_lib.Program.set_work_dir(self.current_app_path)
            self.extension_lib.Signal.get_settings_changed_signal().emit()
        return super(app_designer_wizard, self).validateCurrentPage()

    def name_check(self):
        """
        检查是否已存在同名插件应用，如果存在则进行提示
        """
        app_name = self.app_name.text()  # 应用名称
        self.current_app_path = os.path.join(self.app_path, app_name)

        if os.path.exists(self.current_app_path) and len(self.app_name.text()) > 0:
            QMessageBox.information(self, '提示', '相同名称的扩展应用已存在!\n目录：' + self.app_path + '\n名称：' + app_name)

    def icon_path_choose(self):
        """
        选择插件应用的图标文件
        """
        path = ''
        if self.extension_lib is not None:
            path = os.path.dirname(self.extension_lib.Program.get_main_program_dir())
            path = os.path.join(path, 'pmtoolbox', 'ui', 'src')

        file_path, filetype = QFileDialog.getOpenFileName(self, '选择文件', path, "图片文件 (*.icon *.png *.jpg *.svg *.jpeg)")

        if len(file_path) > 0:
            self.icon_path.setText(file_path)

    def validate_project_info(self) -> bool:
        """
        根据用户在引导页面填写的信息，生成应用文件夹，并填充应用json内容
        Returns:

        """
        print(self.currentPage().title(), self.currentPage().nextId())
        if self.currentPage().nextId() == 2:
            app_type_index = self.app_type.currentIndex()
            print(self.currentPage().objectName())
            app_folder = self.app_dev_path.currentText()
            app_name = self.app_name.text()  # 应用名称
            assert app_name.isidentifier()
            app_path = os.path.join(app_folder, app_name)
            app_display_name = self.app_display_name.text()  # 显示名称
            author = self.author.text()  # 作者
            version = self.version.text()  # 版本号
            icon_path = self.icon_path.text()  # 应用图标
            app_type = self.app_type.currentText()  # 应用类型
            app_class = self.app_class.currentText()  # 分类

            # 应用描述 如果应用描述为空，则默认应用描述等于应用名称
            if len(self.app_desciption.toPlainText()) > 0:
                app_desc = self.app_desciption.toPlainText()
            else:
                app_desc = app_name

            # 检查路径是否已存在，如果存在则进行提示，否则创建
            if os.path.exists(app_path) and len(self.app_name.text()) > 0:
                QMessageBox.information(self, '提示', '相同名称的扩展应用已存在!\n目录：' + self.app_path + '\n名称：' + app_name)
                return False

            os.mkdir(app_path)
            self.current_app_path = app_path

            # 复制图片到应用目录 如果用户未选择图标文件则指定默认图标
            if len(self.icon_path.text()) > 0:
                icon_name = os.path.basename(icon_path)
                shutil.copy(icon_path, os.path.join(self.current_app_path, icon_name))
            else:
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source\default.png')
                icon_name = 'default.png'
                shutil.copy(icon_path, os.path.join(self.current_app_path, icon_name))

            # 整理package.json
            if app_type_index == 0:
                package_dict = {'name': app_name, 'display_name': app_display_name, 'author': author,
                                'version': version, 'description': app_desc, 'icon': icon_name,
                                'command': '', 'group': '', 'readme': 'README.md',
                                'entry_point': {'type': 'file', 'file': 'main.py', 'args': []},
                                'pip_packages': []}
            else:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Not implemented'))
                return False
            package_json = json.dumps(package_dict, ensure_ascii=False, indent=2)
            # 生成package.json 到应用目录
            with open(os.path.join(self.current_app_path, 'package.json'), 'w', encoding='utf-8') as file:
                file.write(package_json)

            # 生成配置信息setting.json到应用目录
            setting_dict = {"locale": "zh-CN", "color": "white"}
            with open(os.path.join(self.current_app_path, 'settings.json'), 'w', encoding='utf-8') as file:
                file.write(json.dumps(setting_dict, ensure_ascii=False, indent=2))
            readme_str = f"""
# {app_display_name}

## {self.tr('Introduction')}
{app_desc}
"""
            with open(os.path.join(self.current_app_path, 'README.md'), 'w', encoding='utf-8') as file:
                file.write(readme_str)

            # 生成 main.py到应用目录
            main_py = ''
            main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source/app_main.py')
            for line in open(main_path, 'r', encoding='utf-8'):
                if line.find("作者") >= 0:
                    line = line.replace(line.split(':')[1], author + '\n')
                if line.find("创建日期") >= 0:
                    import time
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    line = line.replace(line.split(':')[1], now_time + '\n')
                if line.find("说明") >= 0:
                    line = line.replace(line.split(':')[1], app_desc + '\n')
                if line.find("应用分类") >= 0:
                    line = line.replace('应用分类', app_class)
                if line.find("应用名称") >= 0:
                    line = line.replace('应用名称', app_name)
                if line.find("应用图标") >= 0:
                    line = line.replace('应用图标', icon_name)
                if line.find("入口文件") >= 0:
                    line = line.replace('入口文件', app_name + '.py')
                if len(line) > 0:
                    main_py = main_py + line

            with open(os.path.join(self.current_app_path, 'main.py'), 'w', encoding='utf-8') as f:
                f.write(main_py)

            # 写入执行文件
            run_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source/run.py')
            run_target = os.path.join(self.current_app_path, app_name + '.py')
            print(run_target)
            shutil.copy(run_path, run_target)
            return True
        else:
            return False

    def open_designer(self):
        """
        打开qtDesigner进行ui编辑
        Returns:

        """
        import subprocess
        import platform
        if platform.system() == "Windows":
            subprocess.Popen(['pyqt5designer'])
        else:
            subprocess.Popen(['designer'])

    def open_app_folder(self):
        """
        使用资源管理器打开应用所在目录
        Returns:

        """
        os.startfile(self.current_app_path)


if __name__ == '__main__':
    from packages.applications_toolbar.manage_apps import APPManager
    from PySide2.QtWidgets import QApplication

    am = APPManager()
    app = QApplication([])
    adw = app_designer_wizard()
    adw.show()

    app.exec_()
