"""
DO] add a table to store some informations about calculation.
"""
import sys
import time

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from widgets.flowchart.core.flowchart_widget import PMFlowWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    graphics = PMFlowWidget(path='continously_data_process.json')
    graphics.show()
    graphics.pre_run()
    graphics.run_in_fg()
    timer = QTimer()
    timer.start(100)
    i = 0


    def run_fg():
        """
        在前端直接运行代码
        :return:
        """
        t0 = time.time()
        global i,timer
        i += 1
        result = graphics.run_fg_for_one_step()
        print('exec result:', result)
        if i>100:
            timer.stop()
        t1 = time.time()
        print('time elapsed %f'%(t1-t0))


    timer.timeout.connect(run_fg)
    sys.exit(app.exec_())
