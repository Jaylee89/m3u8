from unittest import TestCase
from movie.util.util import Util

class TestUnit(TestCase):

    @classmethod
    def setUpClass(cls):
        print ("this setupclass() method only called once.\n")

    @classmethod
    def tearDownClass(cls):
        print ("this teardownclass() method only called once too.\n")

    def setUp(self):
        print ("do something before test : prepare environment.\n")

    def tearDown(self):
        print ("do something after test : clean up.\n")

    def test_get_random(self):
        """random"""
        result = Util.get_random(2)
        self.assertLessEqual(next(result), 200, msg="{} less equal to 2".format(result))
