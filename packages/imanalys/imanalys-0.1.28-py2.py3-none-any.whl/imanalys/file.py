"""File manipulation collection"""

import shutil
import os
import requests

def move(src: str, temp: str) -> str:
    """Copy file"""
    file_name = os.path.basename(src)
    if not os.path.exists(temp):
        os.makedirs(tmp)
    file_path = os.path.join(tmp, file_name)
    shutil.copyfile(src, file_path)
    return file_path

def download(url: str, temp: str) -> str:
    """Download file"""
    if not os.path.exists(temp):
        os.makedirs(tmp)
    file_name = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(temp, file_name)
    _r = requests.get(url, stream=True)
    if _r.ok:
        with open(file_path, 'wb') as _f:
            for chunk in _r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    _f.write(chunk)
                    _f.flush()
                    os.fsync(_f.fileno())
    return file_path

def delete(path):
    if os.path.exists(path):
        os.remove(path)

def name(path):
    return os.path.basename(path)

def size(path):
    return os.stat(path).st_size
