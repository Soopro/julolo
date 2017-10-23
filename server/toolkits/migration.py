# coding=utf-8
from __future__ import absolute_import

from config import config
from .db import connect_mongodb
from .db import (Media, Promotion, Event, Category, Tip, Store)

from .migrations import *


def migration(cfg_type='default'):
    cfg = config.get(cfg_type)
    if not cfg:
        return None

    mongodb_conn, mongodb = connect_mongodb(cfg)

    # store
    StoreMigration(Store).migrate_all(
        collection=mongodb.Store.collection)

    # promotion
    PromotionMigration(Promotion).migrate_all(
        collection=mongodb.Promotion.collection)

    # category
    CategoryMigration(Category).migrate_all(
        collection=mongodb.Category.collection)

    # event
    EventMigration(Event).migrate_all(
        collection=mongodb.Event.collection)

    # media
    MediaMigration(Media).migrate_all(
        collection=mongodb.Media.collection)

    # tip
    TipMigration(Tip).migrate_all(
        collection=mongodb.Tip.collection)

    return True
