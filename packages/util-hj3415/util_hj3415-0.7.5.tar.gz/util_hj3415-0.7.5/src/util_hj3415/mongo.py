import pymongo
import math
import datetime
from typing import Tuple, List
from collections import OrderedDict
from abc import *
import pandas as pd

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

"""
몽고db구조
RDBMS :     database    / tables        / rows      / columns
MongoDB :   database    / collections   / documents / fields
"""


class UnableConnectServerException(Exception):
    """
    몽고 서버 연결 에러를 처리하기 위한 커스텀 익셉션
    """
    pass


def connect_mongo(addr: str, timeout=5) -> pymongo.MongoClient:
    """
    몽고 클라이언트를 만들어주는 함수.
    필요할 때마다 클라이언트를 생성하는 것보다 클라이언트 한개로 데이터베이스를 다루는게 효율적이라 함수를 따로 뺐음.
    resolve conn error - https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
    :param addr:
    :param timeout:
    :return:
    """
    import certifi
    ca = certifi.where()
    if addr.startswith('mongodb://'):
        # set a some-second connection timeout
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000)
    elif addr.startswith('mongodb+srv://'):
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000, tlsCAFile=ca)
    else:
        raise Exception(f"Invalid address: {addr}")
    try:
        srv_info = client.server_info()
        conn_str = f"Connect to Mongo Atlas v{srv_info['version']}..."
        print(conn_str, f"Server Addr : {addr}")
        return client
    except:
        raise UnableConnectServerException()


class MongoBase:
    def __init__(self, client, db_name: str, col_name: str):
        self.client = client
        self.db_name = db_name
        self.col_name = col_name

        self.my_db = self.client[self.db_name]
        self.my_col = self.client[self.db_name][self.col_name]

    def get_all_docs(self, remove_id=True) -> list:
        items = []
        if remove_id:
            for doc in self.my_col.find({}):
                del doc['_id']
                items.append(doc)
        else:
            items = list(self.my_col.find({}))
        return items

    def clear_col_items(self, ):
        self.my_col.delete_many({})
        print(f"Delete all doccument in {self.col_name} collection..")

    def del_col(self):
        self.my_db.drop_collection(self.col_name)
        print(f"Drop {self.col_name} collection..")

    def _save_df(self, df: pd.DataFrame) -> bool:
        # c103, c104, c106, c108에서 주로 사용하는 저장방식
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False
        result = self.my_col.insert_many(df.to_dict('records'))
        return result.acknowledged


class C1034(MongoBase, metaclass=ABCMeta):
    def __init__(self, client, db_name: str, col_name: str):
        super().__init__(client=client, db_name=db_name, col_name=col_name)

    def get_all_titles(self) -> list:
        titles = []
        for item in self.get_all_docs():
            titles.append(item['항목'])
        return list(set(titles))

    @staticmethod
    def refine_data(data: dict, refine_words: list) -> dict:
        """
        검색된 raw 딕셔너리에서 불필요한 항목들
        ex - ['_id', '항목', '전년대비', '전년대비1', '전분기대비', '전분기대비1']
        을 삭제한다.
        """
        for del_title in refine_words:
            try:
                del data[del_title]
            except KeyError:
                pass
        return data

    def _find(self, title: str, refine_words: list) -> Tuple[List[dict], int]:
        """
        title인자에 해당하는 항목을 검색하여 반환한다.
        c103의 경우는 중복되는 이름의 항목이 있기 때문에
        이 함수는 반환되는 딕셔너리 리스트와 갯수로 구성되는 튜플을 반환한다.
        """
        titles = self.get_all_titles()
        if title in titles:
            count = 0
            data_list = []
            for data in self.my_col.find({'항목': {'$eq': title}}):
                count += 1
                data_list.append(C1034.refine_data(data, refine_words))
            return data_list, count
        else:
            raise Exception(f'{title} is not in {titles}')

    @abstractmethod
    def find(self, title: str) -> dict:
        pass

    def latest_value(self, title: str, pop_count=2) -> Tuple[str, float]:
        """가장 최근 년/분기 값

        해당 타이틀의 가장 최근의 년/분기 값을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀
            pop_count: 유효성 확인을 몇번할 것인가

        Returns:
            tuple: ex - ('2020/09', 39617.5) or ('', 0)

        Note:
            만약 최근 값이 nan 이면 찾은 값 바로 직전 것을 한번 더 찾아 본다.\n
            데이터가 없는 경우 ('', nan) 반환한다.\n
        """
        def chk_integrity(value) -> bool:
            if isinstance(value, str):
                # value : ('Unnamed: 1', '데이터가 없습니다.') 인 경우
                is_valid = False
            elif math.isnan(value):
                # value : float('nan') 인 경우
                is_valid = False
            elif value is None:
                # value : None 인 경우
                is_valid = False
            elif value == 0:
                is_valid = False
            else:
                is_valid = True
            return is_valid

        od = OrderedDict(sorted(self.find(title).items(), reverse=False))
        logger.debug(f'{title} : {od}')

        for i in range(pop_count):
            try:
                d, v = od.popitem(last=True)
            except KeyError:
                # when dictionary is empty
                return '', float('nan')
            if chk_integrity(v):
                logger.debug(f'last_one : {v}')
                return d, v

        return '', float('nan')

    def sum_recent_4q(self, title: str) -> Tuple[str, float]:
        """최근 4분기 합

        분기 페이지 한정 해당 타이틀의 최근 4분기의 합을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            tuple: (계산된 4분기 중 최근분기, 총합)

        Raises:
            TypeError: 페이지가 q가 아닌 경우 발생

        Note:
            분기 데이터가 4개 이하인 경우 그냥 최근 연도의 값을 찾아 반환한다.
        """
        if self.col_name.endswith('q'):
            # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
            # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
            od_q = OrderedDict(sorted(self.find(title).items(), reverse=False))
            logger.debug(f'{title} : {od_q}')

            if len(od_q) < 4:
                # od_q의 값이 4개 이하이면 그냥 최근 연도의 값으로 반환한다.
                y = C1034(self.client, self.db_name, self.col_name[:-1] + 'y')
                return y.latest_value(title)
            else:
                q_sum = 0
                latest_period = list(od_q.items())[-1][0]
                for i in range(4):
                    # last = True 이면 최근의 값부터 꺼낸다.
                    d, v = od_q.popitem(last=True)
                    logger.debug(f'd:{d} v:{v}')
                    q_sum += 0 if math.isnan(v) else v
                return str(latest_period), round(q_sum, 2)
        else:
            raise TypeError(f'Not support year data..{self.col_name}')


class C104(C1034):
    def __init__(self, client, code: str, page: str):
        super().__init__(client=client, db_name=code, col_name=page)

    def get_all_titles(self) -> list:
        """
        상위 C1034클래스에서 c104는 stamp항목이 있기 때문에 삭제하고 리스트로 반환한다.
        """
        titles = super().get_all_titles()
        titles.remove('stamp')
        return titles

    def find(self, title: str) -> dict:
        """
        title에 해당하는 항목을 딕셔너리로 반환한다.
        """
        l, c = super(C104, self)._find(title, ['_id', '항목', '전년대비', '전년대비1', '전분기대비', '전분기대비1'])
        return l[0]

    def save_df(self, c104_df: pd.DataFrame) -> bool:
        """데이터베이스에 저장

        c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에
        stamp 를 검사하여 12시간 전보다 이전에 저장된 자료가 있으면
        삭제한 후 저장하고 12시간 이내의 자료는 삭제하지 않고
        데이터를 추가하는 형식으로 저장한다.

        Example:
            c104_data 예시\n
            [{'항목': '매출액증가율',...'2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율',...'2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        self.my_col.create_index('항목', unique=True)
        time_now = datetime.datetime.now()
        try:
            stamp = self.my_col.find_one({'항목': 'stamp'})['time']
            if stamp < (time_now - datetime.timedelta(days=.5)):
                # 스템프가 12시간 이전이라면..연속데이터가 아니라는 뜻이므로 컬렉션을 초기화한다.
                self.clear_col_items()
        except TypeError:
            # 스템프가 없다면...
            pass
        # 항목 stamp를 찾아 time을 업데이트하고 stamp가 없으면 insert한다.
        self.my_col.update_one({'항목': 'stamp'}, {"$set": {'time': time_now}}, upsert=True)
        return super(C104, self)._save_df(c104_df)

    def modify_stamp(self, days_ago: int):
        """
        인위적으로 타임스템프를 수정한다 - 주로 테스트 용도
        """
        try:
            before = self.my_col.find_one({'항목': 'stamp'})['time']
        except TypeError:
            # 이전에 타임스템프가 없는 경우
            before = None
        time_2da = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        self.my_col.update_one({'항목': 'stamp'}, {"$set": {'time': time_2da}}, upsert=True)
        after = self.my_col.find_one({'항목': 'stamp'})['time']
        print(f"Stamp changed: {before} -> {after}")
