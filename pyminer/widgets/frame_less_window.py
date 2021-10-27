import sys
import os
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStatusBar, QStackedWidget, \
    QApplication
from PySide2.QtGui import QPixmap, QFont, QEnterEvent, QPainter, QPen, QColor, QIcon
from PySide2.QtCore import QMargins, Qt




class TitleBar(QWidget):
    """主窗口无边框后使用的标题栏"""
    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 支持使用QSS设置背景
        self._mouse_pos = None
        layout = QHBoxLayout(self)
        layout.setContentsMargins(QMargins(5, 5, 5, 5))
        layout.setSpacing(2)
        self.title_label = QLabel(self)
        self.title_label.setScaledContents(True)
        self.title_label.setFixedSize(25, 25)
        layout.addWidget(self.title_label, alignment=Qt.AlignLeft)  # 加入窗口图标

        self.title_text = QLabel(self)
        self.title_text.setFixedHeight(25)
        layout.addWidget(self.title_text, alignment=Qt.AlignLeft)  # 加入窗口文字

        layout.addStretch()

        self.minimum_button = QPushButton('0', self)
        self.maximum_button = QPushButton('1', self)
        self.close_button = QPushButton('r', self)
        layout.addWidget(self.minimum_button, alignment=Qt.AlignRight)
        layout.addWidget(self.maximum_button, alignment=Qt.AlignRight)
        layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        font = QFont('webdings')  # 使用webding字体设置按钮的图标
        self.minimum_button.setFont(font)
        self.maximum_button.setFont(font)
        self.close_button.setFont(font)
        self.minimum_button.setFixedSize(25, 25)
        self.maximum_button.setFixedSize(25, 25)
        self.close_button.setFixedSize(25, 25)
        self.minimum_button.clicked.connect(self.window_minimum)  # 设置点击的信号事件
        self.maximum_button.clicked.connect(self.window_maximum)
        self.close_button.clicked.connect(self.window_close)

        # 设置objectName来设置样式
        self.setObjectName('titleBar')
        self.minimum_button.setObjectName('minimumButton')
        self.maximum_button.setObjectName('maximumButton')
        self.close_button.setObjectName('closeButton')
        self.setStyleSheet("""
        #titleBar{
            background-color: rgb(255,255,255);
        }
         #minimumButton,#maximumButton,#closeButton {
            border: none;
            background-color: rgb(255,255,255);
        }
        #minimumButton:hover,#maximumButton:hover {
            color: rgb(33,165,229);
        }
        #closeButton:hover {
            color: rgb(200,49,61);
        }
        """)

        self.setLayout(layout)

    def mouseDoubleClickEvent(self, event):
        self.window_maximum()
        event.accept()  # 接受事件，禁止传到父控件

    # 鼠标移动
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._mouse_pos:
            self.parent().move(self.mapToGlobal(event.pos() - self._mouse_pos))
        event.accept()  # 接受事件,不传递到父控件

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mouse_pos = event.pos()
        event.accept()  # 接受事件,不传递到父控件

    def mouseReleaseEvent(self, event):
        self._mouse_pos = None
        event.accept()  # 接受事件,不传递到父控件

    def window_minimum(self):
        self.parent().showMinimized()

    def window_maximum(self):
        if self.maximum_button.text() == '1':
            self.maximum_button.setText('2')
            self.parent().showMaximized()
        else:
            self.maximum_button.setText('1')
            self.parent().showNormal()

    def window_close(self):
        self.parent().close()

    def set_window_title(self, title):
        self.title_text.setText(title)

    def set_window_icon(self, pix_map):
        if isinstance(pix_map, QPixmap):
            self.title_label.setPixmap(pix_map)


class CenterWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super(CenterWidget, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

    def clear(self):
        for i in range(self.count()):
            widget = self.widget(i)
            self.removeWidget(widget)
            if widget is not None:
                widget.deleteLater()
                del widget


class StatusBar(QStatusBar):
    def __init__(self, *args, **kwargs):
        super(StatusBar, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)


class FrameLessWindow(QWidget):
    """主窗口"""
    MARGIN = 5
    Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)

    def __init__(self, *args, **kwargs):
        super(FrameLessWindow, self).__init__(*args, **kwargs)
        self.resize(1200, 680)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)  # 鼠标追踪，mouseMoveEvent才有效果
        self._direction = None  # 此时鼠标的方向
        self._pressed = False  # 鼠标是否按下
        self._mouse_pos = None  # 记录鼠标位置
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN))

        self.title = TitleBar(self)
        self.title.installEventFilter(self)  # 安装事件过滤,进入控件还原方向和鼠标状态
        layout.addWidget(self.title, alignment=Qt.AlignTop)

        self.center_widget = CenterWidget(self)
        self.center_widget.installEventFilter(self)
        layout.addWidget(self.center_widget)

        self.status_bar = StatusBar(self)
        self.status_bar.installEventFilter(self)
        layout.addWidget(self.status_bar, alignment=Qt.AlignBottom)
        self.setLayout(layout)

    def eventFilter(self, obj, event):
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
            self._direction = None  # 去除方向
            self._pressed = None  # 去除按下标记
        return super(FrameLessWindow, self).eventFilter(obj, event)

    def mousePressEvent(self, event):
        super(FrameLessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mouse_pos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        super(FrameLessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self._direction = None

    def mouseMoveEvent(self, event):
        super(FrameLessWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        pos_x, pos_y = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGIN, self.height() - self.MARGIN
        # print(wm, hm)
        # 窗口最大无需事件
        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self.resize_window(pos)
        if pos_x <= self.MARGIN and pos_y <= self.MARGIN:
            # 左上角
            self._direction = self.LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= pos_x <= self.width() and hm <= pos_y <= self.height():
            # 右下角
            self._direction = self.RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= pos_x and pos_y <= self.MARGIN:
            # 右上角
            self._direction = self.RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif pos_x <= self.MARGIN and hm <= pos_y:
            # 左下角
            self._direction = self.LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= pos_x <= self.MARGIN <= pos_y <= hm:
            # 左边
            self._direction = self.Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= pos_x <= self.width() and self.MARGIN <= pos_y <= hm:
            # 右边
            self._direction = self.Right
            self.setCursor(Qt.SizeHorCursor)
        elif wm >= pos_x >= self.MARGIN >= pos_y >= 0:
            # 上面
            self._direction = self.Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.MARGIN <= pos_x <= wm and hm <= pos_y <= self.height():
            # 下面
            self._direction = self.Bottom
            self.setCursor(Qt.SizeVerCursor)
        else:
            pass

    def showMaximized(self):
        super(FrameLessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        super(FrameLessWindow, self).showNormal()
        self.layout().setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)

    def paintEvent(self, event):
        super(FrameLessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(200, 200, 200, 1), 2 * self.MARGIN))
        painter.drawRect(self.rect())

    def setWindowTitle(self, title):
        super(FrameLessWindow, self).setWindowTitle(title)
        self.title.set_window_title(title)

    def setWindowIcon(self, icon):
        if isinstance(icon, QIcon):
            super(FrameLessWindow, self).setWindowIcon(icon)
            self.title.set_window_icon(icon.pixmap(20, 20))

    def resize_window(self, pos):
        if self._direction is None:
            return
        mpos = pos - self._mouse_pos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self._direction == self.LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self._direction == self.RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mouse_pos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mouse_pos = pos
        elif self._direction == self.RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mouse_pos.setX(pos.x())
        elif self._direction == self.LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mouse_pos.setY(pos.y())
        elif self._direction == self.Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self._direction == self.Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mouse_pos = pos
            else:
                return
        elif self._direction == self.Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self._direction == self.Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mouse_pos = pos
            else:
                return
        self.setGeometry(x, y, w, h)

    def remove_status_bar(self):
        self.status_bar.hide()

    def set_center_widget(self, widget):
        self.center_widget.clear()
        self.center_widget.addWidget(widget)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=FrameLessWindow()
    form.setWindowTitle("PyMiner v2.1")
    form.show()
    sys.exit(app.exec_())