# coding=utf-8
from __future__ import absolute_import

import re

from utils.misc import now

from document import BaseDocument, ObjectId, INDEX_DESC


class Commodity(BaseDocument):

    TYPE_TAOBAO, TYPE_TMALL = 0, 1

    MAX_QUERY = 60

    structure = {
        'item_id': int,
        'shop_type': int,
        'shop_title': unicode,
        'title': unicode,
        'src': unicode,
        'volume': int,
        'price': int,
        'income_rate': int,
        'commission': int,
        'coupon_info': unicode,
        'category': unicode,
        'cid': int,
        'start_time': int,
        'end_time': int,
        'click_url': unicode,
        'coupon_click_url': unicode,
        'creation': int,
        'updated': int,
    }
    required_fields = ['item_id', 'shop_type']
    default_values = {
        'shop_title': u'',
        'title': u'',
        'src': u'',
        'volume': 0,
        'price': 0,
        'income_rate': 0,
        'commission': 0,
        'coupon_info': u'',
        'category': u'',
        'cid': None,
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
        },
        {
            'fields': ['cid'],
        },
        {
            'fields': ['title'],
        },
        {
            'fields': ['end_time'],
        },

        {
            'fields': ['volume', 'commission', 'updated'],
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
            'item_id': int(item_id),
        })

    def find_all(self):
        _sorts = [('updated', INDEX_DESC)]
        return self.find().sort(_sorts).limit(self.MAX_QUERY)

    def find_live(self, cids=None, timestamp=0):
        _query = {
            'end_time': {'$gt': now()}
        }
        if cids is not None:
            _query['cid'] = {
                '$in': [cid for cid in cids if isinstance(cid, int)]
            }
        if timestamp:
            _query['updated'] = {
                '$lt': int(timestamp)
            }
        _sorts = [('volume', INDEX_DESC),
                  ('commission', INDEX_DESC),
                  ('updated', INDEX_DESC)]
        return self.find(_query).sort(_sorts).limit(self.MAX_QUERY)

    def search(self, keyword, cids=None, timestamp=0):
        _query = {
            'title': re.compile(ur'.*{}.*'.format(keyword), re.IGNORECASE),
            'end_time': {'$gt': now()}
        }
        if cids is not None:
            _query['cid'] = {
                '$in': [cid for cid in cids if isinstance(cid, int)]
            }
        if timestamp:
            _query['updated'] = {
                '$lt': int(timestamp)
            }
        _sorts = [('volume', INDEX_DESC),
                  ('commission', INDEX_DESC),
                  ('updated', INDEX_DESC)]
        return self.find(_query).sort(_sorts).limit(self.MAX_QUERY)

    def clear_expired(self):
        return self.collection.remove({
            'end_time': {'$lt': now()}
        })

    def cound_used(self):
        return self.find().count()
