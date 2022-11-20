import zipfile
import shutil
import glob
import io
import os
import re


PRODUCT_PATH = os.path.join(os.path.split(os.path.abspath('.'))[0], 'storage', 'products')


def file_counter(category: str, prodict_id: str) -> int:
    if category in ('program', 'data', 'service'):
        return 1

    return len(glob.glob(os.path.join(
        PRODUCT_PATH, category, str(prodict_id), '*.txt'
    )))

def is_digit(string: str, only_integer: bool = False) -> bool:
    if only_integer:
        return bool(re.match(r'^\d+?$', string))
    return bool(re.match(r'^((\d+?\.\d+?)|\d+?)$', string))

def move_tmp_dir(category: str, prodict_id: str, number: int, dir_name: str) -> str:
    path = os.path.join(PRODUCT_PATH, category, str(prodict_id))
    tmp_dir = os.path.join(path, 'tmp', str(dir_name))

    os.makedirs(tmp_dir, exist_ok=True)

    for file_path in glob.glob(f'{path}/*.txt')[:number]:
        shutil.move(file_path, tmp_dir)

    return tmp_dir

def move_main_dir(tmp_dir: str) -> None:
    path = os.path.split(os.path.split(tmp_dir)[0])[0]

    for file_path in glob.glob(f'{tmp_dir}/*.txt'):
        shutil.move(file_path, path)

    try:
        os.rmdir(tmp_dir)
    except FileNotFoundError:
        pass

def extract(obj: io.BytesIO, save_path: str) -> None:
    os.makedirs(save_path, exist_ok=True)

    if not zipfile.is_zipfile(obj):
        raise Exception

    with zipfile.ZipFile(obj) as file:
        file.extractall(save_path)

def archiv(path: str) -> io.BytesIO:
    buf = io.BytesIO()

    with zipfile.ZipFile(buf, 'w') as file:
        for file_name in os.listdir(path):
            file.write(os.path.join(path, file_name), file_name)

    shutil.rmtree(path, ignore_errors=True)
    return buf

def save_archive(obj: io.BytesIO, file_name: str, save_path: str) -> None:
    os.makedirs(save_path, exist_ok=True)

    if not zipfile.is_zipfile(obj):
        raise Exception

    with open(os.path.join(save_path, file_name), 'wb') as file:
        file.write(obj.getvalue())
