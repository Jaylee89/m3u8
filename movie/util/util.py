import random
# from math import ceil
import os
# from pathlib import Path

class Util:

    @staticmethod
    def read_file(filename, readline=False, readlines=False):
        result = None
        try:
            with open(file=filename, mode="r", buffering=1024, encoding="utf8") as f:
                if f.readable():
                    if readline:
                        result = f.readline()
                    elif readlines:
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

            # _file = Path(path)
            # if _file.is_file():
            #     _file = _file.parent()
            # if not _file.exists():
            #     _file = _file.parent()
            # _file.mkdir(parents=True, exist_ok=True)
            func(stream, path)
        return result

    @staticmethod
    @check_directory
    def write_file(string, path):
        try:
            with open(file=path, mode="w", buffering=1024, encoding="utf8") as f:
                if f.writable():
                    f.write(string)
        except Exception as error:
            print("file read error is {}".format(error))

    @staticmethod
    def get_random(length=1) -> int:
        scope = 800 if length>10 else length*100
        for i in range(length):
            yield random.randint(0, scope)