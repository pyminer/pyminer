from typing import Dict, List

from utils.io.dbconnect.dbBaseTool import *


def create_engine():
    dbCA = dbConnectAccountTool()
    dbCA.pklroad = os.path.join(os.path.dirname(__file__), 'dbConnectAccount.pkl')

    mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    dbtype, connectname = "mysql", "testaccount"
    dbCA.attachConnetName(dbtype, connectname)
    account = dbCA.getConnectAccount()
    print(account)
    mysql = dbFuncTool(account=account, conn_url=mysql_url)
    print(mysql.dbCT.engine)


def create_account(account_name, account, dbtype='mysql'):
    dbtype, connectname = dbtype, account_name
    dbCA = dbConnectAccountTool()
    dbCA.pklroad = os.path.join(os.path.dirname(__file__), 'dbConnectAccount.pkl')
    dbCA.loadConnectAccount()
    dbCA.attachConnetName(dbtype, connectname)

    dbCA.updateConnectAccount(account)
    dbCA.loadConnectAccount()
    print(dbCA.dbconnectaccount)


def get_all_accounts() -> Dict[str, List[str]]:
    dbCA = dbConnectAccountTool()
    dbCA.pklroad = os.path.join(os.path.dirname(__file__), 'dbConnectAccount.pkl')
    dbCA.loadConnectAccount()
    return dbCA.dbconnectaccount


# def get_all_accounts_names()->Dict[str,List[str]]:
#     return {dbtype: [conn_name for conn_name in content.keys()] for dbtype, content in dbCA.dbconnectaccount.items()}

def get_all_accounts_list() -> List[str]:
    accounts_dic = get_all_accounts()
    accounts_dic = {dbtype: [conn_name for conn_name in content.keys()] for dbtype, content in accounts_dic.items()}
    accounts = []
    for dbtype in accounts_dic.keys():
        for name in accounts_dic[dbtype]:
            accounts.append(dbtype + '-' + name)
    print(accounts)
    return accounts


def connect_to_database(conn_name: str, dbtype='mysql') -> dbFuncTool:
    dbCA = dbConnectAccountTool()
    dbCA.pklroad = os.path.join(os.path.dirname(__file__), 'dbConnectAccount.pkl')
    mysql_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    dbCA.attachConnetName(dbtype, conn_name)
    account = dbCA.getConnectAccount()
    mysql = dbFuncTool(account=account, conn_url=mysql_url)
    return mysql


def query(sql_engine: dbFuncTool, query: str):
    return sql_engine.execute(sql=query)


if __name__ == '__main__':
    # stat = 'get_all_accounts'
    # stat = 'get_all_accounts_list'
    # stat = 'connect'
    stat = 'query'
    if stat == 'create_account':
        connectaccount = dict(
            account=dict(
                user="root", password="123456", host="localhost",
                port="3306", database="learning", charset="utf-8"
            ),
            usessh=False,
            SSH={},
            connectdescribe="这又是一个测试"
        )
        create_account('hzy_account', connectaccount)
        connectaccount = dict(
            account=dict(
                user="gandw", password="123456", host="localhost",
                port="3306", database="local_db", charset="utf-8"
            ),
            usessh=False,
            SSH={},
            connectdescribe="这又是一个测试"
        )
        create_account('gandw', connectaccount)
    elif stat == 'get_all_accounts':
        print(get_all_accounts())
    elif stat == 'get_all_accounts_list':
        print(get_all_accounts_list())
    elif stat == 'connect':
        print(connect_to_database('hzy_account', 'mysql'))
    elif stat == 'query':
        engine = connect_to_database('hzy_account', 'mysql')
        print(engine, query(engine, 'select * from scores').get('data'))
