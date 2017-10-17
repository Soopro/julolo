# coding=utf-8
from __future__ import absolute_import

from flask import current_app
from bson import ObjectId

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
