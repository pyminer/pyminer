import os
from dbBaseTool import *

def split_print(dt):
    print(dt)
    print("=" * 50)

dbCA = dbConnectAccountTool()
dbCA.pklroad = ".\dbConnectAccount.pkl"

# 模拟打开数据库模块后，选择需要连接的方案：
desc = dbCA.getConnectAccountDesc()
split_print(desc)

# 模拟获取某个账号的信息、SSH账号等信息
dbtype, connectname = "mysql", "testdt"
dbCA.attachConnetName(dbtype, connectname)
account = dbCA.getConnectAccount()
split_print(account)

# 模拟增加（或更新）一个新的连接
dbtype, connectname = "mysql", "testaccount"
dbCA.attachConnetName(dbtype, connectname)
connectaccount = dict(
    account=dict(
        user="gandw", password="123456", host="localhost",
         port="3306", database="local_db", charset="utf-8"
    ),
    usessh=False,
    SSH={},
    connectdescribe="这又是一个测试"
)
dbCA.updateConnectAccount(connectaccount)
dbCA.loadConnectAccount()
split_print(dbCA.dbconnectaccount)

# 模拟数据库的 "测试连接"
mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
dbtype, connectname = "mysql", "testaccount"
dbCA.attachConnetName(dbtype, connectname)
account = dbCA.getConnectAccount()
dbCT = dbConnectTool(account = account, conn_url = mysql_url)
connect_status = dbCT.createConn()
split_print(connect_status)

# 模拟一个查询操作(mysql)
mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
dbtype, connectname = "mysql", "testaccount"
dbCA.attachConnetName(dbtype, connectname)
account = dbCA.getConnectAccount()
mysql = dbFuncTool(account = account, conn_url = mysql_url)
print(mysql.dbCT.engine)
df = mysql.execute(sql = "select * from mysql.use")
print(df['execute_status'])
print(df['data'])

df2 = mysql.execute(sql = "select * from mysql.user")
print(df["data"])

# 模拟删除一个连接
dbtype, connectname = "mysql", "testaccount"
dbCA.attachConnetName(dbtype, connectname)
dbCA.delConnectAccount()
dbCA.loadConnectAccount()
# split_print(dbCA.dbconnectaccount)
