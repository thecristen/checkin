#!/usr/bin/env python

import os
from setuptools import setup, find_packages

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='checkin',
    version='1.0',
    description='Green Streets Walk/Ride Day Checkin',
    author='Christian Spanring',
    author_email='cspanring@gmail.com',
    url='https://github.com/greenstreetsinitiative/checkin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines(),],
)
