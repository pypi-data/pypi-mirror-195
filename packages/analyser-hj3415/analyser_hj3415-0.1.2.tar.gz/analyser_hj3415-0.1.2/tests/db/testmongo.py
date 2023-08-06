import unittest
import random
import pprint
import pandas as pd
import scraper2_hj3415.nfscrapy.run

from src.analyser_hj3415.db import mongo
from scraper2_hj3415.krx import krx
from scraper2_hj3415 import nfscrapy


class MongoBaseTest(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")

    def setUp(self) -> None:
        self.mongodb = mongo.MongoBase(self.client, '005930', 'c101')

    def test_db_name(self):
        print(self.mongodb.db_name)
        self.mongodb.client = None
        with self.assertRaises(Exception):
            self.mongodb.db_name = "005490"

    def test_get_all_db_name(self):
        print(mongo.MongoBase.get_all_db_name(self.client))

    def test_validate_db(self):
        self.assertTrue(mongo.MongoBase.validate_db(self.client, "005930"))
        with self.assertRaises(Exception):
            mongo.MongoBase.validate_db(self.client, "123456")

    def test_validate_col(self):
        self.assertTrue(self.mongodb.validate_col())
        self.mongodb.col_name = 'c108'
        with self.assertRaises(Exception):
            self.mongodb.validate_col()

    def test_get_all_docs(self):
        pprint.pprint(self.mongodb.get_all_docs())

    def test_del_doc(self):
        self.client['test_db']['test_col'].insert_one({'test1': "test1-1"})
        self.mongodb.db_name = 'test_db'
        self.mongodb.col_name = 'test_col'
        self.mongodb.del_doc({'test1': "test1-1"})


class C103Test(unittest.TestCase):
    addr = "mongodb://192.168.0.173:27017"
    client = mongo.connect_mongo(addr)

    def setUp(self):
        # 테스트 코드의 자료를 저장한다.
        self.test_code = krx.pick_rnd_x_code(1)
        print('code:', self.test_code)
        nfscrapy.run.c103(self.test_code, self.addr)

        # 데이터베이스를 설정한다.
        self.pages = ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                      'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',)
        self.c103 = mongo.C103(self.client, self.test_code[0], self.pages[0])

    def test_save(self):
        # 000000 데이터베이스에 임의의 데이터를 저장하고 완료후 삭제한다.
        temp_db = '000000'
        temp_col = random.choice(self.pages)
        self.c103 = mongo.C103(self.client, temp_db, temp_col)
        data = [
            {'항목': '자산총계', '2020/09': 3757887.4, '2020/12': 3782357.2, '2021/03': 3928262.7, '2021/06': 3847776.7, '2021/09': 4104207.2, '전분기대비': 6.7},
            {'항목': '유동자산', '2020/09': 2036349.1, '2020/12': 1982155.8, '2021/03': 2091553.5, '2021/06': 1911185.2, '2021/09': 2127930.2, '전분기대비': 11.3},
            {'항목': '재고자산', '2020/09': 324428.6, '2020/12': 320431.5, '2021/03': 306199.8, '2021/06': 335923.9, '2021/09': 378017.0, '전분기대비': 12.5}
        ]
        df = pd.DataFrame(data)
        print(f'code: {temp_db}')
        self.c103.save_df(df)

        mongo.MongoBase.del_db(self.client, temp_db)

    def test_find(self):
        # 임의의 종목의 모든 페이지의 모든 타이틀을 출력한다.
        for col in self.pages:
            print('#'*10, col, '#'*10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                d = self.c103.find(title)
                print(title, d)

    def test_latest_value(self):
        # 임의 종목의 모든 타이틀의 최근 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                print(title, self.c103.latest_value(title))

    def test_sum_recent_4q(self):
        # 임의 종목의 모든 타이틀 최근 4분기합을 반환한다. 비교를 위해서 년도의 최근값도 첨가하였다.
        result_dict = {}
        for col in self.pages:
            self.c103.page = col
            for title in self.c103.get_all_titles():
                result_dict[title] = []

        for col in self.pages:
            self.c103.page = col
            if col.endswith('q'):
                for title in self.c103.get_all_titles():
                    result_dict[title] += list(self.c103.sum_recent_4q(title))
            elif col.endswith('y'):
                for title in self.c103.get_all_titles():
                    result_dict[title] += list(self.c103.latest_value(title))

        print('#' * 20)
        pprint.pprint(result_dict)

    def test_find_증감율(self):
        # 임의 종목의 모든 타이틀의 증감율 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                print(title, self.c103.find_증감율(title))


class C103TestHardLoading(unittest.TestCase):
    """
    좀더 많은 종목을 테스트하기 위해서 만든 테스트함수. n으로 종목의 개수를 설정한다.
    """
    addr = "mongodb://192.168.0.173:27017"
    client = mongo.connect_mongo(addr)
    # 임의의 종목 n 개를 뽑아 데이터를 채운다.
    n = 10
    rnd_codes = krx.pick_rnd_x_code(n)
    nfscrapy.run.c103(rnd_codes, addr)

    def setUp(self):
        # 데이터베이스를 설정한다.
        self.pages = ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                      'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',)
        self.c103 = mongo.C103(self.client, self.rnd_codes[0], self.pages[0])

    def test_find_hard_loading(self):
        for code in self.rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#'*10, col, '#'*10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    d = self.c103.find(title)
                    print(title, d)

    def test_latest_value_hard_loading(self):
        for code in self.rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    print(title, self.c103.latest_value(title))

    def test_sum_recent_4q_hard_loading(self):
        for code in self.rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            result_dict = {}
            for col in self.pages:
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    result_dict[title] = []

            for col in self.pages:
                self.c103.page = col
                if col.endswith('q'):
                    for title in self.c103.get_all_titles():
                        result_dict[title] += list(self.c103.sum_recent_4q(title))
                elif col.endswith('y'):
                    for title in self.c103.get_all_titles():
                        result_dict[title] += list(self.c103.latest_value(title))
            pprint.pprint(result_dict)

    def test_find_증감율(self):
        for code in self.rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    print(title, self.c103.find_증감율(title))







class C104Test(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")

    def setUp(self):
        pages = ['c104q', 'c104y']
        self.rnd_code = krx.pick_rnd_x_code(1)[0]
        self.c104 = mongo.C104(self.client, self.rnd_code, random.choice(pages))

    def test_modify_stamp(self):
        self.c104.modify_stamp(days_ago=2)
        self.c104.del_col()

    def test_get_all_titles(self):
        data1 = [
            {'항목': '매출액증가율', '2016/12': 0.6, '2017/12': 18.68, '2018/12': 1.75, '2019/12': -5.49, '2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율', '2016/12': 10.7, '2017/12': 83.46, '2018/12': 9.77, '2019/12': -52.84, '2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24},
            {'항목': '순이익증가율', '2016/12': 19.23, '2017/12': 85.63, '2018/12': 5.12, '2019/12': -50.98, '2020/12': 21.48, '2021/12': 48.01, '전년대비': 72.46, '전년대비1': 26.53},
        ]
        df1 = pd.DataFrame(data1)
        self.c104.save_df(df1)

        print(self.c104.get_all_titles())

        self.c104.del_col()

    def test_save_df(self):
        data1 = [
            {'항목': '매출액증가율', '2016/12': 0.6, '2017/12': 18.68, '2018/12': 1.75, '2019/12': -5.49, '2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율', '2016/12': 10.7, '2017/12': 83.46, '2018/12': 9.77, '2019/12': -52.84, '2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24},
            {'항목': '순이익증가율', '2016/12': 19.23, '2017/12': 85.63, '2018/12': 5.12, '2019/12': -50.98, '2020/12': 21.48, '2021/12': 48.01, '전년대비': 72.46, '전년대비1': 26.53},
        ]

        data2 = [
            {'항목': '총자산증가율', '2016/12': 8.26, '2017/12': 15.1, '2018/12': 12.46, '2019/12': 3.89, '2020/12': 7.28,'2021/12': 7.48, '전년대비': 3.39, '전년대비1': 0.2},
            {'항목': '유동자산증가율', '2016/12': 13.31, '2017/12': 3.93, '2018/12': 18.86, '2019/12': 3.83, '2020/12': 9.28,'2021/12': 8.62, '전년대비': 5.45, '전년대비1': -0.66},
            {'항목': '유형자산증가율', '2016/12': 5.78, '2017/12': 22.07, '2018/12': 3.36, '2019/12': 3.82, '2020/12': 7.62,'2021/12': float('nan'), '전년대비': 3.8, '전년대비1': float('nan')},
            {'항목': '자기자본증가율', '2016/12': 7.76, '2017/12': 11.16, '2018/12': 15.51, '2019/12': 6.11, '2020/12': 4.97,'2021/12': 7.05, '전년대비': -1.13, '전년대비1': 2.08}
        ]
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        print(f'code: {self.rnd_code}')
        # print(df)
        # print(df.to_dict('records'))

        # save test - serial data
        self.c104.save_df(df1)
        self.c104.save_df(df2)

        # save test - duplcate data
        with self.assertRaises(Exception):
            self.c104.save_df(df1)

        # save test - 2DA ago
        self.c104.modify_stamp(days_ago=2)
        self.c104.save_df(df1)
        self.c104.save_df(df2)

        self.c104.del_col()

    def test_find(self):
        self.c104 = mongo.C104(self.client, '005930', 'c104y')
        for col in ['c104y', 'c104q']:
            print(col)
            self.c104.page = col
            for title in self.c104.get_all_titles():
                d = self.c104.find(title)
                print(d)


class C101Tests(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")

    def setUp(self):
        self.c101 = mongo.C101(self.client, code='005930')
        self.codes = krx.get_codes()

    def test_save(self):
        ex_c101 = {'date': '2021.08.09',
                   '코드': '005930',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        ex_c101 = {'date': '2021.08.09',
                   '코드': '005930',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        print(self.c101.get_all())

        self.c101.my_col.delete_many({'date': {"$eq": ex_c101['date']}})

    def test_find(self):
        ex_c101 = {'date': '2021.08.09',
                   '코드': '005930',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        print(self.c101.find('20210809'))

        # 날짜가 없는 경우
        print(self.c101.find('20210709'))

        self.c101.my_col.delete_many({'date': {"$eq": ex_c101['date']}})

    def test_get_all(self):
        ex_c101_1 = {'date': '2021.08.08',
                     '코드': '005930',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        ex_c101_2 = {'date': '2021.08.09',
                     '코드': '005930',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101_1)
        self.c101.save_dict(ex_c101_2)

        import pprint
        pprint.pprint(self.c101.get_all())

        self.c101.my_col.delete_many({'date': {"$eq": ex_c101_1['date']}})
        self.c101.my_col.delete_many({'date': {"$eq": ex_c101_2['date']}})

    def test_get_recent(self):
        ex_c101_1 = {'date': '2021.08.08',
                     '코드': '005930',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        ex_c101_2 = {'date': '2021.08.09',
                     '코드': '005930',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        #self.c101.save(ex_c101_1)
        #self.c101.save(ex_c101_2)

        print(self.c101.get_recent())

        # self.c101.client[self.c101.code][self.c101.page].delete_many({'date': {"$eq": ex_c101_1['date']}})
        # self.c101.client[self.c101.code][self.c101.page].delete_many({'date': {"$eq": ex_c101_2['date']}})


class C106Tests(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")

    def setUp(self):
        self.rnd_code = krx.pick_rnd_x_code(1)[0]
        self.c106y = mongo.C106(self.client, self.rnd_code, 'c106y')
        self.c106q = mongo.C106(self.client, self.rnd_code, 'c106q')

    def test_save_load_find(self):
        data = [{'항목': '전일종가', '린드먼아시아': '6500', '삼성스팩2호': '8280', '큐캐피탈': '4085', '엠벤처투자': '305', '나우IB': '14100'},
                {'항목': '시가총액', '린드먼아시아': '877.5', '삼성스팩2호': '854.1', '큐캐피탈': '885.5', '엠벤처투자': '835.0', '나우IB': '890.3'}]
        df = pd.DataFrame(data)
        print(f'code: {self.rnd_code}')
        self.c106y.save_df(df)
        self.c106q.save_df(df)

        print(self.c106y.load_df())
        print(self.c106q.load_df())

        for title in self.c106y.get_all_titles():
            d = self.c106y.find(title)
            print(d)

        self.c106y.del_col()
        self.c106q.del_col()


class MITests(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")
    indexes = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
               'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def setUp(self):
        self.mi = mongo.MI(client=self.client, index='aud')

    def test_save_and_load(self):
        dict_data = {'date': '2021.07.21', 'value': '1154.50'}
        for index in self.indexes:
            self.mi.index = index
            self.mi.save_dict(dict_data)

        for index in self.indexes:
            self.mi.index = index
            print(self.mi.index, self.mi.get_recent())

        for index in self.indexes:
            self.mi.index = index
            self.mi.del_doc({'date': '2021.07.21'})





