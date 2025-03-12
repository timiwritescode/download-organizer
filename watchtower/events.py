from enum import Enum
from queue import Queue

event_queue = Queue()

class EventTypes(Enum):
    FILE_DELETED="file_deleted"
    FILE_CREATED="file_created"
    FILE_MODIFIED="file_modified"

    DIRECTORY_CREATED="directory_created"
    DIRECTORY_DELETED="directory_deleted"


class Event:
    def __init__(self, event_type, modification):
        self._event_type = event_type
        self._modification = modification

    # def emit_event(self):
    #     "pass new event into memory then consume it "
    #     event_queue.put(self)