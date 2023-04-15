from unittest import TestCase
from movie.vendors.qianyujie.qianyujie import QianYuJie

class TestUnit(TestCase):
    qianyujie: QianYuJie

    def setUp(self) -> None:
        self.qianyujie = QianYuJie()
        return super().setUp()

    def test_json_decode(self):
        self.qianyujie.handle_all_data()
