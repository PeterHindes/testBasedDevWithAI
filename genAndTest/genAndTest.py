import ollama
import os

# create a prompt by reading in the files from the ./project folder
prompt = 'Implement just the runlengthEncode function, only return the function so we can insert it into main.go, do not return any of the test file/test cases. No explanation or anything other than code.'
project_folder = './project'
for filename in os.listdir(project_folder):
  filepath = os.path.join(project_folder, filename)
  if os.path.isfile(filepath) and filename != 'main.go':
    with open(filepath, 'r') as file:
      content = file.read()
      extension = filename.split('.')[-1]
      prompt += f'{filename}\n```{extension}\n{content}\n```\n'

stream = ollama.chat(
  model='llama3.2',
  messages=[{'role': 'user', 'content': prompt}],
  stream=True
)

outStr = ''
for chunk in stream:
  # print(type (chunk).__name__) # dict
  outStr += chunk['message']['content']
  print(chunk['message']['content'], end='', flush=True)

# now we take the returned file, remove the code tag lines
print('\n\n\nSplit\n\n\n')
# print(outStr.split('```'))
nosr = outStr.split('```')[1][2:]
print(nosr)

# write the nosr string out to the file by replacing the line // runlengthEncode from the main.templ file and writing that to main.go
# read all the lines from the main.templ file
print('reading main.templ')
outLines = ''
with open('./project/main.templ', 'r') as file:
  lines = file.readlines()
  for line in lines:
    if line == '// runlengthEncode\n':
      outLines += nosr
      pass
    outLines += line
print(outLines)

# replace the contents of main.go
print('writing main.go')
with open('./project/main.go', 'w') as file:
  file.write(outLines)


# run the go test command to test the new main.go file
# testResults = os.system('cd ./project ; go test')

# print(testResults)

