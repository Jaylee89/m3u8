from unittest import TestCase
from movie.util.json import JSONLoader

class TestUnit(TestCase):
    def test_json_decode(self):
        data = JSONLoader.load_decodable("vendors/qianyujie/全部类目/粤语/20天学会粤语基础篇/1.json")
        self.assertEqual(data.status.status, 200)
        self.assertEqual(data.data.course_chapter[0].course_id, '53')
        self.assertEqual(data.data.course_chapter[0].chapter_id, '616')
