# -*- coding: UTF-8 -*-

import os
import random
import threading
import logging

logger = logging.getLogger(__name__)

from util.load_config import config
from util.random_util import get_random_uuid
from util.auth import auth, cached_data, login
from project.project import add_project, copy_project
from project.stamp import stamp
from my_thread import do_thread

account_info = {}


def add_project_json(template_id: str, project_name: str, members: list):
    """新建项目的json值组装

    Arguments:
        template_id {str} -- project-t1,project-t2,project-t4
        project_name {str} -- project_name
        members {list} -- project members
    """
    user_uuid = cached_data['user_uuid']
    random_uuid = get_random_uuid(8)
    project_uuid = user_uuid + random_uuid
    return {
        "project": {
            "uuid": project_uuid,
            "owner": user_uuid,
            "name": project_name,
            "status": 1,
            "members": []
        },
        "template_id": template_id,
        "members": members
    }


def get_member_list_by_stamp():
    stamp_data = stamp.stamps_data(dic_stamp={"team_member": 0})
    members = stamp_data['team_member']['members']
    return [member['uuid'] for member in members if member['status'] == 1]


def get_json_list(project_name_prefix):
    list_member = get_member_list_by_stamp()
    template_id = 'project-t1'
    for i in range(config['RANGE_START_NUMBER'], config['RANGE_END_NUMBER']):
        yield add_project_json(
            template_id=template_id,
            project_name=project_name_prefix + str(i),
            members=list_member
        )


def _copy_project(project_uuid, name):
    json = {
        "project_uuid": project_uuid,
        "project_name": name
    }
    resp = copy_project(json)
    #logger.info("{}".format(resp))



def _add_project(data):
    resp = add_project(data)
    #logger.info("{}".format(resp))


def main():
    login()

    """
    1. 选择功能: 添加项目、拷贝项目
    2. 添加/拷贝项目：输入本次操作的project name前缀
    3. 拷贝项目：项目模板project uuid
    4. 设定线程数量
    """
    project_uuid = input("请输入project_uuid: ")
    project_uuid = project_uuid.strip()
    if project_uuid == "":
        raise Exception("project_uuid不能为空值")
    else:
        print("您输入的project_uuid = {}".format(project_uuid))



    project_name_prefix = input("请输入project_name_prefix: ")
    project_name_prefix = project_name_prefix.strip()
    if project_name_prefix == "":
        raise Exception("project_name_prefix不能是空值")
    else:
        print("您输入的project_name_prefix = {}".format(project_name_prefix))



    thread_num = input("请输入thread_num: ")
    thread_num = int(thread_num)
    if thread_num < 1:
        raise Exception("线程数量必须>=1")
    else:
        print("您输入的线程数量 = {}".format(thread_num))



    typ = input("""请输入操作类型:
    1. 添加项目
    2. 复制项目
    """)

    _word = {
        1: "添加项目",
        2: "复制项目"
    }

    print("您输入的操作类型: {}".format(_word[int(typ)]))

    def _inner(prefix, typ_str):
        typ = int(typ_str)
        end = config["RANGE_END_NUMBER"]
        l = len(str(end))
        if typ == 2:
            for i in range(config["RANGE_START_NUMBER"], end):
                _copy_project(project_uuid, prefix + str(i).zfill(l))
        elif typ == 1:
            for item in get_json_list(prefix):
                _add_project(item)


    print("开始执行任务...")


    project_number = config['RANGE_END_NUMBER'] - config['RANGE_START_NUMBER']
    if thread_num == 1:
        _inner(project_name_prefix,typ)
        logger.info("总计新增项目: ----------------- {} 个----------------------".format(project_number))
        print("任务执行完毕...")
        return


    ths = []
    count_thr = 0
    for i in range(thread_num):
        th = threading.Thread(target=_inner, args=(project_name_prefix + str(i) + "_", typ))
        th.start()
        ths.append(th)
        count_thr += 1

    for th in ths:
        print(th.getName())
        th.join()


    if count_thr != 0:
        count_projects = count_thr*project_number
        logger.info("总计新增项目:------------------ {} 个----------------------".format(count_projects))

    print("任务执行完毕...")


if __name__ == "__main__":
    main()
