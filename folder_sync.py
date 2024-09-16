import os
import shutil
import time
import hashlib
import argparse
import logging

def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica, logger):
    """Synchronize the replica folder with the source folder."""
    # Walk through the source folder
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, relative_path)

        # Create directories in the replica if they don't exist
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            logger.info(f"Created directory: {replica_root}")

        # Check all files in the source
        for file_name in files:
            source_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_root, file_name)

            # If file doesn't exist in replica or is different, copy it
            if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logger.info(f"Copied file from {source_file} to {replica_file}")

    # Check for files in replica that are not in source and delete them
    for root, dirs, files in os.walk(replica):
        relative_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, relative_path)

        # Remove files not present in source
        for file_name in files:
            replica_file = os.path.join(root, file_name)
            source_file = os.path.join(source_root, file_name)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logger.info(f"Deleted file: {replica_file}")

        # Remove directories not present in source
        for dir_name in dirs:
            replica_dir = os.path.join(root, dir_name)
            source_dir = os.path.join(source_root, dir_name)

            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logger.info(f"Deleted directory: {replica_dir}")

def setup_logger(log_file):
    """Set up logging to both console and file."""
    logger = logging.getLogger("FolderSync")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Script")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    args = parser.parse_args()

    # Set up logger
    logger = setup_logger(args.log_file)

    # Run synchronization periodically
    while True:
        logger.info("Starting synchronization...")
        sync_folders(args.source, args.replica, logger)
        logger.info("Synchronization complete.")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
