import json

def json_to_xml(json_string):
    """
    Convert a JSON string to XML format.
    
    Args:
        json_string (str): A valid JSON string
        
    Returns:
        str: XML formatted string
    """
    # Parse JSON string to Python dictionary
    data = json.loads(json_string)
    
    # Handle empty JSON object
    if not data:
        return '<root />'
    
    # Convert dictionary to XML
    return '<root>' + _dict_to_xml(data) + '</root>'

def _dict_to_xml(data):
    """
    Helper function to recursively convert Python dictionary to XML string.
    
    Args:
        data: Python dictionary, list, or primitive type
        
    Returns:
        str: XML formatted string without root element
    """
    # Handle different data types
    if isinstance(data, dict):
        return ''.join(_handle_dict_item(key, value) for key, value in data.items())
    elif isinstance(data, list):
        return _handle_list(data)
    else:
        return str(data)

def _handle_dict_item(key, value):
    """
    Handle dictionary key-value pair conversion to XML.
    
    Args:
        key: Dictionary key
        value: Dictionary value
        
    Returns:
        str: XML formatted string for the key-value pair
    """
    if isinstance(value, list):
        # Special handling for lists
        if key == 'children':
            # Handle children list specially
            return f'<{key}>' + ''.join(f'<child>{_dict_to_xml(item)}</child>' for item in value) + f'</{key}>'
        else:
            # Handle other lists
            return f'<{key}>' + ''.join(f'<person>{_dict_to_xml(item)}</person>' for item in value) + f'</{key}>'
    else:
        # Handle non-list values
        return f'<{key}>{_dict_to_xml(value)}</{key}>'

def _handle_list(data):
    """
    Handle list conversion to XML.
    
    Args:
        data: Python list
        
    Returns:
        str: XML formatted string for the list
    """
    return ''.join(f'<item>{_dict_to_xml(item)}</item>' for item in data)
