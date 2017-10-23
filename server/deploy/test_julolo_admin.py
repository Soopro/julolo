# coding=utf-8
from __future__ import absolute_import
import multiprocessing

from config import config


conf_name = 'production'
cfg = config.get(conf_name)

bind = '127.0.0.1:15809'
workers = min(multiprocessing.cpu_count(), 2)
accesslog = '{}/log/julolo_admin.access.log'.format(cfg.LOG_FOLDER)
errorlog = '{}/log/julolo_admin.error.log'.format(cfg.LOG_FOLDER)
pidfile = '{}/julolo_admin.pid'.format(cfg.DEPLOY_DIR)
raw_env = 'JULOLO_CONFIG_NAME={}'.format(conf_name)
