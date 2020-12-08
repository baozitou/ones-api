# -*- coding: UTF-8 -*-

import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def tasks_add(json):
    resp = team_api.post('/team/{team_uuid}/tasks/add', "project", json=json)
    logger.debug('response: {}'.format(resp))
    return resp


def tasks_add2(json):
    resp = team_api.post("/team/{team_uuid}/tasks/add2", "project","project", json=json)
    logger.debug("response: {}".format(resp))
    return resp
