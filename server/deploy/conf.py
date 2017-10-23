# coding=utf-8
from __future__ import absolute_import

import os


BASE_DEPLOY_DIR = '/data/deployment_data/julolo'

if not os.path.isdir(BASE_DEPLOY_DIR):
    os.makedirs(BASE_DEPLOY_DIR)
