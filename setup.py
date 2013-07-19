 # -*- encoding: utf-8 -*-

import sys
from setuptools import setup, find_packages


assert sys.version_info >= (2, 7), "Python 2.7+ required."


from selena_agent import VERSION
version = ".".join(str(num) for num in VERSION)


setup(
    name='selena-agent',
    version=version,
    license='Apache Software License v2.0',
    author='Grupa Allegro Sp. z o.o. and Contributors',
    url='http://github.com/allegro/selena-agent',
    author_email='it-ralph-dev@allegro.pl',
    description='SelenaAgent - Selena monitoring agent.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'rq==0.3.8',
        'pycurl==7.18.1',
    ],
    entry_points={
        'console_scripts': [
            'selena-agent = selena_agent.rqworker:main',
        ],
    },
)
