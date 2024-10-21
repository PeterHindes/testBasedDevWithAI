import google.generativeai as genai
import os
import subprocess

genai.configure(api_key="AIzaSyBuw3X-nyaBa86qdT7jyraJWqYG6fmSVms")

model = genai.GenerativeModel("gemini-1.5-flash")
project_folder = './project'

files = ''
for filename in os.listdir(project_folder):
    filepath = os.path.join(project_folder, filename)
    if os.path.isfile(filepath) and filename != 'main.go':
        with open(filepath, 'r') as file:
            content = file.read()
            extension = filename.split('.')[-1]
            text = f'-- {filename}\n\n```{extension}\n{content}\n```\n\n'
            files += text
def is_content_dict(d):
    return "parts" in d

print(is_content_dict({"role": "user", "parts": [{"text": files}]}))

chat = model.start_chat(
    history=[
        {"role": "system", "content": "Implement just the functions under test, return the functions so we can insert it into main.go, do not return any of the test file/test cases. No explanation or anything other than code."},
        {"role": "user", "parts": [{"text": files}]}
    ]
)


exit()


# prompt = 'Implement just the functions under test, return the functions so we can insert it into main.go, do not return any of the test file/test cases. No explanation or anything other than code.'
status = False
response = chat.send_message("Ok, generate the code.")
while not status:
    outStr = response.text
    nosr = outStr.split('```')[1][2:]

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
    
    if status:
        break

    response = chat.send_message(tests+'\nFix the code and test again.')
