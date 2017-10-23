# coding=utf-8
from __future__ import absolute_import
import multiprocessing

bind = '127.0.0.1:15809'
workers = min(multiprocessing.cpu_count(), 3)
accesslog = 'deployment_data/julolo/log/julolo_admin.access.log'
errorlog = 'deployment_data/julolo/log/julolo_admin.error.log'
pidfile = 'deployment_data/julolo/julolo_admin.pid'
raw_env = 'JULOLO_CONFIG_NAME=production'
