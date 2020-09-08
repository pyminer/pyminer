import platform
import subprocess


def check_platform() -> str:
    system = platform.system()
    print(system)
    return system.lower()


def run_command_in_terminal(cmd: str, close_mode: str = 'wait_key'):
    print(check_platform())
    platform_name = check_platform()
    if platform_name == 'windows':
        close_action = {'auto': 'start cmd.exe /k \"%s &&exit \"',
                        'no': 'start cmd.exe /k \"%s \"',
                        'wait_key': 'start cmd.exe /k \"%s &&pause &&exit \"'
                        }
        command = close_action[close_mode] % cmd


    elif platform_name == 'deepin':
        command = 'deepin-terminal -x bash -c \" %s \" ' % (cmd)
    elif platform_name == 'linux':
        command = 'gnome-terminal -x bash -c \"%s ;read\"  ' % (cmd)
    else:
        return
    subprocess.Popen(command, shell=True)


if __name__ == '__main__':
    def test_run_in_terminal():
        import time
        run_command_in_terminal('dir', close_mode='no')
        time.sleep(1)
        run_command_in_terminal('dir', close_mode='wait_key')
        time.sleep(1)
        run_command_in_terminal('dir', close_mode='auto')
