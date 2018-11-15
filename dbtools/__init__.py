# -*- coding: UTF-8 -*-

from dbtools import db
from dbtools import dbhandle

def set_mysql_handle(conn):
    global DBconn
    DBconn=dbhandle.MysqlHandle(conn)


def get_mysql_handle():
    return DBconn

def dbConn():
    try:
        dbconn=db.Mysql()
        set_mysql_handle(dbconn)
    except Exception,e:
        return e
    return None