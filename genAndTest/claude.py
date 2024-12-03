import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# print(api_key)

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api_key,
)
with open("../python/test_json_to_xml_api.py", "r") as file:
    test_code = file.read()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        # model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        system="Your task is to create Python functions based on the provided unit tests. The requests will describe the desired functionality of the function, including the input parameters and expected return value. Implement the functions according to the given specifications, ensuring that they handle edge cases, perform necessary validations, and follow best practices for Python programming. Please include appropriate comments in the code to explain the logic and assist other developers in understanding the implementation.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ('Implement this program based on the following unit tests: ' + test_code)
                        ,
                    }
                ],
            }
        ],
    )
print(message.content[0].text.replace("\\n", "\n").split("```python\n")[1].split("```")[0])

with open("../python/json_to_xml_api.py", "w") as file:
    file.write(message.content[0].text.replace("\\n", "\n").split("```python\n")[1].split("```")[0])


import ctest
ctest.run_tests()