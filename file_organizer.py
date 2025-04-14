import queue
import time
import os
from pathlib import Path

from traceback import format_exception
from config import config
from mime_types import get_file_type, get_mime_type_from_name

from gui import directory_changes
from util import move_file
from watchtower.observatory import Observatory
from gui.file_manager_window import FileMoverWindow

def get_default_file_destination(file_extension: str) -> str:
    file_type = get_file_type(file_extension)
    home_directory = str(Path.home())

    return home_directory + config["directories"][file_type]


def check_default_directories_specified_exist():
    home_dir = str(Path.home())
    audio_files_path = home_dir + config["directories"]["audio"]
    doc_files_path = home_dir + config["directories"]["document"]
    image_files_path = home_dir + config["directories"]["image"]
    video_files_path = home_dir + config["directories"]["video"]

    if os.path.exists(audio_files_path) is not True:
        raise Exception(get_directory_error_message("Audio", audio_files_path))

    if os.path.exists(doc_files_path) is not True:
        raise Exception(get_directory_error_message("Documents", doc_files_path))

    if os.path.exists(image_files_path) is not True:
        raise Exception(get_directory_error_message("Images/Pictures", image_files_path))

    if os.path.exists(video_files_path) is not True:
        raise Exception(get_directory_error_message("Videos", video_files_path))


def get_directory_error_message(dir_type: str, path: str) -> str:
    return f"{dir_type} directory {path} specified does not exist"

if __name__ == "__main__":
    if config["watch_dir"] is None:
        raise Exception(f"Directory to watch not specified in config")

    dir_to_watch = str(Path.home()) + config["watch_dir"]
    if not os.path.exists(dir_to_watch):
        raise Exception(f"Directory {dir_to_watch} does not exist")

    if not os.path.isdir(dir_to_watch):
        raise Exception(f"{dir_to_watch} is not a directory")

    check_default_directories_specified_exist()

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
                            if selected_dir_path == "default":
                                extension = get_mime_type_from_name(filename)
                                destination = get_default_file_destination(extension)

                                write_name = move_file(file_to_move, destination, filename)
                                print(f"Moved file {filename} to {destination}/{write_name}")
                            else:
                                write_name = move_file(file_to_move, selected_dir_path, filename)
                                print(f"Moved file {filename} to {selected_dir_path}/{write_name}")



                    # clear data cache
                    directory_changes.clear_data_cache()


                event_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(format_exception(e))

    except KeyboardInterrupt:
        observatory.stop()