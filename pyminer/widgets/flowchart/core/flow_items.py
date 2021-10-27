"""
绘制层次：

"""
from PySide2.QtCore import QLineF, QPointF, Qt, QRectF, Signal
from PySide2.QtGui import QPolygonF, QPen, QPainterPath, QColor, QPainter, QBrush
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsObject, \
    QStyleOptionGraphicsItem, QWidget, QGraphicsSceneHoverEvent, QGraphicsTextItem, QTextEdit

from typing import TYPE_CHECKING, Tuple, List, Callable, Any

if TYPE_CHECKING:
    from .flowchart_widget import Node, PMGraphicsScene

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_LINE_NORMAL = QColor(30, 30, 30)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)
COLOR_HOVER_MID_POINT = QColor(0, 0, 200)
COLOR_SELECTED = QColor(255, 255, 0)


def round_position(point: QPointF, pixels=5):
    x, y = point.x(), point.y()
    x_cor, y_cor = round(x * 1.0 / pixels) * pixels, round(y * 1.0 / pixels) * pixels
    return QPointF(x_cor, y_cor)


class PMGSimpleSignal():
    """
    简单的信号类
    此信号类接口类似于Signal，但父类不一定必须继承QObject。可以从其他地方发出，并且起到去耦合的作用。
    """

    def __init__(self, *object_types):
        self.object_types = object_types
        self.callbacks = []

    def connect(self, callback: Callable):
        self.callbacks.append(callback)

    def emit(self, *args):
        assert len(args) == len(self.object_types), '输入参数长度与定义时不等'
        for arg, arg_type in zip(args, self.object_types):
            assert isinstance(arg, arg_type), '参数%s类型与定义不同' % repr(arg)

        for cb in self.callbacks:
            cb(*args)

    def disconnect(self, callback: Callable):
        if callback in self.callbacks:
            self.callbacks.remove(callback)


class PMGGraphicsLineItem(QGraphicsLineItem):

    def __init__(self, line: QLineF):
        super(PMGGraphicsLineItem, self).__init__(line)

        self.signal_hover_enter = PMGSimpleSignal(QGraphicsSceneHoverEvent)
        self.signal_hover_leave = PMGSimpleSignal(QGraphicsSceneHoverEvent)
        self.signal_mouse_pressd = PMGSimpleSignal(QGraphicsSceneMouseEvent)
        self.signal_mouse_doubleclicked = PMGSimpleSignal(QGraphicsSceneMouseEvent, PMGGraphicsLineItem)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.signal_hover_enter.emit(event)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.signal_hover_leave.emit(event)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        这里不能进行继承。一旦进行了继承，似乎会让下面所有的东西都收到信号，从而无法选定。
        :param event:
        :return:
        """
        super(PMGGraphicsLineItem, self).mousePressEvent(event)
        self.signal_mouse_pressd.emit(event)

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.signal_mouse_doubleclicked.emit(event, self)

    def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
        """
        屏蔽绘制事件！
        Args:
            QPainter:
            QStyleOptionGraphicsItem:
            widget:

        Returns:

        """
        pass


class CustomLine(QGraphicsLineItem):
    """
    CustomLine不是QObject，没有办法绑定信号，只能用回调函数的方式。
    之前有重绘事件的回调函数，现已删除，改为鼠标事件触发。

    这是一个line，其中起点是start_port,终点end_port，中继点为mid_points中从第1个元素开始依次向前。
    所以一共有起点+终点+len(mid_points)个节点，从而有len(mid_points)+1个线段。

    每一个线段背后都是一个QGraphicsLineItem。为何不是简单绘制？盖因一般的绘制没有办法捕获鼠标事件。
    如果使用QGraphicsLineItem，那么可以捕获键盘事件。

    当点击线段的时候会触发选择事件。首先，线段会调用QGraphicsScene（self.canvas）进行一个清除选择的操作————如果不按ctrl的话。
    然后设置本身状态为选择。

    self.canvas.selectedItems()可获取当前被选中的部件。

    下一步任务：插入节点、删除节点。
    """

    def __init__(self, start_port: 'CustomPort', end_port: 'CustomPort', canvas: 'PMGraphicsScene' = None,
                 mid_points: 'List[CustomMidPoint]' = None):
        super(CustomLine, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动

        self._refreshed = False
        self.color = COLOR_LINE_NORMAL
        self.start_port = start_port
        self.end_port = end_port
        if self not in start_port.connected_lines:
            start_port.connected_lines.append(self)
        if self not in end_port.connected_lines:
            end_port.connected_lines.append(self)
        self.line_items: List['QGraphicsLineItem'] = []
        self.center_points = mid_points if (mid_points is not None) else []
        for p in self.center_points:
            canvas.addItem(p)
            self.connect_midpoint_signals(p)
            p.line = self
        canvas.signal_clear_selection.connect(self.on_clear_selection)
        self.refresh()
        self.canvas = canvas
        self.init_line_items()

    def is_selected(self):
        return self in self.canvas.selected_items

    def get_opposite_port(self, port: 'CustomPort') -> 'CustomPort':
        """

        :param port:某个端口
        :return: 对面的端口
        """
        if port is self.start_port:
            return self.end_port
        else:
            return self.start_port

    def remove_mid_point(self, mid_point: 'CustomMidPoint'):
        """
        移除中间节点
        :param mid_point:
        :return:
        """
        index = self.center_points.index(mid_point)
        point_to_remove = self.center_points.pop(index)
        line_to_remove = self.line_items.pop(index)
        self.canvas.removeItem(point_to_remove)
        self.canvas.removeItem(line_to_remove)
        self.canvas.removeItem(mid_point)
        self.refresh_line_items()
        self.update()
        self.canvas.update_viewport()

    def bind_line_item_signals(self, line_item: 'PMGGraphicsLineItem'):
        """
        绑定线段的信号
        :param line_item:
        :return:
        """
        line_item.signal_mouse_doubleclicked.connect(self.on_line_item_double_clicked)
        line_item.signal_mouse_pressd.connect(self.on_line_item_pressed)
        line_item.signal_hover_enter.connect(self.on_line_item_hover_enter)
        line_item.signal_hover_leave.connect(self.on_line_item_hover_leave)

    def connect_midpoint_signals(self, mid_point: 'CustomMidPoint'):
        mid_point.signal_double_clicked.connect(self.remove_mid_point)
        mid_point.point_dragged.connect(self.refresh)

    def add_mid_point(self, line_item: 'PMGGraphicsLineItem', pos: QPointF):
        """
        增加中间节点
        :param line_item:
        :param pos:
        :return:
        """
        index = self.line_items.index(line_item)
        new_center_point = CustomMidPoint(pos, line=self)
        self.canvas.addItem(new_center_point)
        self.center_points.insert(index, new_center_point)
        self.connect_midpoint_signals(new_center_point)
        if index == 0:
            last_pos = self.start_port.center_pos
        else:
            last_pos = self.center_points[index].center_pos
        next_pos = new_center_point.center_pos
        new_line_item = PMGGraphicsLineItem(QLineF(last_pos, next_pos))

        # pen = QPen()
        # pen.setColor(self.color)
        # pen.setWidth(3)
        # new_line_item.setPen(pen)
        self.canvas.addItem(new_line_item)
        self.line_items.insert(index, new_line_item)
        self.bind_line_item_signals(new_line_item)  # 绑定中间节点的信号。
        print(len(self.line_items))
        self.refresh_line_items()
        self.update()
        self.canvas.update_viewport()

    def on_line_item_double_clicked(self, event: 'QGraphicsSceneMouseEvent', line_item: 'PMGGraphicsLineItem'):

        self.add_mid_point(line_item, pos=event.scenePos())

    def init_line_items(self):
        """
        初始化线段
        :return:
        """
        last_pos = self.start_port.center_pos
        for p in self.center_points:
            pos = p.center_pos
            line_item = PMGGraphicsLineItem(QLineF(last_pos, pos))
            self.bind_line_item_signals(line_item)

            pen = QPen()
            pen.setColor(self.color)
            pen.setWidth(5)
            line_item.setPen(pen)
            self.canvas.addItem(line_item)
            last_pos = pos
            self.line_items.append(line_item)
        line_item = PMGGraphicsLineItem(QLineF(last_pos, self.end_port.center_pos))
        self.bind_line_item_signals(line_item)

        self.canvas.addItem(line_item)
        self.line_items.append(line_item)

    def refresh_line_items(self):
        """
        刷新背后的直线段。
        :return:
        """
        last_pos = self.start_port.center_pos
        if len(self.line_items) == 0:
            return
        for i, p in enumerate(self.center_points):
            pos = p.center_pos
            line = QLineF(last_pos, pos)
            self.line_items[i].setLine(line)
            last_pos = pos

        line = QLineF(last_pos, self.end_port.center_pos)
        self.line_items[-1].setLine(line)

    def on_line_item_hover_enter(self, e: 'QGraphicsSceneHoverEvent'):
        self.color = COLOR_HOVER
        self.update()

    def on_line_item_hover_leave(self, e: 'QGraphicsSceneHoverEvent'):
        if not self.is_selected():
            self.color = COLOR_LINE_NORMAL
            self.update()

    def on_line_item_pressed(self, e: 'QGraphicsSceneMouseEvent'):
        """
        当线段被点击时触发的事件。
        :param e:
        :return:
        """
        if e.button() == Qt.LeftButton:
            if not e.modifiers() == Qt.ControlModifier:
                self.canvas.signal_clear_selection.emit()
            self.canvas.select_item(self)
            self.color = COLOR_SELECTED

    def on_clear_selection(self):
        """
        当清除选择时触发的事件。
        :return:
        """
        self.color = COLOR_LINE_NORMAL
        self.canvas.unselect_item(self)
        # self.update()

    def refresh(self):
        """
        当刷新时触发的事件
        :return:
        """
        self._refreshed = False
        self.refresh_line_items()
        self.update()
        self._refreshed = True

    def draw_arrow(self, QPainter, point_1: QPointF, point_2: QPointF) -> 'QPolygonF':
        """
        绘制箭头。
        :param QPainter:
        :param point_1:
        :param point_2:
        :return:
        """

        line = QLineF(point_1, point_2)

        v = line.unitVector()

        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(int(line.dx() / 2), int(line.dy() / 2)))

        n = v.normalVector()  # 法向量
        n.setLength(n.length() * 0.2)  # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector()  # 两次法向量运算以后，就得到一个反向的法向量
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        # if PYSIDE2:
        QPainter.drawPolygon([p1, p2, p3])
        # else:
        #     QPainter.drawPolygon(p1, p2, p3)
        return QPolygonF([p1, p2, p3, p1])

    def paint(self, q_painter: 'QPainter', style_option_graphics_item: 'QStyleOptionGraphicsItem',
              widget: 'QWidget' = None):

        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(3)
        pen.setJoinStyle(Qt.MiterJoin)  # 让箭头变尖
        q_painter.setPen(pen)

        path = QPainterPath()

        point1 = self.start_port
        path.moveTo(self.start_port.center_pos)
        # for i in self.line_items:
        #     i.setPen(QColor(255, 0, 0))
        #     i.update()
        for p in self.center_points + [self.end_port]:
            pen.setWidth(3)
            q_painter.setPen(pen)
            path.lineTo(p.center_pos)
            q_painter.drawLine(QLineF(point1.center_pos, p.center_pos))
            arrow = self.draw_arrow(q_painter, point1.center_pos, p.center_pos)
            path.addPolygon(arrow)  # 将箭头添加到连线上
            point1 = p

    def get_central_points_positions(self):
        """
        获取所有中间节点的位置。
        :return:
        """
        positions = []
        for point in self.center_points:
            positions.append((point.x(), point.y()))
        return positions

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """
        悬浮事件进入所触发的事件。
        :param event:
        :return:
        """
        self.color = COLOR_HOVER_PORT

        self.update()

    def on_delete(self):
        """
        删除线对象
        首先从起始和结束的端口的连线中删除这个线；
        然后，从画布上移除自身所有的中间线段对象和中继点对象
        从画布上删除自身；
        从所有连线的列表中移除自身。
        :return:
        """
        try:
            self.start_port.connected_lines.remove(self)
        except ValueError:
            import traceback
            traceback.print_exc()
        try:
            self.end_port.connected_lines.remove(self)
        except ValueError:
            import traceback
            traceback.print_exc()
        for line_item in self.line_items:
            self.canvas.removeItem(line_item)
        for mid_item in self.center_points:
            self.canvas.removeItem(mid_item)
        self.canvas.removeItem(self)
        self.canvas.lines.remove(self)


class CustomMidPoint(QGraphicsObject):
    point_dragged = Signal(QGraphicsObject)
    signal_double_clicked = Signal(object)

    def __init__(self, pos: QPointF = None, line: 'CustomLine' = None):
        super(CustomMidPoint, self).__init__()
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.size = (10, 10)
        if pos is not None:
            self.setPos(pos)
        self.line = line
        self.setZValue(1.0)  # 设置层次。

    def boundingRect(self):
        return QRectF(0, 0, self.size[0], self.size[1])

    @property
    def center_pos(self):
        return QPointF(self.x() + self.size[0] / 2, self.y() + self.size[1] / 2)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        鼠标拖动时触发的事件。
        :param event:
        :return:
        """
        mouse_x, mouse_y = event.scenePos().x(), event.scenePos().y()
        self.setPos(round_position(QPointF(mouse_x, mouse_y)))
        self.point_dragged.emit(self)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(self.color)
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER_MID_POINT
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        self.update()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        if evt.button() == Qt.LeftButton:
            pos = (evt.scenePos().x(), evt.scenePos().y())
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())

        elif evt.button() == Qt.RightButton:
            pass
        elif evt.button() == Qt.MidButton:
            pass

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.signal_double_clicked.emit(self)
        # self.line.remove_mid_point(self)


class CustomPort(QGraphicsObject):
    port_clicked = Signal(QGraphicsObject)

    def __init__(self, port_id: str, text: str = 'port', content: Any = None, port_type='input'):
        super(CustomPort, self).__init__()
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.id = port_id
        self.text = text
        self.size = (10, 10)
        self.content = content
        self.connected_lines = []
        self.canvas = None
        self.node: 'Node' = None

        self.text_item = QGraphicsTextItem(parent=self)
        self.port_type = port_type
        if port_type == 'input':
            self.text_item.setPos(10, -5)
        else:
            self.text_item.setPos(-30, -5)
        self.text_item.setPlainText(self.text)

    def set_text(self, text: str):
        self.text_item.setPlainText(text)
        self.text = text

    def boundingRect(self):
        return QRectF(0, 0, self.size[0], self.size[1])

    @property
    def center_pos(self):
        return QPointF(self.x() + self.size[0] / 2, self.y() + self.size[1] / 2)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER_PORT
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        self.update()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        if evt.button() == Qt.LeftButton:
            pos = (evt.scenePos().x(), evt.scenePos().y())
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())
            self.port_clicked.emit(self)
        elif evt.button() == Qt.RightButton:
            pass
        elif evt.button() == Qt.MidButton:
            pass

    def paintEvent(self, paint_event):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()

    def get_pos(self) -> Tuple[int, int]:
        pos = self.pos()
        return pos.x(), pos.y()

    def get_connected_lines(self) -> List['CustomLine']:
        if len(self.connected_lines) == 0:
            return []
        else:
            return self.connected_lines

    def get_connected_port(self) -> List['CustomPort']:
        """
        获取连接的节点
        :return:
        """
        lines = self.get_connected_lines()
        if len(lines) == 0:
            return []
        port_list = []
        for l in lines:
            port_list.append(l.get_opposite_port(self))
        return port_list

    def on_delete(self):
        for line in self.connected_lines:
            line.on_delete()
        self.scene().removeItem(self)

    def parse_id(self) -> Tuple[str, str, str]:
        """
        解析id。id由三个元素构成，由冒号分割。
        如3:input:2,意思就是id3为3的节点中，id为2的输入端口。注意
        :return:
        """
        node_id, type, port_id = self.id.split(':')
        return node_id, type, port_id

    def __repr__(self):
        return super(CustomPort, self).__repr__() + 'id = ' + str(self.id)


class CustomRect(QGraphicsItem):
    def __init__(self, node: 'Node' = None):
        super(CustomRect, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable)  # 只有设置了可以选取才能被选中。
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.node = node

    def boundingRect(self):
        return QRectF(0, 0, 120, 120)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        if self.isSelected():
            self.color = COLOR_SELECTED
        self.update()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.setPos(round_position(
            QPointF(event.scenePos().x() - self.relative_pos[0],
                    event.scenePos().y() - self.relative_pos[1])))
        self.node.refresh_pos()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        [!TODO]整理这里的代码，节点编辑这一块的代码非常乱！
        :param event:
        :return:
        """
        self.on_value_show_requested()
        # self.on_edit_properties_requested()

    def on_value_show_requested(self):
        from PySide2.QtWidgets import QDialog, QVBoxLayout
        val_dlg = QDialog()
        val_dlg.setLayout(QVBoxLayout())
        text_show = QTextEdit()
        text = 'inputs:\n' + repr(self.node.content.input_args) + '\n' + 'results:\n' + repr(self.node.content.results)
        text_show.setText(text)
        val_dlg.layout().addWidget(text_show)
        val_dlg.exec_()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        if evt.button() == Qt.LeftButton:
            pos = (evt.scenePos().x(), evt.scenePos().y())
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())
            if not evt.modifiers() == Qt.ControlModifier:
                self.scene().signal_clear_selection.emit()
            self.scene().select_item(self)
            self.color = COLOR_SELECTED
        elif evt.button() == Qt.RightButton:
            pass
        elif evt.button() == Qt.MidButton:
            pass

    def paintEvent(self, paintEvent):
        pen1 = QPen()
        pen1.setColor(self.color)
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()

    def on_clear_selection(self):
        """
        当清除选择时触发的事件。
        :return:
        """
        self.color = COLOR_NORMAL
        if self.scene() is not None:
            self.scene().unselect_item(self)

    def on_delete(self):
        self.node.on_delete()
        pass
