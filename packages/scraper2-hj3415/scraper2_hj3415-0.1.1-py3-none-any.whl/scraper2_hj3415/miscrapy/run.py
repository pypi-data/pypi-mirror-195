import os
import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

from .mi import calc
from db_hj3415 import mongo2, dbpath
import datetime

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


def chcwd(func):
    """
    scrapy는 항상 프로젝트 내부에서 실행해야 하기 때문에 일시적으로 현재 실행 경로를 변경해주는 목적의 데코레이션 함수
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        before_cwd = os.getcwd()
        logger.info(f'current path : {before_cwd}')
        after_cwd = os.path.dirname(os.path.realpath(__file__))
        logger.info(f'change path to {after_cwd}')
        os.chdir(after_cwd)
        func(*args, **kwargs)
        logger.info(f'restore path to {before_cwd}')
        os.chdir(before_cwd)

    return wrapper


def _use_single(spider):
    # reference from https://docs.scrapy.org/en/latest/topics/practices.html(코드로 스파이더 실행하기)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()


@chcwd
def mi():
    spider_list = ('aud', 'chf', 'gbond3y', 'gold', 'kosdaq', 'kospi', 'silver', 'sp500', 'usdidx', 'usdkrw', 'wti',)
    print('*' * 25, f"Scrape multiprocess mi", '*' * 25)
    logger.info(spider_list)

    start_time = time.time()
    ths = []
    error = False
    for spider in spider_list:
        ths.append(Process(target=_use_single, args=(spider,)))
    for i in range(len(ths)):
        ths[i].start()
    for i in range(len(ths)):
        ths[i].join()
        if ths[i].exitcode != 0:
            error = True

    # calc 모듈을 이용해서 avg_per 과 yield_gap 을 계산하여 저장한다.
    print('*' * 25, f"Calculate and save avgper and yieldgap", '*' * 25)
    client = mongo2.connect_mongo(dbpath.load())
    mi_mongo2 = mongo2.MI(client, 'avgper')
    # mi_sqlite = sqlite.MI()
    today_str = datetime.datetime.today().strftime('%Y.%m.%d')

    avgper = calc.avg_per()
    avgper_dict = {'date': today_str, 'value': str(avgper)}
    logger.info(avgper_dict)
    mi_mongo2.save(mi_dict=avgper_dict, index='avgper')
    print(f'\tSave to mongo... date : {today_str} / title : avgper / value : {avgper}')
    #mi_sqlite.save(mi_dict=avgper_dict, index='avgper')
    #print(f'\tSave to sqlite... date : {today_str} / title : avgper / value : {avgper}')

    yieldgap = calc.yield_gap(client, avgper)
    yieldgap_dict = {'date': today_str, 'value': str(yieldgap)}
    logger.info(yieldgap_dict)
    mi_mongo2.save(mi_dict=yieldgap_dict, index='yieldgap')
    print(f'\tSave to mongo... date : {today_str} / title : yieldgap / value : {yieldgap}')
    #mi_sqlite.save(mi_dict=yieldgap_dict, index='yieldgap')
    #print(f'\tSave to sqlite... date : {today_str} / title : yieldgap / value : {yieldgap}')

    print(f'Total spent time : {round(time.time() - start_time, 2)} sec')
    print('done.')
    return error


@chcwd
def _mi_test(spider: str):
    _use_single(spider=spider)


@chcwd
def mihistory(year: int):
    process = CrawlerProcess(get_project_settings())
    process.crawl('mihistory', year=year)
    process.start()


"""avgper 과 yieldgap 계산
"""
import math
from db_hj3415 import mongo2, dbpath
from eval_hj3415 import eval
from util_hj3415 import utils

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def avg_per() -> float:
    # 가중조화평균으로 평균 per 산출 mi db에 저장
    per_r_cap_all = []
    cap_all = []
    eval_list = eval.make_today_eval_df(dbpath.load()).to_dict('records')
    for data in eval_list:
        # eval data: {'code': '111870', '종목명': 'KH 일렉트론', '주가': 1070, 'PER': -2.28, 'PBR': 0.96,
        # '시가총액': 103300000000, 'RED': -11055.0, '주주수익률': -7.13, '이익지표': -0.30426, 'ROIC': -40.31,
        # 'ROE': 0.0, 'PFCF': -7.7, 'PCR': nan}
        logger.debug(f'eval data: {data}')
        if math.isnan(data['PER']) or data['PER'] == 0:
            continue
        if math.isnan(data['시가총액']):
            continue
        cap_all.append(data['시가총액'])
        per_r_cap_all.append((1 / data['PER']) * data['시가총액'])
    logger.debug(f'Count cap_all :{len(cap_all)}')
    logger.debug(f'Count per_r_cap_all : {len(per_r_cap_all)}')
    try:
        return round(sum(cap_all) / sum(per_r_cap_all), 2)
    except ZeroDivisionError:
        return float('nan')


def yield_gap(client, avg_per: float) -> float:
    # 장고에서 사용할 yield gap, mi db에 저장
    date, gbond3y = mongo2.MI(client, index='gbond3y').get_recent()
    if math.isnan(avg_per) or avg_per == 0:
        return float('nan')
    else:
        yield_share = (1 / avg_per) * 100
        yield_gap = round(yield_share - utils.to_float(gbond3y), 2)
        logger.debug(f"Date - {date}, gbond3y - {gbond3y}, yield_gap - {yield_gap}")
        return yield_gap
