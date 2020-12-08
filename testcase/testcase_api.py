# -*- coding: UTF-8 -*-

import requests
import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def add_testplan_api(json):
    resp = team_api.post("/team/{team_uuid}/testcase/plans/add", "project","project", json=json)
    logger.debug('response: {}'.format(resp))
    return resp

def add_caselibrary_api(json):
    resp = team_api.post("/team/{team_uuid}/testcase/libraries/add", "project","project", json=json)
    logger.debug("response: {}".format(resp))
    return resp

def add_testcase_api(json):
    resp = team_api.post("/team/{team_uuid}/items/add", "project", "project", json=json)
    logger.debug("response: {}".format(resp))
    return resp
