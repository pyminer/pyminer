class MainForm(QDialog):
    def __init__(self,parent=None)
        super(MainForm,self).__init__(parent)

        self.filename=QString()
        self.copiedItem=QByteArray()
        self.pasteOffiset=5
        self.prevPoint=QPoint()

        self.addOffset=5
        self.borders=[]

        self.printer=QPrinter(QPrinter.HightResolution)
        self.printer.setPageSize(QPrinter.Letter)


class GraphicsView(QGraphicsView):
    def __init__(self,parent=None)
        super(GraphicsView,self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)

    def wheelEvent(self,event):
        factor=1.41 **(-event.delta() / 240.0)
        self.scale(factor,factor)