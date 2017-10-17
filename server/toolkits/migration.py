# coding=utf-8
from __future__ import absolute_import

from config import config
from .db import connect_mongodb
from .db import (User, Property)

from .migrations import *


def migration(cfg_type='default'):
    cfg = config.get(cfg_type)
    if not cfg:
        return None

    mongodb_conn, mongodb = connect_mongodb(cfg)

    # users
    UserMigration(User).migrate_all(collection=mongodb.User.collection)
    PropertyMigration(Property).migrate_all(
        collection=mongodb.Property.collection)

    return True
