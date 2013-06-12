============
Selena Agent
============

Installation
------------

Requirements
~~~~~~~~~~~~
Selena agent requires Python 2.7 which is included in the latest Ubuntu Server 12.04 LTS systems::

    $ sudo apt-get install python-dev python-virtualenv

Dependencies::

    $ sudo apt-get install libcurl3 libcurl4-openssl-dev

Message queue
~~~~~~~~~~~~~

Selena agent communicates with a central queue with `Redis <http://redis.io/>`_ as the broker. Install redis::

    $ sudo apt-get install redis-server

Since lost tasks can always be sent again, the durability guarantees which Redis
provides by default are not necessary. You can significantly speed up the queue
by commenting out the ``save`` lines from ``/etc/redis/redis.conf``.

We can check the status of the Redis server::

  $ redis-cli -h localhost -p 6379 -n 0 info

Virtual Environment
~~~~~~~~~~~~~~~~~~~

Create a virtual environment for Python in the user's home directory::

  $ virtualenv . --distribute --no-site-packages

System User
~~~~~~~~~~~

Unprivileged and not owned by a person::

  $ sudo adduser --home /home/selena-agent selena-agent
  $ sudo su - selena-agent

In any shell the user can *activate* the virtual environment. As a result, the
default Python executable and helper scripts will point to those within the
virtualenv directory structure::

  $ which python
  /usr/local/bin/python
  $ source bin/activate
  (selena-agent)$ which python
  /home/selena-agent/bin/python

Installing from pip
~~~~~~~~~~~~~~~~~~~

Simply invoke::

  (selena-agent)$ pip install selena-agent

Installing from sources
~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, to live on the bleeding edge, you can clone the selena-agent git
repository to ``project`` and install it manually::

  (selena-agent)$ git clone git://github.com/allegro/selena-agent.git project
  (selena-agent)$ cd project
  (selena-agent)$ pip install -e .

Configuration
-------------

Create file ``selena-agent/settings-local.py`` and fill in the appropriate data:

Fill Redis connection data::

  REDIS_CONNECTION = {
      'HOST': 'your redis host',
      'PORT': 'your redis port',
      'DB': None,
      'PASSWORD': None,
  }

RQ queue name::

  QUEUE_NAME = 'your RQ queue name'

The salt has to match the one from the main Selena administration page::

  SALT = 'taken from Selena system'

Run
---
To run selena-agent use the command::

  (selena-agent)$ selena-agent
