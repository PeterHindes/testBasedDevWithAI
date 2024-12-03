# As you will see this is a test file for the json_to_xml function. The function must return the xml and if there is a collection it will use one of two names that are the non plural, specifically child for children or person for people.

import unittest
import json
from json_to_xml_api import json_to_xml  # Assuming the function to be tested is in json_to_xml_api.py

class TestJsonToXmlAPI(unittest.TestCase):

    def test_json_to_xml(self):
        test_cases = [
            (json.dumps({}), '<root />'),
            (json.dumps({"name": "John", "age": 30}), '<root><name>John</name><age>30</age></root>'),
            (json.dumps({"person": {"name": "John", "age": 30}}), '<root><person><name>John</name><age>30</age></person></root>'),
            (json.dumps({"people": [{"name": "John"}, {"name": "Jane"}]}), '<root><people><person><name>John</name></person><person><name>Jane</name></person></people></root>'),
            (json.dumps({
                "person": {
                    "name": "John",
                    "age": 30,
                    "children": [
                        {"name": "Jane", "age": 10},
                        {"name": "Doe", "age": 5}
                    ]
                }
            }), '<root><person><name>John</name><age>30</age><children><child><name>Jane</name><age>10</age></child><child><name>Doe</name><age>5</age></child></children></person></root>')
        ]

        for json_data, expected_xml in test_cases:
            with self.subTest(json_data=json_data):
                result = json_to_xml(json_data)
                self.assertEqual(result, expected_xml)

if __name__ == '__main__':
    unittest.main()
