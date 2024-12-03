import anthropic
import os
import argparse
from dotenv import load_dotenv

from unittest import TestLoader, TestResult
from pathlib import Path
import signal
import sys

def run_tests():
    test_loader = TestLoader()
    test_result = TestResult()

    # Use resolve() to get an absolute path
    test_directory = str(Path(__file__).resolve().parent.parent / 'python')

    test_suite = test_loader.discover(test_directory, pattern='test_*.py')

    test_suite.run(result=test_result)

    print("--------------------")

    if test_result.wasSuccessful():
        print("All tests passed! Code is good ✅")
    else:
        result_message = "Tests failed! Code needs work ❌\nFailures:\n"
        for failure in test_result.failures:
            test_case, traceback = failure
            result_message += f"\n\n\n##### Next Failure ####\nFailure in {test_case.id()}:\n{traceback}\n"
        for error in test_result.errors:
            test_case, traceback = error
            result_message += f"\n\n\n##### Next Error ####\nError in {test_case.id()}:\n{traceback}\n"
        print(result_message)
        with open("../python/json_to_xml_api.py", "r") as file:
            generate_and_save_code("You generated the following code that didnt work:\n" + file.read() + "\n\nPlease fix the code and try again. The errors generated were as follows:\n" + result_message)

def generate_and_save_code(additional_info):
    print("Generating code...")
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(api_key=api_key)
    with open("../python/test_json_to_xml_api.py", "r") as file:
        test_code = file.read()
        prompt = (
            'Implement this program based on the following unit tests, there may be custom edge cases, so be sure to pay close attention to all test cases: ' 
            + test_code 
            + "\n\n" 
            + additional_info
        )
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0,
            system="Your task is to create Python functions based on the provided unit tests. The requests will describe the desired functionality of the function, including the input parameters and expected return value. Implement the functions according to the given specifications, ensuring that they handle edge cases, perform necessary validations, and follow best practices for Python programming. Please include appropriate comments in the code to explain the logic and assist other developers in understanding the implementation.",
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
    generated_code = message.content[0].text.replace("\\n", "\n").split("```python\n")[1].split("```")[0]

    with open("../python/json_to_xml_api.py", "w") as file:
        file.write(generated_code)
    
    print("\033[92m" + message.content[0].text + "\033[0m")
    run_tests()

def main():
    parser = argparse.ArgumentParser(description="Run tests or generate code.")
    parser.add_argument('--justtest', action='store_true', help='Only run tests')
    parser.add_argument('--info', type=str, help='Additional information to append to the prompt', default="")
    args = parser.parse_args()

    if args.justtest:
        run_tests()
        return

    generate_and_save_code(args.info)

if __name__ == "__main__":
    def signal_handler(sig, frame):
        print('^C Exiting gracefully...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    main()