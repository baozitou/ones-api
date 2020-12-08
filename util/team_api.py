# -*- coding: UTF-8 -*-

import logging

from util.request import ones_request
from util.auth import cached_data

logger = logging.getLogger(__name__)

def ones_authed_request(method, url, main_product, minor_product, json=None, params=None, url_params={}):
    if cached_data['token'] is None or cached_data['user_uuid'] is None:
        raise RuntimeError("please call method Auth:login!!!")

    if cached_data['team_uuid'] is None:
        raise RuntimeError("please call method Auth:set_team_uuid!!!")

    format_url = url.format(team_uuid=cached_data['team_uuid'], **url_params)
    headers = {
        "Ones-Auth-Token": cached_data['token'],
        "Ones-User-Id": cached_data['user_uuid'],
        'Connection': 'close'
    }
    return ones_request(method, format_url, main_product, minor_product, json=json, headers=headers, params=params)

class TeamApi:
    def get(self, url, main_product, minor_product, params=None, url_params={}):
        '''
        Args:
            url: 后缀
            product:所属产品，可选值:project、wiki
            params:请求头的参数
            url_params:url中需要的值，不需要写team_uuid的值，例如:{'task_uuid':'qwerasdf'}
        '''
        logger.info('ONES {} API is : {}'.format(str.upper(main_product), url.format(team_uuid=cached_data['team_uuid'],**url_params)))
        return ones_authed_request('get', url, main_product, minor_product, params=params, url_params=url_params)


    def post(self, url, main_product, minor_product, json=None, url_params={}):
        '''
        Args:
            url: 后缀
            product:所属产品，可选值:project、wiki
            json:请求体中的参数
            url_params:url中需要的值，不需要写team_uuid的值，例如:{'task_uuid':'qwerasdf'}
        '''
        logger.info('ONES {} API is : {}'.format(str.upper(main_product), url.format(team_uuid=cached_data['team_uuid'],**url_params)))
        return ones_authed_request('post', url, main_product, minor_product, json=json, url_params=url_params)


team_api = TeamApi()
