import os
from typing import List


def mkdirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def touch(filename):
    mkdirs(os.path.dirname(filename))
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('')


def is_file(filename):
    return os.path.isfile(filename)


def read_file(file: str) -> str:
    with open(file, encoding='utf-8') as f:
        return f.read()


def write_file(file: str, content: str):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)


def list_files(path: str) -> List[str]:
    return os.listdir(path)
