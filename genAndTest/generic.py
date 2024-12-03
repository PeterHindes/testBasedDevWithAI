import importlib
import builtins
import os
import argparse
from dotenv import load_dotenv

from unittest import TestLoader, TestResult
from pathlib import Path
import signal
import sys

FUNCTIONTOGENERATE = "kth_factor"
SYSTEMPROMPT = "Your task is to create Python functions based on the provided unit tests. Please make all comments and reasoning before providing the code. The requests will describe the desired functionality of the function, including the input parameters and expected return value. Implement the functions according to the given specifications, and follow best practices for Python programming. You must include appropriate comments in the code to explain the logic and assist other developers in understanding the implementation. If an error is provided, reason through the problem before you generate any changes and explain why you are making them."

def run_tests(justtest=False):
    # everything to ensure we are testing the latest version of the code
    # Reload any existing modules to ensure we're testing the latest version
    if FUNCTIONTOGENERATE in sys.modules:
        importlib.reload(sys.modules[FUNCTIONTOGENERATE])
        
    test_loader = TestLoader()
    test_result = TestResult()

    # Use resolve() to get an absolute path
    test_directory = str(Path(__file__).resolve().parent.parent / 'python')

    test_suite = test_loader.discover(test_directory, pattern='test_'+FUNCTIONTOGENERATE+'.py')

    test_suite.run(result=test_result)

    print("--------------------")

    if test_result.wasSuccessful():
        print("All tests passed! Code is good ✅")
    else:
        result_message = "Tests failed! Code needs work ❌\nFailures:\n"
        result_plain = "Tests failed! Failures:\n"
        for failure in test_result.failures:
            test_case, traceback = failure
            result_message += f"\n\n\n##### Next Failure ####\n\033[91mFailure in {test_case.id()}:\n{traceback}\n\033[0m"
            result_plain += f"\n\n Next Failure \nFailure in {test_case.id()}:\n{traceback}"
        for error in test_result.errors:
            test_case, traceback = error
            result_message += f"\n\n\n##### Next Error ####\n\033[38;5;208mError in {test_case.id()}:\n{traceback}\n\033[0m"
            result_plain += f"\n\n Next Error \nError in {test_case.id()}:\n{traceback}"
        print(result_message)
        if not justtest:
            with open(f"../python/{FUNCTIONTOGENERATE}.py", "r") as file:
                generate_and_save_code("You previously generated the following code that didn't work:\n```python\n" + file.read() + "\n```\n\nPlease fix the code and try again. The errors generated were as follows:\n" + result_plain)

def send_message_to_model(prompt, api_key):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        # model="claude-3-haiku-20240307",
        model="claude-3-5-sonnet-latest",
        max_tokens=1000,
        temperature=0,
        system=SYSTEMPROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
    )
    return message.content[0].text

def send_message_to_model_local(prompt, model):
    import requests
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0,
        "model": model,
        "stream": False,
        "system": SYSTEMPROMPT
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["response"]

def generate_and_save_code(additional_info):
    print("Generating code...")
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    with open(f"../python/test_{FUNCTIONTOGENERATE}.py", "r") as file:
        test_code = file.read()
        prompt = (
            'Please make all comments and reasoning before providing the code. Implement this program based on the following unit tests, be sure to pay close attention to all test cases: \n\n' 
            + test_code 
            + "\n\n" 
            + additional_info
        )
        print(prompt)
        resp = send_message_to_model(prompt, api_key)
        # resp = send_message_to_model_local(prompt, "qwen2.5-coder")
        
        realtext = resp.replace("\\n", "\n")
        generated_code = realtext.split("```python\n")[1].split("```")[0]
        beginingRemark = realtext.split("```python\n")[0]
        endingRemark = realtext.split("```python\n")[1].split("```")[1]

    with open(f"../python/{FUNCTIONTOGENERATE}.py", "w") as file:
        file.write(generated_code)
    
    print("Code generated! 🚀")
    print("\033[96m" + beginingRemark + "\033[0m")
    print("\033[92m" + generated_code + "\033[0m")
    print("\033[96m" + endingRemark + "\033[0m")
    run_tests()

def main():
    parser = argparse.ArgumentParser(description="Run tests or generate code.")
    parser.add_argument('--justtest', action='store_true', help='Only run tests')
    parser.add_argument('--info', type=str, help='Additional information to append to the prompt', default="")
    args = parser.parse_args()

    if args.justtest:
        run_tests(justtest=True)
        return

    generate_and_save_code(args.info)

if __name__ == "__main__":
    def signal_handler(sig, frame):
        print('^C Exiting gracefully...')
        # # Kill any open requests
        # requests.adapters.DEFAULT_RETRIES = 0

        # # Prevent saving any files by overriding open
        # builtins.open = lambda *args, **kwargs: None

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    main()