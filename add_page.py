# -*- coding: UTF-8 -*-

import os
import time
import random
import threading
import logging
from pprint import pprint

logger = logging.getLogger(__name__)

from util.auth import auth, cached_data, login
from util.load_config import config
from util.readfile import read_file
from wiki.page import page_add,page_update
from my_thread import do_thread


def get_page_uuid(space_uuid,page_uuid):
    #space_uuid 页面uuid； page_uuid 页面uuid
    def get_add_page_json(page_uuid):
        add_json = {
            "copy_src_type": "page",
            "copy_src_uuid": config["TEMPLATE_UUID"],
            "page_uuid": page_uuid,
            "status": 1
        }
        print(add_json)
        return add_json
    response=page_add(get_add_page_json(page_uuid),space_uuid)
    add_uuid = response["uuid"]
    add_create_time = int(response["create_time"])

    return add_uuid,add_create_time


def get_update_page(title,space_uuid,page_uuid):
    add_uuid,add_create_time = get_page_uuid(space_uuid,page_uuid)
    create_time = int("{:0<13d}".format(add_create_time))
    update_time = int("{:0<13d}".format(int(time.time())))
    content = '''{}'''.format(read_file("wiki_content.html"))
    update_json = {
        "content": content,
        "create_time": create_time,
        "from_version": -1,
        "is_published": True,
        "page_uuid": page_uuid,
        "space_uuid": space_uuid,
        "status": 1,
        "title": title,
        "updated_time": update_time,
        "uuid": add_uuid
    }
    return update_json


def get_page_json_list(space_uuid, page_uuid, prefix=""):
    end = config['RANGE_END_NUMBER']
    l = len(str(end))
    fmt = prefix + "{}"
    pages_json = []
    for j in range(config['RANGE_START_NUMBER'], end):
        json = get_update_page(
            fmt.format(str(j).zfill(l)),
            space_uuid=space_uuid,
            page_uuid=page_uuid)
        pages_json.append(json)

    return pages_json


def update_pages(space_uuid, page_uuid, prefix=""):
    count = 0
    for json in get_page_json_list(space_uuid, page_uuid, prefix):
        try:
            response = page_update(json, space_uuid, json["uuid"])
            count+=1
        except Exception as ex:
            print("err:", ex)
    return count




def main():
    login()
    page_uuid = ""
    space_uuid = ""
    task_name_prefix = ""
    thread_num = 1

    """
    1. 提示使用者，输入页面组space_uuid、输入页面父节点page_uuid
    2. 并行线程增加任务，线程数量1~n
    3. 线程数量=1，不开thread
    4. 线程数量>1，使用threading.start方式
    5. 多线程的时候，要使用thread.join方式等待线程执行完毕
    """

    space_uuid = input("请输入页面组space_uuid: ")
    space_uuid = space_uuid.strip()
    if space_uuid == "":
        raise Exception("页面组space_uuid不能为空值")
    else:
        print("您输入的页面组space_uuid = {}".format(space_uuid))

    page_uuid = input("请输入页面父节点page_uuid: ")
    page_uuid = page_uuid.strip()
    if page_uuid == "":
        raise Exception("页面父节点page_uuid不能为空值")
    else:
        print("您输入的页面父节点page_uuid = {}".format(page_uuid))

    page_name = input("请输入page_name_prefix: ")
    page_name_prefix = page_name.strip()
    if page_name_prefix == "":
        print("您输入的page_name_prefix是空值")
    else:
        print("您输入的page_name_prefix = {}".format(page_name_prefix))

    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num.strip())
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))

    print("开始执行任务...")

    task_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        update_pages(space_uuid,page_uuid,page_name_prefix)
        logger.info("总计新增工作项:-------------------- {} 条 ----------------------".format(task_number))
        print("任务执行完毕...")
        return

    ths = []
    count_thr = 0
    for i in range(thread_num):
        count_thr += 1
        th = threading.Thread(target=update_pages, args=(space_uuid, page_uuid, "{}t{}_".format(page_name_prefix, i)))
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

