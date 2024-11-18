Folder Synchronization Script
================================
This script synchronizes two folders (source and replica) by maintaining an identical copy of the source folder at the replica folder.
It supports periodic synchronization, logging, and advanced content comparison using MD5 hashing.

Features:
================================
    Folder Synchronization:     Ensures the replica folder matches the source folder exactly.
    Content-Based Comparison:   Compares files using MD5 hashes to detect content changes,
                                even if file size or modification time remains unchanged.
    Periodic Execution:         Performs synchronization at user-defined intervals.
    Logging:                    Logs all file operations (e.g., copy, update, removal) to both the console and a log file.
    Logfile Options:
        Append logs to a custom file.
        Use the most recent log file for appending (LAST option).
        Automatically generates timestamped log files.
    Termination:                Handle user interruptions (e.g., Ctrl+C) and log termination.

Requirements:
================================
    Python 3.6+
    Standard Python libraries (os, shutil, argparse, filecmp, logging, datetime, hashlib, time).

How It Works:
================================
    Synchronization Process:
    --------------------------
        Creates new files or directories in the replica folder to match the source.
        Updates files in the replica folder if they differ from the source.
        Removes files or directories from the replica that do not exist in the source.
        Recursively synchronizes subdirectories.

    Periodic Execution:
    --------------------------
        The script repeats synchronization every t seconds, where t is the user-specified interval (--time).

    Logging:
    --------------------------
        Logs all operations to the console and the specified log file.
        Automatically creates the log directory if it doesn’t exist.

    Termination:
    --------------------------
        Press Ctrl+C to stop the script.
        Logs the termination event.

Usage:
================================
    Run the script with the following options:
    python folder_sync.py -i <source_folder> -o <replica_folder> [options]

    Required Arguments:
    --------------------
    -i, --input: Path to the source folder.
    -o, --output: Path to the replica folder.

    Optional Arguments:
    --------------------
    -l, --logfile:
        Path to the log file.
        Use LAST to append to the most recent log file in the logs directory.
        Default: logs/sync_log-YYMMDD_hhmmss.log (automatically created if not specified).
    -t, --time: Synchronization interval in seconds
        default: 60 seconds.

Examples:
================================
    Basic Synchronization Every 60 Seconds:
        python folder_sync.py -i /path/to/source -o /path/to/replica

    Custom Synchronization Interval (120 seconds):
        python folder_sync.py -i /path/to/source -o /path/to/replica -t 120

    Log Operations to a Specific Logfile:
        python folder_sync.py -i /path/to/source -o /path/to/replica -l /path/to/custom_logfile.log

    Append Logs to the Most Recent Logfile:
        python folder_sync.py -i /path/to/source -o /path/to/replica -l LAST

Log Files:
================================
    Default directory:  logs/
    Default format:     logs/sync_log-YYMMDD_hhmmss.log (e.g., logs/sync_log-241117_151230.log).
    Log file records:
        File creations, updates, and deletions.
        Start and end of each synchronization cycle.
        Termination by user.

Termination:
================================
    To stop the script, press Ctrl+C.
    The script will log the termination event.

Notes:
================================
    Ensure the logs directory is writable, or specify a custom log file with -l.
    Files and folders are compared using MD5 hashes for precise content detection.
    MD5 hashing introduces a small performance overhead for large files but ensures accuracy.


