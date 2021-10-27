# -*- coding:utf-8 -*-
# @Time: 2021/2/7 15:42
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: database_sample.py
import sample
import accountutil
import dbindexing
from PySide2.QtWidgets import QCompleter
from PySide2.QtCore import Qt, QStringListModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dataUI.data_import_mysql import Ui_Form as ImportMysql_Ui_Form
    from .dataUI.data_import_postgresql import Ui_Form as ImportPostgreSQL_Ui_Form
    from .dataUI.data_import_oracle import Ui_Form as ImportOracle_Ui_Form
else:
    from dataUI.data_import_mysql import Ui_Form as ImportMysql_Ui_Form
    from dataUI.data_import_postgresql import Ui_Form as ImportPostgreSQL_Ui_Form
    from dataUI.data_import_oracle import Ui_Form as ImportOracle_Ui_Form


class ImportDBDialog(sample.ImportDialog):
    def load_last(self):
        pass

    def on_database_name_changed(self):
        pass

    def on_username_changed(self):
        pass

    def set_completer(self):
        pass

    def update_comp(self):
        pass


# 优化完成
class ImportMysql(ImportDBDialog, ImportMysql_Ui_Form):
    """
    "导入MySQL"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.account_util = accountutil.DBAccountUtil()
        self.index_util = dbindexing.DatabaseIndexer()
        self.clearImportParam()
        self.label_test.setHidden(True)
        # 事件
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_test.clicked.connect(self.dbConnectTestButton)
        self.pushButton_ok.clicked.connect(self.dbDatasetImportButton)
        self.set_completer()
        self.load_last()

    def load_last(self):
        conns = self.account_util.get_last_connection('mysql')
        if conns is not None:
            self.lineEdit_host.setText(conns['host'])
            self.spinBox_port.setValue(conns['port'])
            self.lineEdit_user.setText(conns['user'])
            self.lineEdit_passwd.setText(conns['passwd'])
            self.lineEdit_db.setText(conns['database'])
            self.lineEdit_table.setText(conns['table'])

    def set_completer(self):
        """
        IP地址输入完毕之后，从已经保存的用户列表中检索相应的用户名、数据库名，并且更新补全措施。
        当用户名输入完成之后，应当可以自动补全密码。

        :return:
        """
        for edit in [self.lineEdit_host, self.lineEdit_db, self.lineEdit_user, self.lineEdit_table]:
            completer = QCompleter()
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            edit.setCompleter(completer)
            edit.textEdited.connect(self.update_comp)
            completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.lineEdit_user.textChanged.connect(self.on_username_changed)
        self.lineEdit_db.textChanged.connect(self.on_database_name_changed)

    def on_database_name_changed(self):
        database = self.lineEdit_db.text()
        host = self.lineEdit_host.text()
        port = self.spinBox_port.value()
        self.update_tables_completions(host, port, database)

    def on_username_changed(self):
        host = self.lineEdit_host.text()
        port = self.spinBox_port.value()
        user = self.lineEdit_user.text()
        passwd = self.account_util.get_passwd('mysql', host, port, user)
        if passwd != '':
            self.lineEdit_passwd.setText(passwd)

    def update_comp(self):
        hosts = self.account_util.get_host_autocomp('mysql')
        self.lineEdit_host.completer().setModel(QStringListModel(hosts))
        host = self.lineEdit_host.text()
        port = self.spinBox_port.value()
        users, dbs = self.account_util.get_users_and_dbs_autocomp('mysql', host, port)
        self.lineEdit_user.completer().setModel(QStringListModel(users))
        databases = self.index_util.get_databases('mysql', host, port)
        if len(databases) == 0:
            databases = dbs
        self.lineEdit_db.completer().setModel(QStringListModel(databases))

    def update_tables_completions(self, host, port, database):
        autocomp = self.index_util.get_tables('mysql', host, port, database)
        if len(autocomp) == 0:
            autocomp = self.account_util.get_tables_autocomp('mysql', host, port, database)
        self.lineEdit_table.completer().setModel(QStringListModel(autocomp))

    def getImportParam(self):
        """
            获取界面中的配置信息
        """
        self.updateWarningMessage(new=False)
        sql = "select * from {db}.{table} {limit};"
        param = {
            "host": self.lineEdit_host.text(),
            "user": self.lineEdit_user.text(),
            "passwd": self.lineEdit_passwd.text(),
            "db": self.lineEdit_db.text(),
            "port": self.spinBox_port.value(),
            "charset": 'utf8'
        }
        table = self.lineEdit_table.text()
        self.checkTextNotNull(param)
        self.checkTextNotNull({"table": table})

        if self.import_message["isError"]:
            return

        self.import_param.update(
            datasetname=table,
            param=param,
            table=table,
            sql=sql.format(db=param["db"], table=table,
                           limit="limit 1" if self.import_param["ispreview"] else "")
        )

    def importDatasetReload(self):
        """加载MySQL的数据集"""
        import pymysql
        conn = pymysql.connect(**self.import_param["param"])
        cur = conn.cursor()
        cur.execute("SET NAMES utf8")
        self.current_dataset[self.import_param["datasetname"]] = self.getCurFetchData(cur)
        cur.close()
        conn.close()

    def dbConnectTestButton(self):
        super(ImportMysql, self).dbConnectTestButton()
        self.index_util.scan_db('mysql', self.lineEdit_host.text(),
                                self.spinBox_port.value(),
                                self.lineEdit_user.text(),
                                self.lineEdit_passwd.text())
        self.update_comp()
        self.update_tables_completions(self.lineEdit_host.text(), self.spinBox_port.value(), self.lineEdit_db.text())
        if not self.import_message['isError']:
            self.account_util.add_connection(**{
                'db_type': 'mysql',
                'table': self.lineEdit_table.text(),
                "host": self.lineEdit_host.text(),
                "user": self.lineEdit_user.text(),
                "passwd": self.lineEdit_passwd.text(),
                "database": self.lineEdit_db.text(),
                "port": self.spinBox_port.value()
            })


# 优化完成，未检验
class ImportOracle(ImportDBDialog, ImportOracle_Ui_Form):
    """
    "导入Oracle"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.label_test.setHidden(True)

        # 事件
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_test.clicked.connect(self.dbConnectTestButton)
        self.pushButton_ok.clicked.connect(self.dbDatasetImportButton)

        self.load_last()

    def load_last(self):
        pass

    def getImportParam(self):
        """
            获取界面中的配置信息
        """
        self.updateWarningMessage(new=False)
        sql = "select * from {db}.{table} {limit};"
        param = {
            "host": self.lineEdit_host.text(),
            "user": self.lineEdit_user.text(),
            "passwd": self.lineEdit_passwd.text(),
            "port": self.spinBox_port.value(),
            "server_name": self.lineEdit_servername.text()
        }
        table = self.lineEdit_table.text()
        self.checkTextNotNull(param)
        self.checkTextNotNull({"table": table})

        if self.import_message["isError"]:
            return

        self.import_param.update(
            datasetname=table,
            param=param,
            table=table,
            sql=sql.format(db=param["db"], table=table,
                           limit="limit 1" if self.import_param["ispreview"] else "")
        )

    def importDatasetReload(self):
        """加载MySQL的数据集"""
        import cx_Oracle
        user, passwd, host, bd = list(self.import_param["param"].values())
        conn_link = '{user}/{port}@{host}:{port}/{server_name}'.format(**self.import_param["param"])
        conn = cx_Oracle.connect(conn_link)
        cur = conn.cursor()
        self.current_dataset[self.import_param["datasetname"]] = self.getCurFetchData(cur)
        cur.close()
        conn.close()


# 优化完成
class ImportPostgreSQL(sample.ImportDialog, ImportPostgreSQL_Ui_Form):
    """
    "导入PostgreSQL"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.center()
        self.clearImportParam()
        self.label_test.setHidden(True)

        # 事件
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_test.clicked.connect(self.dbConnectTestButton)
        self.pushButton_ok.clicked.connect(self.dbDatasetImportButton)

    def getImportParam(self):
        """
            获取界面中的配置信息
        """
        self.updateWarningMessage(new=False)
        sql = "select * from {schema}.{table} {limit};"
        param = {
            "host": self.lineEdit_host.text(),
            "user": self.lineEdit_user.text(),
            "password": self.lineEdit_passwd.text(),
            "database": self.lineEdit_db.text(),
            "port": self.spinBox_port.value()
        }
        schema = self.lineEdit_schema.text()
        table = self.lineEdit_table.text()
        self.checkTextNotNull(param)
        self.checkTextNotNull({"table": table, "schema": schema})

        if self.import_message["isError"]:
            return

        self.import_param.update(
            datasetname=table.replace(".", "_"),
            param=param,
            schema=schema,
            table=table,
            sql=sql.format(schema=schema, table=table,
                           limit="limit 1" if self.import_param["ispreview"] else "")
        )
        # 由于数据库中允许表名称有 “.” 导入Python后会出现问题，因此需要对datasetname进行调整

    def importDatasetReload(self):
        """加载MySQL的数据集"""
        import psycopg2
        conn = psycopg2.connect(**self.import_param["param"])
        cur = conn.cursor()
        cur.execute(self.import_param["sql"])
        self.current_dataset[self.import_param["datasetname"]] = self.getCurFetchData(cur)
        cur.close()
        conn.close()
