# coding=utf-8
from __future__ import absolute_import

from flask import g

from utils.response import output_json

from ..helpers import helper_get_property


@output_json
def get_property():
    user = g.user
    prop = helper_get_property(user)
    return output_prop(prop, user)


# helpers


# outputs
def output_prop(prop, user):
    return {
        'id': prop['_id'],
        'pid': prop['pid'],
        'user_slug': user['slug'],
        'updated': prop['updated'],
        'creation': prop['creation'],
    }
