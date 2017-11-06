# coding=utf-8
from __future__ import absolute_import

from utils.misc import now

from document import BaseDocument, ObjectId


class Store(BaseDocument):

    structure = {
        'taoke_app_key': unicode,
        'taoke_app_secret': unicode,
        'mini_app_id': unicode,
        'mini_app_secret': unicode,
        'pid': unicode,
        'ssl': bool,
        'tpwd_msg': unicode,
        'allow_tpwd': bool,
        'creation': int,
        'updated': int,
    }
    required_fields = ['taoke_app_key', 'taoke_app_secret', 'pid']
    default_values = {
        'mini_app_id': u'',
        'mini_app_secret': u'',
        'ssl': False,
        'tpwd_msg': u'',
        'allow_tpwd': False,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['mini_app_id'],
            'unique': True,
        }
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_one_by_wxmid(self, mini_app_id):
        return self.find_one({
            'mini_app_id': unicode(mini_app_id),
        })
