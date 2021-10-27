# -*- coding: utf-8 -*-
"""
日期：2020-09-21
作者: gandaiwei

说明：
    dbConnectAccountTool -> 连接账号管理工具
    dbConnectTool -> 连接通道工具
    dbFuncTool -> SQL命令处理工具

"""
import time



import pickle
import os
class dbConnectAccountTool(object):
    """
        数据库链接，账号处理。

        注意：
            创建以后，需要优先执行 LoadAccount
    """

    def __init__(self):

        self.pklroad = ".\dbConnectAccount.pkl"
        self.dbconnectaccount = {}
        self.dbtype = ""
        self.connectname = ""

    def attachConnetName(self, dbtype="", connectname=""):
        """
            参数：
                【1】 dbtype(str)：数据库类型
                【2】 connectname(str)：链接的名称，用户填写，用于区分同一个数据库下的不同链接
        """
        self.dbtype = dbtype
        self.connectname = connectname

    def getConnectAccountSSH(self):
        """
            提取SSH信息
        """
        CA = self.getConnectAccount()
        ssh = CA["SSH"]
        account = CA["account"]
        return (
        account["host"], account["port"], ssh["ssh_host"], ssh["ssh_port"], ssh["ssh_username"], ssh["ssh_password"])

    def getConnectAccount(self):
        """
            用途：
                获取连接
            返回结果：
                连接的账号，IP，port，password, SSH 等
        """
        self.loadConnectAccount()
        connectaccount = self.dbconnectaccount[self.dbtype].get(self.connectname)
        return (connectaccount)

    def getConnectAccountDesc(self):
        """
            用途：
                获取连接的信息列表（connectname 和 desc）
            返回结果：
                字典格式，数据结构：{dbtype:{connectname: desc}}
        """
        self.loadConnectAccount()
        res = {}
        for k, v in self.dbconnectaccount.items():
            res.update({k: {}})
            for vk, vv in v.items():
                res[k].update({vk: vv.get("connectdescribe")})
        return (res)

    def delConnectAccount(self):
        """
            用途：
                删除链接通道
            注意：
                前端需要验证是否有选择需要删除的链接
        """
        del self.dbconnectaccount[self.dbtype][self.connectname]
        self.writeConnectAccount()

    def updateConnectAccount(self, connectaccount={}):
        """
            用途：
                新增（更新）连接通道
            参数：
                【3】 connectaccount(dict)：账号的信息，包括用户，密码，地址等，对应的JSON结构：
            注意：上游传入的 connectaccount 结构说明：
                【1】account(json) -> 账号信息
                |- （1）user = 用户 （2）password = 密码   （3）host = 地址
                |- （4）port = 端口 （5）database = 数据库 （6）charset = 字符集

                【2】usessh(boolean) -> 是否使用 SSH 加密通道，默认为 False，表示不使用该通道
                    暂时实现了 SSH 加密通道使用密码加密的方法

                【3】SSH(dict) -> SSH加密通道
                |- （1）ssh_host = 地址 （2）ssh_port = 端口 （3）ssh_username = 用户名
                |- （4）ssh_authenmethod = 加密模式（5）ssh_password = 密码

                【4】 connectdescribe(str) -> 对连接的描述，前端传入时默认为空字符串
        """
        if self.dbtype not in self.dbconnectaccount:
            self.dbconnectaccount.update(dbtype={})

        self.dbconnectaccount[self.dbtype].update({self.connectname: connectaccount})
        # 如果连接不存在，则直接新增；
        # 前端需要检验并提醒是否有同名连接，如果同名会覆盖
        self.writeConnectAccount()

    def writeConnectAccount(self):
        with open(self.pklroad, 'wb') as wfile:
            pickle.dump(self.dbconnectaccount, wfile)
        wfile.close()

    def loadConnectAccount(self):
        """
            用途：
                从 pickle 文件中获取链接账号数据
            返回：
                dbConnectAccount(dict)：连接账号集合，数据结构：{数据库类型:{名称: {连接账号信息}}}
        """
        if not os.path.exists(self.pklroad):
            # 如果文件不存在，则创建一个测试用账号写入到 pkl 文件中
            testdt = dict(
                account=dict(
                    user="root", password="", host="localhost",
                    port="3306", database="", charset="utf-8"
                ),
                usessh=False,
                SSH={},
                connectdescribe="这是一个测试模块"
            )
            self.dbconnectaccount = {"mysql": {"testdt": testdt}}
            self.writeConnectAccount()

        with open(self.pklroad, 'rb') as rfile:
            self.dbconnectaccount = pickle.load(rfile)
        rfile.close()


class dbConnectTool(object):
    """
        数据库通用连接工具
    """

    def __init__(self, account, conn_url):
        """
            参数：
                【1】 account(class)：dbConnectAccountTool(dbtype, connectname)
                【2】 conn_url(str)：通过 url 方式连接数据库
        """
        self.account = account
        self.conn_url = conn_url

    def createSSHConn(self):
        """
            开启 SSH 连接方式
        """
        from sshtunnel import SSHTunnelForwarder
        ssh = self.account["SSH"]
        account = self.account["account"]
        self.ssh_server = SSHTunnelForwarder(
            (ssh["ssh_host"], ssh["ssh_port"]),
            ssh_username=ssh["ssh_username"],
            ssh_password=ssh["ssh_password"],
            remote_bind_address=(account["host"], account["port"])
        )
        self.ssh_server.start()
        self.account["port"] = str(self.ssh_server.local_bind_port)

    def createConn(self):
        """
            用途：
               通过 url 的方式创建连接通道
            参数：
                conn_url：连接url，由数据类型进行定义

            注意：
                暂时没有实现SSL的方法
        """
        from sqlalchemy import create_engine
        try:
            if self.account["usessh"]:
                self.createSSHConn()
            url = self.conn_url.format(**self.account["account"])
            print(url)
            self.engine = create_engine(url, encoding="utf-8")
            conn_status = {"status": "connect", "info": ""}
        except Exception as e:
            import traceback
            traceback.print_exc()
            conn_status = {"status": "error", "info": e}

        return (conn_status)

    def closeConn(self):
        """
            关闭所有通道
        """
        if self.account["usessh"]:
            self.ssh_server.close()


class dbFuncTool(object):
    """
        数据库通用执行方法
    """

    def __init__(self, account, conn_url):
        self.dbCT = dbConnectTool(account=account, conn_url=conn_url)
        self.conn_status = self.dbCT.createConn()

    def execute(self, sql):
        """
            执行命令，需要增加一个装饰器，关于运行时间的装饰器
            返回结果：
                字典结构，包含内容：
                （1）data(pd.dataframe)：数据
                （2）execute_status(str)：查询结果状态，done = 正常；error = 报错
                （3）info(str)：返回信息。GetData = 返回数据，需要呈现；ExecuteSQL = 执行命令，不用呈现
        """
        import pandas as pd
        try:
            conn = self.dbCT.engine.execute(sql)
            if conn.cursor.description:
                df = pd.DataFrame(
                    data=list(conn.cursor.fetchall()),
                    columns=list(map(lambda x: x[0], conn.cursor.description))
                )
                res = {"data": df, "execute_status": "done", "info": "GetData"}
            else:
                df = pd.DataFrame([])
                res = {"data": df, "execute_status": "done", "info": "ExecuteSQL"}
            conn.close()
        except Exception as e:
            res = {"data": pd.DataFrame([]), "execute_status": "error", "info": str(e)}

        self.dbCT.closeConn()
        return (res)

    # "mysql": "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    # "pgsql": "postgresql://{user}:{password}@{host}:{port}/{database}"

# if __name__ == "__main__":
