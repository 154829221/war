# -*- coding: utf-8 -*-
import sys


from flask import Flask
from dbtools import *
from route import *

if __name__ == '__main__':
    #获取数据库链接池
    err = dbConn()
    if err != None:
        print"Connet to mysql error: %s" % err
        exit(2)
    else:
        #将数据库操作限制在dbtools包内。
        #dbhanle=dh.MysqlHandle(dbconn)
        app.run(host='0.0.0.0')

