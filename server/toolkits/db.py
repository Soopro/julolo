# coding=utf-8
from __future__ import absolute_import

from mongokit import Connection as MongodbConn

from common_models import (Promotion, Category, Event, Media)


models = [Promotion, Category, Event, Media]


def connect_mongodb(cfg):
    mongodb_conn = MongodbConn(
        host=cfg.MONGODB_HOST,
        port=cfg.MONGODB_PORT,
        max_pool_size=cfg.MONGODB_MAX_POOL_SIZE,
    )

    mongodb_conn.register(models)

    mongodb = mongodb_conn[cfg.MONGODB_DATABASE]
    if hasattr(cfg, 'MONGODB_USER') and \
       hasattr(cfg, 'MONGODB_PASSWORD') and \
       cfg.MONGODB_USER and cfg.MONGODB_PASSWORD:
        mongodb.authenticate(cfg.MONGODB_USER, cfg.MONGODB_PASSWORD)

    return mongodb_conn, mongodb
