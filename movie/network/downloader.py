from urllib.parse import urlparse
import requests

class Downloader(object):
    def __init__(self, header):
        self.header = header

    def _build_parse_url(self, url, **kwargs):
        return urlparse(url)

    def _get_text(self, url, param=None):
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return (response.status_code, response.text)
    
    def _get_stream(self, url, param=None):
        response = requests.get(url, stream=True, timeout=600, verify=False)
        # response = requests.get(url, verify=False)
        response.raise_for_status()
        return (response.status_code, response.content)
    
    def _get_json(self, url, param=None):
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return (response.status_code, response.json())
    
    def _post(self, url, data=None, json=None, **kwargs):
        response = requests.post(url, data=data, json=json, verify=False)
        response.raise_for_status()
        return response