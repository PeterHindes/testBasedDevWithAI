import google.generativeai as genai
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('APIKEY')

# Configure the generative AI model with the API key
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
project_folder = './project'


prompt = 'Implement just the functions under test, return the functions so we can insert it into main.go, do not return any of the test file/test cases. No explanation or anything other than code.'
status = False
while not status:
    for filename in os.listdir(project_folder):
        filepath = os.path.join(project_folder, filename)
    if os.path.isfile(filepath) and filename != 'main.go':
        with open(filepath, 'r') as file:
            content = file.read()
            extension = filename.split('.')[-1]
            prompt += f'{filename}\n```{extension}\n{content}\n```\n'

    response = model.generate_content(prompt)
    outStr = response.text
    # print(outStr)

    # now we take the returned file, remove the code tag lines
    # print('\n\n\nSplit\n\n\n')
    # print(outStr.split('```'))
    nosr = outStr.split('```')[1][2:]
    # print(nosr)

    outLines = ''
    with open('./project/main.templ', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line == '// code block start\n':
                outLines += nosr
                pass
            outLines += line
    if 'package main' in nosr:
        with open('./project/main.go', 'w') as file:
            file.write(nosr)
    else:
        with open('./project/main.go', 'w') as file:
            file.write(outLines)


    # run the go test command to test the new main.go file check return code and if it is 0 then the tests passed else print the error
    #change directory to the project folder
    os.chdir('./project')
    tests = subprocess.run(['go', 'test'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    status = tests.find('FAIL') == -1
    print(tests)

    os.chdir('..')

    # print(testResults)
