# coding=utf-8
from __future__ import absolute_import

from utils.misc import now

from document import BaseDocument, ObjectId, INDEX_DESC


class Store(BaseDocument):
    STATUS_OFF, STATUS_ON = 0, 1
    MAX_QUERY = 60

    structure = {
        'mini_app_id': unicode,
        'taoke_app_key': unicode,
        'taoke_app_secret': unicode,
        'pid': unicode,
        'ssl': bool,
        'title': unicode,
        'splash': unicode,
        'tpwd_msg': unicode,
        'allow_tpwd': bool,
        'cat_ids': unicode,
        'high_commission': bool,
        'default': bool,
        'status': int,
        'creation': int,
        'updated': int,
    }
    required_fields = ['mini_app_id']
    default_values = {
        'ssl': False,
        'title': u'',
        'splash': u'',
        'tpwd_msg': u'',
        'allow_tpwd': False,
        'cat_ids': u'',
        'high_commission': False,
        'default': False,
        'status': STATUS_OFF,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['mini_app_id'],
            'unique': True,
        },
        {
            'fields': ['default'],
        }
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_one_by_minid(self, mini_app_id):
        return self.find_one({
            'mini_app_id': unicode(mini_app_id),
            'status': self.STATUS_ON
        })

    def find_one_default(self):
        return self.find_one({
            'default': True,
        })

    def find_all(self):
        sorts = [('default', INDEX_DESC)]
        return self.find().sort(sorts).limit(self.MAX_QUERY)

    def freed_default(self):
        return self.collection.update({
            'default': True,
        }, {'$set': {'default': False}}, multi=True)
