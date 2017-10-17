# coding=utf-8
from __future__ import absolute_import
import multiprocessing

bind = '127.0.0.1:8509'
workers = min(multiprocessing.cpu_count(), 3)
accesslog = 'deployment_data/hys/log/hys_admin.access.log'
errorlog = 'deployment_data/hys/log/hys_admin.error.log'
pidfile = 'deployment_data/hys/hys_admin.pid'
raw_env = 'HYS_CONFIG_NAME=production'
