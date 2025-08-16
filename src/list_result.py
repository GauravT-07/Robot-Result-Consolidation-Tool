from pathlib import Path
import os
from color_coding import colour_print, BOLD, BOLD_UNDERLINE

def list_files(file_path, pattern:str ="*.xml"):
    """List the robot files present in the current folder

    Args:
        file_path (str): Folder path with robot output files present
        pattern (str): Name/Pattern of file to search in the folder
    Returns:
        list[str]: list of output files present in the given folder
    """
    try:
            if not os.path.exists(file_path):
                print(f"Path does not exist: {file_path}")
                return
            
            if not os.path.isdir(file_path):
                print(f"Provided path is not a directory: {file_path}")
                return
           # Root directory 
            root_dir = Path(file_path)
            
            # Match all relevant Robot Framework output files recursively
            output_files = list(root_dir.rglob(pattern)) 
            # + list(root_dir.rglob('*.html')) + list(root_dir.rglob('*.log'))
            
            if output_files:
                print_file = "📂 Files present in the directory-: " + str(len(output_files))
                colour_print(print_file, BOLD_UNDERLINE)
                for file in output_files:
                    resultfilepath = "- " + str(file.relative_to(root_dir))  # cleaner path
                    colour_print(resultfilepath,BOLD)
            else:
                print("No files found in the directory.")
                            
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return output_files

if __name__ == "__main__":
    list_files("C:\\Users\\HP\\Desktop\\python_practice\\RobotDemo","*eck*.xml")