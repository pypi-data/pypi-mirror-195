from typing import Union, Optional, Dict, Any
from streamsync.core import Readable, FileWrapper, BytesWrapper, Config
from streamsync.core import initial_state, component_manager

component_manager

VERSION = "0.1.0"

def pack_file(file: Union[Readable, str], mime_type: Optional[str]):
    return FileWrapper(file, mime_type)


def pack_bytes(raw_data, mime_type: Optional[str]):
    return BytesWrapper(raw_data, mime_type)


def init_state(state_dict: Dict[str, Any]):
    initial_state.user_state.state = {}
    initial_state.user_state.ingest(state_dict)
