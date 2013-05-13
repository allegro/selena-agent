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

local_settings = '%s%ssettings-local.py' % (
    os.path.realpath(os.path.dirname(__file__)),
    os.path.sep,
)
if os.path.exists(local_settings):
    execfile(local_settings)
