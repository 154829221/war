# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

tree = ET.parse('country_data.xml')
root = tree.getroot()
#root = ET.fromstring(country_data_as_string)
for child in root:
    print(child.tag, child.attrib)
print root[0][3].text
print root[0][3].attrib
print root[0][3].attrib['direction']

for neighbor in root.iter('neighbor'):
    print(neighbor.attrib)
for neighbor in root.iter('year'):
    print(neighbor.text)

#对新加破的rank值进行则增加20的操作。#修改属性值
for country in root.findall('country'):
    rank = country.find('rank')
    if country.get('name') == 'Singapore':
        new_rank = int(rank.text) + 20
        rank.text = str(new_rank)
        rank.set('updated', 'no')
        rank.set('dead', 'yes')
    name = country.get('name')
    print(name, rank.text)

#将rank值又各自加1
for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    #修改属性值
    rank.set('updated', 'no')
tree.write('output.xml')

#根据限制条件，将其中rank大于50的所在的country删除掉了。
for country in root.findall('country'):
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)
tree.write('remove.xml')

#自行构建一个xml
a = ET.Element('level1')
b = ET.SubElement(a, 'level2-1')
c = ET.SubElement(a, 'level2-2')
d = ET.SubElement(c, 'level3')
d.text='200'
print ET.dump(a)
temp_d=d
c.remove(d)
f = ET.SubElement(c, 'level3')
temp_d.tag='level4'
temp_d.text='200'
g = ET.SubElement(f,temp_d.tag)
g.text='200'

print ET.dump(a)
a.write('buid.xml')

# -->a
#  -->b
#  -->c
#   -->d
# for child in c:
#     print(child)

# print ET.dump(temp_d)