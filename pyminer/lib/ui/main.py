from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QDialog, QTableWidget, QHeaderView, QAbstractItemView, QFrame, \
    QTableWidgetItem


from ui_data_normal import Ui_Dialog
import sys
import numpy as np
import logging
from decimal import Decimal


class MyWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        # 初始化一组正态分布数据
        self.build_normal()

        self.buttonBox.accepted.connect(self.build_normal)
        self.buttonBox.rejected.connect(self.close)

    def custom_menu(self):
        '''
        定制鼠标右键菜单
        :return:
        '''

    def keyPressEvent(self, event):
        """ Ctrl + C复制表格内容 """
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            # 获取表格的选中行
            selected_ranges = self.tableWidget.selectedRanges()[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
            text_str = ""  # 最后总的内容
            # 行（选中的行信息读取）
            for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                row_str = ""
                # 列（选中的列信息读取）
                for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                    item = self.tableWidget.item(row, col)
                    row_str += item.text() + '\t'  # 制表符间隔数据
                text_str += row_str + '\n'  # 换行
            clipboard = QApplication.clipboard()  # 获取剪贴板
            clipboard.setText(text_str)  # 内容写入剪贴板

    def build_normal(self):
        self.v_precision = self.spinBox_precison.value()
        self.v_mean = self.doubleSpinBox_mean.value()
        self.v_std = self.doubleSpinBox_std.value()
        self.v_count = self.spinBox_count.value()

        np.set_printoptions(precision=self.v_precision)
        self.data = np.random.normal(loc=self.v_mean, scale=self.v_std, size=self.v_count)
        print(self.data)
        print(type(self.data))
        # logging.info(data)

        self.show_table()

    def show_table(self):

        self.tableWidget.setSortingEnabled(True)  # 设置表头可以自动排序
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setHorizontalHeaderLabels(['正态分布数据'])

        for i in range(len(self.data)):

            # 调用Decimal 设置数据精度格式
            if self.v_precision == 0:
                decimal_format = '0'
            else:
                decimal_format = '0.' + '0' * self.v_precision

            random_value = Decimal(self.data[i]).quantize(Decimal(decimal_format))  # 调用Decimal 设置数据精度

            item = QTableWidgetItem(str(random_value))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 0, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form1 = MyWindow()
    form1.show()
    sys.exit(app.exec_())
