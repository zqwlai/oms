#-*-coding:utf-8-*-

import MySQLdb
from DBUtils.PooledDB import PooledDB
# 为返回字典格式推荐将连接池的cursorclass设置为它
from MySQLdb.cursors import DictCursor

class Mysql(object):
    __mysql_pool = None

    def __init__(self, host, port, username, password, db):
        self.conn = Mysql.__get_connection(host, port, username, password, db)
        self.cur = self.conn.cursor()

    @staticmethod
    def __get_connection(host, port, username, password, db):
        if not Mysql.__mysql_pool:
            Mysql.__mysql_pool = PooledDB(
                creator=MySQLdb,
                use_unicode=False,
                cursorclass=DictCursor,
                db=db,
                host=host,
                port=port,
                user=username,
                passwd=password,
                charset='utf8',
                mincached=1,    #最小空闲连接数
                maxcached=2,    #最大空闲连接数
                maxconnections=80    #最大连接数
            )

        # 返回连接池中连接对象
        return Mysql.__mysql_pool.connection()

    def query(self, sql, paramers=None):
        self.cur.execute(sql, paramers)
        alldata = self.cur.fetchall()
        self.close()
        return alldata

    def insert(self, sql, paramers=None):
        self.cur.execute(sql, paramers)
        self.conn.commit()
        insert_id =  self.get_insert_id()
        self.close()
        return insert_id

    def update(self, sql, paramers=None):
        self.cur.execute(sql, paramers)
        self.conn.commit()
        self.close()


    def delete(self, sql, paramers=None):
        self.cur.execute(sql, paramers)
        self.conn.commit()
        self.close()

    def get_insert_id(self):
        rs = self.query("SELECT LAST_INSERT_ID() AS lid")
        return rs[0]['lid']


    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
