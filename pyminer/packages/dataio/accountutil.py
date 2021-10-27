# -*- coding:utf-8 -*-
# @Time: 2021/2/7 9:52
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: accountutil.py
import pickle
import os
import socket
from typing import Dict, List, Union, Tuple, Optional
from widgets import create_file_if_not_exist


class DBAccountUtil():
    def __init__(self):
        self.connections: Dict[str, Dict] = {
            'mysql': {},
            'postgresql': {},
            'oracle': {}
        }  # {'host'<str>:{'port'<int>:[{'user':str,'passwd':str,'database':str,'table':str}]}}

        self.last_connection: Dict[str, Optional[Union[str, int]]] = {'mysql': None, 'postgresql': None, 'oracle': None}
        self.load_connections()

    def get_host_autocomp(self, db_type: str) -> List[str]:
        return list(set(self.connections[db_type].keys()))

    def get_users_and_dbs_autocomp(self, db_type: str, host: str, port: int) -> Tuple[List[str], List[str]]:
        host = self.convert_host(host)
        try:
            dic_list = self.connections[db_type][host][port]
            return list(set([dic['user'] for dic in dic_list])), list(set([dic['database'] for dic in dic_list]))
        except:
            import traceback
            traceback.print_exc()
            return [], []

    def get_tables_autocomp(self, db_type: str, host: str, port: int, db_name: str) -> List[str]:
        host = self.convert_host(host)
        try:
            dic_list = self.connections[db_type][host][port]
            return list(set([dic['table'] for dic in dic_list if dic['database'] == db_name]))
        except:
            import traceback
            traceback.print_exc()
            return []

    def get_passwd(self, db_type: str, host: str, port: int, user: str) -> str:
        host = self.convert_host(host)
        try:
            for connection in self.connections[db_type][host][port]:
                if connection['user'] == user:
                    return connection['passwd']
        except:
            return ''

    def add_connection(self, db_type: str, host: str, port: int, user: str, passwd: str, database: str, table: str):
        assert db_type in ['mysql', 'postgresql', ]
        assert isinstance(port, int) and 0 < port < 65536
        host = self.convert_host(host)

        self.last_connection[db_type] = {'host': host, 'port': port, 'user': user, 'passwd': passwd,
                                         'database': database, 'table': table}
        if not host in self.connections[db_type].keys():
            self.connections[db_type][host] = {}
        if not port in self.connections[db_type][host].keys():
            self.connections[db_type][host][port] = []
        connections = self.connections[db_type][host][port]
        for connection in connections:  # connection:{'user': 'hzy', 'passwd': '123123123', 'database': 'mydb', 'table': 'aaaaaa'}
            if connection['user'] == user and connection['passwd'] == passwd and connection[
                'database'] == database and connection['table'] == table:
                return
        self.connections[db_type][host][port].append(
            {'user': user, 'passwd': passwd, 'database': database, 'table': table})
        self.save_connections()

    def load_connections(self):
        conn_file = self.get_connection_file_path()
        if os.path.exists(conn_file):
            try:
                with open(conn_file, 'rb') as f:
                    connections = pickle.load(f)
                    self.connections = connections['connections']
                    self.last_connection = connections['last']
            except:
                import traceback
                traceback.print_exc()
                self.connections = {'mysql': {}, 'postgresql': {}, 'oracle': {}}
                self.last_connection = {'mysql': None, 'postgresql': None, 'oracle': None}

    def save_connections(self):
        conn_file = self.get_connection_file_path()
        create_file_if_not_exist(conn_file)
        with open(conn_file, 'wb') as f:
            pickle.dump({'connections': self.connections, 'last': self.last_connection}, f, protocol=3)

    def get_connection_file_path(self):
        return os.path.join(os.path.expanduser('~'), '.pyminer', 'packages', 'dataio', 'connections.pkl')

    def get_last_connection(self, db_type: str):
        print(self.last_connection)
        return self.last_connection[db_type]

    def convert_host(self, host_name: str) -> str:
        return host_name


if __name__ == '__main__':
    dbau = DBAccountUtil()
    dbau.add_connection('mysql', '127.0.0.1', 3306, 'hzy', '123123123', 'mydb', 'aaaaaa')
    dbau.save_connections()
