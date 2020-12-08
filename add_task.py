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
from project.task import tasks_add, tasks_add2
from my_thread import do_thread


def get_add_task_data(summary, project_uuid, priority=config["PRIORITY"], assign_uuid='', owner_uuid='', parent_uuid='', desc_rich='', issue_type_uuid=''):
    if assign_uuid == '':
        assign_uuid = cached_data['user_uuid']

    if owner_uuid == '':
        owner_uuid = assign_uuid

    uuid = get_random_uuid(8)
    return {
        "uuid": assign_uuid + uuid,
        "assign": assign_uuid,
        "desc_rich": desc_rich,
        "field_values": [],
        "issue_type_uuid": issue_type_uuid,
        "owner": owner_uuid,
        "parent_uuid": parent_uuid,
        "summary": summary,
        "priority": priority,
        "project_uuid": project_uuid
    }


def get_json_list(project_uuid, issuetype_uuid, prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    for j in range(config['RANGE_START_NUMBER'], end):
        # issue_type_uuid 对应的是 全局project配置里的uuid，通过接口获取
        json = get_add_task_data(
            fmt.format(str(j).zfill(l)),
            project_uuid,
            issue_type_uuid=issuetype_uuid)
        yield {
            "tasks": [json]
        }



def add_task(project_uuid, issue_type_uuid, prefix=""):
    count = 0
    for json in get_json_list(project_uuid, issue_type_uuid, prefix):
        try:
            resp = tasks_add2(json)
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count


def main():
    login()
    issue_type_uuid = "KSKtSeMc"
    project_uuid = ""
    task_name_prefix = ""
    thread_num = 1

    """
    1. 提示使用者，输入project_uuid、issue_type_uuid
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """

    project_uuid = input("请输入project_uuid: ")
    project_uuid = project_uuid.strip()
    if project_uuid == "":
        raise Exception("project_uuid不能为空值")
    else:
        print("您输入的project_uuid = {}".format(project_uuid))

    issue_type_uuid = input("请输入issue_type_uuid: ")
    issue_type_uuid = issue_type_uuid.strip()
    if issue_type_uuid == "":
        raise Exception("issue_type_uuid不能为空值")
    else:
        print("您输入的issue_type_uuid = {}".format(issue_type_uuid))

    task_name_prefix = input("请输入task_name_prefix: ")
    task_name_prefix = task_name_prefix.strip()
    if task_name_prefix == "":
        print("您输入的task_name_prefix是空值")
    else:
        print("您输入的task_name_prefix = {}".format(task_name_prefix))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    task_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        add_task(project_uuid,issue_type_uuid,task_name_prefix)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(task_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        th = threading.Thread(target=add_task, args=(project_uuid, issue_type_uuid, "{}t{}_".format(task_name_prefix, i)))
        th.start()
        ths.append(th)


    for th in ths:
        print(th.getName())
        th.join()

    if count_thr != 0:
        count_task=count_thr*task_number
        logger.info("总计新增工作项:------------------- {} 条 ----------------------".format(count_task))

    print("任务执行完毕...")



if __name__ == "__main__":
    main()

