import os.path
from enum import Enum
from pydantic import BaseModel
from typing import Any
from .util import *

class FsNode:
    """
    Base class for file system nodes.
    Node may be a directory or a file
    """

    def __init__(self, name: str, node_type: str, node_path: str, node_size: int = None):
        self._name = name
        self._node_type = node_type
        self._node_size = node_size
        self._node_path = node_path


class FsNodeType(Enum):
    DIRECTORY="directory"
    FILE="file"
    UNKNOWN="unknown"



class NodeInfo(BaseModel):
    name: str
    node_path: str
    node_type: str
    size: int = None
    sub_nodes: Any = None

class Directory(FsNode):
    """
    Class for the directory node.
    Main purpose of class is to get the node info of a specific directory
    """

    def __init__(self,
                 path: str):
        super().__init__(
            get_node_name(path),
            FsNodeType.DIRECTORY.value,
            path,
            get_directory_size(path))
        self._sub_nodes = None

    def get_directory_info(self) -> dict:
        node_info = NodeInfo(
            name=self._name,
            node_path=self._node_path,
            node_type=self._node_type,
            size=self._node_size,

        )

        directory_dict = node_info.model_dump()
        directory_dict["sub_nodes"] = [{
            "name": node._name,
            "node_type": node._node_type} for node in self._sub_nodes ] if self._sub_nodes is not None else []

        return directory_dict

class File(FsNode):
    def __init__(self, path: str):
        super().__init__(get_node_name(path),
                         FsNodeType.FILE.value,
                         path,
                         get_file_size(path))

        self.file_type = get_mime_type(path)
    def get_file_info(self) -> dict:
        node_info = NodeInfo(
            name=self._name,
            node_path=self._node_path,
            node_type=self._node_type,
            size=self._node_size
        ).model_dump()
        node_info["mime_type"] = self.file_type

        return node_info
