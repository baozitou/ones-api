# -*- coding: UTF-8 -*-

import requests
import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def add_project(json):
    response = team_api.post('/team/{team_uuid}/projects/add', "project","project", json=json)
    logger.debug('response: {}'.format(response))
    return response

def copy_project(json):
    resp = team_api.post('/team/{team_uuid}/projects/copy', "project","project", json=json)
    logger.debug('response: {}'.format(resp))
    return resp
