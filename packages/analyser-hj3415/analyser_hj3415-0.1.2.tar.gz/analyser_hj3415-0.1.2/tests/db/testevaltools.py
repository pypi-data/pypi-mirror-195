import unittest
from src.eval_hj3415 import db
from krx_hj3415 import krx
from db_hj3415 import mongo2, dbpath

dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['OUTER'])
# dbpath.save(dbpath.make_path()['LOCAL'])
# dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['ATLAS'])


class C104Tests(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())
        self.c104db = db.C104(self.client, '005930', 'c104y')

    def test_find_cmp(self):
        print(self.c104db.find_cmp('이자보상배율'))
        self.c104db.code = '352700'
        print(self.c104db.find_cmp('이자보상배율'))


class CorpsEvalOneTests(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())
        self.evaldb = db.CorpsEval(self.client, code='005930')

    def tearDown(self):
        pass

    def test_calcprofit(self):
        print(self.evaldb.calc당기순이익())
        # kb금융
        self.evaldb.code = '105560'
        print(self.evaldb.calc당기순이익())

    def test_calcasset1(self):
        print(self.evaldb.calc유동자산())
        # kb금융
        self.evaldb.code = '105560'
        print(self.evaldb.calc유동자산())

    def test_calcdebt(self):
        print(self.evaldb.calc유동부채())
        # kb금융
        self.evaldb.code = '105560'
        print(self.evaldb.calc유동부채())

    def test_calcdebt2(self):
        print(self.evaldb.calc비유동부채())
        # kb금융
        self.evaldb.code = '105560'
        print(self.evaldb.calc비유동부채())
        # 삼성생명
        self.evaldb.code = '032830'
        print(self.evaldb.calc비유동부채())

    def test_findfcf(self):
        print(self.evaldb.findFCF())

    def test_findpfcf(self):
        print(self.evaldb.findPFCF())

    def test_calccurrentratio(self):
        print(self.evaldb.calc유동비율())


class CorpsEvalAllTests(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())
        self.codes = krx.get_codes()
        self.evaldb = db.CorpsEval(self.client, code='005930')

    def tearDown(self):
        pass

    def test_calcprofit(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.calc당기순이익())

    def test_calcasset1(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.calc유동자산())

    def test_calcdebt(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.calc유동부채())

    def test_calcdebt2(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.calc비유동부채())

    def test_findfcf(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.findFCF())

    def test_findpfcf(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.findPFCF())

    def test_calccurrentratio(self):
        for i, code in enumerate(self.codes):
            print('/'.join([str(i),str(code)]))
            self.evaldb.code = code
            print(self.evaldb.calc유동비율(pop_count=3))

    def test_get_recent(self):
        print(self.evaldb.findPFCF())
        print(self.evaldb.get_recent(self.evaldb.findPFCF()))
        print(self.evaldb.findFCF())
        print(self.evaldb.get_recent(self.evaldb.findFCF()))
