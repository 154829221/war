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

def state_status(stat_status):
    ss = ET.Element('stat_status')
    tree = ET.ElementTree(ss)

    for i in stat_status:
        sscountry = ET.SubElement(ss, 'data')
        sscountry.set('country', str(i["country"]))
        sscountry.set('state', str(i["state"]))
        sscountry.text=str(i["sum(develop_point)"])

    tree.write('template/stat_status.xml',encoding="UTF-8",xml_declaration=True)

    response = make_response(open('template/stat_status.xml').read())
    response.headers["Content-type"] = "text/xml"
    return  response