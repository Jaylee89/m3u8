import unittest

from movie.util.util import Util

class TestUnit(unittest.TestCase):

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
        self.assertLessEqual(result, 2, msg="{} less equal to 2".format(result))

if __name__ == '__main__':
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    unittest.main(verbosity=1)