import subprocess
import os
import platform


def open_file_manager(path: str):
    assert os.path.exists(path)
    path = os.path.normcase(path)  # windows的输入命令格式似乎需要注意一下！需要换成斜杠，否则会识别不出来的。
    if platform.system().lower() == 'windows':
        subprocess.Popen(['explorer.exe', path], shell=True)
    elif platform.system().lower() == 'linux':
        if os.system('which nautilus') == 0:
            subprocess.Popen(['nautilus', path])
            return
        elif os.system('which dde-file-manager') == 0:
            subprocess.Popen(['dde-file-manager', path])
            return
        else:
            raise NotImplementedError('Cannot Detect system file manager!')
    else:
        raise NotImplementedError("This Platform is not supported now!")


if __name__ == '__main__':
    # open_file_manager(r'J:\Developing\pyminer_bin\PyMiner\bin\widgets\utilities\platform')
    open_file_manager(r'/home/hzy/图片')
