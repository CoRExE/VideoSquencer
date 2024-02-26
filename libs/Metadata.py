import hashlib
import os
import datetime


def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        md5_hash = hashlib.md5(file_data).hexdigest()
    return md5_hash


def get_metadata(file_path):
    metadata = os.stat(file_path)
    return {
        "name": file_path.split("/")[-1],
        "size": metadata.st_size / (1024 * 1024),
        "modified": datetime.datetime.fromtimestamp(metadata.st_mtime),
        "md5": calculate_md5(file_path)
    }
