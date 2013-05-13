#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from redis import Redis
from rq import Queue, Connection, Worker

from selena_agent import settings
from selena_agent import VERSION


def main():
    redis_connection = Redis(
        host=settings.REDIS_CONNECTION.get('HOST'),
        port=settings.REDIS_CONNECTION.get('PORT'),
        db=settings.REDIS_CONNECTION.get('DB'),
        password=settings.REDIS_CONNECTION.get('PASSWORD'),
    )
    with Connection(redis_connection):
        print("Selena Agent, version %s" % ".".join(
            str(num) for num in VERSION,
        ))
        worker = Worker(Queue(name=settings.QUEUE_NAME))
        worker.work()


if __name__ == '__main__':
    main()
