import json
from ast import literal_eval

# Load the JSON data
with open('.report.json') as f:
    data = json.load(f)

failed_tests = []

for test in data.get('tests', []):
    if test.get('outcome') == 'failed':
        nodeid = test.get('nodeid', '')
        call = test.get('call', {})
        crash = call.get('crash', {})
        
        # Extract message from crash.message, fallback to longrepr if missing
        message = crash.get('message', '')
        if not message:
            message = call.get('longrepr', '')
        
        failed_tests.append({
            'nodeid': nodeid,
            'message': message
        })

# Output the result
print(json.dumps(failed_tests, indent=2))

# Save the result to a file
with open('failed_tests.json', 'w') as f:
    json.dump(failed_tests, f, indent=2)