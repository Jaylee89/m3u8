import json, os

from pathlib import Path

ROOT_PATH = Path(__file__).parent

CONFIG_PATH = os.path.join(ROOT_PATH, "vendors")

class JSONLoader:

    @staticmethod
    def load(file_name: str):
        json_data = None
        file_path = os.path.join(CONFIG_PATH, file_name)
        with open(f"{file_path}") as f:
            if f.readable():
                data = f.read()
                json_data = json.loads(data)
        return json_data