# -*- coding: UTF-8 -*-

import config
import sys


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class MysqlHandle(object):
    #连接池对象
    __pool = None
    def __init__(self,conn):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
        self._conn = conn

    def get_conn(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        try:
            sql = "select state_id,country.name as country,state.name as state ,county.name as  county,sum(develop_point) from county,state,country where  county.state_id = state.id and county.country_id=country.id GROUP BY state ORDER BY SUM(develop_point);"
            dbresult = self._conn.getAll(sql)
        except Exception, err1:
            print("Run sql (%s) error: %s" % sql, err1)
            return None,err1
        else:
            return dbresult,None

    def getStatStatus(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        try:
            sql = "select state_id,country.name as country,state.name as state ,county.name as  county,sum(develop_point) from county,state,country where  county.state_id = state.id and county.country_id=country.id GROUP BY state ORDER BY SUM(develop_point);"
            dbresult = self._conn.getAll(sql)
        except Exception, err1:
            print("Run sql (%s) error: %s" % sql, err1)
            return None,err1
        else:
            return dbresult,None
