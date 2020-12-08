# -*- coding: UTF-8 -*-

import requests
import logging
import os

from util.logger import base_logger
from util.request import ones_POST_request
from util.load_config import config

logger = logging.getLogger(__name__)
cached_data = {}

class Auth:
    '''
    ones api: auth 接口
    '''
    base_logger.init_logger()

    def login(self, email, password):
        if not email or not password:
            raise RuntimeError('User or password is empty!')

        logger.info('Email: {}'.format(email))
        logger.info('Password: <hidden>')
        json={'email': email, 'password': password}
        response = ones_POST_request('/auth/login', 'project','project', json=json)
        cached_data['token'] = response['user']['token']
        cached_data['user_uuid'] = response['user']['uuid']
        return response

    def invite_join_team(self, json):
        repones = ones_POST_request('/auth/invite_join_team', 'project','project', json=json)
        return repones

    def set_team_uuid(self, team_uuid):
        cached_data['team_uuid'] = team_uuid

auth = Auth()

def login():
    response = auth.login(config["EMAIL"], config["PASSWORD"])
    auth.set_team_uuid(config["TEAM_UUID"])
    return response

