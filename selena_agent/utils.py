#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from hashlib import md5


def create_token(items, task_uuid, salt):
    return md5(
        '%s_%s_%s' % (
            [items.get(key) for key in [
                'response_state', 'response_code', 'response_time',
            ]],
            task_uuid,
            salt,
        ),
    ).hexdigest()
