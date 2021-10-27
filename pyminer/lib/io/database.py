from typing import List

from widgets import PMGPanel
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QListWidget, QListWidgetItem, \
    QComboBox, QDialog, QInputDialog
from utils import dbConnectTool, get_all_accounts_list, get_all_accounts, dbConnectAccountTool, create_account
from lib.io.dbConn import DatabaseConn


class DatabaseConfigPanel(QDialog):
    def __init__(self, parent=None):
        super(DatabaseConfigPanel, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.combo_select_database_type = QComboBox()
        self.combo_select_database_type.addItems(['MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'SQLite'])
        self.combo_select_database_type.currentIndexChanged.connect(self.on_database_selected)
        self.layout().addWidget(self.combo_select_database_type)
        conn = DatabaseConn()
        views, engine = conn.create_conn('mysql')

        self.settings_panel = PMGPanel(parent=self, views=views)
        self.settings_panel.signal_settings_changed.connect(self.on_settings_changed)
        self.upper_layout = QHBoxLayout()
        self.layout().addLayout(self.upper_layout)
        self.upper_layout.addWidget(self.settings_panel)
        self.conn_list = QListWidget()
        self.conn_list.itemDoubleClicked.connect(self.item_double_clicked)
        self.upper_layout.addWidget(self.conn_list)
        self.button_test_connection = QPushButton(self.tr('Test Connection'))
        self.button_test_connection.clicked.connect(self.test_connection)
        self.button_create_account = QPushButton(self.tr('Create Account'))
        self.button_create_account.clicked.connect(self.create_account)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_test_connection)
        self.button_layout.addWidget(self.button_create_account)
        self.layout().addLayout(self.button_layout)
        # self.settings_panel.on_settings_changed()
        index = self.combo_select_database_type.currentIndex()
        self.on_database_selected(index)

    def get_current_db_type(self) -> str:
        return self.combo_select_database_type.currentText()

    def on_database_selected(self, index):
        text = self.get_current_db_type().lower()
        conn = DatabaseConn()
        views, engine = conn.create_conn(text)
        self.settings_panel.set_items(views)

        db_type = self.get_current_db_type().lower()
        accounts = get_all_accounts()
        db_accounts = accounts.get(db_type)
        if db_accounts is not None:
            l = list(db_accounts.keys())
        else:
            l = []
        self.show_accounts(l)

    def on_settings_changed(self, settings):
        pass

    def item_double_clicked(self, item: QListWidgetItem):
        """
        列表项双击触发回调
        :param item:
        :return:
        """
        settings = self.settings_panel.get_value()
        db_type = self.get_current_db_type().lower()
        conn_name = item.text()
        print(db_type, conn_name)
        # 模拟获取某个账号的信息、SSH账号等信息
        accounts = get_all_accounts()
        print(accounts, db_type, conn_name)
        if accounts.get(db_type) is not None:
            account = accounts.get(db_type).get(conn_name)
            if account is not None:
                self.settings_panel.set_value(account.get('account'))

        # print(accounts.get(db_type).get(conn_name))

    def show_accounts(self, accounts: List[str]):
        """
        在列表显示所有的连接
        :return:
        """
        self.conn_list.clear()
        self.conn_list.addItems(accounts)

    def test_connection(self):
        """
        连接检测
        :return:
        """
        params = self.settings_panel.get_value()
        connectaccount = dict(
            account=dict(
                user="root", password="123456", host="localhost",
                port="3306", database="learning", charset="utf-8"
            ),
            usessh=False,
            SSH={},
            connectdescribe="这又是一个测试"
        )
        connectaccount['account'].update(params)
        print(connectaccount)
        # dbCA = dbConnectAccountTool()
        mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        dbCT = dbConnectTool(account=connectaccount, conn_url=mysql_url)
        connect_status = dbCT.createConn()
        print(connect_status)
        # db_functool = dbFuncTool(connectaccount, mysql_url)
        # print(query(db_functool,'select * from scores;'))
        if connect_status.get('status') == 'connect':
            QMessageBox.information(self, self.tr('Connection Test'), self.tr('Connection Succeeded!'), QMessageBox.Ok)
        else:
            QMessageBox.information(self, self.tr('Connection Test'), self.tr('Connection Failed!'), QMessageBox.Ok)

    def create_account(self):
        """
        创建一个新的账户
        [TODO]:尚未连接事件
        :return:
        """
        print('创建账户——目前尚未连接事件')
        account_name, stat = QInputDialog.getText(self, '输入账户名称', '请输入账户名称')
        if account_name != '':
            params = self.settings_panel.get_value()
            connectaccount = dict(
                account=dict(
                    user="root", password="123456", host="localhost",
                    port="3306", database="learning", charset="utf-8"
                ),
                usessh=False,
                SSH={},
                connectdescribe="这又是一个测试"
            )
            connectaccount['account'].update(params)
            create_account(account_name, connectaccount)
            index = self.combo_select_database_type.currentIndex()
            self.on_database_selected(index)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable()
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sp2 = DatabaseConfigPanel()
    # sp2.signal_settings_changed.connect(lambda settings: print('views2-settings', settings))
    sp2.show()
    sys.exit(app.exec_())
