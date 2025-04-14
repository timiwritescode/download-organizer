import shutil
import os
import re

from gui import directory_changes, OverwriteOptions
from gui.windows.file_exists_window import FileExistsWindow


def add_number_to_file_name(filename: str, destination_directory: str):
    """Append number to file name in directory where the filename write operation is
    attempting to write into already exists in said directory"""

    name_pattern = filename.split(".")[0].split("(")[0]
    pattern = rf"^{name_pattern}(\(\d+)?"

    strip_extension = lambda x : x.split(".")[0]
    dir_listing = map(strip_extension, os.listdir(destination_directory))
    matched_filenames = [i.split("(")[0]
                         for i in dir_listing if re.match(pattern, i)]
    # increment the count
    name_and_extension = filename.split(".")
    file_extension = "" if len(name_and_extension) < 2 else f".{name_and_extension[1]}"
    name_of_file = name_and_extension[0]

    return f"{name_of_file}({len(matched_filenames)}){file_extension}"


def move_file(filepath: str, destination: str, filename: str):
    """Move File from a destination"""
    try:
        shutil.move(filepath, destination)
        return filename
    except shutil.Error as err:
        if str(err.__str__()).endswith("already exists"):
            # prompt

            file_exist_prompt_gui = FileExistsWindow(filename, destination)
            file_exist_prompt_gui.open_window()
            # overwrite
            if directory_changes.get_write_option() == OverwriteOptions.KEEP_BOTH:
                # keep both files
                updated_filename = add_number_to_file_name(filename, destination)
                destination = destination + "/" + updated_filename
                shutil.move(filepath, destination)
                return updated_filename
            else:
                # overwrite
                destination_file = destination + "/" + filepath.split("/")[-1]
                shutil.move(filepath, destination_file)
                return filename