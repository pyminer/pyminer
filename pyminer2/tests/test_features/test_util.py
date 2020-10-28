from pyminer2.features.util.platformutil import run_command_in_terminal, run_python_file_in_terminal, \
    get_parent_path



def test_run_command_win():
    import time
    run_command_in_terminal('dir', close_mode='auto')
    time.sleep(3)
    run_command_in_terminal('dir', close_mode='wait_key')
    time.sleep(3)
    run_command_in_terminal('dir', close_mode='no')
    time.sleep(3)
    pass
def test_run_command_linux():
    import time
    run_command_in_terminal('ls', close_mode='auto')
    time.sleep(3)
    run_command_in_terminal('ls', close_mode='wait_key')
    time.sleep(3)
    run_command_in_terminal('ls', close_mode='no')
    time.sleep(3)
    pass

def test_run_python_file_in_terminal():

    run_python_file_in_terminal('python_file_to_run.py', close_mode='wait_key')
    pass


def test_get_parent_path():
    print(get_parent_path(r'C:\Windows\SysWOW64', 2))


if __name__ == '__main__':

    # test_run_command()
    test_get_parent_path()
    # test_run_python_file_in_terminal()
