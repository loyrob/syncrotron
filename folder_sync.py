import os
import shutil
import argparse
from filecmp import dircmp
import logging
from datetime import datetime
import hashlib
import time

def generate_logfile_name():
    """
    Generates a default logfile name with a timestamp.
    Format: logs/sync_log-YYMMDD_hhmmss.log
    """
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    return f"logs/sync_log-{timestamp}.log"

def get_last_logfile():
    """
    Finds the most recent log file in the logs directory.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir)
        return generate_logfile_name()

    log_files = [f for f in os.listdir(log_dir) if f.startswith("sync_log-") and f.endswith(".log")]
    if not log_files:
        return generate_logfile_name()

    # Sort log files by timestamp in their names (descending order)
    log_files.sort(reverse=True)
    return os.path.join(log_dir, log_files[0])

def setup_logger(logfile):
    """
    Sets up the logger to log messages to a file and console.
    """
    log_dir = os.path.dirname(logfile)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create the logs directory if it doesn't exist

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(logfile, mode='a'),  # Append to the logfile
            logging.StreamHandler()
        ]
    )

def log_and_print(message):
    """
    Logs a message and prints it to the console.
    """
    logging.info(message)

def calculate_md5(file_path):
    """
    Calculates the MD5 checksum of a file.

    :param file_path: Path to the file.
    :return: MD5 checksum as a string.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def files_are_different(src_path, dest_path):
    """
    Compares two files to determine if they are different based on MD5.

    :param src_path: Path to the source file.
    :param dest_path: Path to the replica file.
    :return: True if files differ, False otherwise.
    """
    return calculate_md5(src_path) != calculate_md5(dest_path)

def sync_folders(source, replica):
    """
    Synchronizes the contents of the source folder with the replica folder.

    :param source: Path to the source folder
    :param replica: Path to the replica folder
    """
    # Ensure the replica folder exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        log_and_print(f"Created directory: {replica}")

    # Compare the two directories
    comparison = dircmp(source, replica)

    # Copy or update files from source to replica
    for file in comparison.left_only:
        src_path = os.path.join(source, file)
        dest_path = os.path.join(replica, file)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
            log_and_print(f"Copied directory: {src_path} to {dest_path}")
        else:
            shutil.copy2(src_path, dest_path)
            log_and_print(f"Copied file: {src_path} to {dest_path}")

    # Remove files from replica that are not in the source
    for file in comparison.right_only:
        replica_path = os.path.join(replica, file)
        if os.path.isdir(replica_path):
            shutil.rmtree(replica_path)
            log_and_print(f"Removed directory: {replica_path}")
        else:
            os.remove(replica_path)
            log_and_print(f"Removed file: {replica_path}")

    # Update files that differ (based on MD5)
    for file in comparison.common_files:
        src_path = os.path.join(source, file)
        dest_path = os.path.join(replica, file)
        if files_are_different(src_path, dest_path):
            shutil.copy2(src_path, dest_path)
            log_and_print(f"Updated file: {src_path} to {dest_path}")

    # Recursively synchronize subdirectories
    for common_dir in comparison.common_dirs:
        sync_folders(os.path.join(source, common_dir), os.path.join(replica, common_dir))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders periodically.")
    parser.add_argument("-i", "--input", required=True, help="Path to the source (input) folder.")
    parser.add_argument("-o", "--output", required=True, help="Path to the replica (output) folder.")
    parser.add_argument("-l", "--logfile", help="Path to the logfile (default: logs/sync_log-YYMMDD_hhmmss.log). Use 'LAST' to append to the most recent logfile.")
    parser.add_argument("-t", "--time", type=int, default=60, help="Time interval in seconds for periodic synchronization (default: 60 seconds).")

    args = parser.parse_args()

    source_folder = args.input
    replica_folder = args.output
    if args.logfile == "LAST":
        logfile = get_last_logfile()
    else:
        logfile = args.logfile or generate_logfile_name()

    setup_logger(logfile)

    if not os.path.exists(source_folder):
        log_and_print(f"Source folder '{source_folder}' does not exist!")
        exit(1)

    log_and_print(f"PERIODIC synchronization start: {source_folder} -> {replica_folder}")
    log_and_print(f"INTERVAL of synchronization: {args.time} seconds")

    try:
        while True:
            log_and_print(f"START synchronization cycle.")
            sync_folders(source_folder, replica_folder)
            log_and_print(f"END Synchronization cycle.")
            time.sleep(args.time)
    except KeyboardInterrupt:
        log_and_print("TERMINATED Synchronization by user.")
