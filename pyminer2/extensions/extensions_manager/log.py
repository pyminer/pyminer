from pyminer2.pmutil import get_main_window


def log(text):
    """日志输出text"""
    get_main_window().slot_flush_console('info', 'Extension', 'Log:' + str(text))


def error(text):
    print("Error:", text)
    get_main_window().slot_flush_console(
        'error', 'Extension', 'Error:' + str(text))


def assert_(boolean, text):
    """
    boolean:bool
    text:str
    若bool为false,以异常级输出text
    """
    if not boolean:
        error(text)
