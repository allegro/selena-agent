#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from time import sleep

from redis import Redis
from redis.exceptions import ConnectionError
from rq import Queue, Connection, Worker

from selena_agent import settings
from selena_agent import VERSION


logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


def main():
    logger.info("Selena Agent, version %s" % ".".join(
        str(num) for num in VERSION))
    redis_connection = Redis(
        host=settings.REDIS_CONNECTION.get('HOST'),
        port=settings.REDIS_CONNECTION.get('PORT'),
        db=settings.REDIS_CONNECTION.get('DB'),
        password=settings.REDIS_CONNECTION.get('PASSWORD'),
    )
    stopped = False
    while True and not stopped:
        try:
            with Connection(redis_connection):
                worker = Worker(Queue(name=settings.QUEUE_NAME))
                worker.work()

                # When the worker receives a stop signal, we can easily exit
                # the loop
                break
        except ConnectionError as e:
            logger.error(
                "Error when connecting to Redis, retrying: {}".format(e))
            sleep(10)


if __name__ == '__main__':
    main()
