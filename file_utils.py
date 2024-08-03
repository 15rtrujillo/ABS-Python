import os


script_path = os.path.dirname(os.path.abspath(__file__))


def get_file_path(file_name: str) -> str:
    """Returns an absolute path to the given file name
    file_name: The name of the file to append"""
    return os.path.join(script_path, file_name)


def get_data_directory() -> str:
    return get_file_path("Data")


def get_files_in_directory(directory: str) -> list[str]:
    """Returns a list of the names of all the files in a directory (including extensions)"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def delete_file(file_path: str):
    os.remove(file_path)


def data_directory_exists() -> bool:
    return os.path.exists(get_data_directory())


def create_data_directory():
    """Creates the ABS directory at the program location"""
    os.mkdir(get_data_directory())
