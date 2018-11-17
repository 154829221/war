# -*- coding: UTF-8 -*-

import config
import sys
import xml.etree.ElementTree as ET
from flask import Flask
from flask import render_template
from flask import make_response

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)

def query_db(stat_status):
    rv= [row for row in stat_status[0]]
    return rv if rv else None

def state_status(stat_status):
    ss = ET.Element('stat_status')
    tree = ET.ElementTree(ss)
    query_status=query_db(stat_status)
    if query_status == None:
        return "获取周县数据失败！"
    for status in query_db(stat_status):
        sscountry = ET.SubElement(ss, 'data')
        sscountry.set('country', str(status["country"]))
        sscountry.set('state', str(status["state"]))
        sscountry.text=str(status["sum(develop_point)"])
    print 'templates/stat_status.xml'
    tree.write('templates/stat_status.xml',encoding="UTF-8",xml_declaration=True)

    response = make_response(open('templates/stat_status.xml').read())
    response.headers["Content-type"] = "text/xml"
    return  response

