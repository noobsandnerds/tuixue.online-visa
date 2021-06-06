""" A thread-safe global variable getter-setter interface."""

import os
import json
from queue import Queue
from threading import Lock
from collections import defaultdict
from typing import List, Optional, Union
from datetime import timedelta, timezone

DATA_PATH = os.path.join(os.curdir, 'data')  # dir stroing file-based data

with open(os.path.join(os.curdir, 'config', 'secret.json')) as f:
    SECRET = json.load(f)

MAX_EMAIL_SENT = 512  # maximum number of emails sent for one POST to email server

FRONTEND_BASE_URI = "tuixue.online"

MONGO_CONFIG = {'host': '127.0.0.1', 'port': 27017, 'database': 'tuixue'}

CRAWLER_API = {
    'register': {
        'cgi': '/register/?type={}&place={}',
        'ais': '/ais/register/?code={}&email={}&pswd={}',
    },
    'refresh': {
        'cgi': '/refresh/?session={}',
        'ais': '/ais/refresh/?code={}&id={}&session={}'
    }
}
WAIT_TIME = {'register': 70, 'refresh': 30}

CD_HOURS = 4
CD_LIST = [
    'B-成都',
    'B-柏林',
    'O-成都',
    'O-福冈',
    'O-札幌',
    'O-慕尼黑',
    'O-悉尼',
    'L-福冈',
    'L-沈阳',
    'L-成都',
    'L-巴拿马',
    'L-悉尼',
    'H-福冈',
    'H-成都',
    'H-沈阳',
    'H-巴拿马',
    'H-东京',
    'F-成都',
]

DEFAULT_FILTER = ['bj', 'sh', 'gz', 'sy', 'bju', 'shu', 'gzu', 'syu']
NONDOMESTIC_DEFAULT_FILTER = ["sg", "gye", "lcy"]

OVERVIEW_CACHE = {}
DETAIL_CACHE = {}

SESSION_UPDATE_QUEUE = Queue()

# isn't it useless?
COUTNRY_CODE_TO_UTC_OFFSET = {
    'ARE': 4, 'AUS': 10, 'BRB': -4, 'CAN': -5, 'CHE': 1,
    'CHN': 8, 'COL': -5, 'ECU': -5, 'FRA': 1, 'GBR': 0,
    'GRC': 2, 'JPN': 9, 'KHM': 7, 'KOR': 9, 'MEX': -6, 'IND': 5.5,
    'NPL': 5.75, 'SGP': 8, 'SRB': 1, 'THA': 7, 'TUR': 3, 'DEU': 1,
}

REGION_ATTR = [
    {"code": "DOMESTIC", "name_cn": "国内", "name_en": "Domestic"},
    {"code": "SOUTH_EAST_ASIA", "name_cn": "东南亚", "name_en": "South East Asia"},
    {"code": "EAST_ASIA", "name_cn": "东亚", "name_en": "East Asia"},
    {"code": "SOUTH_ASIA", "name_cn": "南亚", "name_en": "South Asia"},
    {"code": "OCEANIA", "name_cn": "大洋洲", "name_en": "Oceania"},
    {"code": "WEST_EUROPE", "name_cn": "西欧", "name_en": "West Europe"},
    {"code": "NORTH_AMERICA", "name_cn": "北美", "name_en": "North America"},
    {"code": "WEST_ASIA", "name_cn": "西亚", "name_en": "West Asia"},
    {"code": "EAST_EUROPE", "name_cn": "东欧", "name_en": "East Europe"},
    {"code": "SOUTH_AMERICA", "name_cn": "南美", "name_en": "South America"},
    {"code": "LATIN_AMERICA", "name_cn": "拉美", "name_en": "Latin America"},
    {"code": "NORTH_AFRICA", "name_cn": "北非", "name_en": "North Africa"},
]

# Embassy/consulate attributes
# Tuple[name_cn, name_en, code, sys, region, continent, country, timezone, crawler_code]
EMBASSY_ATTR = [
    ('北京', 'Beijing', 'bj', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '北京'),
    ('北京（非硕博）', 'Beijing (Others)', 'bju', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '北京u'),
    ('上海', 'Shanghai', 'sh', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '上海'),
    ('上海（非硕博）', 'Shanghai (Others)', 'shu', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '上海u'),
    ('成都', 'Chengdu', 'cd', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '成都'),
    ('广州', 'Guangzhou', 'gz', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '广州'),
    ('广州（非硕博）', 'Guangzhou (Others)', 'gzu', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '广州u'),
    ('沈阳', 'Shenyang', 'sy', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '沈阳'),
    ('沈阳（非硕博）', 'Shenyang (Others)', 'syu', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '沈阳u'),
    ('香港（非本地）', 'Hong Kong (non-resident)', 'hk', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '香港'),
    ('香港（本地）', 'Hong Kong (resident)', 'hkr', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '香港r'),
    ('台北', 'Taipei', 'tp', 'cgi', 'DOMESTIC', 'ASIA', 'CHN', 8, '台北'),
    ('金边', 'Phnom Penh', 'pp', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'KHM', 7, '金边'),
    ('新加坡', 'Singapore', 'sg', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'SGP', 8, '新加坡'),
    ('首尔', 'Seoul', 'sel', 'cgi', 'EAST_ASIA', 'ASIA', 'KOR', 9, '首尔'),
    ('河内', 'Hanoi', 'han', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'VNM', 7, '河内'),
    ('胡志明', 'Ho Chi Minh City', 'sgn', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'VNM', 7, '胡志明'),
    ('孟买', 'Mumbai', 'bom', 'cgi', 'SOUTH_ASIA', 'ASIA', 'IND', 5.5, '孟买'),
    ('加尔各答', 'Kolkata', 'ccu', 'cgi', 'SOUTH_ASIA', 'ASIA', 'IND', 5.5, '加尔各答'),
    ('海得拉巴', 'Hyderabad', 'hyd', 'cgi', 'SOUTH_ASIA', 'ASIA', 'IND', 5.5, '海得拉巴'),
    ('金奈', 'Chennai', 'maa', 'cgi', 'SOUTH_ASIA', 'ASIA', 'IND', 5.5, '金奈'),
    ('新德里', 'New Delhi', 'deli', 'cgi', 'SOUTH_ASIA', 'ASIA', 'IND', 5.5, '新德里'),
    ('巴拿马', 'Panama City', 'pty', 'cgi', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'PAN', -5, '巴拿马'),
    ('墨尔本', 'Melbourne', 'mel', 'cgi', 'OCEANIA', 'OCEANIA', 'AUS', 10, '墨尔本'),
    ('珀斯', 'Perth', 'per', 'cgi', 'OCEANIA', 'OCEANIA', 'AUS', 8, '珀斯'),
    ('悉尼', 'Sydney', 'syd', 'cgi', 'OCEANIA', 'OCEANIA', 'AUS', 10, '悉尼'),
    ('伯尔尼', 'Bern', 'brn', 'cgi', 'WEST_EUROPE', 'EUROPE', 'CHE', 2, '伯尔尼'),
    ('福冈', 'Fukuoka', 'fuk', 'cgi', 'EAST_ASIA', 'ASIA', 'JPN', 9, '福冈'),
    ('大阪', 'Osaka', 'itm', 'cgi', 'EAST_ASIA', 'ASIA', 'JPN', 9, '大阪'),
    ('那霸', 'Naha', 'oka', 'cgi', 'EAST_ASIA', 'ASIA', 'JPN', 9, '那霸'),
    ('札幌', 'Sapporo', 'cts', 'cgi', 'EAST_ASIA', 'ASIA', 'JPN', 9, '札幌'),
    ('东京', 'Tokyo', 'hnd', 'cgi', 'EAST_ASIA', 'ASIA', 'JPN', 9, '东京'),
    ('加德满都', 'Kathmandu', 'ktm', 'cgi', 'SOUTH_ASIA', 'ASIA', 'NPL', 5.75, '加德满都'),
    ('柏林', 'Berlin', 'sxf', 'cgi', 'WEST_EUROPE', 'EUROPE', 'DEU', 2, '柏林'),
    ('法兰克福', 'Frankfurt', 'fra', 'cgi', 'WEST_EUROPE', 'EUROPE', 'DEU', 2, '法兰克福'),
    ('慕尼黑', 'Munich', 'muc', 'cgi', 'WEST_EUROPE', 'EUROPE', 'DEU', 2, '慕尼黑'),
    ('曼谷', 'Bangkok', 'bkk', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'THA', 7, '曼谷'),
    ('清迈', 'Chiang Mai', 'cnx', 'cgi', 'SOUTH_EAST_ASIA', 'ASIA', 'THA', 7, '清迈'),
    ('圣何塞', 'San José', 'sjo', 'cgi', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'CRI', -6, '圣何塞'),
    ('圣多明各', 'Santo Domingo', 'sdq', 'cgi', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'DOM', -4, '圣多明各'),
    ('卡萨布兰卡', 'Casablanca', 'cmn', 'cgi', 'NORTH_AFRICA', 'AFRICA', 'MAR', 0, '卡萨布兰卡'),
    ('贝尔法斯特', 'Belfast', 'bfs', 'ais', 'WEST_EUROPE', 'EUROPE', 'GBR', 1, 'en-gb'),
    ('伦敦', 'London', 'lcy', 'ais', 'WEST_EUROPE', 'EUROPE', 'GBR', 1, 'en-gb'),
    ('卡尔加里', 'Calgary', 'yyc', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -6, 'en-ca'),
    ('哈利法克斯', 'Halifax', 'yhz', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -3, 'en-ca'),
    ('蒙特利尔', 'Montreal', 'yul', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -4, 'en-ca'),
    ('渥太华', 'Ottawa', 'yow', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -4, 'en-ca'),
    ('魁北克城', 'Quebec City', 'yqb', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -4, 'en-ca'),
    ('多伦多', 'Toronto', 'yyz', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -4, 'en-ca'),
    ('温哥华', 'Vancouver', 'yvr', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'CAN', -7, 'en-ca'),
    ('阿布扎比', 'Abu Dhabi', 'auh', 'ais', 'WEST_ASIA', 'ASIA', 'ARE', 4, 'en-ae'),
    ('迪拜', 'Dubai', 'dxb', 'ais', 'WEST_ASIA', 'ASIA', 'ARE', 4, 'en-ae'),
    ('贝尔格莱德', 'Belgrade', 'beg', 'ais', 'EAST_EUROPE', 'EUROPE', 'SRB', 2, 'en-rs'),
    ('巴黎', 'Paris', 'cdg', 'ais', 'WEST_EUROPE', 'EUROPE', 'FRA', 2, 'en-fr'),
    ('瓜亚基尔', 'Guayaquil', 'gye', 'ais', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'ECU', -5, 'en-ec'),
    ('基多', 'Quito', 'uio', 'ais', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'ECU', -5, 'en-ec'),
    ('安卡拉', 'Ankara', 'esb', 'ais', 'WEST_ASIA', 'ASIA', 'TUR', 3, 'en-tr'),
    ('伊斯坦布尔', 'Istanbul', 'ist', 'ais', 'WEST_ASIA', 'ASIA', 'TUR', 3, 'en-tr'),
    ('雅典', 'Athens', 'ath', 'ais', 'WEST_EUROPE', 'EUROPE', 'GRC', 3, 'en-gr'),
    ('波哥大', 'Bogota', 'bog', 'ais', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'COL', -5, 'en-co'),
    ('布里奇顿', 'Bridgetown', 'bgi', 'ais', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'BRB', -4, 'en-bb'),
    ('华雷斯城', 'Ciudad Juarez', 'cjs', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -6, 'en-mx'),
    ('瓜达拉哈拉', 'Guadalajara', 'gdl', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -5, 'en-mx'),
    ('埃莫西约', 'Hermosillo', 'hmo', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -7, 'en-mx'),
    ('马塔莫罗斯', 'Matamoros', 'cvj', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -5, 'en-mx'),
    ('墨西哥城', 'Mexico City', 'mex', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -5, 'en-mx'),
    ('蒙特雷', 'Monterrey', 'mty', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -5, 'en-mx'),
    ('诺加莱斯', 'Nogales', 'ols', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -7, 'en-mx'),
    ('新拉雷多', 'Nuevo Laredo', 'nld', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -5, 'en-mx'),
    ('蒂华纳', 'Tijuana', 'tij', 'ais', 'NORTH_AMERICA', 'NORTH_AMERICA', 'MEX', -7, 'en-mx'),
    ('拿骚', 'Nassau', 'nas', 'ais', 'LATIN_AMERICA', 'SOUTH_AMERICA', 'BHS', -4, 'en-bs'),
    ('阿姆斯特丹', 'Amsterdam', 'ams', 'ais', 'WEST_EUROPE', 'EUROPE', 'NLD', 2, 'en-nl'),
    ('布鲁塞尔', 'Brussels', 'bru', 'ais', 'WEST_EUROPE', 'EUROPE', 'BEL', 2, 'en-be'),
    ('佛罗伦萨', 'Florence', 'flr', 'ais', 'WEST_EUROPE', 'EUROPE', 'ITA', 2, 'en-it'),
    ('米兰', 'Milan', 'mxp', 'ais', 'WEST_EUROPE', 'EUROPE', 'ITA', 2, 'en-it'),
    ('那不勒斯', 'Naples', 'nap', 'ais', 'WEST_EUROPE', 'EUROPE', 'ITA', 2, 'en-it'),
    ('罗马', 'Rome', 'fco', 'ais', 'WEST_EUROPE', 'EUROPE', 'ITA', 2, 'en-it'),
    ('马德里', 'Madrid', 'mad', 'ais', 'WEST_EUROPE', 'EUROPE', 'ESP', 2, 'en-es'),
]

VISA_TYPES = 'FJBHOL'
VISA_TYPE_DETAILS = {'F': 'F1/F2', 'J': 'J1/J2', 'H': 'H1B', 'B': 'B1/B2', 'O': 'O1/O2/O3', 'L': 'L1/L2'}

# CGI/AIS_LOCATION are the parameters sent to crawler backend to retrieve session data
CGI_LOCATION = [emb[8] for emb in EMBASSY_ATTR if emb[3] == 'cgi']
AIS_LOCATION = list(set(emb[8] for emb in EMBASSY_ATTR if emb[3] == 'ais'))
SYS_LOCATION = {'cgi': CGI_LOCATION, 'ais': AIS_LOCATION}

# filter of AIS visa data retrieved from cralwer backend by city
AIS_MONITORING_CITY = [emb[1] for emb in EMBASSY_ATTR if emb[3] == 'ais']

CGI_SESS_POOL_SIZE = {'F': 10, 'J': 10, 'B': 8, 'H': 5, 'O': 5, 'L': 5}
AIS_SESS_POOL_SIZE = {visa_type: 1 for visa_type in VISA_TYPES}
SESS_POOL_SIZE = {'cgi': CGI_SESS_POOL_SIZE, 'ais': AIS_SESS_POOL_SIZE}

CGI_FETCH_TIME_INTERVAL = {'F': 60, 'J': 60, 'B': 120, 'H': 180, 'O': 180, 'L': 180}
AIS_FETCH_TIME_INTERVAL = {visa_type: 300 for visa_type in VISA_TYPES}
FETCH_TIME_INTERVAL = {'cgi': CGI_FETCH_TIME_INTERVAL, 'ais': AIS_FETCH_TIME_INTERVAL}

ADDITIONAL_INFO = {}

for lng in ['zh', 'en']:
    path = os.path.join('additional_info', lng)
    ADDITIONAL_INFO[lng] = []

    for country in os.listdir(path):
        file_path = os.path.join(path, country)
        with open(file_path) as f:
            ADDITIONAL_INFO[lng].append({
                'country': country.replace('.md', ''),
                'content': f.read(),
            })

CANCEL_DATE = open(os.path.join('additional_info', 'zh', 'cancel_date.md')).read()

LOCK = Lock()


class USEmbassy:
    """ An abstraction represent a U.S. Embassy or Consulate"""
    @classmethod
    def get_embassy_lst(cls) -> List['USEmbassy']:
        """ Return the list of USEmbassy objects."""
        return [cls(*embassy_attr) for embassy_attr in EMBASSY_ATTR]

    @classmethod
    def get_embassy_by_loc(cls, loc: str) -> Optional['USEmbassy']:
        """ Return an USEbassy object by the location property."""
        return next((emb for emb in cls.get_embassy_lst() if emb.location == loc), None)

    @classmethod
    def get_embassy_by_code(cls, code: str) -> Optional['USEmbassy']:
        """ Return an USEbassy object by the code property."""
        return next((emb for emb in cls.get_embassy_lst() if emb.code == code), None)

    @classmethod
    def get_embassy_list_by_crawler_code(cls, crawler_code: str) -> List[Optional['USEmbassy']]:
        return [emb for emb in cls.get_embassy_lst() if emb.crawler_code == crawler_code]

    @classmethod
    def get_region_mapping(cls) -> List[dict]:
        """ Return a region to embassy code mapping. In JSON convention."""
        return [
            {
                'region': region,
                'embassy_code_lst': [emb.code for emb in cls.get_embassy_lst() if emb.region == region]
            } for region in {emb.region for emb in cls.get_embassy_lst()}
        ]

    @classmethod
    def get_region_country_embassy_tree(cls) -> List[dict]:
        """ Return a region-country-embassy mapping"""
        rce_tree = defaultdict(lambda: defaultdict(list))
        for emb in cls.get_embassy_lst():
            rce_tree[emb.region][emb.country].append(emb.code)

        return [
            {
                'region': region,
                'country_embassy_map': [
                    {
                        'country': country,
                        'embassy_code_lst': embassy_code_lst,
                    } for country, embassy_code_lst in ce_map.items()
                ],
            } for region, ce_map in rce_tree.items()
        ]

    def __init__(
        self,
        name_cn: str,
        name_en: str,
        code: str,
        sys: str,
        region: str,
        continent: str,
        country: str,
        utcoffset: Union[float, int],
        crawler_code: str,
    ) -> None:
        self.name_cn = name_cn
        self.name_en = name_en
        self.code = code
        self.sys = sys
        self.region = region
        self.continent = continent
        self.country = country
        self.timezone = timezone(timedelta(hours=utcoffset))
        self.crawler_code = crawler_code

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name_cn={self.name_cn}, name_en={self.name_en}, code={self.code})'

    @property
    def location(self) -> str:
        """ Return the location value for data storage."""
        return self.crawler_code if self.sys == 'cgi' else self.name_en


class GlobalVar:  # Can we just define a dictionary for it?
    """ Global variable class."""
    var_dct = {}


def assign(var_name, var_value):
    """ Assign value to the global variable."""
    with LOCK:
        GlobalVar.var_dct[var_name] = var_value


def value(var_name, default_value):
    """ Get value of the var_name
        Initiate and assign a new one if none exists.
    """
    with LOCK:
        if var_name not in GlobalVar.var_dct:
            GlobalVar.var_dct[var_name] = default_value
            return default_value
    return GlobalVar.var_dct[var_name]
