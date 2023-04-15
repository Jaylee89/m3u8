from urllib.parse import urlparse
from util.json import JSONLoader
import requests

class Downloader(object):
    header: dict
    is_mock = False

    def __init__(self, *args, **kwargs):
        self.is_mock = args[0]
        self.header = kwargs

    def _build_parse_url(self, url, **kwargs):
        return urlparse(url)

    def _get_text(self, url, params=None):
        response = requests.get(url, params=params, verify=False)
        return (response.ok, response.text)
    
    def _get_stream(self, url, params=None):
        response = requests.get(url, params=params, stream=True, timeout=600, verify=False)
        # response = requests.get(url, verify=False)
        return (response.ok, response.content)

    def _get_json(self, url, params=None, file_name: str = ""):
        is_mock, object = self.enable_mock_data(file_name)
        if is_mock:
            return (is_mock, object)
        response = requests.get(url, params=params, **self.header, verify=False)
        return (response.ok, JSONLoader.load_decodable_with_bytes(response.content))

    def _post_json(self, url, data=None, json=None, file_name: str = ""):
        is_mock, object = self.enable_mock_data(file_name)
        if is_mock:
            return (is_mock, object)
        response = requests.post(url, data=data, json=json, **self.header, verify=False)
        return (response.ok, JSONLoader.load_decodable_with_bytes(response.content))

    def enable_mock_data(self, file_name: str):
        try:
            object = JSONLoader.load_decodable(file_name)
            return (self.is_mock, object)
        except Exception:
            return (False, None)
