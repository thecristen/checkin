import os
from setuptools import setup

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
     packages.append('django-redis-cache')
     packages.append('hiredis')

setup(
    name='checkin',
    version='1.0',
    description='Green Streets Walk/Ride Day Checkin',
    author='Christian Spanring',
    author_email='cspanring@gmail.com',
    url='https://github.com/greenstreetsinitiative/checkin',
    install_requires=[open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines(),],
)
