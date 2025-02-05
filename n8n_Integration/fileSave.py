from flask import Flask, request, jsonify
#from flask_httpauth import HTTPBasicAuth
import os
import re

app = Flask(__name__)
#auth = HTTPBasicAuth()

# Define valid username and password (in a real-world scenario, use environment variables or a database)
USER_DATA = {
    "testerLLM": "testerLLMPass"  # Replace with a secure username and password
}

# Helper function to validate file name
def is_valid_filename(filename):
    # Ensure the filename does not contain any invalid characters or relative path components
    if re.search(r'[\\/*?:"<>|]', filename):  # Check for invalid characters
        return False
    if ".." in filename or "/" in filename or "\\" in filename:  # Check for relative paths
        return False
    return True

# Verify user credentials
# @auth.verify_password
# def verify_password(username, password):
#     print(username, password)
#     if username in USER_DATA and USER_DATA[username] == password:
#         return username

@app.route('/upload', methods=['POST'])
# @auth.login_required  # Protect this endpoint with Basic Auth
def upload_file():
    try:
        # Parse JSON data from the request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Extract fileName and fileContent from the request body
        file_name = data.get("fileName")
        file_content = data.get("fileContent")

        if not file_name or not file_content:
            return jsonify({"error": "Both 'fileName' and 'fileContent' are required"}), 400

        # Validate the file name
        if not is_valid_filename(file_name):
            return jsonify({"error": "Invalid file name. File name must not contain relative paths or invalid characters."}), 400

        # Save the file to the local directory
        with open(file_name, 'w') as file:
            file.write(file_content)

        return jsonify({"message": f"File '{file_name}' saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
