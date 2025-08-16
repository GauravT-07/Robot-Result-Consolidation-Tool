from robot.api import ExecutionResult
import re
from color_coding import colour_print, BOLD, GREEN, RED, BOLD_UNDERLINE
from list_result import list_files
from pathlib import Path

def list_test_results_in_folder(folder_path, tag_pattern=".*"):
    """list test present in the result folder matching with the given pattern

    Args:
        folder_path (Path | str): path to your robot output folder
    """
    output_files = list_files(folder_path)
    print_file = "✅ Matching tag found -: "
    colour_print(print_file, GREEN)    
    for file in output_files: # type: ignore
        list_test(file, tag_pattern)

def list_test(result_file_to_parse, tag_pattern=".*"):
    """list test present in the result file matching with the given pattern

    Args:
        result_file (str): robot output.xml file   
        tag_pattern (str): tag/pattern to filter test from given result_file, Default = everything   
    """

    # Path to Robot Framework's output XML
    result_file = ExecutionResult(result_file_to_parse)
    tag_pattern = re.compile(tag_pattern, re.IGNORECASE)  # e.g., names starting with "Smoke"
    match_test = find_matching_tests_with_tags(result_file.suite,tag_pattern)
    if(len(match_test)!=0):
        print_file = "File-name -: " + str(result_file_to_parse)
        colour_print(print_file, BOLD_UNDERLINE)
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

def print_test_results_in_folder(folder_path):
    """Print all test results from your robot output folder

    Args:
        folder_path (Path | str): path to your robot output folder
    """
    output_files = list_files(folder_path)
    for file in output_files: # type: ignore
        print_file = "File-name -: " + str(file)
        colour_print(print_file, BOLD_UNDERLINE)
        result = ExecutionResult(file)
        print_test_results(result.suite)

def list_tags_from_result_files(folder_path):
    """List statistics for each tag
    """
    output_files = list_files(folder_path)
    for file in output_files: # type: ignore
        result = ExecutionResult(file)
        print_file = "File-name -: " + str(file)
        colour_print(print_file, BOLD_UNDERLINE)        
    # The tag statistics are stored in result.statistics.tags
        for tag_stat in result.statistics.tags:
            print(f"Tag: {tag_stat.name}, "
                f"Passed: {tag_stat.passed}, "
                f"Failed: {tag_stat.failed}, "
                f"Skipped: {tag_stat.skipped}")

def check_tags(tags_to_check, output_file):
    """Check if given tags exist in Robot output.xml and print their stats."""
    flag = False
    result = ExecutionResult(output_file)

    # Build a dictionary for quick lookup
    tag_stats_map = {tag_stat.name: tag_stat for tag_stat in result.statistics.tags}

    # Check each user-specified tag
    for tag in tags_to_check:
        if tag in tag_stats_map:
            t = tag_stats_map[tag]
            print(f"✅ Tag found: {t.name}, Passed: {t.passed}, Failed: {t.failed}, Skipped: {t.skipped}")
        else:
            flag = True
            print(f"❌ Tag not found: {tag}")
    return flag

def check_tags_in_results_folder(folder_path, tags_to_check):
    """Check tags for all test results from your robot output folder

    Args:
        folder_path (Path | str): path to your robot output folder
        tags_to_check: List of tags to check in your robot output folder
    """
    output_files = list_files(folder_path)
    problem_files = []
    for file in output_files: # type: ignore
        print_file = "File-name -: " + str(file)
        colour_print(print_file, BOLD_UNDERLINE)
        if(check_tags(tags_to_check, file)):
            problem_files.append(file)
    if(len(problem_files)!=0):  
        str_to_print = "Probelm with files given below:"  
        colour_print(str_to_print, BOLD_UNDERLINE)    
        for file in problem_files:
            print("File-name -: ", end="")
            print_file = str(file)
            colour_print(print_file, RED)
            
            

if __name__ == "__main__":
    # list_test("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo\\output.xml")
    # output_path = Path("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo\\output.xml")
    #print_test_results_in_folder("C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata")
    list_test_results_in_folder('C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata','gaurav')
    tags_to_check = ['gaurav','akshay']
    #list_tags_from_result_files("C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata")
    #check_tags(tags_to_check, "C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata\\result\\output.xml")
    #check_tags_in_results_folder("C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata", tags_to_check)
    #check_tags_in_results_folder("C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata\\testcase-2", ['sun','rise'])



