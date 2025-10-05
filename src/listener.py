import os
import time
import shutil
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from merge_results import merge_robot_results  

# ==================================================
# Utility Functions
# ==================================================

def get_latest_output_file(folder_path):
    """
    Return the latest Robot output XML file in the given folder.
    Looks for files ending with '_output.xml' or exactly 'output.xml'.
    """
    output_files = list(Path(folder_path).rglob("*output.xml"))
    if not output_files:
        return None
    latest = max(output_files, key=os.path.getmtime)
    return latest

def is_test_passed(output_xml):
    """
    Parse a Robot Framework output.xml file to check if the suite result is PASS.
    Returns True if overall suite status == 'PASS', else False.
    """
    try:
        tree = ET.parse(output_xml)
        root = tree.getroot()
        suite = root.find("suite")
        if suite is not None:
            status = suite.find("status")
            if status is not None and status.get("status", "").upper() == "PASS":
                return True
        return False
    except Exception as e:
        print(f"[ERROR] Failed to read {output_xml}: {e}")
        return False

def copy_result_folders(src_dir, dest_dir, exclude_file):
    """
    Copy Robot result folders from src_dir to dest_dir excluding the one
    containing the exclude_file (usually the latest output.xml).
    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    for folder in src_dir.iterdir():
        if folder.is_dir():
            xml_files = list(folder.glob("*output.xml"))
            if not xml_files:
                continue
            output_file = xml_files[0]
            if output_file != exclude_file:
                if is_test_passed(output_file):
                    target_path = dest_dir / folder.name
                    if not target_path.exists():
                        shutil.copytree(folder, target_path)
                        print(f"[INFO] Copied {folder} -> {target_path}")
                    else:
                        print(f"[SKIP] {folder} already exists in merge directory.")
                else:
                    print(f"[SKIP] {folder.name} failed tests, not copying.")


def read_last_merged_time(state_file):
    """Read last merge timestamp from a state file."""
    if not os.path.exists(state_file):
        return None
    with open(state_file, "r") as f:
        timestamp = f.read().strip()
        return datetime.fromisoformat(timestamp) if timestamp else None


def write_last_merged_time(state_file, timestamp):
    """Store the last merged timestamp."""
    with open(state_file, "w") as f:
        f.write(timestamp.isoformat())


def run_merge_process(src_dir, merge_dir, state_file):
    """Perform the merge process once."""
    latest_output = get_latest_output_file(src_dir)
    if not latest_output:
        print("[WARN] No output.xml found in source directory.")
        return

    last_merge_time = read_last_merged_time(state_file)
    latest_time = datetime.fromtimestamp(os.path.getmtime(latest_output))

    if last_merge_time and latest_time <= last_merge_time:
        print("[INFO] No new results since last merge.")
        return

    print(f"[INFO] New results found. Last output.xml: {latest_output}")

    # Copy result folders except the latest one
    copy_result_folders(src_dir, merge_dir, latest_output)

    # Merge results using your existing merge function
    print("[INFO] Merging results...")
    merge_robot_results(merge_dir,"merge")  # your merge logic

    # Update last merged time
    write_last_merged_time(state_file, latest_time)
    print(f"[INFO] Merge complete at {latest_time.isoformat()}")


# ==================================================
# Main Listener Logic
# ==================================================

def start_listener(src_dir, merge_dir, wait_minutes, run_once=False):
    state_file = Path(merge_dir) / ".last_merge_time"

    while True:
        print("\n[LISTENER] Checking for new Robot results...")
        run_merge_process(src_dir, merge_dir, state_file)
        if run_once:
            break
        print(f"[WAIT] Sleeping for {wait_minutes} minutes...")
        time.sleep(wait_minutes * 60)



# ==================================================
# CLI Entry Point
# ==================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Robot Result Consolidation Listener")
    parser.add_argument("--folder", required=True, help="Path to the folder containing robot results")
    parser.add_argument("--merge-dir", required=True, help="Directory where merged results will be stored")
    parser.add_argument("--wait", type=int, default=10, help="Minutes to wait before next check")
    parser.add_argument("--once", action="store_true", help="Run only once instead of continuous listening")

    args = parser.parse_args()

    print("[START] Robot Results Listener started")
    start_listener(args.folder, args.merge_dir, args.wait, args.once)
