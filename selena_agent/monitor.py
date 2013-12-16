#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import pycurl
import StringIO
import sys
import time

from selena_agent import settings
from selena_agent.utils import create_token


RESPONSE_STATE_OK = 1
RESPONSE_STATE_PERFORMANCE = 2
RESPONSE_STATE_DIE = 3
RESPONSE_AGENT_FAIL = 5

AUTH_METHOD_BY_ID = {
    '1': pycurl.HTTPAUTH_NONE,
    '2': pycurl.HTTPAUTH_BASIC,
    '3': pycurl.HTTPAUTH_DIGEST,
    '4': pycurl.HTTPAUTH_GSSNEGOTIATE,
    '5': pycurl.HTTPAUTH_NTLM,
}


def _get_post_data_as_list(post_string):
    return [
        tuple(segment.split('=')) for segment in post_string.split("&")
    ]


def _check_monitored_phrases(content, monitored_phrases):
    result = {}
    for phrase_id in monitored_phrases:
        is_ok = True
        if content:
            in_response = monitored_phrases[phrase_id][0] in content
            if monitored_phrases[phrase_id][1] and in_response:
                is_ok = False
            elif not monitored_phrases[phrase_id][1] and not in_response:
                is_ok = False
        else:
            is_ok = False
        result[phrase_id] = is_ok
    return result


def _do_request(url, useragent, timeout=30, referer=None, auth={},
                post_string=None, monitored_phrases=None, response_code=200):
    result = {}
    if monitored_phrases:
        monitored_phrases = json.loads(monitored_phrases)
    post_data = _get_post_data_as_list(post_string) if post_string else []
    auth_method = str(auth.get('method', 1))
    user = auth.get('user')
    password = auth.get('password')
    resp_code = int(response_code)
    c = pycurl.Curl()
    try:
        c.setopt(c.URL, str(url))
        sio = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, sio.write)
        c.setopt(c.NOSIGNAL, 1)
        c.setopt(c.TIMEOUT, timeout)
        if resp_code >= 300 and resp_code < 400:
            c.setopt(c.FOLLOWLOCATION, 0)
        else:
            c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.MAXREDIRS, 5)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.COOKIEFILE, str('/tmp/cookie.txt'))
        c.setopt(c.COOKIEJAR, str('/tmp/cookie.txt'))
        c.setopt(c.USERAGENT, str(useragent))
        if referer:
            c.setopt(c.REFERER, str(referer))
        if auth_method != '1' and user and password:
            c.setopt(c.USERPWD, str('%s:%s' % (user, password)))
            c.setopt(c.HTTPAUTH, AUTH_METHOD_BY_ID[auth_method])
        if post_data:
            c.setopt(c.POST, 1)
            c.setopt(c.HTTPPOST, post_data)
        c.perform()

        response_code = int(c.getinfo(c.RESPONSE_CODE))
        content = sio.getvalue()
        response_content = u''
        if (
            c.getinfo(c.CONTENT_TYPE) is None or
            'image' not in c.getinfo(c.CONTENT_TYPE)
        ):
            try:
                response_content = u'%s' % content.decode("utf-8")
            except ValueError:
                try:
                    response_content = u'%s' % content.decode("iso-8859-2")
                except ValueError:
                    pass
        result.update({
            'response_code': response_code,
            'response_time': c.getinfo(c.TOTAL_TIME),
            'namelookup_time': c.getinfo(c.NAMELOOKUP_TIME),
            'connect_time': c.getinfo(c.CONNECT_TIME),
            'pretransfer_time': c.getinfo(c.PRETRANSFER_TIME),
            'starttransfer_time': c.getinfo(c.STARTTRANSFER_TIME),
            'redirect_time': c.getinfo(c.REDIRECT_TIME),
            'size_download': c.getinfo(c.SIZE_DOWNLOAD),
            'speed_download': c.getinfo(c.SPEED_DOWNLOAD),
            'effective_url': c.getinfo(c.EFFECTIVE_URL),
            'redirect_count': c.getinfo(c.REDIRECT_COUNT),
            'num_connects': c.getinfo(c.NUM_CONNECTS),
            'monitored_phrases': _check_monitored_phrases(
                response_content,
                monitored_phrases,
            ),
        })
    except pycurl.error as e:
        result.update({
            'error': str(e[1]),
        })
    except:
        result.update({
            'error': str(sys.exc_info()),
        })
    c.close()
    return result


def run_test(config, start_time):
    if (int(time.time()) - start_time) > 60:
        return {}
    result = _do_request(
        config['url'],
        config['useragent'],
        config['connection_timeout'],
        config['referer'],
        config['auth'],
        config['post'],
        config['monitored_phrases'],
        config['response_code'],
    )
    if 'response_code' not in result:
        result.update({
            'response_code': 0,
        })
    if all((
        result.get('response_code') == config['response_code'],
        result.get('response_time') <= config['performance_issues_time'],
    )):
        response_state = RESPONSE_STATE_OK
    elif result.get('response_code') == config['response_code']:
        response_state = RESPONSE_STATE_PERFORMANCE
    else:
        response_state = RESPONSE_STATE_DIE
    result.update({
        'response_state': response_state,
        'response_time': result.get(
            'response_time',
            config['connection_timeout'],
        ),
    })
    token = create_token(result, config['uuid'], settings.SALT)
    result.update({
        'token': token,
    })
    return result
