# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g
from bson import ObjectId

from services.taoke import Taoke

from apiresps.errors import NotFound


# user
def find_user(id_or_slug, skip_except=False):
    if ObjectId.is_valid(id_or_slug):
        user = current_app.mongodb.User.find_one_by_id(id_or_slug)
    else:
        user = current_app.mongodb.User.find_one_by_slug(id_or_slug)
    if not user and not skip_except:
        raise NotFound('user')
    return user


# taoke
def connect_taoke():
    store = g.store
    taoke = Taoke(
        app_key=store['app_key'],
        app_secret=store['app_secret'],
        pid=store['pid'],
        ssl=store['ssl'],
    )
    return taoke
