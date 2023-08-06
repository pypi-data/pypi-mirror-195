import os
import sys
import time

from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, cpu_count
from scrapy.utils.project import get_project_settings

from util_hj3415 import utils, mongo

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


def _run_scrapy(spider: str, codes: list, mongo_addr: str):
    """
    scrapy 스파이더를 스크립트로 실행할 수 있는 함수
    :param spider:
    :param codes:
    :param mongo_addr:
    :return:
    """
    if mongo_addr == "":
        mongo_client = None
    else:
        try:
            mongo_client = mongo.connect_mongo(mongo_addr)
        except mongo.UnableConnectServerException:
            conn_str = f"Unable to connect to the server.(MY IP : {utils.get_ip_addr()})"
            print(f"{conn_str} Server Addr : {mongo_addr}", file=sys.stderr)
            return

    process = CrawlerProcess(get_project_settings())
    process.crawl(spider, code=codes, mongo_client=mongo_client)
    process.start()

    if mongo_client is not None:
        mongo_client.close()


def _code_divider(entire_codes: list) -> tuple:
    """
    전체 종목 코드를 리스트로 넣으면 cpu 코어에 맞춰 나눠 준다.
    reference from https://stackoverflow.com/questions/19086106/how-to-utilize-all-cores-with-python-multiprocessing
    :param entire_codes:
    :return:
    """

    def _split_list(alist, wanted_parts=1):
        """
        멀티프로세싱할 갯수로 리스트를 나눈다.
        reference from https://www.it-swarm.dev/ko/python/%EB%8D%94-%EC%9E%91%EC%9D%80-%EB%AA%A9%EB%A1%9D%EC%9C%BC%EB%
        A1%9C-%EB%B6%84%ED%95%A0-%EB%B0%98%EC%9C%BC%EB%A1%9C-%EB%B6%84%ED%95%A0/957910776/
        :param alist:
        :param wanted_parts:
        :return:
        """
        length = len(alist)
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]

    core = cpu_count()
    print(f'Get number of core for multiprocessing : {core}')
    n = core - 1
    if len(entire_codes) < n:
        n = len(entire_codes)
    print(f'Split total {len(entire_codes)} codes by {n} parts ...')
    divided_list = _split_list(entire_codes, wanted_parts=n)
    return n, divided_list


def _mp_c10168(page: str, codes: list, mongo_addr: str):
    """
    전체 코드를 코어수 대로 나눠서 멀티 프로세싱 시행
    reference from https://monkey3199.github.io/develop/python/2018/12/04/python-pararrel.html

    멀티프로세싱시 mongoclient를 만들어서 호출하는 방식은 에러가 발생하니 각 프로세스에서 개별적으로 생성해야한다.
    referred from https://blog.naver.com/PostView.nhn?blogId=stop2y&logNo=222211823932&categoryNo=136&parentCategoryNo=
    0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView

    :param page:
    :param codes:
    :param mongo_addr:
    :return:
    """

    if page not in ('c101', 'c106', 'c108'):
        raise NameError
    print('*' * 25, f"Scrape multiprocess {page.capitalize()}", '*' * 25)
    print(f'Total {len(codes)} items..')
    logger.info(codes)
    n, divided_list = _code_divider(codes)

    start_time = time.time()
    ths = []
    error = False
    for i in range(n):
        ths.append(Process(target=_run_scrapy, args=(page, divided_list[i], mongo_addr)))
    for i in range(n):
        ths[i].start()
    for i in range(n):
        ths[i].join()
    print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')


def _mp_c1034(page: str, codes: list, mongo_addr: str):
    """
    c103 6개, c104 8개 페이지수대로 멀티프로세싱 시행
    :param page:
    :param codes:
    :return:
    """
    if page == 'c103':
        spiders = ('c103_iy', 'c103_by', 'c103_cy', 'c103_iq', 'c103_bq', 'c103_cq')
    elif page == 'c104':
        spiders = ('c104_aq', 'c104_bq', 'c104_cq', 'c104_dq', 'c104_ay', 'c104_by', 'c104_cy', 'c104_dy')
    else:
        raise NameError
    title = spiders[0].split('_')[0]
    print('*' * 25, f"Scrape multiprocess {title}", '*' * 25)
    print(f'Total {len(codes)} items..')
    logger.info(codes)

    start_time = time.time()
    ths = []
    error = False
    for spider in spiders:
        ths.append(Process(target=_run_scrapy, args=(spider, codes, mongo_addr)))
    for i in range(len(ths)):
        ths[i].start()
    for i in range(len(ths)):
        ths[i].join()
    print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')


@chcwd
def c101(codes: list, mongo_addr: str = ""):
    """
    c101을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    _mp_c10168('c101', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c103(codes: list, mongo_addr: str = ""):
    """
    c103을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    _mp_c1034('c103', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c104(codes: list, mongo_addr: str = ""):
    """
    c104을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    _mp_c1034('c104', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c106(codes: list, mongo_addr: str = ""):
    """
    c106을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    _mp_c10168('c106', codes=codes, mongo_addr=mongo_addr)

"""
@chcwd
def c108(codes: list, mongo_addr: str = ""):
    _mp_c10168('c108', codes=codes, mongo_addr=mongo_addr)
"""

