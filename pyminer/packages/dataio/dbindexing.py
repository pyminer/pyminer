# -*- coding:utf-8 -*-
# @Time: 2021/2/7 14:49
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: dbindexing.py
import os
import pickle
import socket
from typing import List

from widgets import create_file_if_not_exist


class DatabaseIndexer():
    def __init__(self):
        self.databases = {'mysql': {},
                          'postgresql': {},
                          'oracle': {}}
        self.reserved_databases = {'mysql': ['mysql', 'performance_schema', 'sys', 'information_schema']}
        self.load_database_index()

    def scan_db(self, db_type: str, host: str, port: int, user: str, passwd: str) -> bool:
        host = self.convert_host(host)
        if db_type == 'mysql':
            self.scan_mysql(host, port, user, passwd)
            return True
        else:
            return False

    def scan_mysql(self, host, port, user, passwd):
        import pymysql

        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd)
        cur = conn.cursor()
        cur.execute('show databases;')
        databases = [t[0] for t in cur.fetchall() if t[0] not in self.reserved_databases['mysql']]
        d = {}
        for database in databases:
            cur.execute('use %s;' % database)
            cur.execute("show tables;")
            d[database] = [table[0] for table in cur.fetchall()]
        cur.close()
        conn.close()
        self.databases['mysql'][(host, port)] = d

    def save_database_index(self):
        path = self.get_index_file_path()
        create_file_if_not_exist(path)
        with open(path, 'wb') as f:
            pickle.dump(self.databases, f)

    def load_database_index(self):
        path = self.get_index_file_path()
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    self.databases = pickle.load(f)
            except EOFError:
                pass

    def get_index_file_path(self) -> str:
        return os.path.join(os.path.expanduser('~'), '.pyminer', 'packages', 'dataio', 'databases.pkl')

    def get_databases(self, db_type: str, host: str, port: int) -> List[str]:
        host = self.convert_host(host)
        try:
            return list(self.databases[db_type][(host, port)].keys())
        except:
            import traceback
            traceback.print_exc()
            return []

    def get_tables(self, db_type: str, host: str, port: int, db_name: str) -> List[str]:
        host = self.convert_host(host)
        try:
            return self.databases[db_type][(host, port)][db_name]
        except KeyError:
            return []

    def convert_host(self, host_name) -> str:
        """
        TODO :地址转换需要时间，由于超时，所以这个问题需要解决,暂时没有任何作用。
        :param host_name:
        :return:
        """
        return host_name


if __name__ == '__main__':
    indexer = DatabaseIndexer()
    indexer.scan_mysql(host='127.0.0.1', port=3306, user='root', passwd='123456')
    indexer.save_database_index()
    print(indexer.get_databases('mysql', '127.0.0.1', 3306))
    print(indexer.get_tables('mysql', '127.0.0.1', 3306, 'monitor_data'))
