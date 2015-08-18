#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


REDIS_CONNECTION = {
    'HOST': None,
    'PORT': None,
    'DB': None,
    'PASSWORD': None,
}

QUEUE_NAME = None

SALT = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s line:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

local_settings = '%s%ssettings-local.py' % (
    os.path.realpath(os.path.dirname(__file__)),
    os.path.sep,
)
if os.path.exists(local_settings):
    execfile(local_settings)
