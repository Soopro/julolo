# coding=utf-8
from __future__ import absolute_import
import multiprocessing

from config import config


conf_name = 'production'
cfg = config.get(conf_name)

bind = '127.0.0.1:15800'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '{}/log/julolo_api.access.log'.format(cfg.LOG_FOLDER)
errorlog = '{}/log/julolo_api.error.log'.format(cfg.LOG_FOLDER)
pidfile = '{}/julolo_api.pid'.format(cfg.DEPLOY_DIR)
raw_env = 'JULOLO_CONFIG_NAME={}'.format(conf_name)
