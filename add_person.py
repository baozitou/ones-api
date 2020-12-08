# -*- coding: UTF-8 -*-

import os
import sys
import time
import random
import threading
import logging

Logger = logging.getLogger(__name__)

# from itertools import islice
from util.auth import auth, login
from project.invitation import invitation
from util.load_config import load_config, config
from my_thread import MyThread, do_thread


account_info = {}

def set_emails(emails):
    invite_email_list = []
    for email in emails:
        setting = {}
        setting["email"]=email
        setting["is_team_administrator"] = False
        invite_email_list.append(setting)
    json = {
        "invite_settings":invite_email_list,
        "license_types": [7, 4, 5, 1, 3, 2]
    }
    #time.sleep(2)
    invitation.add_batch(json)

def invite_join_team(email, password, name, invite_code):
    json = {
        "email": email,
        "password": password,
        "name": name,
        "invite_code": invite_code
    }
    resp = auth.invite_join_team(json)
    print(resp)

def get_email_list(start=1, end=30):
    email_list = []
    l = len(str(end))
    fmt = "u{}{}@ones.ai"
    for i in range(20):
        ch = chr(ord('a')+i)
        email_list.extend([fmt.format(ch, str(j).zfill(l)) for j in range(start, end)])
    print(email_list)
    return email_list


def join_team_by_invitations(invitations_list, name=None):
    for item in invitations_list:
        if item["is_expired"] == True:
            continue
        #time.sleep(3)
        email = item["email"]
        index = email.index('@')
        name = email[0:index]
        invite_join_team(email, config["DEFAULT_PASSWORD"], name, item["code"])
        account_info[email] = config["DEFAULT_PASSWORD"]
        print("{name} --> already join team: ".format(name=name), email)


def main():
    login()
    email_list = get_email_list(config["RANGE_START_NUMBER"], config["RANGE_END_NUMBER"])
    set_emails(email_list)
    invitations_respones = invitation.invitations()
    invitations_list = invitations_respones["invitations"]
    do_thread(join_team_by_invitations, invitations_list, arg_name="invitations_list", thread_num=20)
    count_number = (config["RANGE_END_NUMBER"] - config["RANGE_START_NUMBER"]) * 20
    Logger.info("总计新增人员：-------------------------{}----------------------".format(count_number))


if __name__ == "__main__":
    main()
