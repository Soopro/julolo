# coding=utf-8
from __future__ import absolute_import

from utils.misc import now

from document import BaseDocument, ObjectId, INDEX_DESC


class Commodity(BaseDocument):

    structure = {
        'item_id': unicode,
        'shop': unicode,
        'type': unicode,
        'title': unicode,
        'volume': int,
        'src': unicode,
        'figures': unicode,
        'price': int,
        'coupon': unicode,
        'category': unicode,
        'start_time': unicode,
        'end_time': unicode,
        'creation': int,
        'updated': int,
    }
    required_fields = ['item_id', 'type']
    default_values = {
        'shop': u'',
        'title': u'',
        'volume': 0,
        'src': u'',
        'figures': u'',
        'price': 0,
        'coupon': u'',
        'category': u'',
        'start_time': u'',
        'end_time': u'',
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['item_id'],
            'unique': True,
        }
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_all(self):
        return self.find().sort('updated', INDEX_DESC)
