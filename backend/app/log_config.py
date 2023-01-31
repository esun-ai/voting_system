# -*- coding:utf-8 -*-
# Copyright (C) 2023  E.SUN BANK.
# @Author: Hsin-Hsien Ho, Wan-Chu Lin
# @Date: 2023/01
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import logging.config 
import logging
from datetime import datetime
from gunicorn import glogging

logger = logging.getLogger(__name__)
time_name = datetime.now().strftime('%Y%m%d_%H%M%S')

logging_cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'KeyValueFormatter': {
            'format': (
                'timestamp=%(asctime)s pid=%(process)d '
                'loglevel=%(levelname)s msg=%(message)s'
            )
        },
    },
    'handlers': {
        "default_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "error_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "default_file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "KeyValueFormatter",
            "filename": f"app/logger/debug_{time_name}.log",
            "encoding": "utf8"
        },
        "error_file": {
            "formatter": "KeyValueFormatter",
            "class": "logging.FileHandler",
            "filename": f"app/logger/error_{time_name}.log",
        },
        "access_file": {
            "formatter": "KeyValueFormatter",
            "class": "logging.FileHandler",
            "filename": f"app/logger/access_{time_name}.log",
        },
    },
    'loggers': {
        "gunicorn.error": {
            "level": "ERROR",
            "handlers": ["error_console", "error_file"],
            "propagate": False,
            "qualname": "gunicorn.error"
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_console", "access_file"],
            "propagate": False,
            "qualname": "gunicorn.access"
        },
        "gunicorn.mylog": {
            "level": "INFO",
            "handlers": ["default_console", "default_file"],
            "propagate": False,
            "qualname": "gunicorn.mylog"
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default_console', "default_file"],
    }
}


def configure_logging():
    logging.config.dictConfig(logging_cfg)


class UniformLogger(glogging.Logger):

    def setup(self, cfg):
        configure_logging()
