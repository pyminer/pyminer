from PySide2.QtCore import QUrl, QObject, Slot

from PySide2.QtGui import QGuiApplication

from PySide2.QtQuick import QQuickView


class MyClass(QObject):

    @Slot(int, result=str)  # 声明为槽，输入参数为int类型，返回值为str类型
    def returnValue(self, value):
        return str(value + 10)


if __name__ == '__main__':
    path = 'src/demo1.qml'

    app = QGuiApplication([])

    view = QQuickView()

    con = MyClass()

    context = view.rootContext()

    context.setContextProperty("con", con)

    view.engine().quit.connect(app.quit)

    view.setSource(QUrl(path))

    view.show()

    app.exec_()
