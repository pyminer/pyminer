import os
import platform
import subprocess
import sys
from typing import Union, Optional


def check_platform() -> str:
    """
    Check platform.
    returns 'linux', 'windows' or 'osx'

    Returns: platform name in lowercase, a str
    """
    system = platform.system()
    plat = platform.platform(1, 1)
    return system.lower()


def run_command_in_terminal(cmd: str, close_mode: str = 'wait_key') -> None:
    """
    Run command in system terminal.
    TODO: Adapt it to OSX and Linux system!!!

    Args:
        cmd: application command, which should be platform-crossing.
        close_mode: What the terminal do when execution finished. There are a few options:['wait_key','auto','no'].

            * 'wait_key' means the terminal closes when user pressed any key after execution.
            * 'auto' means the terminal closes instantly after execution.
            * 'no' means the terminal will keep shown until user manually close it.

    Returns:

    """
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


def run_command_in_terminal_block(cmd: str, close_mode: str = 'wait_key') -> None:
    """
    Run command in a terminal window, and the running event will block current Program.
    The programm will be continued after closing the command terminal.
    TODO:Is this function threading-safe?

    Args:
        cmd: application command, which should be platform-crossing.
        close_mode: What the terminal do when execution finished. There are a few options:['wait_key','auto','no'].

            * 'wait_key' means the terminal closes when user pressed any key after execution.
            * 'auto' means the terminal closes instantly after execution.
            * 'no' means the terminal will keep shown until user manually close it.

    Returns:
    """
    platform_name = check_platform()
    if platform_name == 'windows':
        close_action = {'auto': 'start cmd.exe /k \"%s &&exit \"',
                        'no': 'start cmd.exe /k \"%s \"',
                        'wait_key': 'start cmd.exe /k \"%s &&pause &&exit \"'
                        }
        command = close_action[close_mode] % cmd
        f = os.popen(command, 'r', 1)

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


def run_python_file_in_terminal(file_path, interpreter_path: str = None, close_mode: str = 'wait_key',
                                blocking=False) -> Optional[str]:
    """
    Run Python file in terminal
    Args:
        file_path:
        interpreter_path:
        close_mode:
        blocking:

    Returns:

    """
    if interpreter_path is None:
        interpreter_path = sys.executable
    if blocking:
        return run_command_in_terminal_block('%s %s' % (interpreter_path, file_path), close_mode=close_mode)
    else:
        return run_command_in_terminal('%s %s' % (interpreter_path, file_path), close_mode=close_mode)


def check_application(app_name):
    os.system(app_name)


def get_parent_path(path: str, storey: int = 1) -> str:
    """
    获取文件或者文件夹的父路径。
    Args:
        path: original path(file or folder)
        storey: If is 1,return parent path;if is 2,return the parent path's parent path

    Returns:
    """
    for i in range(storey):
        path = os.path.dirname(path)
    return path


if __name__ == '__main__':
    run_python_file_in_terminal('./test/python_file_test.py', blocking=True)


    def test_run_in_terminal():
        import time
        run_command_in_terminal('dir', close_mode='no')
        time.sleep(1)
        run_command_in_terminal('dir', close_mode='wait_key')
        time.sleep(1)
        run_command_in_terminal('dir', close_mode='auto')


    test_run_in_terminal()
