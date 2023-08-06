import datetime
import unittest
from src.util_hj3415 import utils, noti, mongo
import pandas as pd

class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mail(self):
        noti.mail_to('util_hj3415', 'test')

    def test_telegram(self):
        import os
        noti.telegram_to(botname='manager',
                         text=f'>>> python {os.path.basename(os.path.realpath(__file__))} test')
        for name in ['manager', 'dart', 'eval', 'cybos']:
            noti.telegram_to(botname=name, text='test')

    def test_to_float(self):
        a = ['1432', '1,432', '23%', 1432, float('nan'), None, float('inf')]
        for s in a:
            print(utils.to_float(s))

    def test_to_int(self):
        a = ['1432', '1,432', '23%', 1432, float('nan'), None, float('inf')]
        for s in a:
            print(utils.to_int(s))

    def test_deco_num(self):
        a = ['1432123331', '1,43223123', '23123123123%', 1432123123132, float('nan')]
        for s in a:
            print(utils.deco_num(s))

    def test_date_to_str(self):
        print(utils.date_to_str(datetime.datetime.today()))

    def test_str_to_date(self):
        print(utils.str_to_date('2021년 04월 13일'))
        print(utils.str_to_date('2021/04/13'))
        print(utils.str_to_date('2021-04-13'))
        print(utils.str_to_date('2021.04.13'))
        print(utils.str_to_date('20210413'))

    def test_get_price_now(self):
        print(utils.get_price_now(code='005930'))

    def test_scrape_simple_data(self):
        print(utils.scrape_simple_data(url='https://m.stock.naver.com/index.html#/domestic/stock/056730/total'
                                       , selector='#content > div > div > div > strong'))

    def test_chk_date(self):
        dates = ['2021/11/10', '20210230', '2023/11', '2012.11.10']
        for date in dates:
            print('isYmd: ', date, utils.isYmd(date))
            print('isY/m: ', date, utils.isY_slash_m(date))

    def test_get_kor_amount(self):
        print(utils.get_kor_amount(1234567890))
        print(utils.get_kor_amount(1111111111))
        print(utils.get_kor_amount(1234567890, omit='억'))
        print(utils.get_kor_amount(1234567890, omit='천만'))
        print(utils.get_kor_amount(1234567890, omit='만'))
        print(utils.get_kor_amount(1234567890, omit='천'))
        print(utils.get_kor_amount(1234567890, str_suffix=''))

    def test_nan_to_zero(self):
        print(utils.nan_to_zero(float('nan')))
        print(utils.nan_to_zero(123))
        with self.assertRaises(TypeError):
            print(utils.nan_to_zero('123'))

    def test_get_driver(self):
        import os, time
        from selenium.webdriver.common.by import By

        wait = 1
        _CUR_DIR = os.path.dirname(os.path.realpath(__file__))
        _TEMP_DIR = os.path.join(_CUR_DIR, '_down_krx')
        addr = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'
        driver = utils.get_driver(temp_dir=_TEMP_DIR)
        driver.get(addr)
        time.sleep(wait * 2)

        print('Manipulating buttons', end='', flush=True)
        driver.find_element(By.XPATH, '//*[@id="rWertpapier"]').click()  # 라디오버튼
        time.sleep(wait)
        print('.', end='', flush=True)
        # 검색버튼 XPATH - '//*[@id="searchForm"]/section/div/div[3]/a[1]'(2023.2.28)
        driver.find_element(By.XPATH, '//*[@id="searchForm"]/section/div/div[3]/a[1]').click()  # 검색버튼
        time.sleep(wait)
        print('.', end='', flush=True)
        # 검색버튼 XPATH - '//*[@id="searchForm"]/section/div/div[3]/a[2]'(2023.2.28)
        driver.find_element(By.XPATH, '//*[@id="searchForm"]/section/div/div[3]/a[2]').click()  # 엑셀다운버튼
        time.sleep(wait * 2)
        print('.', flush=True)

    def test_get_driver_for_dentaljob(self):
        from selenium.webdriver.common.by import By

        driver = utils.get_driver()
        driver.implicitly_wait(10)
        driver.get('https://www.dentaljob.co.kr/00_Member/00_Login.aspx')
        print('Trying login and refresh...')

        try:
            print('Input id and password')
            driver.find_element(By.NAME, 'login_id').send_keys('hj3415')
            driver.find_element(By.NAME, 'login_pw').send_keys('piyrw421')

            print('Click the login button')
            driver.find_element(By.ID, 'ctl00_ctl00_cbody_cbody_btnLogin').click()
            print('Click the 개재중인 채용광고 link')
            driver.find_element(By.XPATH, '//*[@id="login_on"]/div[2]/p[1]/a').click()
            print('Click the JumpUp button')
            driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_cbody_cbody_pnViewMenuAuth"]/table/tbody/tr[1]/td[2]/p[2]/img[1]').click()
            print('Done.')
        except:
            #print('Wrong.')
            noti.telegram_to(botname="manager", text="Something wrong during dentaljob refreshing.")
        finally:
            driver.close()


class C104Test(unittest.TestCase):
    client = mongo.connect_mongo("mongodb://192.168.0.173:27017")

    def setUp(self):
        import random
        pages = ['c104q', 'c104y']
        self.rnd_code = utils.pick_rnd_x_code(1)[0]
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
