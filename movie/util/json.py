import json, os

from types import SimpleNamespace

from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

class JSONLoader:

    @staticmethod
    def load(file_name: str):
        json_data = None
        file_path = os.path.join(ROOT_PATH, file_name)
        with open(f"{file_path}") as f:
            if f.readable():
                data = f.read()
                json_data = json.loads(data)
        return json_data

    @staticmethod
    def load_decodable(file_name: str):
        file_path = os.path.join(ROOT_PATH, file_name)
        with open(f"{file_path}") as f:
            if f.readable():
                data = f.read()
                object = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return object