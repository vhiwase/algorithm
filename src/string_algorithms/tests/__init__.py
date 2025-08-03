import sys
from pathlib import Path

def add_project_root_to_sys_path():
    project_root = Path(__file__).resolve().parents[1]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.append(project_root_str)

add_project_root_to_sys_path()

from .test_string_sequence_matcher import *

__all__ = test_string_sequence_matcher.__all__