# -*- coding: UTF-8 -*-

import requests
import os
import logging

logger = logging.getLogger(__name__)

from util.load_config import config

def ones_POST_request(url, main_product, minor_product, json=None, params=None, headers={}):
    return ones_request("POST", url, main_product, minor_product, json, params, headers)

def ones_request(method, url, main_product, minor_product, json=None, params=None, headers={}):
    '''
    ONES_API 请求基础方法
    '''
    base_url = config['ONES_API_URL'].format(main_product=main_product,minor_product=minor_product)
    final_url = base_url + url
    referer = config["REFERER"].format(product=main_product)
    headers.update({
        "content-type": "application/json",
        "referer": referer})
        #根据环境变更
    return base_request(method, final_url, json=json, params=params, headers=headers)


def base_request(method, url, json, params, headers):
    '''
    请求基础方法
    '''
    response = requests.request(str.upper(method), url, json = json, params = params, headers = headers)
    logger.info("状态码：{}".format(response.status_code))
    try:
        result = response.json()
    except ValueError:
        print("result is not a valid json format!!!")
    else:
        return result
    return None
