import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QSpacerItem, QSizePolicy, QGraphicsView, \
    QFrame, QApplication
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap


class PMFlowWidget(QWidget):
    def __init__(self):
        from .resources import icon_lc_save, icon_sc_shadowcurser, icon_lc_connectorlinesarrowend, icon_lc_undo, \
            icon_lc_redo, icon_sc_deletepage, icon_lc_aligncenter, icon_lc_alignmiddle, icon_lc_zoomin, \
            icon_lc_zoomout, icon_dataprovider, \
            icon_sc_autosum, icon_lc_drawchart, icon_lc_statisticsmenu, icon_lc_dbreportedit
        _translate = QCoreApplication.translate
        super().__init__()
        self.setObjectName("tab_flow")

        self.verticalLayout_6 = QVBoxLayout(self)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_3 = QWidget(self)
        self.widget_3.setMinimumSize(QSize(0, 30))
        self.widget_3.setObjectName("widget_3")

        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.toolButton_4 = QToolButton(self.widget_3)
        icon7 = QIcon()
        icon7.addPixmap(QPixmap(":/pyqt/source/images/NavOverFlow_Start.png"), QIcon.Normal,
                        QIcon.Off)
        self.toolButton_4.setIcon(icon7)
        self.toolButton_4.setIconSize(QSize(25, 25))
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout_6.addWidget(self.toolButton_4)
        self.toolButton_3 = QToolButton(self.widget_3)
        icon8 = QIcon()
        icon8.addPixmap(
            QPixmap(":/pyqt/source/images/lc_basicstop.png"),
            QIcon.Normal,
            QIcon.Off)
        self.toolButton_3.setIcon(icon8)
        self.toolButton_3.setIconSize(QSize(25, 25))
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_6.addWidget(self.toolButton_3)
        self.toolButton_6 = QToolButton(self.widget_3)

        self.toolButton_6.setIcon(icon_lc_save)
        self.toolButton_6.setIconSize(QSize(25, 25))
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_6.addWidget(self.toolButton_6)
        self.toolButton_5 = QToolButton(self.widget_3)

        self.toolButton_5.setIcon(icon_sc_shadowcurser)
        self.toolButton_5.setIconSize(QSize(25, 25))
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_6.addWidget(self.toolButton_5)
        self.toolButton_2 = QToolButton(self.widget_3)

        self.toolButton_2.setIcon(icon_lc_connectorlinesarrowend)
        self.toolButton_2.setIconSize(QSize(25, 25))
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_6.addWidget(self.toolButton_2)
        self.toolButton = QToolButton(self.widget_3)

        self.toolButton.setIcon(icon_lc_undo)
        self.toolButton.setIconSize(QSize(25, 25))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_6.addWidget(self.toolButton)
        self.toolButton_7 = QToolButton(self.widget_3)

        self.toolButton_7.setIcon(icon_lc_redo)
        self.toolButton_7.setIconSize(QSize(25, 25))
        self.toolButton_7.setObjectName("toolButton_7")
        self.horizontalLayout_6.addWidget(self.toolButton_7)
        self.toolButton_8 = QToolButton(self.widget_3)

        self.toolButton_8.setIcon(icon_sc_deletepage)
        self.toolButton_8.setIconSize(QSize(25, 25))
        self.toolButton_8.setObjectName("toolButton_8")
        self.horizontalLayout_6.addWidget(self.toolButton_8)
        self.toolButton_9 = QToolButton(self.widget_3)

        self.toolButton_9.setIcon(icon_lc_aligncenter)
        self.toolButton_9.setIconSize(QSize(25, 25))
        self.toolButton_9.setObjectName("toolButton_9")
        self.horizontalLayout_6.addWidget(self.toolButton_9)
        self.toolButton_10 = QToolButton(self.widget_3)

        self.toolButton_10.setIcon(icon_lc_alignmiddle)
        self.toolButton_10.setIconSize(QSize(25, 25))
        self.toolButton_10.setObjectName("toolButton_10")
        self.horizontalLayout_6.addWidget(self.toolButton_10)
        self.toolButton_11 = QToolButton(self.widget_3)

        self.toolButton_11.setIcon(icon_lc_zoomin)
        self.toolButton_11.setIconSize(QSize(25, 25))
        self.toolButton_11.setObjectName("toolButton_11")
        self.horizontalLayout_6.addWidget(self.toolButton_11)
        self.toolButton_12 = QToolButton(self.widget_3)

        self.toolButton_12.setIcon(icon_lc_zoomout)
        self.toolButton_12.setIconSize(QSize(25, 25))
        self.toolButton_12.setObjectName("toolButton_12")
        self.horizontalLayout_6.addWidget(self.toolButton_12)
        self.toolButton_13 = QToolButton(self.widget_3)

        self.toolButton_13.setIcon(icon_dataprovider)
        self.toolButton_13.setIconSize(QSize(25, 25))
        self.toolButton_13.setObjectName("toolButton_13")
        self.horizontalLayout_6.addWidget(self.toolButton_13)
        self.toolButton_16 = QToolButton(self.widget_3)

        self.toolButton_16.setIcon(icon_sc_autosum)
        self.toolButton_16.setIconSize(QSize(25, 25))
        self.toolButton_16.setObjectName("toolButton_16")
        self.horizontalLayout_6.addWidget(self.toolButton_16)
        self.toolButton_17 = QToolButton(self.widget_3)

        self.toolButton_17.setIcon(icon_lc_drawchart)
        self.toolButton_17.setIconSize(QSize(25, 25))
        self.toolButton_17.setObjectName("toolButton_17")
        self.horizontalLayout_6.addWidget(self.toolButton_17)
        self.toolButton_14 = QToolButton(self.widget_3)

        self.toolButton_14.setIcon(icon_lc_statisticsmenu)
        self.toolButton_14.setIconSize(QSize(25, 25))
        self.toolButton_14.setObjectName("toolButton_14")
        self.horizontalLayout_6.addWidget(self.toolButton_14)
        self.toolButton_15 = QToolButton(self.widget_3)

        self.toolButton_15.setIcon(icon_lc_dbreportedit)
        self.toolButton_15.setIconSize(QSize(25, 25))
        self.toolButton_15.setObjectName("toolButton_15")
        self.horizontalLayout_6.addWidget(self.toolButton_15)
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.widget_3)

        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_6.addWidget(self.graphicsView)

        self.toolButton_4.setText(_translate("MainWindow", "..."))
        self.toolButton_3.setText(_translate("MainWindow", "..."))
        self.toolButton_6.setText(_translate("MainWindow", "..."))
        self.toolButton_5.setText(_translate("MainWindow", "..."))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.toolButton_7.setText(_translate("MainWindow", "..."))
        self.toolButton_8.setText(_translate("MainWindow", "..."))
        self.toolButton_9.setText(_translate("MainWindow", "..."))
        self.toolButton_10.setText(_translate("MainWindow", "..."))
        self.toolButton_11.setText(_translate("MainWindow", "..."))
        self.toolButton_12.setText(_translate("MainWindow", "..."))
        self.toolButton_13.setText(_translate("MainWindow", "..."))
        self.toolButton_16.setText(_translate("MainWindow", "..."))
        self.toolButton_17.setText(_translate("MainWindow", "..."))
        self.toolButton_14.setText(_translate("MainWindow", "..."))
        self.toolButton_15.setText(_translate("MainWindow", "..."))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graphics = PMFlowWidget()
    graphics.show()

    sys.exit(app.exec_())
