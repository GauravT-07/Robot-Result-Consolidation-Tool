import os
import shutil
import subprocess
from list_result import list_files

def merge_robot_results(src_folder, merged_name):
    # # src_folder = os.path.abspath(src_folder)
    # new_folder = os.path.abspath(new_folder_path)
    # os.makedirs(new_folder, exist_ok=True)

    # # Find all XML files in source folder
    # xml_files = [f for f in os.listdir(src_folder) if f.endswith(".xml")]
    xml_files = list_files(src_folder)
    xml_paths = [os.path.join(src_folder, f) for f in xml_files]# type: ignore

    # for f in xml_files:# type: ignore
    #     shutil.copy(os.path.join(src_folder, f), new_folder)  # Copy originals

    merged_xml_path = os.path.join(src_folder, f"{merged_name}.xml")
    log_html_path = os.path.join(src_folder, f"{merged_name}_log.html")
    report_html_path = os.path.join(src_folder, f"{merged_name}_report.html")

    # Run rebot merge via subprocess
    result = subprocess.run([
        "rebot",
        "--output", merged_xml_path,
        "--log", log_html_path,
        "--report", report_html_path
    ] + xml_paths, check=False)

    # Check exit code
    if result.returncode == 0:
        print("✅ Merge completed successfully.")
    else:
        print(f"⚠️ Merge completed, but rebot returned exit code {result.returncode}.")
        print("   (This usually means some tests failed.)")

    print(f"\n✅ All original files copied to: {src_folder}")
    print(f"✅ Merged XML: {merged_xml_path}")
    print(f"✅ Log file: {log_html_path}")
    print(f"✅ Report file: {report_html_path}")



def merge_robot_results_to_new_folder(src_folder, new_folder_path, merged_name):
    # src_folder = os.path.abspath(src_folder)
    new_folder = os.path.abspath(new_folder_path)
    os.makedirs(new_folder, exist_ok=True)

    # # Find all XML files in source folder
    # xml_files = [f for f in os.listdir(src_folder) if f.endswith(".xml")]
    xml_files = list_files(src_folder)
    xml_paths = [os.path.join(src_folder, f) for f in xml_files]# type: ignore

    for f in xml_files:# type: ignore
        shutil.copy(os.path.join(src_folder, f), new_folder)  # Copy originals

    merged_xml_path = os.path.join(new_folder, f"{merged_name}.xml")
    log_html_path = os.path.join(new_folder, f"{merged_name}_log.html")
    report_html_path = os.path.join(new_folder, f"{merged_name}_report.html")

    # Run rebot merge via subprocess
    result = subprocess.run([
        "rebot",
        "--output", merged_xml_path,
        "--log", log_html_path,
        "--report", report_html_path
    ] + xml_paths, check=False)

    # Check exit code
    if result.returncode == 0:
        print("✅ Merge completed successfully.")
    else:
        print(f"⚠️ Merge completed, but rebot returned exit code {result.returncode}.")
        print("   (This usually means some tests failed.)")

    print(f"\n✅ All original files copied to: {new_folder}")
    print(f"✅ Merged XML: {merged_xml_path}")
    print(f"✅ Log file: {log_html_path}")
    print(f"✅ Report file: {report_html_path}")


# # Example usage
# merge_robot_results(
#     src_folder=r"C:\\Users\\HP\\Desktop\\python_practice\\Robot-Result-Consolidation-Tool\\testdata\\testcase-2",
#     merged_name="final_merged"
# )
