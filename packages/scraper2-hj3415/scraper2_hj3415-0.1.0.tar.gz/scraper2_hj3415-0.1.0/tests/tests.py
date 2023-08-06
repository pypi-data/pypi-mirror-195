import unittest
from util_hj3415 import utils
from src.scraper2_hj3415.nfscrapy import run as nfsrun


class SaveNfsTests(unittest.TestCase):
    def setUp(self):
        self.code_one = "005930"
        #self.code_one = ""
        self.mongo_addr = "mongodb://192.168.0.173:27017"
        #self.mongo_addr = ""
        self.rnd_code_list = utils.pick_rnd_x_code(2)

    def test_c101(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c101([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c101(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c101(self.rnd_code_list, self.mongo_addr)

    def test_c103(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c103([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c103(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c103(self.rnd_code_list, self.mongo_addr)
            
    def test_c104(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c104([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c104(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c104(self.rnd_code_list, self.mongo_addr)

    def test_c106(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c106([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c106(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c106(self.rnd_code_list, self.mongo_addr)
