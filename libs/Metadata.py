import hashlib
import os
import datetime


def calculate_md5(file_path):
    """
    Calculate the MD5 hash of the file located at the given file path.

    :param file_path: The path to the file for which to calculate the MD5 hash.
    :return: The MD5 hash of the file data.
    """
    with open(file_path, 'rb') as file:
        file_data = file.read()
        md5_hash = hashlib.md5(file_data).hexdigest()
    return md5_hash


def get_metadata(file_path):
    """
    Get metadata for a file including name, path, size in MB, modification time, and MD5 hash.

    Parameters:
    file_path (str): The path to the file for which metadata is needed.

    Returns:
    dict: A dictionary containing name, path, size, modification time, and MD5 hash of the file.
    """
    metadata = os.stat(file_path)
    return {
        "name": file_path.split("/")[-1],
        "path": file_path,
        "size": round(metadata.st_size / (1024 * 1024), 2),
        "modified": datetime.datetime.fromtimestamp(metadata.st_mtime),
        "md5": calculate_md5(file_path)
    }
