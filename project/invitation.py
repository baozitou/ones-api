# -*- coding: UTF-8 -*-

import requests
import logging
import time

from util.team_api import team_api

logger = logging.getLogger(__name__)


class Invitation:
    '''
    ones api: filter 接口
    '''

    def peek(self, peek_json):
        '''
        Args:
            peek_json:peek接口特定的json
        '''
        response = team_api.post('/team/{team_uuid}/filters/peek', "project","project", json=peek_json)
        logger.debug('response: {}'.format(response))
        return response

    def invitations(self):
        '''
        获取团队的邀请列表
        '''
        #time.sleep(2)
        response = team_api.get('/team/{team_uuid}/invitations', 'project', "project")
        logger.debug('response: {}'.format(response))
        return response

    def add_batch(self, json):
        '''
        批量发送邀请邮箱
        Args:
            json:{
                "email":[
                    "email1@ones.ai",
                    "email2@ones.ai"
                ]
            }
        '''
        response = team_api.post('/team/{team_uuid}/invitations/add_batch', 'project',"project", json=json)
        logger.debug('response: {}'.format(response))
        return response

    def get_pending_member(self):
        '''
        获取等待激活的用户
        '''
        response = team_api.post('/team/{team_uuid}/stamps/data', 'project',"project", json={
            "evaluated_permission": 0,
            "team": 0,
            "team_member": 0
        })
        logger.debug('response: {}'.format(response))
        return response["team_member"]["pending_members"]


invitation = Invitation()