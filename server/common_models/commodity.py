# coding=utf-8
from __future__ import absolute_import

from utils.misc import now

from document import BaseDocument, ObjectId, INDEX_DESC


class Commodity(BaseDocument):

    TYPE_TAOBAO, TYPE_TMALL = 0, 1

    MAX_QUERY = 60

    structure = {
        'item_id': int,
        'shop': unicode,
        'type': int,
        'title': unicode,
        'src': unicode,
        'volume': int,
        'price': int,
        'income_rate': int,
        'commission': int,
        'coupon': unicode,
        'category': unicode,
        'start_time': int,
        'end_time': int,
        'click_url': unicode,
        'coupon_click_url': unicode,
        'creation': int,
        'updated': int,
    }
    required_fields = ['item_id', 'type']
    default_values = {
        'shop': u'',
        'title': u'',
        'src': u'',
        'volume': 0,
        'price': 0,
        'income_rate': 0,
        'commission': 0,
        'coupon': u'',
        'category': u'',
        'start_time': 0,
        'end_time': 0,
        'click_url': u'',
        'coupon_click_url': u'',
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

    def find_one_by_itemid(self, item_id):
        return self.find_one({
            'item_id': unicode(item_id),
        })

    def find_all(self):
        return self.find().sort('updated', INDEX_DESC).limit(self.MAX_QUERY)

    def clear_expired(self):
        return self.collection.remove({
            'end_time': {'$lt': now()}
        })

    def cound_used(self):
        return self.find().count()
