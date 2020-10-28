import os
import platform
import subprocess
import sys


def check_platform() -> str:
    system = platform.system()
    plat = platform.platform(1, 1)
    return system.lower()


def run_command_in_terminal(cmd: str, close_mode: str = 'wait_key'):
    platform_name = check_platform()
    if platform_name == 'windows':
        close_action = {'auto': 'start cmd.exe /k \"%s &&exit \"',
                        'no': 'start cmd.exe /k \"%s \"',
                        'wait_key': 'start cmd.exe /k \"%s &&pause &&exit \"'
                        }
        command = close_action[close_mode] % cmd
        subprocess.Popen(command, shell=True)


    elif platform_name == 'linux':
        ret = os.system('which gnome-terminal')

        if ret == 0:
            close_action = {'auto': 'deepin-terminal -C \"%s\"',
                            'no': 'deepin-terminal -C \"%s\" --keep-open',
                            'wait_key': 'deepin-terminal -C \"%s\" --keep-open'
                            }
            command = close_action[close_mode] % cmd
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


def run_python_file_in_terminal(file_path, interpreter_path: str = None, close_mode: str = 'wait_key'):
    if interpreter_path is None:
        interpreter_path = sys.executable
    run_command_in_terminal('%s %s' % (interpreter_path, file_path), close_mode=close_mode)


def check_application(app_name):
    os.system(app_name)


def get_parent_path(path, storey=1):
    """
    获取文件或者文件夹的父路径。
    :param path:
    :param storey:
    :return:
    """
    for i in range(storey):
        path = os.path.dirname(path)
    return path


if __name__ == '__main__':
    plat = check_platform()
    print(plat)
