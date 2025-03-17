import queue
import time
import sys
import shutil
import os
import re
from traceback import format_exception

from gui import directory_changes, OverwriteOptions
from gui.windows.file_exists_window import FileExistsWindow
from watchtower.observatory import Observatory
from gui.file_manager_window import FileMoverWindow


def add_number_to_file_name(filename: str, destination_directory: str):
    # Get the number of files with that name,
    pattern = rf"^{filename}(\(\d+)?"

    files_with_same_name = os.listdir(destination_directory)
    files_with_same_name = [i.split("(")[0] for i in files_with_same_name if re.match(pattern, i)]
    # increment the count
    name_and_extension = filename.split(".")
    file_extension = "" if len(name_and_extension) < 2 else f".{name_and_extension[1]}"
    name_of_file = name_and_extension[0]

    return f"{name_of_file}({len(files_with_same_name)}){file_extension}"




def move_file(filepath: str, destination: str, filename: str):
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

    



if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Path not specified")

    dir_to_watch = sys.argv[1]
    if not os.path.exists(dir_to_watch):
        raise Exception(f"Directory {dir_to_watch} does not exist")

    if not os.path.isdir(dir_to_watch):
        raise Exception(f"{dir_to_watch} is not a directory")
    observatory = Observatory(dir_to_watch)

    try:
        observatory.start()
        time.sleep(1)
        while True:
            event_queue = observatory.get_event_queue()
            try:
                event = event_queue.get(timeout=1)
                if event._event_type == "FILE_CREATED":
                    print(f"Event: {event._event_type}, Modification: {event._modification}")

                    if not event._modification["name"].endswith("swp"):
                        filename = event._modification["name"]
                        FileMoverWindow(filename).open_window()
                        file_to_move = event._modification["node_path"]
                        selected_dir_path = directory_changes.get_selected_dir()

                        if selected_dir_path is not None:
                            write_name = move_file(file_to_move, selected_dir_path, filename)
                            print(f"Moved file {filename} to {selected_dir_path}/{write_name}")



                event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(format_exception(e))

    except KeyboardInterrupt:
        observatory.stop()