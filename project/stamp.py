# -*- coding: UTF-8 -*-

import logging

from datetime import datetime
from util.team_api import team_api

logger = logging.getLogger(__name__)
__all__ = ['stamp']


class Stamp:
    '''
    ones api: stamp 接口
    '''

    def stamps_data(self, dic_stamp):
        ''''
        dic_stamp:传stamp里需要返回的字典值
        例如：
            {"transition": 1500000000000000}
        '''
        response = team_api.post(
            '/team/{team_uuid}/stamps/data', "project","project", json=_stamp_json(dic_stamp))
        logger.debug('Stamp stamps_data response: {}'.format(response))
        return response


stamp = Stamp()


def _stamp_json(dic_stamp):
    now_stamp = datetime.now().timestamp()
    list_now_stamp = str(now_stamp).split('.')
    str_now_stamp = ''.join(list_now_stamp)
    format_now_stamp = int(str_now_stamp)
    json = {
        "team": format_now_stamp,
        "team_member": format_now_stamp,
        "department": format_now_stamp,
        "group": format_now_stamp,
        "project": format_now_stamp,
        "sprint": format_now_stamp,
        "issue_type": format_now_stamp,
        "issue_type_config": format_now_stamp,
        "field": format_now_stamp,
        "field_config": format_now_stamp,
        "task_status": format_now_stamp,
        "task_link_type": format_now_stamp,
        "task_status_config": format_now_stamp,
        "transition": format_now_stamp,
        "permission_rule": format_now_stamp,
        "evaluated_permission": format_now_stamp,
        "role": format_now_stamp,
        "role_config": format_now_stamp,
        "dashboard": format_now_stamp,
        "all_project": format_now_stamp,
        "testcase_library": format_now_stamp,
        "testcase_plan": format_now_stamp,
        "testcase_config": format_now_stamp,
        "pipeline": format_now_stamp,
        "component_template": format_now_stamp,
        "component": format_now_stamp,
        "project_template": format_now_stamp}
    if dic_stamp:
        for key, value in dic_stamp.items():
            if key in json:
                json[key] = value
            else:
                logger.info('no key:{} in stamp json '.format(key))
    return json
