# -*- coding: UTF-8 -*-

import os
import time
import random
import threading
import logging

logger = logging.getLogger(__name__)

from util.auth import login
from util.load_config import config
from testcase.testcase_api import add_testplan_api



def get_testplan_json(assigns_list,user_uuid,name):
    json = {
        "plan": {
            "name": name,
            "assigns": assigns_list,
            "stage": "smoke",
            "members": [{
                "user_domain_type": "testcase_administrators",
                "user_domain_param": ""
            }, {
                "user_domain_type": "testcase_plan_assign",
                "user_domain_param": ""
            }, {
                "user_domain_type": "single_user",
                "user_domain_param": user_uuid
            }],
            "related_project_uuid": None,
            "related_sprint_uuid": None,
            "related_issue_type_uuid": None
        },
        "is_update_default_config": True
    }

    return json

def get_json_list(assigns_list,user_uuid,prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    space_json_list = []
    for j in range(config['RANGE_START_NUMBER'], end):
        json = get_testplan_json(
            assigns_list,
            user_uuid,
            name=fmt.format(str(j).zfill(l))
        )
        space_json_list.append(json)
    return space_json_list


def add_testplan(assigns_list,user_uuid,prefix=""):
    count = 0
    for testplan_json in get_json_list(assigns_list,user_uuid,prefix):
        try:
            resp = add_testplan_api(testplan_json)
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count


def main():
    res_login = login()
    user_uuid = res_login["user"]["uuid"]
    testplan_name_prefix = ""
    thread_num = 1

    """
    1. 提示使用者，输入测试计划name
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """
    testplan_name_prefix = input("请输入testplan_name_prefix: ")
    testplan_name = testplan_name_prefix.strip()
    if testplan_name == "":
        print("您输入的testplan_name_prefix是空值")
    else:
        print("您输入的testplan_name_prefix = {}".format(testplan_name))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    testplan_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        add_testplan([user_uuid],user_uuid,prefix=testplan_name)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(testplan_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        titel = "{}t_{}".format(testplan_name, i)
        th = threading.Thread(target=add_testplan, args=([user_uuid],user_uuid,titel))
        th.start()
        ths.append(th)


    for th in ths:
        print(th.getName())
        th.join()

    if count_thr != 0:
        count_space=count_thr*testplan_number
        logger.info("总计新增工作项:------------------- {} 条 ----------------------".format(count_space))

    print("任务执行完毕...")



if __name__ == "__main__":
    main()

