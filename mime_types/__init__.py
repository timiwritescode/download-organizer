import re
from .audio_mimes import audio_mimes
from .document_mimes import document_mimes
from .picture_mimes import image_mimes
from .video_mimes import video_mimes

extension_pattern = r'^[^\\/:*?"<>|\r\n]+\.[a-zA-Z0-9]{2,5}$'

def get_mime_type_from_name(name: str)-> str:
    if re.match(extension_pattern, name) is False:
        raise Exception("Filename does not match pattern " + extension_pattern)

    mime_type = name.split(".")[-1]
    return mime_type

def get_file_type(extension: str) -> str:
    if not extension.startswith("."):
        extension = "." + extension
    if extension in audio_mimes:
        return "audio"
    if extension in video_mimes:
        return "video"
    if extension in image_mimes:
        return "image"
    if extension in document_mimes:
        return "document"
