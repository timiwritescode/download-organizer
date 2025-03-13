import queue
import time
import sys
import shutil
import os
from traceback import format_exception
import threading

from watchtower.observatory import Observatory
from gui.file_manager_window import FileMoverWindow


def move_file(file, destination):
    shutil.move(file, destination)
    print(f"Moved {file} to {destination}")


def display_gui(event):
    gui_window = FileMoverWindow(event._modification["name"]).open_window()
    if not gui_window:
        return

    selected_dir_path = gui_window.get_selected_path()

    print("SELECTED: " + selected_dir_path)
    file_to_move = event._modification["node_path"]
    move_file(file_to_move, selected_dir_path)


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
                    display_gui(event)

                print(f"Event: {event._event_type}, Modification: {event._modification}")

                event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(format_exception(e))

    except KeyboardInterrupt:
        observatory.stop()