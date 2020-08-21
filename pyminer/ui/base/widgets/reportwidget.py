from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSpacerItem,QSizePolicy,QPushButton
from PyQt5.QtCore import QSize,QCoreApplication


class PMReportWidget(QWidget):
    def __init__(self):
        super().__init__()
        _translate = QCoreApplication.translate
        self.setObjectName("tab_report")

        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QWidget(self)
        self.widget_2.setMaximumSize(QSize(16777215, 30))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pushButton_browser_open = QPushButton(self.widget_2)
        self.pushButton_browser_open.setMinimumSize(QSize(80, 0))
        self.pushButton_browser_open.setObjectName("pushButton_browser_open")
        self.horizontalLayout_4.addWidget(self.pushButton_browser_open)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.horizontalLayout_result = QHBoxLayout()
        self.horizontalLayout_result.setObjectName("horizontalLayout_result")
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout_result.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_result)

        self.pushButton_browser_open.setText(_translate("MainWindow", "浏览器打开"))