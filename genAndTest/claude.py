import anthropic
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
# remove quotes from the api key
api_key = api_key[1:-1]

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api_key,
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="Your task is to create Python functions based on the provided unit tests. The requests will describe the desired functionality of the function, including the input parameters and expected return value. Implement the functions according to the given specifications, ensuring that they handle edge cases, perform necessary validations, and follow best practices for Python programming. Please include appropriate comments in the code to explain the logic and assist other developers in understanding the implementation.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": '''Implement this program based on the following unit tests: 
import unittest
from check_tic_tac_toe import checkTicTacToeWin

class TestCheckTicTacToeWin(unittest.TestCase):
    def test_horizontal_win(self):
        board = [
            ['X', 'X', 'X'],
            ['O', 'O', ' '],
            [' ', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_vertical_win(self):
        board = [
            ['X', 'O', ' '],
            ['X', 'O', ' '],
            ['X', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_diagonal_win(self):
        board = [
            ['X', 'O', ' '],
            ['O', 'X', ' '],
            [' ', ' ', 'X']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_no_win(self):
        board = [
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', 'X']
        ]
        self.assertEqual(checkTicTacToeWin(board), None)
    
    def test_undecided_game(self):
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            ['O', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), None)

if __name__ == '__main__':
    unittest.main()
'''
                    ,
                }
            ],
        }
    ],
)
print(message.content[0].text.replace("\\n", "\n").split("```python\n")[1].split("```")[0])

with open("../python/check_tic_tac_toe.py", "w") as file:
    file.write(message.content[0].text.replace("\\n", "\n").split("```python\n")[1].split("```")[0])


from unittest import TestLoader, TestResult
from pathlib import Path

test_loader = TestLoader()
test_result = TestResult()

# Use resolve() to get an absolute path
# https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve
test_directory = str(Path(__file__).resolve().parent.parent / 'python')

test_suite = test_loader.discover(test_directory, pattern='test_*.py')
test_suite.run(result=test_result)

if test_result.wasSuccessful():
    print("All tests passed! Code is good ✅")
else:
    print("Tests failed! Code needs work ❌")
    # for failure in test_result.failures:
    #     print(failure)
    # for error in test_result.errors:
    #     print(error)