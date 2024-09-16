# Folder Sync

## Description

**Folder Sync** is a Python script that synchronizes two folders: a source folder and a replica folder. The goal is to ensure that the replica folder is an identical copy of the source folder after each synchronization. The script also performs periodic synchronizations at a user-defined interval.

## Features

- One-way synchronization: the replica folder is updated to match the source folder.
- New or modified files in the source folder are copied to the replica.
- Files that no longer exist in the source folder are deleted from the replica.
- Synchronizations are performed periodically, with a user-defined interval.
- File creation, deletion, and copying operations are logged both to the console and a log file.

## Usage

Run the script by passing the following parameters via the command line:

```bash
python folder_sync.py <source_folder> <replica_folder> <sync_interval> <log_file_path>
```

## Parameters:

- <source_folder>: Absolute path to the source folder to be synchronized.
- <replica_folder>: Absolute path to the replica folder where files will be copied.
- <sync_interval>: Synchronization interval in seconds (time between periodic synchronizations).
- <log_file_path>: Absolute path to the log file where operations will be recorded.
