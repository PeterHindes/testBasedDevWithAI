import json
import xml.etree.ElementTree as ET

def json_to_xml(json_data):
    """
    Converts a JSON string to an XML string.

    Args:
        json_data (str): A JSON-formatted string.

    Returns:
        str: An XML string representation of the input JSON data.
    """
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input")

    root = ET.Element('root')
    _convert_to_xml(data, root)
    return ET.tostring(root, encoding='utf-8').decode('utf-8')

def _convert_to_xml(data, parent):
    """
    Recursively converts a Python dictionary or list to an XML structure.

    Args:
        data (dict or list): The input data to be converted to XML.
        parent (xml.etree.ElementTree.Element): The parent XML element.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                child = ET.SubElement(parent, key)
                _convert_to_xml(value, child)
            else:
                ET.SubElement(parent, key).text = str(value)
    elif isinstance(data, list):
        for item in data:
            child = ET.SubElement(parent, 'person')
            _convert_to_xml(item, child)
    else:
        parent.text = str(data)
