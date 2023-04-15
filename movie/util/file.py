import os

from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

class File:

    @staticmethod
    def read_file(file_name, read_lines=False):
        result = None
        file_path = os.path.join(ROOT_PATH, file_name)
        try:
            with open(file=file_path, mode="r", buffering=1024, encoding="utf8") as f:
                if f.readable():
                    if read_lines:
                        result = f.readlines()
                    else:
                        result = f.read()
        except Exception as error:
            print("file read error is {}".format(error))
        return result

    def check_directory(func):
        def result(stream, path):
            _path = os.path.dirname(path)
            if not os.path.exists(_path):
                os.makedirs(_path)
            func(stream, path)
        return result

    @staticmethod
    @check_directory
    def write_file(data: str, file_name: str):
        try:
            file_path = os.path.join(ROOT_PATH, file_name)
            with open(file=file_path, mode="w", buffering=1024, encoding="utf8") as f:
                if f.writable():
                    f.write(data.strip() + "\n")
        except Exception as error:
            print("file read error is {}".format(error))