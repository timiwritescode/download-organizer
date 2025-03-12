from queue import Queue
from tracemalloc import take_snapshot
from .node import Directory, File
from .events import event_queue, EventTypes, Event
import os
import threading
import time

class Observatory:
    """
    A class for the directory watch engine
    """
    def __init__(self, path: str):
        self._thread = None
        self._path = path
        self._event_queue = Queue()
        
        self._running = threading.Event()

    def get_event_queue(self):
        return self._event_queue

    def _watch_directory(self):

        current_snapshot = self._take_snap_shot()
        while not self._running.is_set():
            time.sleep(2)
            # if not event_queue.empty():
            #     event = event_queue.get()
            #     #  check queue
            #     # print(f"Event: {event._event_type}, Modification: {event._modification}")
            #     event_queue.task_done()

            new_snapshot = self._take_snap_shot()
            if current_snapshot != new_snapshot:
                self._compare_snapshot(current_snapshot, new_snapshot)
                # something has changed, compare the two snap shots

                current_snapshot = new_snapshot


    def _take_snap_shot(self):
        """
        Take the snapshot of a directory
        :return: list
        """
        snapshot = []
        # iterate over a directory

        # add recursiveness
        for entry in os.listdir(self._path):
            entry_path = os.path.join(self._path, entry)
            if os.path.isdir(os.path.join(entry_path)):
                directory = Directory(entry_path)
                snapshot.append(directory.get_directory_info())
            else:
                # add as a file
                file = File(entry_path)
                snapshot.append(file.get_file_info())

        return snapshot


    def start(self):
        """Watchc spicified directory in different thread"""
        self._running.clear()
        self._thread = threading.Thread(target=self._watch_directory, daemon=True)
        self._thread.start()
        # self._watch_directory()


    def stop(self):
        """Stop watching directory"""
        self._running.set()
        self._thread.join()


    def _compare_snapshot(self, initial_snapshot: list, new_snapshot: list) -> None:
        """Compare the initial snapshot with a just taken snapshot and if there are changes,
            emits the changes with the appropriat"""
        # Find what is different in both snapshot
        # if it is file created, emit the event file created
        # if it is deleted, emit event file deleted
        for entry in initial_snapshot:
            if self._is_deleted(entry, new_snapshot):
                event_type = EventTypes.FILE_DELETED.name if entry["node_type"] == "file" \
                                                    else EventTypes.DIRECTORY_DELETED.name
                deleted_event = Event(event_type, entry)
                self._event_queue.put(deleted_event)

        # check new snapshot
        for entry in new_snapshot:
            if self._is_created(entry, initial_snapshot):
                event_type = EventTypes.FILE_CREATED.name if entry["node_type"] == "file" \
                    else EventTypes.DIRECTORY_CREATED.name
                created_event = Event(event_type, entry)
                self._event_queue.put(created_event)


    def _is_deleted(self, entry: dict, new_snapshot: list) -> bool:
        """
        check if an entry in an initial snapshot, 0 is in a new snapshot 1
        :param entry: a dictionary of file or directory info from the initial snapshot
        :param snapshot_: The modified snapshot
        :return: bool
        """
        if entry in new_snapshot:
            return False

        return True

    def _is_created(self, entry: dict, old_snapshot: list) -> bool:
        """
        Check if an entry in a new snapshot is present in old snapshot.
        If it is not, then the file has just been created

        :param entry: a dictionary of file info or directory info from the new snapshot
        :param old_snapshot: the initial snapshot being compared with new snapshot
        :return: bool
        """
        if entry not in old_snapshot:
            return True

        return False