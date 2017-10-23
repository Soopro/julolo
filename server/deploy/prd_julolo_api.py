# coding=utf-8
from __future__ import absolute_import
import multiprocessing

from .conf import BASE_DEPLOY_DIR


bind = '127.0.0.1:15800'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '{}/log/julolo_api.access.log'.format(BASE_DEPLOY_DIR)
errorlog = '{}/log/julolo_api.error.log'.format(BASE_DEPLOY_DIR)
pidfile = '{}/julolo_api.pid'.format(BASE_DEPLOY_DIR)
raw_env = 'JULOLO_CONFIG_NAME=production'
