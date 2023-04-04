import glob
from concurrent.futures import ThreadPoolExecutor
import m3u8
import os, math
import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

import json, random, time
from vendors.qianyujie.model import QianYuJie, CourseChapter
from util.util import Util

headers = {
    "Host": "82497838.clarc.cn",
    "Connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxd8e7462679f3ac0e/44/page-frame.html"
}

# uid = "16825"
uid = "16523"

def download_video_url(id, file_name, parent_name):
    real_url = f"https://82497838.clarc.cn/course/chapter_detail?chapter_id={id}&uid={uid}"
    response = requests.get(real_url, headers=headers)
    response.raise_for_status()
    content = response.content

    json_data = json.loads(content)

    status = json_data["status"]
    if status["status"] != 200 and status["succeed"] != 1:
        print(f"Error: {id}, {file_name}, {parent_name}")
        return (False, None)
    data = json_data["data"]
    video_url = data["video"]
    video_info = (f"{parent_name},{file_name}-{id},{video_url}")
    print(video_info)

    Util.write_file(f"{video_info}\n", "tmp/qianyujie/video_info.txt")

def download_ts(url, file_name, folder):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.content
        # data = AESDecrypt(data, key=key, iv=key)
        with open(f"{folder}/{file_name}.mp4", "ab") as f:
            f.write(data)
        print(f"\r{file_name}.mp4 Downloaded", end="  ")
    except BaseException as error:
        print(error)


def get_real_url(url):
    playlist = m3u8.load(uri=url, headers=headers)
    return playlist.playlists[0].absolute_uri if len(playlist.playlists) else url


def AESDecrypt(cipher_text, key, iv):
    if key is None:
        return cipher_text
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text

def get_root_data():
    real_url = f"https://82497838.clarc.cn/course/chapter?uid={uid}&course_id=53"
    response = requests.get(real_url, headers=headers)
    response.raise_for_status()
    content = response.content

    json_data = json.loads(content)

    status = json_data["status"]
    if status["status"] != 200 and status["succeed"] != 1:
        return (False, None)
    data = json_data["data"]
    course_chapters = data["course_chapter"]

    chapters = []
    qianyujie = QianYuJie(chapters)
    for chapter in course_chapters:
        course_id = chapter["course_id"]
        chapter_id = chapter["chapter_id"]
        name = chapter["name"] + f"{str(len(children))}"
        children = chapter["children"]

        chapter_model = CourseChapter(course_id, chapter_id, name)
        children_model = []
        for child in children:
            course_id_sub = child["course_id"]
            chapter_id_sub = child["chapter_id"]
            name_sub = child["name"]
            chapter_child_model = CourseChapter(course_id_sub, chapter_id_sub, name_sub)
            children_model.append(chapter_child_model)

        if len(children_model) != 0:
            chapter_model.set_children(children_model)

        chapters.append(chapter_model)
    qianyujie.data = chapters
    return (True, qianyujie)

def parse_chapter_detail(qianyujie):

    chapters = qianyujie.data

    name_and_chapter_ids = []
    for index, chapter in enumerate(chapters):
        parent_name = f"{str(index)}{chapter.name}"
        children = chapter.children
        for child in children:
            child_name = child.name
            child_chapter_id = child.chapter_id
            name_and_chapter_ids.append((parent_name, child_name, child_chapter_id))

    # read info from local file
    # read_video_url(name_and_chapter_ids)

    max_workers = 10
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for (parent_name, file_name, id) in name_and_chapter_ids:
            pool.submit(download_video_url, id, file_name, parent_name)
    # return results

def download_video(tempdir, max_workers=1):
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    # result, data = get_root_data()
    # if not result:
    #     return

    # _ = parse_chapter_detail(data)

    readlines = Util.read_file("tmp/qianyujie/video_info.txt", readlines=True)
    video_urls = []
    for data in readlines:
        data_split = data.split(",")
        video_urls.append((data_split[0], data_split[1], data_split[2].strip()))

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for (path, file_name, url) in video_urls:
            folder = os.path.join(tempdir, path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            pool.submit(download_ts, url, file_name, folder)

def generate_video(save_name, tempdir, cut_count=0):
    files = glob.glob(f'{tempdir}/*.ts')
    _ = files.sort(reverse = False)
    cut_array = calculate_cut_count(files, cut_count)
    for i, element in enumerate(cut_array):
        with open(f"{save_name}_{i}.mp4", 'wb') as fw:
            for file in element:
                print(f'\rread {file}\r')
                with open(file, 'rb') as fr:
                    fw.write(fr.read())

def calculate_cut_count(files, cut_count=0) -> list:
    result = []
    data_length = len(files)
    if cut_count!=0 and data_length>cut_count:
        piece = math.floor(data_length/cut_count)
        for i in range(cut_count):
            __tmp = []
            if i == cut_count-1:
                __tmp = files[i*piece:]
            else:
                __tmp = files[i*piece:piece*(i+1)]
            result.append(__tmp)
    else:
        result.append(files)
    return result

if __name__ == "__main__":
    tempdir="tmp/qianyujie"
    _ = download_video(tempdir=tempdir)