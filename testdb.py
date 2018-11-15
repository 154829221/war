# -*- coding: utf-8 -*-
from dbtools import db
from dbtools import dbhandle as dh 

def getConn():
    try:
        dbconn=db.Mysql()
    except Exception,e:
        return None,e
    return dbconn,None



if __name__ == "__main__":
    #获取数据库链接池
    dbconn, err = getConn()
    if err != None:
        print"Connet to mysql error: %s" % err
        exit(2)
    else:
        dbhandle=dh.MysqlHandle(dbconn)
        statStatus=dbhandle.getStatStatus()
        print(statStatus)
        exit(0)
