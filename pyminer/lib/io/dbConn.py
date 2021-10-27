# -*- coding:utf8 -*-
class DatabaseConn(object):

    def tr(self, s: str):
        return s

    def __init__(self):
        self.conn_url = "{user}:{password}@{host}:{port}/{database}"

    def create_conn(self, dbtype="mysql"):
        """
            选择创建的通道
            Auth:
                GanDaiWei
            Args:
                dbtype: 传入数据库类型
            Returns:
                view: 连接通道的视图效果
                engine: 链接的 url 字符串
        """
        conn_dict = {
            "mysql": self.mysql_conn,
            "postgresql": self.pgsql_conn,
            "oracle": self.oracle_conn,
            "sql server": self.mssql_conn,
            "sqlite": self.sqlite_conn
        }

        assert dbtype in conn_dict, 'Can not create connection to {}'.format(dbtype)
        view, engine, engine_type = conn_dict[dbtype]()
        engine = engine if engine_type else engine + self.conn_url  # 如果 url 不完整情况下需要进行拼接
        return (view, engine)

    def mssql_conn(self):
        """
            创建 SQL server 的链接
            mssql = Microsoft SQL server，即 SQLserver
            Returns:
                前端界面视图、使用引擎、是否完整
        """
        mssql_view = [
            ('line_ctrl', 'database', self.tr('Database Name'), ''),
            [
                ('line_ctrl', 'host', self.tr('Host Name/IP'), ''),
                ('line_ctrl', 'port', self.tr('Port'), '1521')
            ],
            ('line_ctrl', 'initialDB', self.tr('Initial Database'), 'master'),  # 初始数据库连接
            ('line_ctrl', 'user', self.tr('User'), ''),
            ('password_ctrl', 'password', self.tr('Password'), ''),
            ('line_ctrl', 'dbDesc', self.tr('Database Description'), '')
        ]
        return (mssql_view, "mssql+pymssql://", False)

    def sqlite_conn(self):
        """
            创建 SQLite 的链接
            Returns:
                前端界面视图、使用引擎、是否完整
        """
        sqlite_view = [
            ('line_ctrl', 'database', self.tr('Database Name'), ''),
            ('line_ctrl', 'file', self.tr('Database File Road'), ''),
            ('line_ctrl', 'user', self.tr('User'), ''),
            ('password_ctrl', 'password', self.tr('Password'), ''),
            ('line_ctrl', 'dbDesc', self.tr('Database Description'), '')
        ]
        return (sqlite_view, "sqlite://{}", True)

    def oracle_conn(self):
        """
            创建 Oracle 的链接
            Returns:
                前端界面视图、使用引擎、是否完整
        """
        oracle_view = [
            ('line_ctrl', 'database', self.tr('Database Name'), ''),
            # ('combo_ctrl', 'connType', self.tr('Connect Type'), 'Basic', ['Basic', 'TNS']), # 暂时只支持 Basic 类型连接
            [
                ('line_ctrl', 'host', self.tr('Host Name/IP'), ''),
                ('line_ctrl', 'port', self.tr('Port'), '1521')
            ],
            ('line_ctrl', 'user', self.tr('User'), ''),
            ('password_ctrl', 'password', self.tr('Password'), ''),
            ('line_ctrl', 'databasedesc', self.tr('Database Description'), '')
        ]
        return (oracle_view, "oracle://", False)

    def pgsql_conn(self):
        """
            创建 PgSQL 的链接
            Returns:
                前端界面视图、使用引擎、是否完整
        """
        pgsql_view = [
            ('line_ctrl', 'database', self.tr('Database Name'), ''),
            [
                ('line_ctrl', 'host', self.tr('Host Name/IP'), 'localhost'),
                ('line_ctrl', 'port', self.tr('Port'), '5432')
            ],
            ('line_ctrl', 'initialDB', self.tr('Initial Database'), 'postgres'),  # 初始数据库连接
            ('line_ctrl', 'user', self.tr('User'), 'postgres'),
            ('password_ctrl', 'password', self.tr('Password'), ''),
            ('line_ctrl', 'databasedesc', self.tr('Database Description'), '')
        ]
        return (pgsql_view, "postgresql://", False)

    def mysql_conn(self):
        """
            创建MySQL的链接
            Returns:
                前端界面视图、使用引擎、是否完整
        """
        mysql_view = [
            ('line_ctrl', 'database', self.tr('Database Name'), ''),
            [
                ('line_ctrl', 'host', self.tr('Host Name/IP'), 'localhost'),
                ('line_ctrl', 'port', self.tr('Port'), '3306')
            ],
            ('line_ctrl', 'user', self.tr('User'), 'root'),
            ('password_ctrl', 'password', self.tr('Password'), ''),
            ('line_ctrl', 'databasedesc', self.tr('Database Description'), '')
        ]
        return (mysql_view, "mysql+pymysql://", False)


if __name__ == "__main__":
    dbConn = DatabaseConn()
    a = dbConn.create_conn("MySQL")
    b = dbConn.create_conn("PgSQL")
    print(a, b)
    error = dbConn.create_conn("Mysql")
