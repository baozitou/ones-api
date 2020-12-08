# -*- coding: UTF-8 -*-

import requests
import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def plan_add(json):
    url = "/team/{team_uuid}/items/add"
    resp = team_api.post(url, "project", "project", json=json)
    logger.debug('response: {}'.format(resp))
    return resp

# http://54.223.93.94/project/api/project/team/DnXpawSp/items/add