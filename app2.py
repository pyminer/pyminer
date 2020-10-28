import cgitb
import time
import logging
from pyminer2.pmappmodern import main
import ctypes
import platform

if platform.system().lower() == 'windows':
    """
    无论是点击bat还是在终端运行，如果你发现控制台窗口闪现一下就关闭了，那么就是由以下代码造成的。
    注释掉以下代码即可正常显示控制台。
    """
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

if __name__ == '__main__':
    t0 = time.time()  # 开始时间
    # 异常处理设置
    cgitb.enable(format='text')

    # 日志设置
    logger = logging.getLogger(__name__)

    t2 = time.time()  # 结束时间
    logging.info(f'time spent for importing modules {t2 - t0}')  # 打印日志，启动耗时
    main()
