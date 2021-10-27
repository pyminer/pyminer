import random
import sys
import math
from typing import Tuple, Union, List

from PySide2.QtCore import QTimer, Qt, QRectF, QPoint
from PySide2.QtGui import QPainter, QLinearGradient, QFontMetricsF, QPen, QFontMetrics, QRadialGradient, QConicalGradient, \
    QColor, QPolygon
from PySide2.QtWidgets import QWidget, QLCDNumber, QApplication


class PMGGauge(QWidget):
    def __init__(self, val_range: Union[Tuple[Union[float, int], Union[float, int]],
                                        List[Union[float, int]]] = None,
                 initial_value: float = None, title: str = 'Untitled',
                 warning_rate: float = 0.8):
        super().__init__()
        self._brush_color = Qt.black
        if val_range is None:
            val_range = (0, 100)
        assert val_range[0] < val_range[1]
        if initial_value is None:
            initial_value = val_range[0]

        self._warning_rate = warning_rate
        self.setWindowTitle("GaugePanel")
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)

        self.lcd_display = QLCDNumber(self)
        self.lcd_display.setDigitCount(4)
        self.lcd_display.setMode(QLCDNumber.Dec)
        self.lcd_display.setSegmentStyle(QLCDNumber.Flat)
        self.lcd_display.setStyleSheet('border:2px solid green;color:green;background:silver')

        self._start_angle = 120  # 以QPainter坐标方向为准,建议画个草图看看
        self._end_angle = 60  # 以以QPainter坐标方向为准
        self._scale_main_num = 10  # 主刻度数
        self._scaleSubNum = 10  # 主刻度被分割份数
        self._min_value = val_range[0]
        self._max_value = val_range[1]
        self._title = title
        self._value = initial_value
        self._min_radio = 1  # 缩小比例,用于计算刻度数字
        self._decimals = 0  # 小数位数

    def alert(self, alert_level: int):
        """
        1:严重警报
        2：一般警报
        其他值为正常
        :param alert_level:
        :return:
        """
        if alert_level == 2:
            self._brush_color = QColor(200, 100, 40)
        elif alert_level == 1:
            self._brush_color = QColor(220, 50, 30)
        else:
            self._brush_color = Qt.black
        self.update()

    def set_warning_rate(self, warning_rate: float):
        assert 0 < warning_rate < 1
        self._warning_rate = warning_rate

    def set_min_max_value(self, min, max):
        self._min_value = min
        self._max_value = max

    def set_title(self, title):
        self._title = title

    def set_value(self, value):
        assert self._min_value <= value <= self._max_value, \
            f'Value %s is not in range [{self._min_value},{self._max_value}]' % (repr(value))
        self._value = value
        self.update()

    def set_min_radio(self, min_radio):
        self._min_radio = min_radio

    def set_decimals(self, decimals):
        self._decimals = decimals

    def paintEvent(self, event):
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)  # painter坐标系原点移至widget中央
        painter.scale(side / 200, side / 200)  # 缩放painterwidget坐标系，使绘制的时钟位于widge中央,即钟表支持缩放

        self.draw_panel(painter)  # 画外框表盘
        self.draw_scale_num(painter)  # 画刻度数字
        self.draw_scale_line(painter)  # 画刻度线
        self.drawTitle(painter)  # 画标题备注
        self.drawValue(painter)  # 画数显
        self.drawIndicator(painter)  # 画指针

    def draw_panel(self, p):
        p.save()
        radius = 100
        lg = QLinearGradient(-radius, -radius, radius, radius)
        lg.setColorAt(0, Qt.white)
        lg.setColorAt(1, Qt.black)
        p.setBrush(lg)
        p.setPen(Qt.NoPen)
        p.drawEllipse(-radius, -radius, radius * 2, radius * 2)

        p.setBrush(self._brush_color)
        p.drawEllipse(-92, -92, 92 * 2, 92 * 2)
        p.restore()

    def draw_scale_num(self, p):
        sin = math.sin
        cos = math.cos
        p.save()
        p.setPen(Qt.white)
        start_rad = self._start_angle * (3.14 / 180)
        step_rad = (360 - (self._start_angle - self._end_angle)) * (3.14 / 180) / self._scale_main_num

        fm = QFontMetricsF(p.font())
        for i in range(0, self._scale_main_num + 1):
            sina = sin(start_rad + i * step_rad)
            cosa = cos(start_rad + i * step_rad)

            tmp_val = i * ((self._max_value - self._min_value) / self._scale_main_num) + self._min_value
            tmp_val = tmp_val / self._min_radio
            s = '{:.0f}'.format(tmp_val)
            w = fm.size(Qt.TextSingleLine, s).width()
            h = fm.size(Qt.TextSingleLine, s).height()
            x = 80 * cosa - w / 2
            y = 80 * sina - h / 2
            p.drawText(QRectF(x, y, w, h), s)

        p.restore()

    def draw_scale_line(self, p):
        p.save()
        p.rotate(self._start_angle)
        scale_nums = self._scale_main_num * self._scaleSubNum
        angle_step = (360 - (self._start_angle - self._end_angle)) / scale_nums
        p.setPen(Qt.white)

        pen = QPen(Qt.white)
        for i in range(0, scale_nums + 1):
            if i >= self._warning_rate * scale_nums:
                pen.setColor(Qt.red)

            if i % self._scale_main_num == 0:
                pen.setWidth(2)
                p.setPen(pen)
                p.drawLine(64, 0, 72, 0)
            else:
                pen.setWidth(1)
                p.setPen(pen)
                p.drawLine(67, 0, 72, 0)
            p.rotate(angle_step)

        p.restore()

    def drawTitle(self, p):
        p.save()
        p.setPen(Qt.white)
        fm = QFontMetrics(p.font())
        w = fm.size(Qt.TextSingleLine, self._title).width()
        p.drawText(int(-w / 2), -45, self._title)
        p.restore()

    def drawValue(self, p):
        side = min(self.width(), self.height())
        w, h = int(side / 2 * 0.4), int(side / 2 * 0.2)
        x, y = int(self.width() / 2 - w / 2), int(self.height() / 2 + side / 2 * 0.55)
        self.lcd_display.setGeometry(x, y, w, h)

        ss = '{:.' + str(self._decimals) + 'f}'
        self.lcd_display.display(ss.format(self._value))

    def drawIndicator(self, p):
        p.save()
        polygon = QPolygon([QPoint(0, -2), QPoint(0, 2), QPoint(60, 0)])
        deg_rotate = self._start_angle + (360 - (self._start_angle - self._end_angle)) / (
                self._max_value - self._min_value) * (self._value - self._min_value)
        # 画指针
        p.rotate(deg_rotate)
        halogd = QRadialGradient(0, 0, 60, 0, 0)
        halogd.setColorAt(0, QColor(60, 60, 60))
        halogd.setColorAt(1, QColor(160, 160, 160))
        p.setPen(Qt.white)
        p.setBrush(halogd)
        p.drawConvexPolygon(polygon)
        p.restore()

        # 画中心点
        p.save()
        rad_gradient = QRadialGradient(0, 0, 10)
        rad_gradient = QConicalGradient(0, 0, -90)
        rad_gradient.setColorAt(0.0, Qt.darkGray)
        rad_gradient.setColorAt(0.5, Qt.white)
        rad_gradient.setColorAt(1.0, Qt.darkGray)
        p.setPen(Qt.NoPen)
        p.setBrush(rad_gradient)
        p.drawEllipse(-5, -5, 10, 10)
        p.restore()


if __name__ == "__main__":
    import cgitb

    cgitb.enable()
    app = QApplication(sys.argv)
    gp = PMGGauge(val_range=(0, 100), initial_value=0, title='CPU占用%', warning_rate=0.75)
    gp.show()

    timer = QTimer()
    timer.start(100)
    timer.timeout.connect(lambda: gp.set_value(random.randint(0, 100)))

    timer2 = QTimer()
    timer2.start(1000)
    timer2.timeout.connect(lambda: gp.alert(random.randint(0, 2)))
    app.exec_()
