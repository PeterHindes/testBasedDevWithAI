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
    
    def _build_xml(obj, parent_tag=None):
        """
        Recursively build XML string from Python object
        
        Args:
            obj: Python object (dict, list, str, int, etc.)
            parent_tag: The parent tag name for context
            
        Returns:
            str: XML formatted string
        """
        # Handle empty dictionary
        if not obj and isinstance(obj, dict):
            return '<root />'
            
        # Handle dictionary
        if isinstance(obj, dict):
            parts = []
            for key, value in obj.items():
                # Handle nested content
                xml_content = _build_xml(value, key)
                parts.append(f'<{key}>{xml_content}</{key}>')
            
            # If this is the top level, wrap in root tags
            if parent_tag is None:
                return f'<root>{"".join(parts)}</root>'
            return "".join(parts)
            
        # Handle lists (collections)
        if isinstance(obj, list):
            parts = []
            # Determine the singular form for special collections
            singular_tag = 'person' if parent_tag == 'people' else 'child' if parent_tag == 'children' else parent_tag
            
            for item in obj:
                xml_content = _build_xml(item, singular_tag)
                parts.append(f'<{singular_tag}>{xml_content}</{singular_tag}>')
            return "".join(parts)
            
        # Handle primitive values (strings, numbers, etc.)
        return str(obj)
    
    return _build_xml(data)
