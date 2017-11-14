# coding=utf-8
from __future__ import absolute_import

from flask import g

from utils.response import output_json


@output_json
def get_store():
    store = g.store
    return {
        'id': store['_id'],
        'splash': store['splash'],
        'allow_tpwd': store['allow_tpwd'],
        'tpwd_msg': store['tpwd_msg'],
        'cat_ids': store['cat_ids'],
        'high_commission': store['high_commission'],
        'updated': store['updated'],
        'creation': store['creation']
    }
