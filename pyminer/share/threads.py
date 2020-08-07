import subprocess
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal

from pyminer.features.extensions import package_manager


class WorkThread(QThread):
    finishSignal = pyqtSignal(str)

    def __init__(self, ip, port, parent=None):
        super(WorkThread, self).__init__(parent)

        self.ip = ip
        self.port = port

    def run(self):
        '''
        重写方法
        '''

        print('=============sleep======ip: {}, port: {}'.format(self.ip, self.port))
        time.sleep(20)

        self.finishSignal.emit('This is a test.')
        return


class ThreadPipInstall(QThread):
    """
    pip 包安装线程
    """
    finishSignal = pyqtSignal(str)

    def __init__(self, package_name, source_index, target_path, version, parent=None):
        super().__init__(parent)

        self.package_name = package_name
        self.source_index = source_index
        self.target_path = target_path
        self.version = version

    def run(self):
        '''
        重写方法
        '''

        print('开始安装name:{},path:{},version:{},index:{},'.format(self.package_name, self.target_path, self.version,
                                                                self.source_index))
        cmd = sys.executable + " -m pip install " + self.source_index + " " + self.target_path + " " + self.package_name + self.version

        self.package_install = plugins.PackageInstallForm()
        self.package_install.textEdit_log.setPlainText("")  # 清空当前日志
        self.package_install.textEdit_log.insertPlainText("正在执行{0}".format(cmd) + '\n')

        # import shlex
        # cmd=shlex.split(cmd)
        print("正在执行命令：", cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        while p.poll() is None:  # 判断subprocess进程是否结束
            line = p.stdout.readline()
            line = line.strip()
            if line:
                self.finishSignal.emit(line + '\n')
        if p.returncode == 0:
            print('Subprogram success')
        else:
            print('Subprogram failed')

        return


class ThreadJupyter(QThread):
    """
    jupyter-notebook线程
    """
    finishSignal = pyqtSignal(str)

    def __init__(self, jupyter_path, parent=None):
        super().__init__(parent)

        self.jupyter_path = jupyter_path

    def run(self):
        """
        重写方法
        """
        cmd = sys.executable +' '+ self.jupyter_path
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        while p.poll() is None:  # 判断subprocess进程是否结束
            line = p.stdout.readline()
            line = line.strip()
            if line:
                self.finishSignal.emit(line)
        if p.returncode == 0:
            print('Subprogram success')
        else:
            print('Subprogram failed')

        return


class ThreadIpython(QThread):
    """
    jupyter-notebook线程
    """
    finishSignal = pyqtSignal(str)

    def __init__(self, ipython_cmd, parent=None):
        super().__init__(parent)

        self.ipython_cmd = ipython_cmd

    def run(self):
        """
        重写方法
        """
        p = subprocess.Popen(self.ipython_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        while p.poll() is None:  # 判断subprocess进程是否结束
            line = p.stdout.readline()
            line = line.strip()
            if line:
                self.finishSignal.emit(line)
        if p.returncode == 0:
            print('Subprogram success')
        else:
            print('Subprogram failed')

        return


