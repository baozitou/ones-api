# -*- coding: UTF-8 -*-

import json
import os

class ConfigCache:

    def __init__(self):
        self._cache = {}

    def load_config(self, config_file):
        if config_file in self._cache:
            return self._cache[config_file]

        path = os.path.abspath(config_file)
        with open(path, "r") as f :
            config = json.load(f)
            self._cache[path] = config
            return config


load_config = ConfigCache().load_config
config_file_path = os.path.join(os.path.dirname(__file__), '../config.json')
config = load_config(config_file_path)
