# coding=utf-8
from __future__ import absolute_import
import multiprocessing


DEPLOY_DIR = '/data/deployment_data/julolo'

bind = '127.0.0.1:15809'
workers = min(multiprocessing.cpu_count(), 2)
accesslog = '{}/log/julolo_admin.access.log'.format(DEPLOY_DIR)
errorlog = '{}/log/julolo_admin.error.log'.format(DEPLOY_DIR)
pidfile = '{}/julolo_admin.pid'.format(DEPLOY_DIR)
raw_env = 'JULOLO_CONFIG_NAME=production'
