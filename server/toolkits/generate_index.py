# coding=utf-8
from __future__ import absolute_import

from config import config
from .db import connect_mongodb, models


def generate_index(cfg_type='default'):
    cfg = config.get(cfg_type)
    if not cfg:
        return None

    mongodb_conn, mongodb = connect_mongodb(cfg)

    # start generate
    for model in models:
        curr_collection = mongodb[model.__collection__]
        curr_collection.drop_indexes()
        model.generate_index(curr_collection)
        print 'indexed:', model.__collection__
    return True
