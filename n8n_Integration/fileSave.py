from flask import Flask, request, jsonify
#from flask_httpauth import HTTPBasicAuth
import os
import re
import json
import time
import subprocess
import signal

app = Flask(__name__)
#auth = HTTPBasicAuth()

# Define valid username and password (in a real-world scenario, use environment variables or a database)
USER_DATA = {
    "testerLLM": "testerLLMPass"  # Replace with a secure username and password
}

# Helper function to validate file name
def is_valid_filename(filename):
    # Ensure the filename does not contain any invalid characters or relative path components
    if re.search(r'[\\:*?"<>|]', filename):  # Check for invalid characters
        return False
    if ".." in filename or "\\" in filename or filename.startswith("/"):  # Check for absolute paths
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
        os.makedirs("files", exist_ok=True)  # Ensure the "files" directory exists
        with open(file_name, 'w') as file:
            file.write(file_content)
        
        return jsonify({"message": f"File '{file_name}' saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def build_directory_structure(root_dir):
    """
    Recursively builds a hierarchical JSON representation of the directory structure.
    """
    result = {"name": os.path.basename(root_dir), "type": "directory", "children": []}
    
    for entry in os.listdir(root_dir):
        app.logger.info(entry)
        full_path = os.path.join(root_dir, entry)
        
        if os.path.isdir(full_path):
            # If it's a directory, recurse into it
            # unless it is __pycache__ or .git
            if entry != "__pycache__" and entry != ".git":
                result["children"].append(build_directory_structure(full_path))
        elif os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as file:
                content = file.read()
            result["children"].append({
                "name": entry,
                "type": "file",
                "content": content
            })
    
    return result

@app.route('/get-directory-json', methods=['GET'])
# @auth.login_required  # Protect this endpoint with Basic Auth
def get_directory_json():
    """
    HTTP GET endpoint to retrieve the directory structure as JSON.
    Expects a 'path' query parameter specifying the root directory.
    """
    root_dir = request.args.get('path')
    
    if not root_dir or not os.path.isdir(root_dir):
        return jsonify({"error": "Invalid or missing 'path' parameter"}), 400
    
    try:
        directory_structure = build_directory_structure(root_dir)
        filesAndFolders = {
            "filesAndFolders": directory_structure
        }
        return jsonify(filesAndFolders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-script', methods=['GET'])
def run_script():
    script = request.args.get('fileName')
    
    if not script:
        return jsonify({"error": "Missing 'fileName' parameter"}), 400
    
    try:
        # Open a file to write the script output
        with open("script_output.log", "w") as log_file:
            # Start the Python script in the background
            # print(f"conda activate tests; python {script}")
            # process = subprocess.Popen(['bash',"-c",f"conda activate tests; python {script}"] , shell=False)
            
            # time.sleep(15)
            # # Run pytest
            pytest_result = subprocess.run("pytest --json-report ./SimpleTest/", shell=True)
            
            # time.sleep(5)
            # Terminate the background script
            # os.kill(process.pid, signal.SIGINT)
            
            time.sleep(1)

            # run SimpleTest/format_test_results.py
            pytest_result = subprocess.run("python ./SimpleTest/format_test_results.py", shell=True)

            time.sleep(1)
            with open("failed_tests.json", "r") as file:
                return jsonify(json.load(file)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)