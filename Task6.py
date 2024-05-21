import xml.etree.ElementTree as ET

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return ET.tostring(root, encoding='unicode')