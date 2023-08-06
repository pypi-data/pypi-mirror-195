import glob
import os
from typing import List

DATASET_DIR = os.path.abspath(os.path.dirname(__file__))

_HTML_PATTERNS = ['html', 'htm']


def load_dataset_from_directory(dir_: str, recursive: bool = True) -> List[str]:
    dir_ = dir_ or DATASET_DIR
    files = []
    for ext_name in _HTML_PATTERNS:
        if recursive:
            pattern = os.path.join(dir_, '**', f'*.{ext_name}')
            files.extend(glob.glob(pattern, recursive=True))
        else:
            pattern = os.path.join(dir_, f'*.{ext_name}')
            files.extend(glob.glob(pattern))

    return sorted(files)


def load_local_dataset(recursive: bool = True) -> List[str]:
    return load_dataset_from_directory(DATASET_DIR, recursive=recursive)
