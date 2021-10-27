# -*- coding:utf-8 -*-
# @Time: 2021/1/27 9:13
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: check_dependency.py
import os
import platform
import subprocess
import sys
import time


def run_command_in_terminal_block(cmd: str) -> None:
    platform_name = platform.system().lower()
    if platform_name == 'windows':
        close_action = 'start cmd.exe /k \"%s \"'
        command = close_action % cmd
        f = os.popen(command, 'r', 1)

    elif platform_name == 'linux':
        ret = os.system('which gnome-terminal')

        if ret == 0:
            close_action = 'deepin-terminal -C \"%s\" --keep-open'

            command = close_action % cmd
            subprocess.Popen(command, shell=True)
        else:
            close_action = {'auto': 'gnome-terminal -x bash -c "%s;"',
                            'no': 'gnome-terminal -x bash -c "%s; read"',
                            'wait_key': 'gnome-terminal -x bash -c "%s; read"'
                            }
            command = close_action[close_mode] % (cmd)
            subprocess.Popen(command, shell=True)

    else:
        return


def is_version_satisfied(current_version: str, required_version: str) -> bool:
    """
    判断版本号是否满足要求
    current_version>=required_version:返回True
    否则返回False
    Args:
        current_version:当前版本
        required_version:

    Returns:

    """
    app_version_l = current_version.split('.')
    remote_version_l = required_version.split('.')
    assert len(app_version_l) == len(remote_version_l)
    for velemapp, velemremote in zip(app_version_l, remote_version_l):
        if int(velemapp) < int(velemremote):
            return False
        elif int(velemapp) > int(velemremote):
            print("warning:app version %s is newer than version on server %s." % (current_version, required_version))
    return True


def check_installed_packages():
    try:
        from PySide2.QtWidgets import QWidget, QApplication
        app = QApplication(sys.argv)
        w = QWidget()

    except Exception:
        import traceback
        traceback.print_exc()
        import tkinter as tk
        window = tk.Tk()
        textwidget = tk.Text(window)
        textwidget.pack()
        textwidget.insert(tk.INSERT, '很抱歉，您的环境{interpreter_path}缺少PySide2组件以致我们无法导入PySide2。\n'
                                     '您现在看到的界面是由tkinter制作的报错界面。\n'
                                     '请尝试运行以下命令：\n'
                                     '{interpreter_path} -m pip install -r requirements.txt\n'
                                     '我们已经为您准备好了现成的开发环境，可以在这里安装：\n'
                                     'xxx://asdasdwe//ada.com'.format(interpreter_path=sys.executable))
        window.title('PMiner依赖错误！')
        window.mainloop()
        sys.exit(1)

    from PySide2.QtWidgets import QTextBrowser
    operator = '>='
    try:
        import lib.comm
        assert is_version_satisfied(str(lib.comm.__version__), '0.4')
    except Exception:
        import traceback
        dlg = QTextBrowser()
        dlg.setText('{package_name}包未安装,或者未满足版本要求(>={required_version})\n'
                    '执行命令：{interpreter_path} -m pip install {package_name}{operator}{required_version}\n'
                    '错误详细信息：{exc}'.format(
            required_version='0.4',
            package_name='comm',
            operator=operator,
            interpreter_path=sys.executable,
            exc=traceback.format_exc()))
        dlg.setMinimumWidth(800)
        dlg.setMinimumHeight(600)
        dlg.show()
        # QMessageBox.warning(None, 'PyMiner Warning',
        #                     )
        QApplication.instance().exec_()
        sys.exit(1)


try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QTextBrowser, QLabel, QHBoxLayout, QPushButton, QDialog
    from lib.io.exceptions import PyMinerException


    class ExceptionHandlerDialog(QDialog):
        def __init__(self, exc: BaseException):
            super(ExceptionHandlerDialog, self).__init__()
            self.setWindowTitle(self.tr('An Exception Occured!'))
            self.setLayout(QVBoxLayout())
            fail_descriptions_browser = QTextBrowser()
            label0 = QLabel(self.tr('Exception notes and solutions'))
            label1 = QLabel(self.tr('Exception Details'))
            failure_traceback_browser = QTextBrowser()
            import traceback
            failure_traceback_browser.setPlainText(traceback.format_exc())
            self.layout().addWidget(label0)
            self.layout().addWidget(fail_descriptions_browser)
            self.layout().addWidget(label1)
            self.layout().addWidget(failure_traceback_browser)
            self.setMinimumWidth(800)
            self.setMinimumHeight(600)

            exc_content = repr(exc)
            exc_content = exc_content if exc_content != '' else self.tr('No description or solutions for this error.')
            exception_name = self.tr('Unknown Error')
            self.solution_command = ''
            if isinstance(exc, PyMinerException):
                md = exc.to_markdown()
                self.solution_command = exc.solution_command
                # if exc.solution_command!='':
                #     run_command_in_terminal_block()
                # if type(exc.error)==type(ModuleNotFoundError):

            else:
                if type(exc) == type(ValueError()):
                    exception_name = self.tr('Value Error')
                    print(exc)

                md = """
    # {exception_name}
    An Exception happens,But don't panic.
    ## Descriptions:
    {exception_content}
                """.format(exception_name=exception_name, exception_content=exc_content)
            fail_descriptions_browser.setMarkdown(md)
            buttons_layout = QHBoxLayout()
            button_handle_automatically = QPushButton(self.tr('Try Handle automatically'))
            button_close = QPushButton(self.tr('Close'))
            if self.solution_command != '':
                buttons_layout.addWidget(button_handle_automatically)
            buttons_layout.addWidget(button_close)
            self.layout().addLayout(buttons_layout)

            button_close.clicked.connect(self.close)
            button_handle_automatically.clicked.connect(self.on_try_handle_automatically)

        def on_try_handle_automatically(self):
            """
            尝试用解决方案来解决此异常
            Returns:

            """
            run_command_in_terminal_block(self.solution_command, close_mode='no')
except:
    import traceback

    traceback.print_exc()
    pass


def reinstall_requirements():
    if platform.system().lower() == "windows":
        req_name = 'requirements.txt'
    elif platform.system().lower().startswith("linux"):
        req_name = 'requirements_linux.txt'
    elif platform.system().lower().startswith("darwin"):
        req_name = 'requirentmes_mac.txt'
    else:
        raise SystemError('Platform not supported!')
    req_path = os.path.join(os.path.dirname(__file__), req_name)
    with open(req_path, 'r') as f:
        requirements = [line.strip() for line in f.readlines()]
    print(requirements)

    for req in requirements:
        req = req.strip()
        if req == "":
            continue
        if req.find('>') != -1 or req.find('<') != -1 or req.find('=') != -1:
            ret = os.system(f'{sys.executable} -m pip install {req} -i https://mirrors.cloud.tencent.com/pypi/simple')
        else:
            ret = os.system(
                f'{sys.executable} -m pip install --upgrade {req} -i https://mirrors.cloud.tencent.com/pypi/simple')

    if ret == 0:
        input('安装完成，重启PyMiner即可生效。请按回车键退出，或直接关闭此控制台窗口,然后重新启动PyMiner.')
    else:
        input('自动安装包失败，请查看错误信息或与开发团队联系。')


def reinstall_requirements_with_gui():
    """
    重新安装依赖，并打开GUI
    Returns:

    """
    import tkinter as tk
    import threading

    root = tk.Tk()
    root.wm_title("请稍等，正在在线安装有关的依赖。")
    text = tk.Text(root)
    text.pack()

    def gui_print(line: str, end='\n'):
        text.insert('end', f'{line}{end}')
        text.see('end')

    def th_f():
        try:
            import chardet
        except:
            gui_print('chardet not found, installing ...')
            with subprocess.Popen(f'{sys.executable} -m pip install chardet', stdout=subprocess.PIPE) as p:
                p.stdout.read()
            gui_print('chardet installed')
            import chardet

        if platform.system().lower() == "windows":
            req_name = 'requirements.txt'
        elif platform.system().lower().startswith("linux"):
            req_name = 'requirements_linux.txt'
        elif platform.system().lower().startswith("darwin"):
            req_name = 'requirentmes_mac.txt'
        else:
            raise SystemError('Platform not supported!')
        req_path = os.path.join(os.path.dirname(__file__), req_name)
        mirror = 'https://mirrors.cloud.tencent.com/pypi/simple'
        cmd = f'{sys.executable} -m pip install -i {mirror} -r {req_path}'

        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as p:
            for line in p.stdout:
                encoding = chardet.detect(line)['encoding']
                line = line.decode(encoding)
                gui_print(line, end='')
        root.destroy()

    th = threading.Thread(target=th_f)
    th.setDaemon(True)
    th.start()
    root.mainloop()

    subprocess.Popen(["cmd.exe", "/C", "start", f"{sys.executable}", "app2.py"])
    print([f"{sys.executable} app2.py"])
    time.sleep(5)
    print("程序退出。")

    # if ret == 0:
    #     input('安装完成，重启PyMiner即可生效。请按回车键退出，或直接关闭此控制台窗口,然后重新启动PyMiner.')
    # else:
    #     input('自动安装包失败，请查看错误信息或与开发团队联系。')


if __name__ == '__main__':
    try:
        reinstall_requirements_with_gui()
    except:
        import traceback

        traceback.print_exc()
        input("执行错误，按回车键退出>>")
