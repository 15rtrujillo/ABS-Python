import datetime
import os
import zipfile


script_path = os.path.dirname(os.path.abspath(__file__))


def get_file_path(file_name: str) -> str:
    """Returns an absolute path to the given file name
    file_name: The name of the file to append"""
    return os.path.join(script_path, file_name)


def get_data_directory() -> str:
    """Get an absolute path to the /Data directory"""
    return get_file_path("Data")


def get_data_file_path(file_name: str) -> str:
    """Returns an absolute path to a file in the data directory"""
    return get_file_path(f"Data/{file_name}")


def get_files_in_directory(directory: str) -> list[str]:
    """Returns a list of the names of all the files in a directory (including extensions)"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def delete_file(file_path: str):
    """Wrapper for os.remove(path)"""
    os.remove(file_path)


def data_directory_exists() -> bool:
    """Determine if the /Data directory exists"""
    return os.path.exists(get_data_directory())


def create_data_directory():
    """Creates the ABS directory at the program location"""
    os.mkdir(get_data_directory())

def create_backup_file():
    """Create a zip file with the contents of the Data directory."""
    backup_filename = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S") + ".backup"
    file_path = get_data_file_path(backup_filename)

    files = [file for file in get_files_in_directory(get_data_directory()) if file == "Bookshelf.abs" or ".list" in file]

    with zipfile.ZipFile(file_path, "w") as zip_file:
        for file in files:
            zip_file.write(get_data_file_path(file), file)
