# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from document import ObjectId, INDEX_DESC


class Goods(BaseDocument):
    TYPE_MARKET, TYPE_TMALL = 0, 1

    structure = {
        'item_id': int,
        'shop_id': int,
        'shop': unicode,
        'type': int,
        'title': unicode,
        'item_url': unicode,
        'click_url': unicode,
        'coupon_url': unicode,
        'coupon': unicode,
        'start_time': int,
        'end_time': int,
        'category': int,
        'poster': unicode,
        'figures': [unicode],
        'price': int,
        'volume': int,
        'commn_rate': int,
        'commn_type': int,
        'updated': int,
        'creation': int
    }
    required_fields = ['item_id', 'shop_id']
    default_values = {
        'title': u'',
        'shop': u'',
        'type': TYPE_MARKET,
        'item_url': u'',
        'click_url': u'',
        'coupon_url': u'',
        'coupon': u'',
        'start_time': 0,
        'end_time': 0,
        'category': 0,
        'poster': u'',
        'figures': [],
        'price': 0,
        'volume': 0,
        'commn_rate': 0,
        'commn_type': 0,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['item_id'],
            'unique': True,
        },
        {
            'fields': ['shop_id'],
        },
        {
            'fields': ['type'],
        },
        {
            'fields': ['category'],
        },
        {
            'fields': ['end_time'],
        },
        {
            'fields': ['updated'],
        }
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_one_by_itemid(self, item_id):
        return self.find_one({
            'item_id': item_id,
        })

    def find_tmall(self):
        return self.find({
            'type': self.TYPE_TMALL,
        }).sort('updated', INDEX_DESC)

    def find_goods(self, _id):
        return self.find().sort('updated', INDEX_DESC)

    def clear(self):
        return self.collection.remove({
            'end_time': {'$lt': now()},
        })
