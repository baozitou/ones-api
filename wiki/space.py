# -*- coding: UTF-8 -*-

import requests
import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def space_add(json):
    url = "/team/{team_uuid}/spaces/add"
    resp = team_api.post(url, "wiki","wiki", json=json)
    logger.debug('response: {}'.format(resp))
    return resp

