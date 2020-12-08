# -*- coding: UTF-8 -*-

import os
import time
import random
import threading
import logging

logger = logging.getLogger(__name__)

from util.auth import login
from util.load_config import config
from testcase.testcase_api import add_caselibrary_api



def get_caselibrary_json(user_uuid,name):
    json = {
        "library": {
            "name": name,
            "members": [{
                "user_domain_type": "testcase_administrators",
                "user_domain_param": ""
            }, {
                "user_domain_type": "single_user",
                "user_domain_param": user_uuid
            }],
            "field_config_uuid": "MEh3txwK"
        }
    }

    return json

def get_json_list(user_uuid,prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    space_json_list = []
    for j in range(config['RANGE_START_NUMBER'], end):
        json = get_caselibrary_json(
            user_uuid,
            name=fmt.format(str(j).zfill(l))
        )
        space_json_list.append(json)
    return space_json_list


def add_caselibrary(user_uuid,prefix=""):
    count = 0
    for caselibrary_json in get_json_list(user_uuid,prefix):
        try:
            resp = add_caselibrary_api(caselibrary_json)
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count


def main():
    res_login = login()
    user_uuid = res_login["user"]["uuid"]
    thread_num = 1

    """
    1. 提示使用者，输入用例库name
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """
    caselibrary_name_prefix = input("请输入caselibrary_name_prefix: ")
    caselibrary_name = caselibrary_name_prefix.strip()
    if caselibrary_name == "":
        print("您输入的caselibrary_name_prefix是空值")
    else:
        print("您输入的caselibrary_name_prefix = {}".format(caselibrary_name))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    caselibrary_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        add_caselibrary(user_uuid,prefix=caselibrary_name)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(caselibrary_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        titel = "{}t_{}".format(caselibrary_name, i)
        th = threading.Thread(target=add_caselibrary, args=(user_uuid,titel))
        th.start()
        ths.append(th)


    for th in ths:
        print(th.getName())
        th.join()

    if count_thr != 0:
        count_space=count_thr*caselibrary_number
        logger.info("总计新增工作项:------------------- {} 条 ----------------------".format(count_space))

    print("任务执行完毕...")



if __name__ == "__main__":
    main()

