# coding=utf-8
from __future__ import absolute_import

from utils.misc import now
from document import BaseDocument, ObjectId, INDEX_DESC, INDEX_ASC


class Category(BaseDocument):
    STATUS_OFF, STATUS_ON = 0, 1

    MAX_STORAGE = 600
    MAX_QUERY = 60

    structure = {
        'slug': unicode,
        'cat_ids': unicode,
        'title': unicode,
        'caption': unicode,
        'label': unicode,
        'icon': unicode,
        'poster': unicode,
        'splash': unicode,
        'priority': int,
        'status': int,
        'updated': int,
        'creation': int
    }
    sensitive_fields = ['label']
    required_fields = ['slug']
    default_values = {
        'cat_ids': u'',
        'title': u'',
        'caption': u'',
        'label': u'',
        'icon': u'',
        'poster': u'',
        'splash': u'',
        'priority': 0,
        'status': STATUS_OFF,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['slug'],
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

    def find_one_by_slug(self, slug):
        return self.find_one({
            'slug': slug
        })

    def find_all(self):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find().sort(sorts).limit(self.MAX_QUERY)

    def find_activated(self):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find({
            'status': self.STATUS_ON,
        }).sort(sorts).limit(self.MAX_QUERY)
