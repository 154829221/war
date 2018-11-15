# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
# #获取 XML 文档对象 ElementTree
# tree = ET.parse('example.xml')
# #获取 XML 文档对象的根结点 Element
# root = tree.getroot()
# #打印根结点的名称
# # print root.tag
#
# xml_str = ET.tostring(root)
# # print xml_str
# root = ET.fromstring(xml_str)
# # print root.tag

data = ET.Element('data')
country = ET.SubElement(data, 'country')
country.attrib['name'] = '魏'
state1 = ET.SubElement(country, 'state')
state1.attrib['name'] = '兖州'
state2 = ET.SubElement(country, 'state')
state2.attrib['name'] = '幽州'
county = ET.SubElement(state1, 'county')

xml_str = ET.tostring(data, encoding='utf-8')

#生成树并存放
tree = ET.ElementTree(data)
tree.write('example1.xml', encoding='UTF-8')

# # 获取 XML 文档对象 ElementTree
# tree = ET.parse('example.xml')
# # 获取 XML 文档对象的根结点 Element
# root = tree.getroot()
# # print root.tag
# # 递归查找所有的 neighbor 子结点
# # for neighbor in root.iter('neighbor'):
# #     print neighbor.attrib

# for country in root.findall('country'):
#     rank = country.find('rank').text
#     name = country.get('name')
#     print name, rank