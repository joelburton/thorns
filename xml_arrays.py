import xml.etree.ElementTree as ET
tree = ET.parse('gameinfo.dbg')
for arr in tree.findall('.//array'):
    ET.dump(arr)
