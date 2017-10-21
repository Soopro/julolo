# coding=utf-8
from __future__ import absolute_import

import re

from document import BaseDocument, ObjectId, INDEX_DESC
from utils.misc import now


class Media(BaseDocument):
    MAX_QUERY = 120

    structure = {
        'user_id': ObjectId,
        'key': unicode,
        'filename': unicode,
        'mimetype': unicode,
        'size': int,
        'creation': int,
        'updated': int,
    }

    required_fields = ['key']

    default_values = {
        'user_id': None,
        'filename': u'',
        'mimetype': u'',
        'size': 0,
        'creation': now,
        'updated': now,
    }

    indexes = [
        {
            'fields': ['key'],
            'unique': True,
        },
        {
            'fields': ['user_id']
        },
        {
            'fields': ['size']
        },
        {
            'fields': ['updated']
        },
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id)
        })

    def find_one_by_uid_id(self, user_id, _id):
        return self.find_one({
            'user_id': ObjectId(user_id) if user_id else None,
            '_id': ObjectId(_id)
        })

    def find_one_by_key(self, key):
        return self.find_one({
            'key': key
        })

    def find_by_uid(self, user_id):
        cursor = self.find({
            'user_id': ObjectId(user_id) if user_id else None,
        }).sort('updated', INDEX_DESC)
        return cursor.limit(self.MAX_QUERY)

    def find_all(self, master=False):
        if master:
            _query = {
                'user_id': None
            }
        else:
            _query = {
                'user_id': {'$ne': None}
            }
        cursor = self.find(_query).sort('updated', INDEX_DESC)
        return cursor.limit(self.MAX_QUERY)

    def clear(self, key):
        return self.collection.remove({
            'key': re.compile(ur'^{}/.*'.format(key), re.IGNORECASE)
        })

    def count_size(self, user_id):
        group = self.collection.aggregate([{
            '$match': {
                'user_id': ObjectId(user_id) if user_id else None,
            }
        }, {
            '$group': {
                '_id': None,
                'total_size': {'$sum': '$size'}
            }
        }])
        total_size = 0
        for entry in group['result']:
            total_size += entry['total_size']
        return total_size
