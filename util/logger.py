# -*- coding: UTF-8 -*-

import logging

class BaseLogger:
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s [%(module)s] %(message)s"

    def init_logger(self):
        logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)

base_logger = BaseLogger()
