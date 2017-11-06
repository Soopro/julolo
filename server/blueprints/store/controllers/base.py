# coding=utf-8
from __future__ import absolute_import

from flask import g

from utils.response import output_json


@output_json
def get_store():
    store = g.store
    return {
        'id': store['_id'],
        'event_limit': store['event_limit'],
        'promotion_limit': store['promotion_limit'],
        'tpwd': store['tpwd'],
        'updated': store['updated'],
        'creation': store['creation']
    }
