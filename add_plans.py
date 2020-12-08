# -*- coding: UTF-8 -*-

import os
import time
import random
import threading
import logging

logger = logging.getLogger(__name__)

from util.auth import auth, cached_data, login
from util.load_config import config
from util.random_util import get_random_uuid
from plan.plans import plan_add
from my_thread import do_thread



def get_add_plans_json(assign,name):
    json = {
        "item": {
            "item_type": "program",
            "name": name,
            "related_type": "none",
            "parent": "",
            "assign": assign
	    }
    }
    return json

def get_json_list(assign, prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    space_json_list = []
    for j in range(config['RANGE_START_NUMBER'], end):
        json = get_add_plans_json(
            assign=assign,
            name=fmt.format(str(j).zfill(l))
        )
        space_json_list.append(json)
    return space_json_list


def add_plans(assign, prefix=""):
    count = 0
    for plans_json in get_json_list(assign, prefix):
        try:
            resp = plan_add(plans_json)
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count


def main():
    res_login = login()
    user_uuid = res_login["user"]["uuid"]
    space_name_prefix = ""
    thread_num = 1

    """
    1. 提示使用者，输入plan_name
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """
    plan_name_prefix = input("请输入plan_name_prefix: ")
    plan_name = plan_name_prefix.strip()
    if plan_name == "":
        print("您输入的plan_name_prefix是空值")
    else:
        print("您输入的plan_name_prefix = {}".format(plan_name))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    space_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        add_plans(assign=user_uuid,prefix=plan_name)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(space_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        th = threading.Thread(target=add_plans, args=(user_uuid, "{}t_{}".format(plan_name, i)))
        th.start()
        ths.append(th)


    for th in ths:
        print(th.getName())
        th.join()

    if count_thr != 0:
        count_space=count_thr*space_number
        logger.info("总计新增工作项:------------------- {} 条 ----------------------".format(count_space))

    print("任务执行完毕...")



if __name__ == "__main__":
    main()

