import os

def get_node_name(path: str) -> str:
    return path.split("/")[-1]


def get_directory_size(directory: str) -> int:
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size



def get_file_size(filepath: str) -> int:
    return os.path.getsize(filepath)


def get_mime_type(filepath: str) -> str:
    return filepath.split("/")[-1].split(".")[-1]