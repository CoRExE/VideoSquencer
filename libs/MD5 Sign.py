import hashlib


def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        md5_hash = hashlib.md5(file_data).hexdigest()
    return md5_hash
