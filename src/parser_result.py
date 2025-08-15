from robot.api import ExecutionResult
import re
from color_coding import colour_print, BOLD, GREEN, RED
from list_result import list_files
from pathlib import Path

def list_test(result_file, tag_pattern=".*"):
    """list test present in the result file matching with the given pattern

    Args:
        result_file (str): robot output.xml file   
        tag_pattern (str): tag/pattern to filter test from given result_file, Default = everything   
    """

    # Path to Robot Framework's output XML
    result_file = ExecutionResult(result_file)
    tag_pattern = re.compile(tag_pattern, re.IGNORECASE)  # e.g., names starting with "Smoke"
    match_test = find_matching_tests_with_tags(result_file.suite,tag_pattern)
    # Output matched test names and their tags
    for test_name, tags in match_test:
        print(f"Test: {test_name} | Matched Tag(s): {tags}")

def find_matching_tests_with_tags(suite,tag_pattern):
    """_summary_
    find matching suite for you robot result
    
    Args:
        suite(Object): suite is a robot.model.testsuite.TestSuite object 
    Returns:
        matches(list): list of test matching with the given tags
    """    
    matches = []
    for test in suite.tests:
        matched_tags = [tag for tag in test.tags if tag_pattern.match(tag)]
        if matched_tags:
            matches.append((test.name, matched_tags))
    for subsuite in suite.suites:
        matches += find_matching_tests_with_tags(subsuite,tag_pattern)
    return matches

# Loop through all suites and tests
def print_test_results(suite):
    """Print test results from your robot output file

    Args:
        suite(Object): suite is a robot.model.testsuite.TestSuite object 
    """
    for test in suite.tests:
        print(f"Test: {test.name}")
        print(f"Test tag - : {[tag for tag in test.tags]}")
        print(f"  Status    : ",end="")
        colour_print('PASS', GREEN) if(test.status == 'PASS') else colour_print('FAIL', RED)
        print(f"  Start Time: {test.starttime}")
        print(f"  End Time  : {test.endtime}")
        print(f"  Suite name  : {suite.name}")
        if test.message:
            print(f"  Message   : {test.message}")
        print()

    # Recursively handle nested suites
    for child in suite.suites:
        print_test_results(child)

def print_test_results_in_folder(folder_path:Path|str):
    """Print all test results from your robot output folder

    Args:
        folder_path (Path | str): path to your robot output folder
    """
    output_files = list_files(folder_path)
    for file in output_files: # type: ignore
        result = ExecutionResult(file)
        print_test_results(result.suite)

def check_tags():
    """List statistics
    """
    result = ExecutionResult("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo\\output.xml")

# The tag statistics are stored in result.statistics.tags
    for tag_stat in result.statistics.tags:
        print(f"Tag: {tag_stat.name}, "
            f"Passed: {tag_stat.passed}, "
            f"Failed: {tag_stat.failed}, "
            f"Skipped: {tag_stat.skipped}")

if __name__ == "__main__":
    # list_test("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo\\output.xml")
    # output_path = Path("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo\\output.xml")
    #print_test_results_in_folder("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo")
    check_tags()




