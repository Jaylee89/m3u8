from util import Util
import json, re
# from html.parser import HTMLParser
from bs4 import BeautifulSoup

if __name__ == "__main__":
    html_path = "/Users/jayleeli/work/video/m3u8/movie/data/使徒行者2/index.html"

    text = Util.read_file(filename=html_path)
    htmlCharset = "utf-8"
    soup = BeautifulSoup(text, features="html.parser") #, from_encoding=htmlCharset

    data = []
    #<script>var allPlayUrl=
    #<script>var cms_player = 
    #</script>

    allPlayUrl = "var allPlayUrl="
    cms_player= "var cms_player = "
    for d in soup.findAll("script"):
        value = d.string
        print(value)
        # p1 = re.compile(r"<script>var allPlayUrl=(.*)</script>", re.M|re.I)
        # p2 = re.compile(r"<script>var cms_player = (.*)</script>", re.M|re.I)
        if value is None:
            continue
        # search1 = re.findall(r"var allPlayUrl=(.*);", value)
        # search2 = re.findall(r"var cms_player=(.*);", value)

        parse_data = None
        if value.startswith(allPlayUrl):
            parse_data = value.replace(allPlayUrl, "")
            data.append(parse_data.replace(";", ""))
        elif value.startswith(cms_player):
            parse_data = value.replace(cms_player, "")
            data.append(parse_data.replace(";", ""))
        # if search1:
        #     data.append(search1)
        # elif search2:
        #     data.append(search2)

    



