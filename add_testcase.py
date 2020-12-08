# -*- coding: UTF-8 -*-

import time
import threading
import logging

logger = logging.getLogger(__name__)

from util.auth import login
from util.load_config import config
from testcase.testcase_api import add_testcase_api


def get_testcase_json(testcase_library,testcase_module,user_uuid,testcase_name):
    testcase_json = {
        "item": {
            "name": testcase_name,
            "assign": user_uuid,
            "priority": "JEm3CE2o",   #可配置在config中，或直接更改，testcase优先级
            "type": "UayhCo8M",       #可配置在config中，用例类型
            "module_uuid": testcase_module,
            "condition": "已进入ONES TestCase 的用例库内",
            "library_uuid": testcase_library,
            "desc": "",
            "steps": [{
                "id": 1,
                "desc": "打开用例库，添加用例",         #可配置在config中，或直接更改，
                "result": "可以正常添加用例"    #可配置在config中，或直接更改，
            }, {
                "id": 2,
                "desc": "打开用例库，删除用例",
                "result": "可以正常删除用例"
            }],
            "testcase_case_steps": [{
                "id": 1,
                "desc": "打开用例库，添加用例",
                "result": "可以正常添加用例"
            }, {
                "id": 2,
                "desc": "打开用例库，删除用例",
                "result": "可以正常删除用例"
            }],
            "item_type": "testcase_case",
            "testcase_library": testcase_library,
            "testcase_module": testcase_module
        }
    }
    return testcase_json


def get_page_json_list(testcase_library,testcase_module,user_uuid, prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    pages_json = []
    for j in range(config['RANGE_START_NUMBER'], end):
        json = get_testcase_json(
            testcase_library,
            testcase_module,
            user_uuid,
            testcase_name=fmt.format(str(j).zfill(l))
        )
        pages_json.append(json)

    return pages_json


def add_testcase(testcase_library,testcase_module,user_uuid, prefix=""):
    count = 0
    for json in get_page_json_list(testcase_library, testcase_module, user_uuid, prefix):
        try:
            response = add_testcase_api(json)
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count




def main():
    res_login = login()
    user_uuid = res_login["user"]["uuid"]
    thread_num = 1

    """
    1. 提示使用者，输入用例库：testcase_library、testcase_module的uuid
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """

    testcase_library_uuid = input("请输入用例库testcase_library_uuid: ")
    testcase_library = testcase_library_uuid.strip()
    if testcase_library == "":
        raise Exception("页面组testcase_library_uuid不能为空值")
    else:
        print("您输入的用例库testcase_library_uuid = {}".format(testcase_library))

    testcase_module_uuid = input("请输入用例模块的testcase_module_uuid: ")
    testcase_module = testcase_module_uuid.strip()
    if testcase_module == "":
        raise Exception("用例模块的testcase_module_uuid不能为空值")
    else:
        print("您输入的用例模块testcase_module_uuid = {}".format(testcase_module))

    testcase_name_prefix = input("请输入testcase_name_prefix: ")
    testcase_name = testcase_name_prefix.strip()
    if testcase_name == "":
        print("您输入的testcase_name_prefix是空值")
    else:
        print("您输入的testcase_name_prefix = {}".format(testcase_name))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    testcase_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        add_testcase(testcase_library,testcase_module,user_uuid,prefix=testcase_name)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(testcase_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        time.sleep(0.5)
        th = threading.Thread(target=add_testcase, args=(testcase_library,testcase_module,user_uuid,
                                                         "{}t{}_".format(testcase_name, i)))
        th.start()
        time.sleep(0.5)
        ths.append(th)


    for th in ths:
        print(th.getName())
        th.join()

    if count_thr != 0:
        count_testcase=count_thr*testcase_number
        logger.info("总计新增工作项:------------------- {} 条 ----------------------".format(count_testcase))

    print("任务执行完毕...")



if __name__ == "__main__":
    main()

