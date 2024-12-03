import json
from json_to_xml_api import json_to_xml

# Sample JSON data
json_data = json.dumps({
    # "name": "John",
    # "age": 30,
    # "city": "New York"
})


# Convert JSON to XML
xml_data = json_to_xml(json_data)

# Print the XML data
print(xml_data)