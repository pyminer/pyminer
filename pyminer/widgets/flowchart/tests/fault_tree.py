import sys
import time

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from widgets.flowchart.core.flowchart_widget import PMFlowWidget

if __name__ == '__main__':
    times = {True: 0, False: 1}
    app = QApplication(sys.argv)
    graphics = PMFlowWidget(path='fault_tree.json')
    graphics.show()
    graphics.pre_run()
    graphics.run_in_fg()
    timer = QTimer()
    timer.start(1)
    i = 0


    def run_fg():
        """
        在前端直接运行代码
        :return:
        """
        t0 = time.time()
        global i, timer
        steps = 100
        for j in range(steps):
            i += 1
            # result = graphics.run_in_fg([])

            result = graphics.run_fg_for_one_step()
            times[result[0]] += 1

        print('exec result:', result)
        if i > 10000:
            timer.stop()
        t1 = time.time()

        print('Run Times:%d,Reliability is %f' % (i, times[True] / (times[True] + times[False])))
        print('time elapsed %f' % (t1 - t0))


    timer.timeout.connect(run_fg)
    sys.exit(app.exec_())
