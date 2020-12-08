# -*- coding: UTF-8 -*-

import requests
import logging

from util.team_api import team_api

logger = logging.getLogger(__name__)

def page_add(json,space_uuid):
    url = "/team/{team_uuid}"+"/space/{}/drafts/add".format(space_uuid)
    resp = team_api.post(url, "wiki","wiki", json=json)
    logger.debug('response: {}'.format(resp))
    return resp


def page_update(json,space_uuid,add_uuid):
    url = "/team/{team_uuid}"+"/space/{}/draft/{}/update".format(space_uuid,add_uuid)
    resp = team_api.post(url, "wiki","wiki", json=json)
    logger.debug("response: {}".format(resp))
    return resp
