import os

from network.downloader import Downloader
from util.util import Util

if __name__ == '__main__':
    url = "http://www.metvb1.com/play/8248-2-30.html"
    file_path = dirname = os.path.join(os.path.dirname(__file__), "config", "user-agent.txt")
    user_agent = Util.read_file(filename=file_path, readline=True)
    header = {
        "User-Agent": user_agent,
        # "Cache-Control": "max-age=0",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Connection": "keep-alive",
        # "Host": "www.metvb1.com",
        # "Referer": "http://www.metvb1.com/play/8248-2-30.html"
    }
    download = Downloader(header=header)
    stream = download._get_stream(url=url)
    response_data = None
    if stream[0] == 200:
        response_data = stream[1]
    assert response_data

    dirname = os.path.join(os.path.dirname(__file__), "data", "使徒行者2")
    html_path = os.path.join(dirname, "index.html")
    Util.write_file(response_data.decode("utf-8"), html_path)


