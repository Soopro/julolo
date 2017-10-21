# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from document import ObjectId, INDEX_DESC, INDEX_ASC


class Tip(BaseDocument):
    STATUS_OFF, STATUS_ON = 0, 1

    MAX_STORAGE = 600
    MAX_QUERY = 60

    structure = {
        'key': unicode,
        'title': unicode,
        'content': unicode,
        'src': unicode,
        'priority': int,
        'status': int,
        'updated': int,
        'creation': int
    }
    required_fields = ['key']
    default_values = {
        'title': u'',
        'content': u'',
        'src': u'',
        'priority': 0,
        'status': STATUS_OFF,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['key'],
            'unique': True,
        },
        {
            'fields': [('priority', INDEX_ASC), ('updated', INDEX_DESC)],
        },
        {
            'fields': ['status'],
        },
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_one_by_key(self, key):
        return self.find_one({
            'key': key
        })

    def find_all(self):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find().sort(sorts).limit(self.MAX_QUERY)

    def find_activated(self):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find({
            'status': self.STATUS_ON,
        }).sort(sorts).limit(self.MAX_QUERY)
