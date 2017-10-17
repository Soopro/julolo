# coding=utf-8
from __future__ import absolute_import
import multiprocessing

bind = '127.0.0.1:8500'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = 'deployment_data/hys/log/hys_api.access.log'
errorlog = 'deployment_data/hys/log/hys_api.error.log'
pidfile = 'deployment_data/hys/hys_api.pid'
raw_env = 'HYS_CONFIG_NAME=production'
