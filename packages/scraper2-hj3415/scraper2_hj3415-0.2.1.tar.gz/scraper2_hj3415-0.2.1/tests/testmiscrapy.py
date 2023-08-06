import unittest
from src.scraper2_hj3415.krx import krx
from src.scraper2_hj3415.miscrapy import run as mirun


class MiscrapyTests(unittest.TestCase):
    def setUp(self):
        self.mongo_addr = "mongodb://192.168.0.173:27017"
        # self.mongo_addr = ""

    def test_one_spider(self):
        # spiders = ('aud', 'chf', 'gbond3y', 'gold', 'kosdaq', 'kospi', 'silver', 'sp500', 'usdidx', 'usdkrw', 'wti',)
        mirun._mi_test('chf', self.mongo_addr)


