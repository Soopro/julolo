# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from services.taoke import Taoke


def helper_list_favorites():
    store = current_app.mongodb.Store.find_one_default()
    if not store:
        return None
    taoke = Taoke(
        app_key=store['taoke_app_key'],
        app_secret=store['taoke_app_secret'],
        pid=store['pid'],
        ssl=store['ssl'],
    )
    return taoke.list_favorites()
