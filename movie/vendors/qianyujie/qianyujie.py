"""
1. get chapters list and merge into array
2. fetch the data from array
"""
import sys

from util.flow import Flow
from network.downloader import Downloader
from model import QianYuJieResponse, LanguageInfoModel

from concurrent.futures import ThreadPoolExecutor
from util.file import File

"""
common info
"""
headers = {
    "Host": "82497838.clarc.cn",
    "Connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxd8e7462679f3ac0e/66/page-frame.html"
}

class QianYuJie:
    uid: str = "16822"
    downloader: Downloader
    navs: list = []
    course_info: list = []
    chapter_info: list = []

    result: list = []

    def __init__(self):
        self.downloader = Downloader(True, headers=headers)

    def handle_all_data(self):
        api_status, language_list = self._get_language_list()
        if api_status is False:
            sys.exit()
        name, assortment_id = self._to_select_a_language(language_list)
        if assortment_id and type(assortment_id) == str:
            api_status, course_list = self._get_course_list(assortment_id)
            course_name, selected_course_id = self._to_select_a_course(course_list)
            if selected_course_id and type(selected_course_id) == str:
                api_status, chapter_list = self._get_chapter_list(selected_course_id)
                self._to_analyze_all_chapters(chapter_list)
        
        self.download(name, course_name)

    def download(self, name, course_name):
        """
        1. write data to txt file
        2. download video in multiple threads
        """
        # max_workers = 10
        # with ThreadPoolExecutor(max_workers=max_workers) as pool:
        #     for index, v in enumerate(self.chapter_info):
        #         children = v.children
        #         new_index = index+1
        #         if children and len(children) > 0:
        #             for child in children:
        #                 pool.submit(self.handle_chapter_detail_data, child.chapter_id, new_index, name, course_name, v.name, child_chapter_name=child.name)
        #         else:
        #             pool.submit(self.handle_chapter_detail_data, v.chapter_id, new_index, name, course_name, v.name)

        """
        for testing & debug
        """
        for index, v in enumerate(self.chapter_info):
            children = v.children
            if children and len(children) > 0:
                for child in children:
                    self.handle_chapter_detail_data(v.chapter_id, index+1, name, course_name, v.name, child_chapter_name=child.name)
            else:
                self.handle_chapter_detail_data(v.chapter_id, index+1, name, course_name, v.name)

    def handle_chapter_detail_data(self, chapter_id, index, name, course_name, parent_chapter_name, child_chapter_name=None):
        api_status, chapter_detail = self._get_chapter_detail(chapter_id)
        if api_status is False:
            print(f"failed info is {chapter_id}, {name}, {course_name}")
            return
        course_id, chapter_id, chapter_name, video = self._to_analyze_chapter_detail(chapter_detail)

        if child_chapter_name is None:
            chapter_name = f"{index}.{chapter_name}" if not chapter_name.startswith(str(index)) else chapter_name
            chapter_detail_txt = ",".join(list((name, course_name, f"{chapter_name}-{course_id}-{chapter_id}", video)))
        else:
            parent_chapter_name = f"{index}.{parent_chapter_name}" if not parent_chapter_name.startswith(str(index)) else parent_chapter_name
            chapter_detail_txt = ",".join(list((name, course_name, parent_chapter_name, f"{chapter_name}-{course_id}-{chapter_id}", video)))

        self.result.append(chapter_detail_txt)
        File.write_file(chapter_detail_txt, f"vendors/qianyujie/全部类目/{name}/{course_name}/video_info.txt")

        if child_chapter_name is None:
            chapter_detail_batch = " ".join(list(("curl", video, "--output", f"{chapter_name}-{course_id}-{chapter_id}.mp4")))
        else:
            chapter_detail_batch = " ".join(list(("curl", video, "--output", f"{parent_chapter_name}/{chapter_name}-{course_id}-{chapter_id}.mp4")))
        File.write_file(chapter_detail_batch, f"vendors/qianyujie/全部类目/{name}/{course_name}/batch.sh")

    # download part
    def _get_language_list(self) -> tuple:
        file_name = "mocks/qianyujie/all_languages.json"
        response_json = self.downloader._get_json("https://82497838.clarc.cn/index", file_name=file_name)
        return response_json

    def _get_course_list(self, assortment_id: str) -> tuple:
        params = {
            "assortment_id": assortment_id,
            "page": 1,
            "page_size": 20
        }
        file_name = "mocks/qianyujie/cantonese_course_list.json"
        response_json = self.downloader._get_json("https://82497838.clarc.cn/course/list", params, file_name=file_name)
        return response_json

    def _get_chapter_list(self, course_id: str) -> tuple:
        params = {
            "uid": self.uid,
            "course_id": course_id
        }
        file_name = "mocks/qianyujie/pinyin_chapters_with_children.json"
        response_json = self.downloader._get_json("https://82497838.clarc.cn/course/chapter", params, file_name=file_name)
        return response_json

    def _get_chapter_detail(self, chapter_id: str) -> tuple:
        params = {
            "uid": self.uid,
            "chapter_id": chapter_id
        }
        file_name = "mocks/qianyujie/chapter_detail.json"
        response_json = self.downloader._get_json("https://82497838.clarc.cn/course/chapter_detail", params, file_name=file_name)
        return response_json

    # data analysis part
    def _to_select_a_language(self, dict_items) -> tuple:
        if QianYuJieResponse.check_status(dict_items):
            data = dict_items.data
            nav = data.nav
            for object in nav:
                self.navs.append(LanguageInfoModel(object.name, assortment_id=object.assortment_id))
            
            flow = Flow(self.navs)
            option = flow.select_option()
            name = option.name
            assortment_id = option.assortment_id
            return (name, assortment_id)

    def _to_select_a_course(self, dict_items) -> tuple:
        if QianYuJieResponse.check_status(dict_items):
            data = dict_items.data
            courses = data.course
            for object in courses:
                self.course_info.append(LanguageInfoModel(object.name, course_id=object.course_id))
            
            flow = Flow(self.course_info)
            option = flow.select_option()
            name = option.name
            course_id = option.course_id
            return (name, course_id)

    def _to_analyze_all_chapters(self, dict_items):
        if QianYuJieResponse.check_status(dict_items):
            data = dict_items.data
            chapter_ids = data.course_chapter
            for object in chapter_ids:
                self.chapter_info.append(LanguageInfoModel(object.name, course_id=object.course_id, chapter_id=object.chapter_id, children=object.children))

    def _to_analyze_chapter_detail(self, dict_items):
        if QianYuJieResponse.check_status(dict_items):
            data = dict_items.data
            course_id = data.course_id
            chapter_id = data.chapter_id
            chapter_name = data.chapter_name
            video = data.video
            return (course_id, chapter_id, chapter_name, video)