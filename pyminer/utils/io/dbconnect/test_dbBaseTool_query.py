from utils.io.dbconnect.dbBaseTool import *

dbCA = dbConnectAccountTool()
dbCA.pklroad = ".\dbConnectAccount.pkl"

mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
dbtype, connectname = "mysql", "testaccount"
dbCA.attachConnetName(dbtype, connectname)
account = dbCA.getConnectAccount()
print(account)
mysql = dbFuncTool(account=account, conn_url=mysql_url)
print(mysql.dbCT.engine)

df = mysql.execute(sql="select * from scores")
print(df['execute_status'])
print(df['data'])

