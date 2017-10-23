# coding=utf-8
from __future__ import absolute_import
import multiprocessing

bind = '127.0.0.1:15800'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = 'deployment_data/julolo/log/julolo_api.access.log'
errorlog = 'deployment_data/julolo/log/julolo_api.error.log'
pidfile = 'deployment_data/julolo/julolo_api.pid'
raw_env = 'JULOLO_CONFIG_NAME=testing'
