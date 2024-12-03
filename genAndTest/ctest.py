from unittest import TestLoader, TestResult
from pathlib import Path
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
        print("Tests failed! Code needs work ❌")
        print("Failures:")
        for failure in test_result.failures:
            test_case, traceback = failure
            print(f"\n\n\n##### Next Failure ####\nFailure in {test_case.id()}:\n{traceback}\n")
        for error in test_result.errors:
            test_case, traceback = error
            print(f"\n\n\n##### Next Error ####\nError in {test_case.id()}:\n{traceback}\n")

if __name__ == '__main__':
    run_tests()