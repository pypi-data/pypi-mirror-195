import random
import unittest
import pprint
from src.eval_hj3415.eval import red, mil, blue, growth, make_today_eval_df, _make_df_part, yield_valid_spac
from db_hj3415 import mongo2, dbpath

dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['OUTER'])
# dbpath.save(dbpath.make_path()['LOCAL'])
# dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['ATLAS'])


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())
        self.codes = mongo2.Corps(self.client).get_all_corps()
        self.code = '000320'
        self.code = random.choice(self.codes)

    def tearDown(self):
        """테스트 종료 후 파일 삭제 """
        pass

    def test_one(self):
        # 한 종목 전부다
        print('/'.join([str(1), self.code]))
        print(red(self.client, self.code))

        pp = pprint.PrettyPrinter(width=200)
        pp.pprint(mil(self.client, self.code))
        pp.pprint(blue(self.client, self.code))
        pprint.pprint(growth(self.client, self.code), width=150)

    def test_red(self):
        # 특정 한 종목
        print(red(self.client, self.code))

        # 디비 안 전체 종목
        for i, code in enumerate(self.codes):
            print('/'.join([str(i), str(code)]))
            print(red(self.client, code))

    def test_mil(self):
        # 특정 한 종목
        print(mil(self.client, self.code))

        # 디비 안 전체 종목
        for i, code in enumerate(self.codes[:]):
            print('/'.join([str(i), str(code)]))
            print(mil(self.client, code))

    def test_blue(self):
        # 특정 한 종목
        pprint.pprint(blue(self.client, self.code), width=200)

        # 디비 안 전체 종목
        for i, code in enumerate(self.codes):
            print('/'.join([str(i), str(code)]))
            pprint.pprint(blue(self.client, code), width=200)

    def test_growth(self):
        # 특정 한 종목
        pprint.pprint(growth(self.client, self.code), width=150)

        # 디비 안 전체 종목
        for i, code in enumerate(self.codes[:]):
            print('/'.join([str(i), str(code)]))
            pprint.pprint(growth(self.client, code), width=150)


class GetDFTest(unittest.TestCase):
    def test_make_df_part(self):
        codes = ['025320', '000040', '060280', '003240']
        from multiprocessing import Queue
        q = Queue()
        _make_df_part(dbpath.load(), codes, q)

    def test_get_df(self):
        print(make_today_eval_df(db_addr=dbpath.load()))


class SpacTest(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())

    def test_valid_spac(self):
        for code, name, price in yield_valid_spac(self.client):
            print(code, name, price)
