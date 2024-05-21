import xml.etree.ElementTree as ET

def write_xml(data, file_path):
    tree = ET.ElementTree(ET.fromstring(data))
    tree.write(file_path)