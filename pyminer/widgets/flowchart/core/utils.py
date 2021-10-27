from PySide2.QtCore import QPointF


def round_position(point: QPointF, pixels=5):
    """
    圆整位置。
    :param point:
    :param pixels:圆整的单位（最好是1，2，5，10，20，...）
    :return:
    """
    x, y = point.x(), point.y()
    x_cor, y_cor = round(x * 1.0 / pixels) * pixels, round(y * 1.0 / pixels) * pixels
    return QPointF(x_cor, y_cor)
