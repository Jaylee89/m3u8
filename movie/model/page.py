
class Page(object):
    start: int
    end: int
    domain: str
    all_urls: Any
    m3u8_dict: dict
    __slots__ = ("start", "end", "domain", "all_urls", "m3u8_dict")

    def __init__(self, start, end, domain, all_urls = [], **m3u8_dict):
        # super().__init__()
        self.start = start
        self.end = end
        self.domain = domain
        self.all_urls = all_urls
        self.m3u8_dict = m3u8_dict
    